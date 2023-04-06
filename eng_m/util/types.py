import sympy

from typing import Union


symbol = Union[
    sympy.core.mul.Mul,
    sympy.core.add.Add,
    sympy.core.symbol.Symbol,
    sympy.core.power.Pow,
    int,
    float,
]
