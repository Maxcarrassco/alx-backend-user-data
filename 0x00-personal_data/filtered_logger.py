#!/usr/bin/env python3
"""ALX SE Backend User Data Module."""
import re
import logging
from typing import List
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return the Obfuscated version of a message."""
    return re.sub(
        fr"({'|'.join(fields)})=[^{separator}]*", fr"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the message while obfuscating it."""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Return a new log"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.info)
    logger.propagate = False
    fmt = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a db connection."""
    DB_USER = os.environ['PERSONAL_DATA_DB_USERNAME']
    DB_PASSWORD = os.environ['PERSONAL_DATA_DB_PASSWORD']
    DB_HOST = os.environ['PERSONAL_DATA_DB_HOST']
    DB_NAME = os.environ['PERSONAL_DATA_DB_NAME']
    return mysql.connector.connect(host=DB_HOST, user=DB_USER,
                                   password=DB_PASSWORD, database=DB_NAME)


def main() -> None:
    """Print user record from db."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    fmt = RedactingFormatter(PII_FIELDS)
    for (name, email, phone, ssn,
         password, ip, last_login, user_agent) in cursor:
        msg = (
            f'name={name};email={email};phone={phone};ssn={ssn}'
            f'password=password;ip={ip};'
            f'last_login={last_login};user_agent={user_agent};')
        logger = logging.LogRecord('user-data', logging.INFO, None, None,
                                   msg, None, None)
        print(fmt.format(logger))


if __name__ == '__main__':
    main()
