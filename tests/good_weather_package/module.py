from __future__ import annotations
from typing import TYPE_CHECKING

try:
    from typing import List
except ImportError:
    if not TYPE_CHECKING:
        List = list  # Fallback for very old/very modern Python versions

"""Module with correct type annotations that won't trigger beartype violations."""


def main(numbers: list[int]) -> int:
    """Function with correct types - no beartype violations."""
    return sum(numbers)


def helper_function(text: str) -> str:
    """Another function with correct types."""
    return text.upper()
