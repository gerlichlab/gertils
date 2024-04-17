"""Utilities for working with GPUs"""

import logging

try:
    import tensorflow as tf  # type: ignore[import]
except ModuleNotFoundError:
    logging.exception("Cannot import tensorflow, so cannot use module: %s", __file__)
    raise
else:
    from tensorflow.python.eager.context import PhysicalDevice as TFPhysDev  # type: ignore[import]

__all__ = [
    "count_tensorflow_gpus",
    "list_tensorflow_gpus",
    "print_tensorflow_gpu_count",
]


def count_tensorflow_gpus() -> int:
    """Count the number of GPUs that tensorflow can see."""
    return len(list_tensorflow_gpus())


def list_tensorflow_gpus() -> list[TFPhysDev]:  # type: ignore[no-any-unimported]
    """List the GPUs that tensorflow can see."""
    return tf.config.list_physical_devices("GPU")  # type: ignore[no-any-return]


def print_tensorflow_gpu_count() -> None:
    """Print the number of GPUs that tensorflow can see."""
    print(f"Num GPUs Available: {count_tensorflow_gpus()}")  # noqa: T201
