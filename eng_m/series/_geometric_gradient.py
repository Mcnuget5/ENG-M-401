from eng_m import Series, Interest
from eng_m.util.types import expression


def geometric_gradient(
    base: expression,
    geometric_factor: expression,
    length: int,
    interest: Interest,
    compounds: int = 1,
) -> Series:
    """
    Returns a geometric gradient series with the a certain amount of payments, with the
    first payment on start of year 1.

    Parameters
    ----------
    base: expression - base value for geometric gradient series
    geometric_factor: expression - factor to increase payments by
    length: int - number of payments to be made
    interest: Interest - interest associated with this series

    Returns
    -------
    AnnualSeries - geometric gradient series with length + 1 elements, with the first
                   payment on start of year 1
    """
    return Series(
        [0] + [base * geometric_factor**i for i in range(length)],
        interest,
        compounds=compounds,
    )
