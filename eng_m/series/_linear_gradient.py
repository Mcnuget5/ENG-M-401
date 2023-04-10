from eng_m import Series, Interest
from eng_m.util.types import expression


def linear_gradient(
    base: expression, length: int, interest: Interest, compounds: int = 1
) -> Series:
    return Series([base * i for i in range(length)], interest, compounds=compounds)
