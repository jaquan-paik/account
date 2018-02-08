import logging.config

import os


def setup_logging(site: str, log_level: str, log_dir: str) -> None:
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            }
        },
        'filters': {
            '404_filter': {
                '()': 'lib.log.filters.not_found.NotFoundFilter',
            },
        },
        'handlers': {
            'file': {
                'level': log_level,
                'filename': os.path.join(log_dir, site + '.log'),
                'formatter': 'verbose',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'backupCount': 21,
                'when': 'D',  # daily
                'encoding': 'utf-8',
            }
        },
        'loggers': {
            'common': {
                'handlers': ['file'],
                'level': log_level,
            },
            'django': {
                'handlers': ['file'],
                'level': log_level,
            },
            'django.request': {
                'handlers': ['file'],
                'filters': ['404_filter'],
                'level': log_level,
                'propagate': False,
            },
            'django.template': {
                'handlers': ['file'],
                'level': log_level,
                'propagate': False,
            }
        },
    })
