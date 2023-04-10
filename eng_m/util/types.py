import sympy

from typing import Union


expression = Union[
    sympy.core.mul.Mul,
    sympy.core.add.Add,
    sympy.core.symbol.Symbol,
    sympy.core.power.Pow,
    int,
    float,
]

optional = Union[
    int,
    float,
    None,
]

unsolved = Union[
    sympy.core.mul.Mul,
    sympy.core.add.Add,
    sympy.core.symbol.Symbol,
    sympy.core.power.Pow,
]

numeric = Union[int, float]
