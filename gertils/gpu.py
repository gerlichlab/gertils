"""Utilities for working with GPUs"""

import logging

try:
    from tensorflow import config as tf_config
except ModuleNotFoundError:
    logging.exception("Cannot import tensorflow, so cannot use module: %s", __file__)
    raise

__all__ = [
    "count_tensorflow_gpus",
    "list_tensorflow_gpus",
    "print_tensorflow_gpu_count",
]


def count_tensorflow_gpus() -> int:
    """Count the number of GPUs that tensorflow can see."""
    return len(list_tensorflow_gpus())


def list_tensorflow_gpus() -> list[tf_config.PhysicalDevice]:
    """List the GPUs that tensorflow can see."""
    return tf_config.list_physical_devices("GPU")


def print_tensorflow_gpu_count() -> None:
    """Print the number of GPUs that tensorflow can see."""
    print(f"Num GPUs Available: {count_tensorflow_gpus()}")  # noqa: T201
