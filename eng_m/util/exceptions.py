from __future__ import annotations


class InvalidInterestError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoBuenoSeriesMuchasGraciasError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
