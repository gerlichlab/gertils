"""Custom exception types"""

__author__ = "Vince Reuter"


class GerlichToolsException(Exception):
    """Base exception type for this package"""


class IllegalExperimentNumberException(Exception):
    """Error type for when an experiment number is illegal."""

    def __init__(self, exp_num: int, message: str):
        super().__init__(message)
        self._exp_num = exp_num

    @property
    def number(self) -> int:
        """Return the experiment number underlying this exception"""
        return self._exp_num


class TensorflowNotFoundException(GerlichToolsException):
    """Error type for when tensorflow is needed but not found"""
