"""Tests for the integer wrappers"""

import numpy as np
import pytest

from gertils.types import (
    FieldOfViewFrom1,
    ImagingChannel,
    NucleusNumber,
    TimepointFrom0,
    TraceIdFrom0,
)

WRAPPERS = [
    FieldOfViewFrom1,
    ImagingChannel,
    NucleusNumber,
    TimepointFrom0,
    TraceIdFrom0,
]


@pytest.mark.parametrize("wrapper", WRAPPERS)
@pytest.mark.parametrize("value", [True, False, np.int64(1), 1.0, "1", None])
def test_wrapper_rejects_a_value_that_is_not_an_int(wrapper, value):
    with pytest.raises(TypeError):
        wrapper(value)


@pytest.mark.parametrize("wrapper", WRAPPERS)
def test_wrapper_holds_the_int_it_wraps(wrapper):
    assert wrapper(1).get == 1
