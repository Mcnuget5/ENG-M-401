import pytest
import sympy

import eng_m


def test_q3() -> None:
    """
    You purchase a machine for $125,000 that is useful for 5 years and has salvage
    value $50,000. It generates $100,000 per year and costs $40,000 per year.
    At a CCA rate of 30%, a tax rate of 40%, and a minimum acceptable rate of return
    of 15%, what is the net income in year 2?
    """
    machine = eng_m.Depreciable(125000, 50000, 5, cca=0.3)
    revenues = [0, 100000, 100000, 100000, 100000, 100000]
    costs = [0, 40000, 40000, 40000, 40000, 40000]
    project = eng_m.Project(
        revenues,
        cost=costs,
        depreciable=[machine],
        tax_rate=0.4,
        marr=eng_m.Interest(0.4),
    )
    project.net_income(2)


def test_q4() -> None:
    """
    A depreciable asset was purchased 3 years ago for $250,000. It is sold for
    $280,000 and the asset had a CCA rate of 30%. If the company's marginal tax rate
    is 40%, find the tax credits (debits) accrued on this disposal.
    """
    asset = eng_m.Depreciable(250000, 280000, 3, cca=0.3)
    asset.disposal_tax_effect(0.4)


def test_q5() -> None:
    """
    A revenueless asset costing $2,110,000 has a five year service life and salvage
    value equal to ten percent its principal value. It has a CCA rate of 30%.
    Additionally, 40% of the asset's principal will be financed with a 5 year loan
    at 10% interest. If the marginal tax rate is 35% and the minimum acceptable rate
    of return is 18%, find the equivalent annual worth.
    """
    x = sympy.Symbol("x")
    asset = eng_m.Depreciable(2110000, 2110000 * 0.1, 5, cca=0.3)
    loan = eng_m.Loan(0.4 * 2110000, x, eng_m.Interest(0.1), 5, compounds=1)
    loan.principals(x)
    project = eng_m.Project(
        [0, 0, 0, 0, 0, 0],
        loan=loan,
        depreciable=[asset],
        tax_rate=0.35,
        marr=eng_m.Interest(0.18),
    )
    assert project.eaw == pytest.approx(-443402, abs=1)
    assert project.net_cash_flow(0) == pytest.approx(-1266000, abs=1)
    assert project.net_cash_flow(1) == pytest.approx(-82330, abs=1)
    assert project.net_income(3) == pytest.approx(-280802, abs=1)
    assert project.ebit(4) == pytest.approx(-302285, abs=1)


def test_q6() -> None:
    """
    A machine costing $20,000 with a 10 year useful life and no salvage value is
    purchased. It generates $6,000 per year and costs $1,000 per year. At a 15%
    minimum acceptable rate of return, how many years does the machine take to become
    profitable?
    """
    asset = eng_m.Depreciable(20000, 0, 10)
    revenues = [0] + [6000] * 10
    costs = [0] + [1000] * 10
    project = eng_m.Project(
        revenues, cost=costs, depreciable=[asset], marr=eng_m.Interest(0.15)
    )
    assert project.start(6) < 0
    assert project.start(7) > 0
