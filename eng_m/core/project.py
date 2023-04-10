from eng_m.core.series import Series

from eng_m.util.types import numeric, expression


class Project(Series):
    def __init__(
        self,
        investment_cost: expression,
        salvage_value: expression,
        useful_life: int,
        compounds: int,
        revenues: list[expression],
        expenses: list[expression],
    ) -> None:
        pass
