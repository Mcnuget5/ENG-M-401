import pytest
import sympy

import eng_m


def test_q1() -> None:
    """
    A contract is signed paying $3,059,405 at start of year 0, $2,463,788 for 5 years
    afterward, and then $2,926,395 for 5 years afterward. Find the npv of this contract
    with 9% interest.
    """
    interest = eng_m.Interest(0.09)
    initial_payment = eng_m.Series([3059405], interest)
    next_payment = eng_m.series.equal_payment_series(2463788, 5, interest)
    next_next_payment = eng_m.series.equal_payment_series(2926395, 5, interest)
    assert initial_payment.concat(next_payment).concat(
        next_next_payment
    ).npv == pytest.approx(20040626.51)


def test_q2() -> None:
    """
    At the start of year 1, 2, 3, 6, 7, and 8, $\\(n\\) is deposited. On years 9 and 10,
    $7,388 is withdrawn. What is the minimum value \\(n\\) that can pay for the
    withdrawls at 7% interest?
    """
    interest = eng_m.Interest(0.07)
    n = sympy.Symbol("n")
    series = eng_m.Series([0, n, n, n, 0, 0, n, n, n, -7388, -7388], interest=interest)
    assert series.zero(n) == pytest.approx(1729.38, abs=0.01)


def test_q3() -> None:
    """
    Series 1: $50, $0, -$100, -$150, -$200, -$250
    Find the equal payment for an equal payment series of the same length as series 1
    to have equal net present values at 7% interest.
    """
    interest = eng_m.Interest(0.07)
    n = sympy.Symbol("n")
    series_one = eng_m.Series([50, 0, -100, -150, -200, -250], interest)
    series_two = eng_m.series.equal_payment_series(n, 6, interest)
    assert series_one.equate(series_two, n) == pytest.approx(-96.20, abs=0.01)


def test_q5() -> None:
    """
    Your credit card charges 16.1% annual nominal interest, compounded daily.
    Find the monthly nominal interest rate and annual effective interest rate.
    """
    interest = eng_m.Interest(0.161, compounds=365)
    assert interest.annual_effective_interest == pytest.approx(0.1746, abs=0.0001)
    interest.compounds = 12
    assert interest.periodic_interest == pytest.approx(0.0134, abs=0.0001)


def test_q6() -> None:
    """
    Your credit card charges 1.26% monthly nominal interest, compounded monthly.
    What is the annual nominal interest rate and the annual effective interest rate?
    """
    interest = eng_m.Interest(0.0126, compounds=12, interest_type="periodic")
    assert interest.annual_nominal_interest == pytest.approx(0.1512, abs=0.0001)
    assert interest.annual_effective_interest == pytest.approx(0.1621, abs=0.0001)
