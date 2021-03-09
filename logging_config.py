LOG_CONF = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(asctime)s] [%(levelname)s] (%(name)s:%(funcName)s:%(lineno)s): %(message)s"},
        "commit": {"format": "[%(asctime)s] %(message)s"},
    },
    "filters": {},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "botocore": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "boto3": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "github": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "urllib3": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
