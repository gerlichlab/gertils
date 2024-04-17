"""Tests for the GPU tools"""

import pytest


def test_no_tensorflow__causes_module_not_found_error_on_gpu_import():
    with pytest.raises(ModuleNotFoundError):
        import gertils.gpu
    with pytest.raises(ModuleNotFoundError):
        from gertils import gpu  # noqa: F401
    # Does not raise an exception.
    import gertils  # noqa: F401
