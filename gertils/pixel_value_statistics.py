"""Tools for taking statistics over pixel values"""

import dataclasses
import logging
import math
from collections.abc import Iterable
from typing import Any, TypeAlias, cast

import numpy as np
import numpy.typing as npt
from dask.array.core import Array as DaskArray
from numpydoc_decorator import doc

from .geometry import ImagePoint3D, ZCoordinate
from .types import ImagingChannel, PixelArray

__all__ = [
    "RegionalPixelStatistics",
    "compute_pixel_statistics",
    "compute_pixel_statistics_for_channel",
]

Numeric: TypeAlias = (
    float
    | int
    | np.float16
    | np.float32
    | np.float64
    | np.int8
    | np.int16
    | np.int32
    | np.int64
    | np.uint8
    | np.uint16
    | np.uint32
    | np.uint64
)


@doc(
    summary="Store a handful of pixel value stats for a particular ROI.",
    extended_summary=(
        "The statistics are taken over the z-plane closest to the ROI's center, "
        "plus any planes of padding above and below it."
    ),
    parameters=dict(
        center_mean="Mean of the pixel values",
        center_sigma="Standard deviation of the pixel values",
        center_min="Minimum of the pixel values",
        center_med="Median of the pixel values",
        center_max="Maximum of the pixel values",
        pixel_count="Number of pixels the statistics are taken over",
    ),
)
@dataclasses.dataclass(kw_only=True, frozen=True)
class RegionalPixelStatistics:  # noqa: D101
    center_mean: float
    center_sigma: float
    center_min: float
    center_med: float
    center_max: float
    pixel_count: int

    @property
    def to_dict(self) -> dict[str, float]:  # noqa: D102
        return dataclasses.asdict(self)

    @classmethod
    def from_image(
        cls,
        img: PixelArray,
        central_z: ZCoordinate,
        *,
        plus_minus_planes: int = 1,
        require_full_padding: bool = False,
    ) -> "RegionalPixelStatistics":
        """Compute stats for the given region (defined by whole given image)."""
        # Only the shape is read here, so that a lazy array such as dask's isn't loaded yet.
        shape = np.shape(img)
        if len(shape) != 3:  # noqa: PLR2004
            raise ValueError(
                f"To build {cls.__name__}, image must be 3D, not {len(shape)}D"
            )
        planes = _z_window(
            central_z,
            shape[0],
            plus_minus_planes=plus_minus_planes,
            require_full_padding=require_full_padding,
        )
        # Only the planes of the window are loaded, so the statistics below are plain numbers.
        # Indexing a dask array has no type information; the window is the same kind of array.
        return _statistics_of(np.asarray(cast("PixelArray", img[planes])))


def _z_window(
    central_z: ZCoordinate,
    num_planes: int,
    *,
    plus_minus_planes: int,
    require_full_padding: bool,
) -> slice:
    """Get the z-planes to measure: the one nearest the point, plus padding, cut off at the edges."""
    # Round halves up, as for x and y; round() would round them to the nearest even number.
    round_z: int = math.floor(central_z + 0.5)
    if round_z < 0:
        raise ValueError(
            f"Cannot extract pixel values from negative z-slice. ({round_z}, from {central_z})"
        )
    if round_z == num_planes and central_z < num_planes:
        logging.warning(
            f"Rounding central_z down from {central_z} to comply with z-depth of {num_planes}"  # noqa: G004
        )
        round_z = int(central_z)
    elif round_z >= num_planes:
        raise ValueError(
            f"Cannot extract pixel values from z-slice ({round_z}, from {central_z}) for image with {num_planes} z-slice(s)."
        )

    if plus_minus_planes < 0:
        raise ValueError(
            f"Number of planes on either side of the central plane can't be negative; got {plus_minus_planes}"
        )
    lower_slice_bound = round_z - plus_minus_planes
    upper_slice_bound = round_z + plus_minus_planes + 1
    if lower_slice_bound < 0 or upper_slice_bound > num_planes:
        oob_slice_msg = f"[{lower_slice_bound}, {upper_slice_bound}) slice for image of {num_planes} z-slices"
        if require_full_padding:
            raise ValueError(oob_slice_msg)
        logging.debug(oob_slice_msg)
    # Clip only here, so that the check above still sees a window that runs below plane 0.
    return slice(max(0, lower_slice_bound), upper_slice_bound)


def _statistics_of(pixels: npt.NDArray[Any]) -> RegionalPixelStatistics:
    """Compute the statistics over pixels already loaded."""
    return RegionalPixelStatistics(
        center_mean=pixels.mean(),
        center_sigma=pixels.std(),
        center_min=pixels.min(),
        center_med=np.float64(np.median(pixels)),
        center_max=pixels.max(),
        pixel_count=pixels.size,
    )


@dataclasses.dataclass(frozen=True)
class _Region:
    """Where to measure around a point: the bounds to report, and the slices that cut out pixels."""

    bounds: dict[str, int]
    planes: slice
    rows: slice
    columns: slice


def _locate_region(  # noqa: PLR0913
    img: PixelArray,
    pt: ImagePoint3D,
    *,
    diameter: int,
    plus_minus_planes: int,
    require_full_padding: bool,
    require_full_region: bool,
) -> _Region:
    """Find and check the region around a point that is measured in each channel."""
    # np.shape is typed for numpy and dask arrays alike, and doesn't load a dask array.
    shape = np.shape(img)
    if len(shape) != 4:  # noqa: PLR2004
        raise ValueError(f"Image must be 4D (channel, z, y, x), not {len(shape)}D")
    if diameter < 1:
        raise ValueError(f"Diameter of the region must be positive; got {diameter}")
    # Centre the region on the nearest pixel, rounding halves up; round() would round them to even.
    left: int = math.floor(pt.x + 0.5) - diameter // 2
    right: int = left + diameter
    top: int = math.floor(pt.y + 0.5) - diameter // 2
    bottom: int = top + diameter
    # Clip the region to the image, so that the bounds reported are those of the pixels measured.
    num_planes, num_rows, num_cols = shape[1:]
    y_min, y_max = max(0, top), min(bottom, num_rows)
    x_min, x_max = max(0, left), min(right, num_cols)
    if y_min >= y_max or x_min >= x_max:
        raise ValueError(
            f"Region x [{left}, {right}), y [{top}, {bottom}) around point ({pt.x}, {pt.y}) "
            f"lies outside the image of {num_cols} x {num_rows} pixels"
        )
    if require_full_region and (y_min, y_max, x_min, x_max) != (
        top,
        bottom,
        left,
        right,
    ):
        raise ValueError(
            f"Region x [{left}, {right}), y [{top}, {bottom}) around point ({pt.x}, {pt.y}) "
            f"extends beyond the image of {num_cols} x {num_rows} pixels"
        )
    planes = _z_window(
        pt.z,
        num_planes,
        plus_minus_planes=plus_minus_planes,
        require_full_padding=require_full_padding,
    )
    return _Region(
        bounds={
            "y_min_px": y_min,
            "y_max_px": y_max,
            "x_min_px": x_min,
            "x_max_px": x_max,
        },
        planes=planes,
        rows=slice(y_min, y_max),
        columns=slice(x_min, x_max),
    )


@doc(
    summary="Compute statistics over the pixels of one channel, in a region centered on a point.",
    parameters=dict(
        img="Image in which to measure pixels",
        pt="Center of region to measure",
        channel="Channel of image in which to measure pixels",
        diameter="Size (width and height) of region around point in which to measure pixels",
        channel_column="Name for the field/column in which to store channel from which pixels were taken",
        plus_minus_planes="Number of z-planes on either side of the central plane to include",
        require_full_padding="Raise an error rather than use fewer z-planes at the edge of the stack",
        require_full_region="Raise an error rather than measure a region cut off by the edge of the image",
    ),
    returns="Record mapping key/field to value",
    raises=dict(
        ValueError=(
            "If the image isn't 4D; if the diameter isn't positive; if the region lies entirely "
            "outside the image, or the point beyond the last z-plane; or, when required, if the "
            "region or its z-padding extends beyond the image"
        ),
    ),
    see_also=dict(
        compute_pixel_statistics="The same, for several channels at once",
    ),
)
def compute_pixel_statistics_for_channel(  # noqa: PLR0913
    img: PixelArray,
    pt: ImagePoint3D,
    *,
    channel: ImagingChannel,
    diameter: int,
    channel_column: str,
    plus_minus_planes: int = 1,
    require_full_padding: bool = False,
    require_full_region: bool = False,
) -> dict[str, Numeric]:
    region = _locate_region(
        img,
        pt,
        diameter=diameter,
        plus_minus_planes=plus_minus_planes,
        require_full_padding=require_full_padding,
        require_full_region=require_full_region,
    )
    # Only the region is read, and of it only the planes of the z-window.
    # Indexing a dask array has no type information; the region is the same kind of array.
    region_img = cast(
        "PixelArray", img[channel.get, region.planes, region.rows, region.columns]
    )
    return {
        channel_column: channel.get,
        **region.bounds,
        **_statistics_of(np.asarray(region_img)).to_dict,
    }


@doc(
    summary="Compute statistics over pixels from multiple channels, in a region centered on a point.",
    parameters=dict(
        img="Image in which to measure pixels",
        pt="Center of region to measure",
        channels="Channels of image in which to measure pixels",
        diameter="Size (width and height) of region around point in which to measure pixels",
        channel_column="Name for the field/column in which to store channel from which pixels were taken",
        plus_minus_planes="Number of z-planes on either side of the central plane to include",
        require_full_padding="Raise an error rather than use fewer z-planes at the edge of the stack",
        require_full_region="Raise an error rather than measure a region cut off by the edge of the image",
    ),
    returns="List of records, one per channel, each mapping key/field to value",
    raises=dict(
        ValueError=(
            "If the image isn't 4D; if the diameter isn't positive; if the region lies entirely "
            "outside the image, or the point beyond the last z-plane; or, when required, if the "
            "region or its z-padding extends beyond the image"
        ),
    ),
    see_also=dict(
        compute_pixel_statistics_for_channel="The same, for a single channel",
    ),
)
def compute_pixel_statistics(  # noqa: PLR0913
    img: PixelArray,
    pt: ImagePoint3D,
    *,
    channels: Iterable[ImagingChannel],
    diameter: int,
    channel_column: str,
    plus_minus_planes: int = 1,
    require_full_padding: bool = False,
    require_full_region: bool = False,
) -> list[dict[str, Numeric]]:
    channels = list(channels)
    region = _locate_region(
        img,
        pt,
        diameter=diameter,
        plus_minus_planes=plus_minus_planes,
        require_full_padding=require_full_padding,
        require_full_region=require_full_region,
    )
    if isinstance(img, DaskArray):
        # Cut out the region of all channels at once and load it in one computation, so that
        # stored chunks holding several channels are read once. Indexing a dask array has no type
        # information; the result is the same kind of array.
        all_channels = cast(
            "PixelArray",
            img[
                [ch.get for ch in channels], region.planes, region.rows, region.columns
            ],
        )
        region_imgs = list(np.asarray(all_channels))
    else:
        region_imgs = [
            np.asarray(img[ch.get, region.planes, region.rows, region.columns])
            for ch in channels
        ]
    return [
        {channel_column: ch.get, **region.bounds, **_statistics_of(region_img).to_dict}
        for ch, region_img in zip(channels, region_imgs, strict=True)
    ]
