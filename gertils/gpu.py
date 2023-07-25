"""Utilities for working with GPUs"""

from typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

from .exceptions import TensorflowNotFoundException

try:  # pylint: disable=no-else-raise
    import tensorflow as tf  # type: ignore[import]
except ModuleNotFoundError as e:
    print(f"ERROR: Cannot import tensorflow, so cannot use module: {__file__}")
    raise TensorflowNotFoundException() from e
else:
    from tensorflow.python.eager.context import PhysicalDevice as TFPhysDev  # type: ignore[import] # pylint: disable=line-too-long # isort:skip

__all__ = [
    "count_tensorflow_gpus",
    "list_tensorflow_gpus",
    "print_tensorflow_gpu_count",
]
__author__ = "Vince Reuter"
__email__ = "vincent.reuter@imba.oeaw.ac.at"


def count_tensorflow_gpus() -> int:
    """Count the number of GPUs that tensorflow can see."""
    return len(list_tensorflow_gpus())


def list_tensorflow_gpus() -> List[TFPhysDev]:  # type: ignore[no-any-unimported]
    """List the GPUs that tensorflow can see."""
    return tf.config.list_physical_devices("GPU")  # type: ignore[no-any-return]


def print_tensorflow_gpu_count() -> None:
    """Print the number of GPUs that tensorflow can see."""
    print(f"Num GPUs Available: {count_tensorflow_gpus()}")
