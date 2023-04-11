"""
Series
------
Represents a series of arbitrary payments per time step with constant interest.
"""
from __future__ import annotations

import sympy
from typing import get_args

from eng_m.core.interest import Interest

from eng_m.util.types import expression, optional, numeric, unsolved
from eng_m.util.exceptions import (
    InvalidInterestError,
    NoBuenoSeriesMuchasGraciasError,
)


class Series:
    """
    Defines a payment series with arbitrary payments per year and arbitrary interest.

    # TODO: "cache" effective interest

    Parameters
    ----------
    payment : Iterable
        Iterable of numerics representing
    """

    def __init__(
        self, payment: list[expression], interest: Interest, compounds: int = 1
    ) -> None:
        self.payments = payment
        self.interest = interest
        self.compounds = compounds

    @property
    def irr(self):
        return NotImplemented

    @property
    def eaw(self) -> expression:
        if self._effective_interest() == 0.0:
            return self.npv / len(self.payments) * self.compounds
        return (
            self.npv
            * (
                self._effective_interest()
                * (1 + self._effective_interest()) ** (len(self.payments) - 1)
            )
            / ((1 + self._effective_interest()) ** (len(self.payments) - 1) - 1)
        )

    @property
    def acceptability(self) -> bool:
        if self.npv > 0:
            return True
        return False

    @property
    def nfv(self) -> expression:
        """
        Returns the net final value of a payment series

        Returns
        -------
        Net final value of this payment series.
        """
        return sum(
            [
                self.payments[i]
                * ((1 + self._effective_interest()) ** (len(self.payments) - i))
                for i in range(len(self.payments))
            ]
        )

    @property
    def npv(self) -> expression:
        """
        Returns the net present value of a payment series.

        Returns
        -------
        Net present value of this payment series.
        """
        return sum(
            [
                self.payments[i] / ((1 + self._effective_interest()) ** i)
                for i in range(len(self.payments))
            ]
        )

    def concat(self, other: Series) -> Series:
        """
        Appends the payments of two series together. Both series must have equal
        compounds and interest.

        Parameters
        ----------
        other
        """
        if self.interest != other.interest:
            raise InvalidInterestError(
                "payment series must have equal annual effective interest and compounds"
                "per year"
            )
        if self.compounds != other.compounds:
            raise NoBuenoSeriesMuchasGraciasError("series unequal compounds per year")
        return Series(
            self.payments + other.payments,
            interest=self.interest,
            compounds=self.compounds,
        )

    def end(self, period: int) -> numeric:
        """
        Returns the value of the series at the end of year \\(n\\), after the annual
        payment at year \\(n\\) and the interest at year \\(n\\) are added. Payments
        after year \\(n\\) are not taken into account.

        # TODO: implement end() for arbitrary period lengths

        Parameters
        ----------
        period: int -

        Returns
        -------

        """
        return (1 + self._effective_interest()) * self.start(period)

    def equate(self, other: Series, symbol: sympy.Symbol) -> numeric:
        """

        :param other:
        :param symbol:
        :return:
        """
        return float(sympy.solve(self.npv - other.npv, symbol)[0])

    def start(self, period: int) -> numeric:
        """
        Returns the value of the series at the start of year \\(n\\), after the annual
        payment at year \\(n\\) is made. Interest year \\(n\\) and all payments after
        year \\(n\\) not taken into account.

        Parameters
        ----------
        period: int -

        Returns
        -------

        """
        if period >= len(self.payments):
            return self.nfv * (1 + self._effective_interest()) ** (
                period - len(self.payments)
            )
        return sum(
            [
                self.payments[i] * (1 + self._effective_interest()) ** (period - i)
                for i in range(period + 1)
            ]
        )

    def subs(self, subs: dict) -> None:
        """
        Substitutes all instances of a sympy symbol with a value.
        """
        for i, j in enumerate(self.payments):
            if isinstance(j, get_args(unsolved)):
                self.payments[i] = j.subs(subs)  # type: ignore

    def zero(self, symbol: sympy.Symbol) -> optional:
        """
        Finds a value for the variable in this payment series such that its
        npv == nfv == 0. If there exists no solution, return None.

        Parameters
        ----------
        symbol: sympy.Symbol - the variable to solve for

        Returns
        -------

        """
        try:
            return float(sympy.solve(self.npv, symbol)[0])
        except IndexError:
            return None

    def _effective_interest(self) -> float:
        """

        Returns
        -------

        """
        return (1 + self.interest.periodic_interest) ** (
            self.interest.compounds / self.compounds
        ) - 1

    def __add__(self, other: Series) -> Series:
        if self.interest != other.interest:
            raise InvalidInterestError(
                "payment series must have equal annual effective interest and compounds"
                "per year"
            )
        if len(self) != len(other):
            raise NoBuenoSeriesMuchasGraciasError("added series must be of same length")
        return Series(
            payment=[self.payments[i] + other.payments[i] for i in range(len(self))],
            interest=self.interest,
        )

    def __getitem__(self, offset: int) -> expression:
        return self.payments[offset]

    def __len__(self) -> int:
        return len(self.payments)

    def __repr__(self) -> str:
        return f"{self.payments}\n{self._effective_interest()}"

    net_present_value = npv
    net_final_value = nfv
