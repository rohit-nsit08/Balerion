"""
placeholder
"""

DEBUG = True                    # Whether or not to show DEBUG level messages

LOGGING = {                     # dictConfig for output stream and file logging
    'version': 1,              
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(levelname)s::%(module)s - %(message)s',
        },
        'file': {
            'format': '[%(asctime)s] %(levelname)s::(P:%(process)d T:%(thread)d)::%(module)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
        'class': 'logging.StreamHandler',
        'formatter':'console',
        'level': 'DEBUG',
        },
        'file': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter':'file',
        'level': 'INFO',
        'when': 'midnight',
        'filename': 'balerian.log',
        'interval': 1,
        'backupCount': 0,
        'encoding': None,
        'delay': False,
        'utc': False,
        },
    },
    'loggers': {
        'crawler_logger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    }
} 