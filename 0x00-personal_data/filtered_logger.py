#!/usr/bin/env python3
"""
Returns the log message obfuscated
"""
import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "ssn", "password", "phone_number")

patterns = {
        'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        'replace': lambda x: r'\g<field>={}'.format(x),
        }


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """Obfuscates specified fields."""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize formatter with fields"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record by redacting fields"""
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and configures a logger for user data with redaction."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)

    logger.addHandler(stream_handler)
    return logger
