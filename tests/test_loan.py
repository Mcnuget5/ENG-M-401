import pytest
import sympy

import eng_m


def test_variable_principal() -> None:
    """
    What principal can $1,000 per year for 10 years pay off at 30% nominal annual
    interest rate compounded monthly?
    (answer from: `sum 1000 / 1.6320941326 ^ i from i = 1 to 10`)
    """
    n = sympy.Symbol("n")
    interest = eng_m.Interest(0.3, compounds=12, interest_type="nominal")
    loan = eng_m.Loan(-n, 1000, interest, 10, compounds=1)
    assert loan.zero(n) == pytest.approx(2749.70, abs=0.01)


def test_variable_payment() -> None:
    """
    You borrow $883,389 and have 10 semiannual payments to pay it off. Interest is 0.1%
    daily. What are your semiannual payments?
    """
    n = sympy.Symbol("n")
    interest = eng_m.Interest(0.001, compounds=365, interest_type="periodic")
    loan = eng_m.Loan(-883389, n, interest, 10, compounds=2)
    assert loan.zero(n) == pytest.approx(210783.29, abs=0.01)
