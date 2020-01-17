import logging.config


DAYS = 30
UPDATE_TIME = '00:00'
TOP_FLIGHTS = (
    ('ALA', 'TSE'),
    ('TSE', 'ALA'),
    ('ALA', 'MOW'),
    ('MOW', 'ALA'),
    ('ALA', 'CIT'),
    ('CIT', 'ALA'),
    ('TSE', 'MOW'),
    ('MOW', 'TSE'),
    ('TSE', 'LED'),
    ('LED', 'TSE'),
)


REDIS_HOST = 'kiwi_redis'
REDIS_PORT = 6379
REDIS_DB = 0


# LOGGING ------------------------------------------------------------------------------------------------
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
