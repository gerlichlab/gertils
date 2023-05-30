"""Custom exception types"""

__author__ = "Vince Reuter"

__all__ = ["GerlichToolsException", "TensorflowNotFoundException"]


class GerlichToolsException(Exception):
    pass


class TensorflowNotFoundException(GerlichToolsException):
    pass
