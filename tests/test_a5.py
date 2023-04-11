import pytest

import eng_m


def test_q1() -> None:
    """
    Here are four arbitrarily defined series. Find their equivalent annual
    worth at 10% interest and their acceptability.
    """
    interest = eng_m.Interest(0.1)
    assert eng_m.Series(
        [-2200, 400, 500, 600, 700, 800], interest
    ).eaw == pytest.approx(0.66, abs=0.01)
    assert eng_m.Series(
        [-4500, 3000, 2000, 1000, 500, 500], interest
    ).eaw == pytest.approx(338.58, abs=0.01)
    assert eng_m.Series(
        [-8000, -2000, 6000, 2000, 4000, 2000], interest
    ).eaw == pytest.approx(162.77, abs=0.01)
    assert eng_m.Series(
        [-9700, 2000, 4000, 8000, 8000, 4000], interest
    ).eaw == pytest.approx(2475.02, abs=0.01)


def test_q2() -> None:
    """
    Here are two more arbitrary series. Find their present worths at 9%
    interest.
    """
    interest = eng_m.Interest(0.09)
    assert eng_m.Series(
        [-850, -1500, -435, 775, 775, 1275, 1275, 975, 675, 375, 660], interest
    ).npv == pytest.approx(1467.67, abs=0.01)
    assert eng_m.Series(
        [-2800, -565, 820, 820, 1080, 1880, 1500, 980, 580, 380, 840], interest
    ).npv == pytest.approx(2243.35, abs=0.01)


def test_q4() -> None:
    """
    You own a depreciable asset worth $49,036,000 at start of year 0, with a
    useful life of 8 years, and salvage value worth $4,776,000. Using the
    straight line method, find the book value at the end of year 2.
    """
    assert eng_m.Depreciable(49036000, 4776000, 8).book_value(2) == pytest.approx(
        37971000.0, abs=0.01
    )


def test_q5() -> None:
    """
    You own a depreciable asset worth $12,000 at the start of year 0, with a
    useful life of 5 years, and salvage value worth $2,000. Using the SOYD
    method, find the SOYD denominator, the amount of depreciation after the
    first year of use, and the book value atht end of year 4.
    """
    depreciable = eng_m.Depreciable(12000, 2000, 5)
    assert depreciable.soyd == 15
    assert depreciable.depreciation(1, method="soyd") == pytest.approx(
        3333.33, abs=0.01
    )
    assert depreciable.book_value(4, method="soyd") == pytest.approx(2666.67, abs=0.01)


def test_q6() -> None:
    """
    You own an office building worth $429,350 (CCA Class 1). Find the marginal
    capital cost allowance each year for the first 5 years, using the half-year
    convention.
    """
    depreciable = eng_m.Depreciable(429350, 0, 100, cca=1, depreciation_class=True)
    assert depreciable.cca(0) == pytest.approx(0, abs=0.01)
    assert depreciable.cca(1) == pytest.approx(8587.00, abs=0.01)
    assert depreciable.cca(2) == pytest.approx(16830.52, abs=0.01)
    assert depreciable.cca(3) == pytest.approx(16157.30, abs=0.01)
    assert depreciable.cca(4) == pytest.approx(15511.01, abs=0.01)
    assert depreciable.cca(5) == pytest.approx(14890.57, abs=0.01)
