# type: ignore
"""Module with incorrect type usage that will trigger beartype violations."""


def main(numbers: list[int]) -> str:
    return sum(numbers)


def helper_function(text: str) -> int:
    return text.upper()
