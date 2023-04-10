from eng_m import Series, Interest
from eng_m.util.types import expression


def equal_payment_series(
    value: expression, length: int, interest: Interest, compounds: int = 1
) -> Series:
    """
    Returns a series with equal payments an arbitrary number of times with arbitrary
    interest.

    Parameters
    ----------
    value
    length
    interest

    Returns
    -------

    """
    return Series([value for _ in range(length)], interest, compounds=compounds)


def sinking_fund(
    final_value: expression, length: int, interest: Interest, compounds: int = 1
) -> Series:
    """
    Returns an equal payment series with arbitrary interest worth a certain value at the
    start of the last year. This series' npv == nfv == 0.

    Parameters
    ----------
    final_value: eng_m.util.types.symbol - the desired quantity to withdraw at the last
                                           time step
    length: int - the number of equal payments to be made
    interest: eng_m.Interest - the interest to be used for the series

    Returns
    -------
    eng_m.Series - a series of equal payments with \\(final_value - payment\\) withdrawn
                   at the last time step.
    """
    payment = final_value * (
        interest.periodic_interest / ((1 + interest.periodic_interest) ** length - 1)
    )
    series = [-payment for _ in range(length)]
    series[-1] += final_value
    return Series(series, interest, compounds=compounds)


def capital_recovery(
    initial_value: expression, length: int, interest: Interest, compounds: int = 1
):
    """
    Returns an equal payment series with arbitrary interest worth a certain value at the
    start of the zeroth year.

    Parameters
    ----------
    initial_value: eng_m.util.types.symbol - the desired quantity to deposit at the
                                             first time step
    length: int - the number of equal payments to be made
    interest: eng_m.Interest - the interest to be used for the series

    Returns
    -------
    eng_m.Series - a series of equal payments with initial_value deposited at the zeroth
                   time step.
    """
    payment = (
        initial_value
        * ((1 + interest.periodic_interest) ** length)
        * interest.periodic_interest
        / ((1 + interest.periodic_interest) ** length - 1)
    )
    series = [-initial_value] + [payment for i in range(length)]
    return Series(series, interest, compounds=compounds)
