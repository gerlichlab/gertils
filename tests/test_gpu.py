"""Tests for GPU-related utilities"""

import pytest
from gertils.exceptions import TensorflowNotFoundException


def test_gpu_import__errors_without_tensorflow_and_otherwise_has_correct_public_members():
    try:
        import tensorflow
    except ModuleNotFoundError:
        with pytest.raises(TensorflowNotFoundException) as err_ctx:
            import gertils.gpu
        assert isinstance(err_ctx.value, TensorflowNotFoundException)
    else:
        from gertils import gpu as gputools

        assert gputools.__all__ == [
            "count_tensorflow_gpus",
            "list_tensorflow_gpus",
            "print_tensorflow_gpu_count",
        ]
