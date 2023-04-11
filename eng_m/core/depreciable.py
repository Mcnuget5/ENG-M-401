from typing import Optional

from eng_m.util.types import expression

from eng_m.util.maps import cca_rates


class Depreciable:
    def __init__(
        self,
        principal_value: expression,
        salvage_value: expression,
        useful_life: int,
        cca: float = 0.0,
        depreciation_class: bool = False,
    ) -> None:
        """
        Defines a depreciating asset.

        Parameters
        ----------
        principal_value
        salvage_value
        useful_life
        cca
        depreciation_class
        """
        self.principal_value = principal_value
        self.salvage_value = salvage_value
        self.useful_life = useful_life
        if depreciation_class:
            self.cca_rate = cca_rates[cca]
        else:
            self.cca_rate = cca

    @property
    def soyd(self) -> int:
        return sum([i for i in range(self.useful_life)])

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

    def depreciation(
        self, period: int, method: str = "straight-line"
    ) -> Optional[expression]:
        """
        Returns the amount of depreciation of an asset in period

        Parameters
        ----------
        period
        method
        """
        if method == "straight-line":
            return (self.principal_value - self.salvage_value) * period
        elif method == "soyd":
            return (
                (self.useful_life - period)
                / self.soyd
                * (self.principal_value - self.salvage_value)
            )
        return NotImplemented

    def disposal_tax_effect(self, tax_rate: float) -> expression:
        return (
            (self.principal_value - self.cca(self.useful_life, cumulative=True))
            - self.salvage_value
        ) * tax_rate

    def net_salvage_value(self, tax_rate: float) -> expression:
        return self.salvage_value + self.disposal_tax_effect(tax_rate)

    sum_of_years_depreciable = soyd
