"""Utilities for working with GPUs"""

from typing import *
from .exceptions import TensorflowNotFoundException

try:
    import tensorflow as tf
except ModuleNotFoundError as e:
    print(f"ERROR: Cannot import tensorflow, so cannot use module: {__file__}")
    raise TensorflowNotFoundException()
else:
    from tensorflow.python.eager.context import PhysicalDevice as TFPhysDev

__author__ = "Vince Reuter"

__all__ = [
    "count_tensorflow_gpus",
    "list_tensorflow_gpus",
    "print_tensorflow_gpu_count",
]


def count_tensorflow_gpus() -> int:
    return len(list_tensorflow_gpus())


def list_tensorflow_gpus() -> List[TFPhysDev]:
    return tf.config.list_physical_devices("GPU")


def print_tensorflow_gpu_count() -> None:
    print(f"Num GPUs Available: {count_tensorflow_gpus()}")
