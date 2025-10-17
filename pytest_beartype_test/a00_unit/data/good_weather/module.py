"""Module with correct type annotations that won't trigger beartype violations."""


def main(numbers: list[int]) -> int:
    """Function with correct types - no beartype violations."""
    return sum(numbers)


def helper_function(text: str) -> str:
    """Another function with correct types."""
    return text.upper()
