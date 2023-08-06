"""CoBib logging module."""

import logging
import logging.config


def log_to_stream(level='WARNING'):
    """Configures a StreamHandler logger.

    Args:
        level (str, optional): verbosity level indicator.
    """
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d %(message)s'
            },
        },
        'handlers': {
            'default': {
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'formatter': 'standard',
                'propagate': True
            }
        }
    })


def log_to_file(level='INFO'):
    """Configures a FileHandler logger.

    Args:
        level (str, optional): verbosity level indicator.
    """
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d %(message)s'
            },
        },
        'handlers': {
            'default': {
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': '/tmp/cobib.log',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'formatter': 'standard',
                'propagate': True
            }
        }
    })
