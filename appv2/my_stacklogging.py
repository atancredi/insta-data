#type: ignore
import logging
from logging import DEBUG, root, Formatter
from json import dumps
from math import modf
from typing import Optional, List
from time import time

# (stack)logger VERSION: v2.0.1
# 1.0.0: old version
# 1.1.0: refactored
# 1.2.0: added timelog
# 2.0.0: added color and json formatter, the logger is now modular
# 2.0.1: refactored and such

#REGION class helpers
class Serializable:
    def as_dict(self, obj = None):
        ret = {}
        if obj != None:
            read = obj.__dict__
        else:
            read = self.__dict__

        for key in read:
            value = read[key]
            if "data." in str(type(value)):
                ret[key] = self.as_dict(obj=value)
            else:
                ret[key] = value
        return ret

class Settable:
    def __setitem__(self,k,v):
        setattr(self,k,v)

    def __getitem__(self,k):
        return getattr(self, k)

    def set(self,obj: dict):
        if obj == None:
            return

        for key in obj:
            self[key] = obj[key]
#ENDREGION

#REGION data
RESERVED = frozenset(
    (
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "id",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    )
)

class Payload(Serializable,Settable):
    """
    Payload: this class contains the data to be logged
    """
    message: str = ""
    severity: str = ""
    timestamp: Optional[dict] = None
    thread: Optional[int] = None
    extra: Optional[dict] = None

    def fill(self, record: logging.LogRecord)->None:
        self.message = record.msg
        self.severity = record.levelname
        self.message = record.msg
        self.severity = record.levelname
        self.thread = record.thread
        subsecond, second = modf(record.created)
        self.timestamp = {"seconds": int(second), "nanos": int(subsecond * 1e9)}

        extra_keys = []
        for key, value in record.__dict__.items():
            if key not in RESERVED and not key.startswith("_"):
                extra_keys.append(key)
        if len(extra_keys) > 0:
            self.extra = {}
            for key in extra_keys:
                try:
                    dumps(record.__dict__[key])  # serialization/type error check
                    self.extra[key] = record.__dict__[key]
                except TypeError:
                    self.extra[key] = str(record.__dict__[key])
#ENDREGION

#REGION formatters
class ColorFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    green = '\x1b[38;5;42m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt = '%(asctime)s | %(levelname)8s | %(message)s'):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.info: self.grey + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class JsonFormatter(logging.Formatter):

    reduced_output: bool = True

    def __init__(self, reduced_output = None):
        super().__init__()
        self.fmt = '%(message)s'
        if reduced_output is not None:
            self.reduced_output = reduced_output

    def format(self,record: logging.LogRecord):
        payload = Payload()
        payload.fill(record)

        payload = payload.__dict__
        if self.reduced_output:
            del payload["thread"]
            del payload["timestamp"]

        return dumps(payload)
#ENDREGION

#REGION core
class StackLogger:
    logger: logging.Logger

    def __init__(self, level=DEBUG, formatter=None, reduced_output=False) -> None:
        self.level = level
        self.formatter = formatter
        self.reduced_output = reduced_output

        self.remove_all_loggers()
        self.logger, self.logger_handler = self.set_root_logger()

    def set_root_logger(self):
        logger = logging.getLogger()
        logger.setLevel(self.level)

        logger_handler = logging.StreamHandler()
        logger_handler.setLevel(self.level)
        if self.formatter:
            logger_handler.setFormatter(self.formatter)

        logger.propagate = True
        logger.disabled = False
        logger.addHandler(logger_handler)

        return logger, logger_handler

    def remove_all_loggers(self,include_root=True):
        loggers = self.get_all()
        if include_root:
            loggers.append(logging.getLogger())
        for l in loggers:
            l.propagate = False
            l.disabled = True
            l.handlers.clear()

    def set_level(self,level):
        self.logger.setLevel(level)
        self.logger.removeHandler(self.logger_handler)
        self.logger_handler.setLevel(level)
        self.logger.addHandler(self.logger_handler)

    def get_all(self) -> List[logging.Logger]:
        return [logging.getLogger(name) for name in root.manager.loggerDict]

    def get(self):
        return self.logger
#ENDREGION

#REGION timelog
class Timelog:
    time: float

    def __enter__(self):
        self.time = time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.time = time() - self.time
#ENDREGION

def new_logger(level: int = DEBUG, reduced_output: bool = True, formatter: Formatter = JsonFormatter()) -> logging.Logger:
    return StackLogger(level=level, reduced_output=reduced_output, formatter=formatter).get()
