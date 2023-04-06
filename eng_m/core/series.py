"""
Series
------
Represents a series of arbitrary payments per time step with constant interest.
"""
from __future__ import annotations

import sympy

from eng_m.core.interest import Interest

from eng_m.util.types import symbol
from eng_m.util.exceptions import UnequalInterestError


class Series:
    """
    Defines a payment series with arbitrary payments per year and arbitrary interest.

    Parameters
    ----------
    payment : Iterable
        Iterable of numerics representing
    """

    def __init__(
        self,
        payment: list[symbol],
        interest: Interest,
        compounds: float = 1,
    ) -> None:
        self.payments = payment
        self.interest = interest
        self.compounds = compounds

    @property
    def npv(self) -> float:
        """
        Returns the net present value of a payment series.

        :return:
        """
        return sum(
            [
                self.payments[i] / ((1 + self.interest.annual_effective_interest) ** i)
                for i in range(len(self.payments))
            ]
        )

    def concat(self, other: Series) -> Series:
        """
        Appends the payments of two series together. Both series must be equal.

        :param series:
        :return:
        """
        if self.interest != other.interest:
            raise UnequalInterestError(
                "payment series must have equal annual effective interest and compounds"
                "per year"
            )
        return Series(
            payment=self.payments + other.payments,
            interest=self.interest,
            compounds=self.compounds,
        )

    def end(self, period: int) -> float:
        """
        TODO: this
        Parameters
        ----------
        period

        Returns
        -------

        """
        return 0.0

    def equate(self, other: Series, symbol: sympy.Symbol) -> float:
        """

        :param other:
        :param symbol:
        :return:
        """
        return sympy.solve(self.npv - other.npv, symbol)

    def start(self, period: int) -> float:
        """
        TODO: this
        Parameters
        ----------
        period

        Returns
        -------

        """
        return 0.0

    def __add__(self, other: Series) -> Series:
        """
        # TODO this shit

        Parameters
        ----------

        """
        if self.interest != other.interest:
            raise UnequalInterestError(
                "payment series must have equal annual effective interest and compounds"
                "per year"
            )
        return Series(payment=self.payments, interest=self.interest)

    net_present_value = npv
