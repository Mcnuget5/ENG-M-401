from eng_m.core.interest import Interest
from eng_m.core.series import Series
from eng_m.core.depreciable import Depreciable

from typing import Optional, Union

from eng_m.util.types import expression, numeric
from eng_m.util.maps import cca_rates


class Project:
    def __init__(
        self,
        revenue,
        cost,
        loan,
        depreciable: Optional[Depreciable] = None,
        marr: Optional[Interest] = None,
    ) -> None:
        """
        Projects at minimum have a revenue payment series and admit an operating cost
        series, a loan, and a depreciable item.
        """
        pass

    @property
    def eaw(self) -> expression:
        pass
