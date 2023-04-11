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


def test_l24_q1() -> None:
    """
    You purchase a class 8 asset costing $100,000 with 6 useful years and zero
    salvage value. It generates $300,000 per year, and costs $150,000 in labour
    and materials. At 40% marginal tax rate and a 12% minimum acceptable rate
    of return, is this purchase viable?
    """
    asset = eng_m.Depreciable(100000, 0, 6, cca=8, cca_class=True)
    revenues = [0, 300000, 300000, 300000, 300000, 300000, 300000]
    costs = [0, 150000, 150000, 150000, 150000, 150000, 150000]
    project = eng_m.Project(
        revenues,
        cost=costs,
        depreciable=[asset],
        tax_rate=0.4,
        marr=eng_m.Interest(0.12),
    )
    assert project.npv == pytest.approx(295929, abs=1)
    assert project.net_cash_flow(3) == pytest.approx(95760, abs=1)
    assert project.net_income(5) == pytest.approx(84470, abs=1)
    assert project.ebit(6) == pytest.approx(142627, abs=1)


def test_l24_q2() -> None:
    """
    You purchase the following:
    Equipment: $600,000, useful for 4 years, $200,000 salvage value, CCA class 43
    Building: $1,200,000, useful for 4 years, $600,000 salvage value, 4% CCA rate
    Land: $200,000, useful for 4 years, $300,000 salvage value, 0% CCA rate.
    You generate $900,000 in revenue per year and spend $250,000 in operating costs.
    At 40% tax and 17% minimal acceptable rate of return, is this a viable investment?
    """
    equipment = eng_m.Depreciable(600000, 200000, 4, cca=43, cca_class=True)
    building = eng_m.Depreciable(1200000, 600000, 4, cca=0.04)
    land = eng_m.Depreciable(200000, 300000, 4)
    revenues = [0, 900000, 900000, 900000, 900000]
    costs = [0, 250000, 250000, 250000, 250000]
    project = eng_m.Project(
        revenues,
        cost=costs,
        depreciable=[equipment, building, land],
        tax_rate=0.4,
        marr=eng_m.Interest(0.17),
    )
    assert project.ebit(2) == pytest.approx(449960, abs=1)
    assert project.net_cash_flow(3) == pytest.approx(450903, abs=1)
    assert project.net_income(4) == pytest.approx(319007, abs=1)
    # no, this is not a viable investment.
    assert project.npv < 0
    assert project.eaw < 0


def test_l24_q3() -> None:
    """
    stuff
    """
    x = sympy.Symbol("x")
    loan = eng_m.Loan(100000, x, eng_m.Interest(0.1), length=4, compounds=1)
    loan.subs({x: loan.zero(x)})
    depreciable = eng_m.Depreciable(200000, 30000, 4, 0.3)
    revenue = [0] + [100000 for _ in range(4)]
    project = eng_m.Project(
        revenue=revenue,
        loan=loan,
        depreciable=[depreciable],
        tax_rate=0.35,
        marr=eng_m.Interest(0.15),
    )
    assert project.net_cash_flow(0) == pytest.approx(-100000, abs=1)
    assert project.net_cash_flow(1) == pytest.approx(47453, abs=1)
    assert project.net_cash_flow(2) == pytest.approx(54049, abs=1)
    assert project.net_cash_flow(3) == pytest.approx(47864, abs=1)
    assert project.net_cash_flow(4) == pytest.approx(83112, abs=1)
    assert project.net_income(0) == pytest.approx(0, abs=1)
    assert project.net_income(1) == pytest.approx(39000, abs=1)
    assert project.net_income(2) == pytest.approx(26751, abs=1)
    assert project.net_income(3) == pytest.approx(38236, abs=1)
    assert project.net_income(4) == pytest.approx(46892, abs=1)
