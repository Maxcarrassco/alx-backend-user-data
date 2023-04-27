#!/usr/bin/env python3
"""ALX SE Backend User Data Module."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    return re.sub(fr"({'|'.join(fields)})=[^{sep}]*", fr"\1={redaction}", msg)
