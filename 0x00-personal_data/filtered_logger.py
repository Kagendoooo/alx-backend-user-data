#!/usr/bin/env python3
"""
Returns the log message obfuscated
"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """Obfuscates specified fields."""
    pattern = f"({'|'.join(fields)})=[^;]+"
    return re.sub(
        pattern, lambda match: f"{match.group(1)}={redaction}", message)
