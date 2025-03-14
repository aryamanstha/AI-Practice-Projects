import logging.config
from pythonjsonlogger import jsonlogger
import re


class filter_sensitive_data(logging.Filter):
    def filter(self, record):
        record.msg = re.sub(r"(password[:=])\s*\S+", "password=********",str(record.getMessage()),flags=re.IGNORECASE)
        return True
    
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "sensitive_data": {
            "()": filter_sensitive_data
        }
    },
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
            "filters": ["sensitive_data"]
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "DEBUG"}},
}

logging.config.dictConfig(LOGGING)