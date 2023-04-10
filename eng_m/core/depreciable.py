from typing import Optional

from eng_m.util.types import expression, numeric


class Depreciable:
    def __init__(
        self,
        investment_value: expression,
        salvage_value: expression,
        useful_life: int,
        revenues: list[expression],
        costs: list[expression],
        tax_rate: Optional[expression] = None,
        marr: Optional[numeric] = None,
    ):
        pass
