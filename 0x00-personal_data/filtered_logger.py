#!/usr/bin/env python3
"""ALX SE Backend User Data Module."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return the Obfuscated version of a message."""
    return re.sub(
        fr"({'|'.join(fields)})=[^{separator}]*", fr"\1={redaction}", message)
