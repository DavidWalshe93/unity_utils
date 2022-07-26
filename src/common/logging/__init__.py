"""
Author:     David Walshe
Date:       17 May 2022
"""

from typing import Any, Dict
from datetime import datetime
import json
from decimal import Decimal

from logging import Logger, Formatter, NOTSET, StreamHandler, LogRecord
from logging.handlers import RotatingFileHandler

from pygments import highlight, lexers, formatters


class JSONLogger(Logger):
    """Create a logger that outputs JSON."""

    def __init__(self, name: str, level: int = NOTSET):
        """
        Create a new logger.

        :param name: The name of the logger.
        :param level: The log level to start this logger with.
        """
        super().__init__(name=name, level=level)
        self.default_fields = {}

    def _log(self, level, msg, args, **kwargs):
        """
        Overrides the main log method to inject default fields.

        If the msg is not a dict object, the default fields will be ignored.
        """
        if isinstance(msg, dict) and self.default_fields:
            message = self.default_fields.copy()
            message.update(msg)
        else:
            message = msg

        super()._log(level=level, msg=message, args=args, **kwargs)

    def default_setup(self, level: str, propagate: bool = False):
        """
        Performs basic setup for the logger.

        :param level: The log level to set.
        :param propagate: If logs should progagate to higher level handlers.
        """
        self.setLevel(level=level.upper())
        self.propagate = propagate

        handler = StreamHandler()
        handler.setLevel(level=level.upper())
        handler.setFormatter(StreamJSONFormatter())
        self.addHandler(handler)

        handler = RotatingFileHandler(filename=f"./logs/app.log.json", maxBytes=1048576, backupCount=5)
        handler.setLevel(level=level.upper())
        handler.setFormatter(JSONFormatter())
        self.addHandler(handler)

    def add_default_fields(self, default_fields: Dict[str, Any]):
        """
        Add default feilds that are used in all logs. If the log message is a dict, it is merged into the default
        fields before logging, overriding any default fields as applicable.
        :param default_fields: The default fields to add.
        """
        self.default_fields.update(default_fields)

    def clear_default_fields(self):
        """Clear all default fields."""
        self.default_fields = {}

    def clear_formatters(self):
        """
        Clear all formatters for every handler attached to this logger or its parents. working to the top of the
        logging stack. This is particularly useful in the context of an AWS Lambda functions where Amazon injects a
        log formatter at the top of the logging stack that prevents logs from being pure JSON.
        """
        current_logger = self
        while current_logger:
            for handler in current_logger.handlers:
                handler.setFormatter(JSONFormatter())
            current_logger = current_logger.parent  # Is None if no parent is present, exiting the while loop.

    def set_handler_levels(self, level: str):
        """
        Set the log level on the current handler and all parent handlers
        :param level: The level to set for handlers.
        """
        current_logger = self
        while current_logger:
            current_logger.handlers = []
            current_logger = current_logger.parent  # Is None if no parent is present, exiting the while loop.


class CustomJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects and Decimal objects."""

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


class JSONFormatter(Formatter):
    """A formatter that outputs JSON."""

    def format(self, record: LogRecord):
        """Format the log record as JSON."""
        log_info = {
            "t": datetime.utcfromtimestamp(record.created).isoformat().split(".")[0] + "Z",
            "level": record.levelname
        }

        if record.exc_info:
            log_info["exceptionInfo"] = self.formatException(ei=record.exc_info)
        if not isinstance(record.msg, (str, int, float, dict, list, bool, type(None))):
            log_info["message"] = str(record.msg)
        else:
            log_info["message"] = record.msg

        return json.dumps(log_info, cls=CustomJsonEncoder)


class StreamJSONFormatter(JSONFormatter):
    """A formatter that outputs colorized JSON."""

    def format(self, record: LogRecord):
        """Format the log record as JSON."""
        formatted_json = super().format(record)
        colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())

        return colorful_json.strip()