"""
Author:     David Walshe
Date:       28 May 2022
"""

from logging import setLoggerClass, getLogger
from os import environ

from src.common.logging import JSONLogger

setLoggerClass(JSONLogger)

# Obtain logger configuration from environment variables.
LOGGER_NAME = environ.get("LOGGER_NAME", "app-logger")
LOGGER_LEVEL = environ.get("LOGGER_LEVEL", "INFO")

# Specifying the type of logger as a JSONLogger allows IDE auto-complete to work on new functions.
logger: JSONLogger = getLogger(LOGGER_NAME)
logger.default_setup(level=LOGGER_LEVEL)
