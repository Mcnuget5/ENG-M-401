import copy
import pytest
import sympy

import eng_m


def test_q1a() -> None:
    """
    Buy a $220,000 home with 10% down payment with a 20-year mortgage at 8.66% nominal
    annual interest rate, compounded semiannually. What is the monthly effective
    interest rate and your monthly payment?
    """
    # Method A: payment series
    x = sympy.Symbol("x")
    interest = eng_m.Interest(0.0866, compounds=2, interest_type="nominal")
    down = eng_m.Series([-220000 * 0.9], interest, compounds=12)
    payments = eng_m.series.equal_payment_series(x, 20 * 12, interest, compounds=12)
    payments = down.concat(payments)

    # Check monthly effective interest rate
    interest_check = copy.copy(interest)
    interest_check.recompound(12)
    assert interest_check.periodic_interest == pytest.approx(0.00709, abs=0.00001)

    # Check monthly payments
    assert payments.zero(x) == pytest.approx(1719.26, abs=0.01)

    # Method B: loan class
    y = sympy.Symbol("y")
    interest = eng_m.Interest(0.0866, compounds=2, interest_type="nominal")
    loan = eng_m.Loan(-220000 * 0.9, y, interest, length=20 * 12, compounds=12)
    assert loan.zero(y) == pytest.approx(1719.26, abs=0.01)


def test_q1b() -> None:
    """
    Buy a $220,000 home with 10% down payment with a 30-year mortgage at 11.31% nominal
    annual interest rate, compounded semiannually. What is the monthly effective
    interest rate and your monthly payment?
    """
    # Method A: payment series
    x = sympy.Symbol("x")
    interest = eng_m.Interest(0.1131, compounds=2, interest_type="nominal")
    down = eng_m.Series([-220000 * 0.9], interest, compounds=12)
    payments = eng_m.series.equal_payment_series(x, 30 * 12, interest, compounds=12)
    payments = down.concat(payments)

    # Check monthly effective interest rate
    interest_check = copy.copy(interest)
    interest_check.recompound(12)
    assert interest_check.periodic_interest == pytest.approx(0.00921, abs=0.00001)

    # Check monthly payments
    assert payments.zero(x) == pytest.approx(1893.44, abs=0.01)

    # Method B: loan class
    y = sympy.Symbol("y")
    interest = eng_m.Interest(0.1131, compounds=2, interest_type="nominal")
    loan = eng_m.Loan(-220000 * 0.9, y, interest, length=30 * 12, compounds=12)
    assert loan.zero(y) == pytest.approx(1893.44, abs=0.01)


def test_q2() -> None:
    """
    You borrow $10,000 at 9.2% annual interest, paying $2,000 back per year. What is the
    loan balance after the 3rd payment is made?
    """
    interest = eng_m.Interest(0.092)
    loan = eng_m.Loan(10000, -2000, interest, length=3, compounds=1)
    assert loan.start(3) == pytest.approx(6452.78, abs=0.01)


def test_q3() -> None:
    """
    Find the conventional payback period and the discounted payback period for this
    arbitrarily defined payment series at 10% interest rate.
    """
    interest = eng_m.Interest(0.1)
    loan = eng_m.Loan(
        -127500,
        [6667, 11250, 15000, 33750, 37500, 45750, 54000, 62250, 70500, 78750],
        interest,
        compounds=1,
    )
    assert loan.conventional_payback == 6
    assert loan.discounted_payback == 8
