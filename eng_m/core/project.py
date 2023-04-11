from eng_m.core.depreciable import Depreciable
from eng_m.core.interest import Interest
from eng_m.core.loan import Loan
from eng_m.core.series import Series

from typing import Optional, Sequence

from eng_m.util.types import expression


class Project:
    def __init__(
        self,
        revenue: Sequence[expression],
        cost: Optional[list[expression]] = None,
        loan: Optional[Loan] = None,
        depreciable: Optional[Depreciable] = None,
        tax_rate: float = 0.0,
        marr: Interest = Interest(0.0),
    ) -> None:
        """
        Projects at minimum have a revenue payment series and admit an operating cost
        series, a loan, and a depreciable item.

        # TODO: MAKE SURE WHEN U USE, EVERYTHING IS EQUAL LENGTH. THIS IS NOT CHECKED
                FOR U.
        """
        self._assert_equal_lengths()
        self.revenues = revenue
        self.cost = cost
        self.loan = loan
        self.depreciable = depreciable
        self.tax_rate = tax_rate
        self.marr = marr

    @property
    def eaw(self) -> expression:
        return Series(
            [self.net_cash_flow(i) for i in range(len(self.revenues))], self.marr
        ).npv

    def net_cash_flow(self, period: int) -> expression:
        net = self.net_income(period)

        if self.depreciable is not None:
            if period == 0:
                net -= self.depreciable.principal_value
            if period == self.depreciable.useful_life:
                net += self.depreciable.net_salvage_value(self.tax_rate)
            net += self.depreciable.cca(period)

        if self.loan is not None:
            net -= self.loan.principals(delta=True)[period]

        return net

    def net_income(self, period: int) -> expression:
        return self.ebit(period) * (1 - self.tax_rate)

    def ebit(self, period: int) -> expression:
        costs = 0.0

        if self.cost is not None:
            costs += self.cost[period]
        if self.loan is not None:
            costs -= self.loan.interests()[period]
        if self.depreciable is not None:
            costs += self.depreciable.cca(period)

        return self.revenues[period] - costs

    def income_taxes(self, period: int) -> expression:
        return self.ebit(period) * self.tax_rate

    def _assert_equal_lengths(self):
        pass
