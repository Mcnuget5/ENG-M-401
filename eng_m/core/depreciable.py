from typing import Optional

from eng_m.util.types import numeric, expression

from eng_m.util.maps import cca_rates


class Depreciable:
    def __init__(
        self,
        principal_value: expression,
        salvage_value: expression,
        useful_life: int,
        cca: Optional[float] = None,
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
    def soyd(self):
        return sum([i for i in range(self.useful_life)])

    def cca(self, period: int) -> expression:
        """
        Returns the capital cost allowance allowable for a year
        """
        if period == 0:
            return self.principal_value * self.cca_rate * 0.5
        return (
            self.principal_value
            * (1 - self.cca_rate * 0.5)
            * self.cca_rate
            * ((1 - self.cca_rate) ** (period - 1))
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

    sum_of_years_depreciable = soyd
