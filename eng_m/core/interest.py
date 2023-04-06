from __future__ import annotations

from eng_m.util.time import periods_to_time


class Interest:
    def __init__(
        self,
        interest: float,
        compounds: float = 1,
        interest_type: str = "nominal",
    ):
        """
        Defines interest

        Parameters
        ----------
        interest : float
            Amount of interest per time period
        compounds : float
            Number of times interest accumulates per year
        interest_type : str = "nominal"
            Assumes `interest` is annual nominal if "nominal", `interest` is per period
            if "periodic", and `interest` is annual effective if "effective"
        """
        self._validate(interest, compounds, interest_type)

        self._compounds = compounds
        self._value = self._get_interest(interest, compounds, interest_type)

    @property
    def annual_effective_interest(self) -> float:
        """
        Returns the annual effective interest rate.
        """
        return (1 + self._value) ** self._compounds - 1

    @property
    def annual_nominal_interest(self) -> float:
        """
        Returns the annual nominal interest rate.
        """
        return self._value * self._compounds

    @property
    def periodic_interest(self) -> float:
        """
        Returns the interest per period.
        """
        return self._value

    @property
    def compounds(self) -> float:
        return self._compounds

    @compounds.setter
    def compounds(self, new_compounds: float) -> None:
        """
        Changes the number of compounds per year keeping constant annual nominal
        interest.

        :param new_compounds:
        :return:
        """
        self._value = self._get_interest(
            self._value * self._compounds, new_compounds, "nominal"
        )
        self._compounds = new_compounds

    def recompound(self, new_compounds: float) -> None:
        """
        Changes the number of compounds per year keeping constant annual effective
        interest.

        :param new_compounds:
        :return:
        """
        self._value = self._get_interest(
            self._value**self._compounds, new_compounds, "effective"
        )
        self._compounds = new_compounds

    def compounds_as_time(self) -> str:
        """

        :return:
        """
        if int(self._compounds) in periods_to_time:
            return periods_to_time[int(self._compounds)]
        return str(round(365 / self._compounds, 2)) + "days"

    @staticmethod
    def _get_interest(interest: float, compounds: float, interest_type: str) -> float:
        """

        :param interest:
        :param compounds:
        :param interest_type:
        :return:
        """
        if interest_type == "nominal":
            return interest / compounds
        if interest_type == "effective":
            return interest ** (1 / compounds)
        return interest

    @staticmethod
    def _validate(interest: float, compounds: float, interest_type: str) -> None:
        if interest < 0.0:
            raise ValueError("negative interest not supported")
        if compounds < 1:
            raise ValueError(
                "interest compounds rarer than once per annum not supported"
            )
        if interest_type not in ("periodic", "nominal"):
            raise ValueError("interest type must be `periodic` or `nominal`")
        return

    def __eq__(self, other: object):
        if not isinstance(other, Interest):
            return NotImplemented
        return (self.annual_effective_interest == other.annual_effective_interest) and (
            self.periodic_interest == other.periodic_interest
        )

    def __repr__(self):
        return str(self.annual_effective_interest)
