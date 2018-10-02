import logging
import logging.config


def get_configured_logger(loggly_key):

    logging_config = {
        'version': 1,
        'handlers': {
            'loggly': {
                'class': 'loggly.handlers.HTTPSHandler',
                'formatter': 'basic',
                'level': 'INFO',
                'url': 'https://logs-01.loggly.com/inputs/{}/tag/python'.format(loggly_key)
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'basic',
                'stream': 'ext://sys.stdout',
            }
        },
        'formatters': {
            'basic': {
                'format': '%(asctime)s | %(name)15s:%(lineno)3s:%(funcName)15s | %(levelname)7s | %(message)s'
            }
        },
        'loggers': {
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'loggly']
            }
        }
    }
    # set log config
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("root")
    return logger
