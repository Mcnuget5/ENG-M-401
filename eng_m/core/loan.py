from __future__ import annotations

import sympy

from eng_m.core.series import Series
from eng_m.core.interest import Interest

from eng_m.util.types import expression
from eng_m.util.exceptions import InvalidSeriesError

from typing import Union, Optional, get_args


class Loan(Series):
    def __init__(
        self,
        principal: expression,
        payment: Union[expression, list[expression]],
        interest: Interest,
        length: Optional[int] = None,
        compounds: int = 12,
    ):
        if isinstance(payment, list) and length is None:
            super().__init__([-principal] + payment, interest, compounds)
        elif isinstance(payment, get_args(expression)) and isinstance(length, int):
            super().__init__(
                [-principal] + [payment for _ in range(length)], interest, compounds
            )
        else:
            raise InvalidSeriesError("what")

    @property
    def conventional_payback(self) -> Optional[int]:
        """
        Returns the conventional payback period of a loan assuming negative principal.
        Uses end-of-period convention. Returns none if loan never paid off.
        """
        sum = 0
        for i, j in enumerate(self.payments):
            sum += j  # type: ignore
            if sum > -0.000001:
                return i
        return None

    @property
    def discounted_payback(self) -> Optional[int]:
        """
        Returns the conventional payback period of a loan assuming negative principal.
        Uses end-of-period convention.
        # todo: dp'able, top down.
        """
        for i, j in enumerate(range(len(self.payments))):
            if self.start(j) > -0.000001:
                return i
        return None

    def principals(
        self, variable: Optional[sympy.Symbol] = None, delta: bool = False
    ) -> list[expression]:
        """
        # todo: rly slow. easily fixable with a top-down dp approach.
        """
        if variable is not None:
            self.subs({variable: self.zero(variable)})
        if delta:
            principals = self.principals()
            return [self.payments[0]] + [
                principals[i + 1] - principals[i] for i in range(len(principals) - 1)
            ]
        return [self.start(i) for i in range(len(self.payments))]

    def interests(self, variable: Optional[sympy.Symbol] = None) -> list[expression]:
        """
        # todo: little janky but works for all realistic test cases :3
        """
        if variable is not None:
            principals = self.principals(variable)
        else:
            principals = self.principals()

        interest = []
        for i, j in enumerate(principals):
            interest.append(self.interest.periodic_interest * j)

        return [0] + interest[:-1]
