import pytest
import sympy

import eng_m


def test_l9_q1() -> None:
    """
    You buy a 5-year GIC for $1,000, with 3% interest per half-annum compounded every
    half-annum. 2 years later, you buy a 3-year GIC for $1,000 with 2% interest per
    half-annum compounded every half-annum. How much money do you receive when both
    these GICs mature?
    """
    interest_five_year = eng_m.Interest(0.03, compounds=2, interest_type="periodic")
    interest_three_year = eng_m.Interest(0.02, compounds=2, interest_type="periodic")
    gic_five_year = eng_m.Series(
        [1000, 0, 0, 0, 0, 0, 0, 0, 0, 0], interest_five_year, compounds=2
    )
    gic_three_year = eng_m.Series(
        [0, 0, 0, 0, 1000, 0, 0, 0, 0, 0], interest_three_year, compounds=2
    )
    assert gic_five_year.nfv + gic_three_year.nfv == pytest.approx(2470.08, 0.01)


def test_l9_q2() -> None:
    """
    How much is $3,000 in 5 years worth today at 8% interest?
    """
    interest = eng_m.Interest(0.08)
    series = eng_m.Series([0, 0, 0, 0, 0, 3000], interest)
    assert series.npv == pytest.approx(2041.75, 0.01)


def test_l10_q1() -> None:
    """
    At 8% interest, is a single payment of $17,000,000 today or $1,000,000 every year
    starting at start of year 1 better?
    """
    interest = eng_m.Interest(0.08)
    choice = eng_m.Series([0], interest).concat(
        eng_m.series.equal_payment_series(1000000, 25, interest)
    )
    assert choice.npv < 17000000


def test_l11_q1() -> None:
    """
    The maintenance cost of a truck starts at $1,000 at the start of year 1 and
    increases by $250 per year, up to $2,000 at the start of year 5. At 12% interest,
    how much should be deposited now to pay for the maintenance cost?
    """
    interest = eng_m.Interest(0.12)
    x = sympy.Symbol("x")
    maint = eng_m.Series([x, -1000, -1250, -1500, -1750, -2000], interest)
    print(maint.zero(x))
