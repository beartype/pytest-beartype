# type: ignore
from __future__ import annotations
from typing import TYPE_CHECKING

try:
    from typing import List
except ImportError:
    if not TYPE_CHECKING:
        List = list  # Fallback for very old/very modern Python versions


"""Module with incorrect type usage that will trigger beartype violations."""


def main(numbers: list[int]) -> str:
    return sum(numbers)


def helper_function(text: str) -> int:
    return text.upper()
