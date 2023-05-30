"""Custom exception types"""

__author__ = "Vince Reuter"

__all__ = ["GerlichToolsException", "TensorflowNotFoundException"]


class GerlichToolsException(Exception):
    """Base exception type for this package"""


class TensorflowNotFoundException(GerlichToolsException):
    """Error type for when tensorflow is needed but not found"""
