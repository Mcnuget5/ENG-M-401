from __future__ import annotations

from eng_m.util.types import expression, numeric

from eng_m.util.maps import cca_rates


class Depreciable:
    def __init__(
        self,
        principal_value: expression,
        salvage_value: expression,
        useful_life: int,
        cca: numeric = 0.0,
        cca_class: bool = False,
    ) -> None:
        """
        Defines a depreciating asset.

        Parameters
        ----------
        principal_value
        salvage_value
        useful_life
        cca
        cca_class
        """
        self.principal_value = principal_value
        self.salvage_value = salvage_value
        self.useful_life = useful_life
        if cca_class:
            self.cca_rate = cca_rates[cca]
        else:
            self.cca_rate = cca

    @property
    def soyd(self) -> int:
        return sum([i + 1 for i in range(self.useful_life)])

    def book_value(self, period: int, method: str = "straight-line"):
        return self.principal_value - self.depreciation(period, method)

    def cca(self, period: int, cumulative: bool = False) -> expression:
        """
        Returns the capital cost allowance allowable for the start of a year
        """
        if period == 0:
            return 0.0
        if period == 1:
            return self.principal_value * self.cca_rate * 0.5

        if cumulative:
            return self.cca(period) + self.cca(period - 1, cumulative=True)

        return (
            self.principal_value
            * (1 - self.cca_rate * 0.5)
            * self.cca_rate
            * ((1 - self.cca_rate) ** (period - 2))
        )

    def depreciation(self, period: int, method: str = "straight-line") -> expression:
        """
        Returns the amount of depreciation of an asset in period

        Parameters
        ----------
        period
        method
        """
        if method == "straight-line":
            return (
                (self.principal_value - self.salvage_value) * period / self.useful_life
            )
        elif method == "soyd":
            return (
                (sum([self.useful_life - i for i in range(period)]))
                / self.soyd
                * (self.principal_value - self.salvage_value)
            )
        raise NotImplementedError()

    def disposal_tax_effect(self, tax_rate: float) -> expression:
        """
        Returns the amount of tax benefits or costs provided by asset disposal.
        """
        if self.salvage_value > self.principal_value:
            return (-self.cca(self.useful_life, cumulative=True)) * tax_rate - (
                0.5 * tax_rate
            ) * (self.salvage_value - self.principal_value)
        return (
            (self.principal_value - self.cca(self.useful_life, cumulative=True))
            - self.salvage_value
        ) * tax_rate

    def net_salvage_value(self, tax_rate: float) -> expression:
        return self.salvage_value + self.disposal_tax_effect(tax_rate)

    sum_of_years_depreciable = soyd
