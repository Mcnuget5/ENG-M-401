import pytest
import sympy

import eng_m


def test_q1() -> None:
    """
    You are lent $19,119. Your lendor earns 7.99% interest annually. What lump-sum
    payment should you make at the start of year two for your lendor's investment to be
    worth it?
    """
    interest = eng_m.Interest(0.0799)
    series = eng_m.Series([19119, 0], interest)
    assert series.nfv == pytest.approx(22296.27)


def test_q2() -> None:
    """
    Option 1: receive $11,793 at the start of year 5
    Option 2: deposit \\(n\\) dollars at 5.35% interest
    For what value \\(n\\) are the two options equivalent?
    """
    n = sympy.Symbol("n")
    interest = eng_m.Interest(0.0535)
    option_one = eng_m.Series([0, 0, 0, 0, 11793], interest)
    option_two = eng_m.Series([n, 0, 0, 0, 0], interest)
    assert option_one.equate(option_two, n) == pytest.approx(9573.84)
