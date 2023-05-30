"""Tests for GPU-related utilities"""

import pytest
from gertils.exceptions import TensorflowNotFoundException


def test_gpu_import_depends_on_tensorflow_presence():
    try:
        import tensorflow
    except ImportError:
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
