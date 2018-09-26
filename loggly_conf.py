import logging
import logging.config


def get_configured_logger(loggly_key):

    logging_config = {
        u'version': 1,
        u'handlers': {
            u'loggly': {
                u'class': u'loggly.handlers.HTTPSHandler',
                u'formatter': u'basic',
                u'level': u'INFO',
                u'url': u'https://logs-01.loggly.com/inputs/{}/tag/python'.format(loggly_key)
            },
            u'console': {
                u'class': u'logging.StreamHandler',
                u'level': u'INFO',
                u'formatter': u'basic',
                u'stream': u'ext://sys.stdout',
            }
        },
        u'formatters': {
            u'basic': {
                u'format': u'%(asctime)s | %(name)15s:%(lineno)3s:%(funcName)15s | %(levelname)7s | %(message)s'
            }
        },
        u'loggers': {
            u'root': {
                u'level': u'INFO',
                u'handlers': [u'console', u'loggly']
            }
        }
    }
    # set log config
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("root")
    return logger
