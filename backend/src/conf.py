import logging.config

DAYS_AHEAD = 5
TOP_FLIGHTS = (
    ('ALA', 'TSE'),
    # ('TSE', 'ALA'),
    # ('ALA', 'MOW'),
    # ('MOW', 'ALA'),
    # ('ALA', 'CIT'),
    # ('CIT', 'ALA'),
    # ('TSE', 'MOW'),
    # ('MOW', 'TSE'),
    # ('TSE', 'LED'),
    # ('LED', 'TSE'),
)

# LOGGING ---------------------------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'main': {'format': '[%(levelname)s] [%(asctime)s] [%(module)s:%(lineno)d] %(message)s',
                            'datefmt': '%d/%m/%Y %H:%M:%S'}},
    'handlers': {
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'main'},
    },
    'loggers': {
        'main_logger': {'handlers': ['console'], 'propagate': False, 'level': 'DEBUG'},
    }
}
logging.config.dictConfig(LOGGING)
