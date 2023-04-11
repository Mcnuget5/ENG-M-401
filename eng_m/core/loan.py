import sympy

from eng_m.core.series import Series
from eng_m.core.interest import Interest

from eng_m.util.types import expression, numeric
from eng_m.util.exceptions import NoBuenoSeriesMuchasGraciasError

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
                [-principal] + [payment for _ in range(length)], interest, compounds  # type: ignore
            )
        else:
            raise NoBuenoSeriesMuchasGraciasError("what")

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

    def principals(self, variable: Optional[sympy.Symbol] = None) -> list[numeric]:
        """
        # todo: rly slow. easily fixable with a top-down dp approach.
        """
        if variable is not None:
            self.subs({variable: self.zero(variable)})
        return [self.start(i) for i in range(len(self.payments))]

    def interests(self, variable: Optional[sympy.Symbol] = None) -> list[numeric]:
        pass
