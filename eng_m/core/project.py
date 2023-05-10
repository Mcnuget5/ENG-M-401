from eng_m.core.depreciable import Depreciable
from eng_m.core.interest import Interest
from eng_m.core.loan import Loan
from eng_m.core.series import Series

from typing import Optional, Sequence

from eng_m.util.types import expression
from eng_m.util.exceptions import InvalidSeriesError


class Project(Series):
    def __init__(
        self,
        revenue: Sequence[expression],
        cost: Optional[Sequence[expression]] = None,
        loan: Optional[Loan] = None,
        depreciable: Optional[Sequence[Depreciable]] = None,
        tax_rate: float = 0.0,
        marr: Interest = Interest(0.0),
    ) -> None:
        """
        Projects at minimum have a revenue payment series and admit an operating cost
        series, a loan, and a depreciable item.
        """
        self.revenues = revenue
        self.cost = cost
        self.loan = loan
        self.depreciables = depreciable
        self.tax_rate = tax_rate
        self.marr = marr
        self._assert_equal_lengths()
        super().__init__(
            [self.net_cash_flow(i) for i in range(len(self.revenues))],
            interest=self.marr,
        )

    def net_cash_flow(self, period: int) -> expression:
        net = self.net_income(period)

        if self.depreciables is not None:
            if period == 0:
                net -= sum([i.principal_value for i in self.depreciables])
            if period == self.depreciables[0].useful_life:
                net += sum(
                    [i.net_salvage_value(self.tax_rate) for i in self.depreciables]
                )
            net += sum([i.cca(period) for i in self.depreciables])

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
        if self.depreciables is not None:
            costs += sum([i.cca(period) for i in self.depreciables])

        return self.revenues[period] - costs

    def income_taxes(self, period: int) -> expression:
        return self.ebit(period) * self.tax_rate

    def _assert_equal_lengths(self):
        if self.cost is not None:
            if len(self.cost) != len(self.revenues):
                raise InvalidSeriesError("revenue and cost unequal length")
        if self.loan is not None:
            if len(self.loan) != len(self.revenues):
                raise InvalidSeriesError("revenue and loan unequal length")
        if self.depreciables is not None:
            if any(
                [i.useful_life + 1 != len(self.revenues) for i in self.depreciables]
            ):
                raise InvalidSeriesError("revenue and depreciable unequal length")
