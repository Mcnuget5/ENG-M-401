import pytest
import random

import eng_m


def test_series_end_lump_sum() -> None:
    """
    Receive a lump sum payment of $12,000 at start of year 0, with interest = 12%.
    What is the value of this at end of year 5?
    """
    interest = eng_m.Interest(0.12)
    series = eng_m.Series([12000], interest)
    assert series.end(5) == pytest.approx(23685.87)


def test_series_end() -> None:
    """
    Receive $1,000 per year for 5 years, with interest = 10%. How much money do you
    have in this account at end of year 3?
    """
    interest = eng_m.Interest(0.1)
    series = eng_m.series.equal_payment_series(1000, 6, interest)
    assert series.end(3) == pytest.approx(5105.1)


def test_series_end_limit() -> None:
    """
    Receive $1,000 per year for 5 years, with interest = 10%. How much money do you
    have in this account at end of year 6?
    """
    interest = eng_m.Interest(0.1)
    series = eng_m.series.equal_payment_series(1000, 6, interest)
    assert series.end(6) == pytest.approx(9335.8881)


def test_series_start_lump_sum() -> None:
    """
    Receive a lump sum payment of $14,000 at start of year 0, with interest = 11%.
    What is the value of this at the start of year 3?
    """
    interest = eng_m.Interest(0.11)
    series = eng_m.Series([14000], interest)
    assert series.start(3) == pytest.approx(19146.83)


def test_series_start() -> None:
    """
    Receive $1,000 per year for 5 years with interest = 10%. How much money do you have
    in this account at start of year 4?
    """
    interest = eng_m.Interest(0.1)
    series = eng_m.series.equal_payment_series(1000, 6, interest)
    assert series.start(4) == pytest.approx(6105.1)


def test_series_start_limit() -> None:
    """
    Receive $1,000 per year for 5 years with interest = 10%. How much money do you have
    in this account at start of year 6?
    """
    interest = eng_m.Interest(0.1)
    series = eng_m.series.equal_payment_series(1000, 6, interest)
    assert series.start(6) == pytest.approx(8487.171)


def test_sinking_fund_worthlessness() -> None:
    """
    Tests that sinking fund has nfv == npv == 0 for an arbitrary input.
    """
    series = eng_m.series.sinking_fund(
        random.randint(0, 10000),
        random.randint(5, 30),
        eng_m.Interest(random.random() / 2),
    )
    assert series.npv == pytest.approx(0, abs=0.0001)
    assert series.nfv == pytest.approx(0, abs=0.0001)


def test_capital_recovery_worthlessness() -> None:
    """
    Tests that capital recovery has nfv == npv == 0 for an arbitrary input.
    """
    series = eng_m.series.capital_recovery(
        random.randint(0, 10000),
        random.randint(5, 30),
        eng_m.Interest(random.random() / 2),
    )
    print(series)
    assert series.npv == pytest.approx(0, abs=0.0001)
    assert series.nfv == pytest.approx(0, abs=0.0001)


def test_geometric_gradient_series() -> None:
    """
    Tests that the geometric gradient series function returns what's expected
    """
    series = eng_m.series.geometric_gradient(1000, 1.1, 5, eng_m.Interest(0.1))
    assert series.payments[0] == pytest.approx(0, abs=0.01)
    assert series.payments[1] == pytest.approx(1000, abs=0.01)
    assert series.payments[2] == pytest.approx(1100, abs=0.01)
    assert series.payments[3] == pytest.approx(1210, abs=0.01)
    assert series.payments[4] == pytest.approx(1331, abs=0.01)
    assert series.payments[5] == pytest.approx(1464.1, abs=0.01)
