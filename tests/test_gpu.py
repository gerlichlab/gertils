"""Tests for GPU-related utilities"""

import pytest

from gertils.exceptions import TensorflowNotFoundException

# pylint: disable=[import-outside-toplevel]


def test_gpu_import__errors_without_tensorflow_and_otherwise_has_correct_public_members():
    try:
        import tensorflow  # type: ignore[import] # pylint: disable=unused-import
    except ModuleNotFoundError:
        with pytest.raises(TensorflowNotFoundException) as err_ctx:
            import gertils.gpu # pylint: disable=unused-import
        assert isinstance(err_ctx.value, TensorflowNotFoundException)
    else:
        from gertils import gpu as gputools

        assert set(gputools.__all__) == set(
            [
                "count_tensorflow_gpus",
                "list_tensorflow_gpus",
                "print_tensorflow_gpu_count",
            ]
        )
