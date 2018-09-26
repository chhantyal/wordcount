import re
import argparse
from operator import add

from pyspark.sql import SparkSession

from loggly_conf import get_configured_logger


class Parser:

    def __init__(self, loggly_key):
        self.loggly_key = loggly_key

    def word_split(self, x):
        """
        - Method/function which runs on Spark executor
        - Log some useful information
        - Use regex to split only words(not special characters)
        :param x: Spark rdd or tuple with (text, line_num)
        :return: words
        """
        words = re.split('\W+', x[0])
        length = len(words)
        # configures logger in executors on first run
        logger = get_configured_logger(self.loggly_key)
        logger.info("Line {} contains {} words.".format(x[1], length))
        # filter empty values
        return filter(lambda a: a, words)


def main(input_path, loggly_key):
    """
    Main entrypoint to Spark
    :param input_path: input file or path
    :param loggly_key: loggly customer key for remote logging
    :return: None
    """
    spark = SparkSession.builder.appName("WordCount").getOrCreate()

    lines = spark.sparkContext.textFile(input_path).zipWithIndex()
    txt_parser = Parser(loggly_key)
    counts = lines.flatMap(lambda x: txt_parser.word_split(x)).map(lambda x: (x, 1)).reduceByKey(add)
    output = counts.sortBy(lambda x: x[1], ascending=False).collect()

    for (word, count) in output:
        print("%s: %i" % (word, count))
    # configures logger in driver
    logger = get_configured_logger(loggly_key)
    logger.info("Wordcount complete")
    spark.stop()


if __name__ == '__main__':  # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        help='Input file or directory path',
        required=True)

    parser.add_argument(
        '-k', '--loggly_key',
        help='Loggly consumer key',
        required=True)

    args = parser.parse_args()

    main(input_path=args.input, loggly_key=args.loggly_key)
