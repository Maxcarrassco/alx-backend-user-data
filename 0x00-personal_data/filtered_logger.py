#!/usr/bin/env python3
"""ALX SE Backend User Data Module."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    for field in fields:
        msg = re.sub(fr'(?<={field}=)([^{sep}]*)', redaction, msg)
    return msg
