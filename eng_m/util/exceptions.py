from __future__ import annotations


class UnequalInterestError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
