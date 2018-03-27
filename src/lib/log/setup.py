import logging.config

import sys

from infra.configure.constants import LogLevel


def setup_logging(debug: bool=False) -> None:
    log_level = LogLevel.DEBUG if debug else LogLevel.INFO
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
                'class': 'lib.log.formatters.single_line.SingleLineFormatter',
            }
        },
        'filters': {
            '404_filter': {
                '()': 'lib.log.filters.not_found.NotFoundFilter',
            },
        },
        'handlers': {
            'stream': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'stream': sys.stderr,
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'common': {
                'handlers': ['stream'],
                'level': log_level,
            },
            'django': {
                'handlers': ['stream'],
                'level': log_level,
            },
            'django.request': {
                'handlers': ['stream'],
                'filters': ['404_filter'],
                'level': log_level,
                'propagate': False,
            },
            'django.template': {
                'handlers': ['stream'],
                'level': log_level,
                'propagate': False,
            }
        },
    })
