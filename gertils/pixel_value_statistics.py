"""Tools for taking statistics over pixel values"""

import dataclasses
import logging
import math
from collections.abc import Iterable
from typing import TypeAlias

import numpy as np
from numpydoc_decorator import doc  # type: ignore[import]

from .geometry import ImagePoint3D, ZCoordinate
from .types import ImagingChannel, PixelArray

__all__ = ["RegionalPixelStatistics", "compute_pixel_statistics"]

Numeric: TypeAlias = (
    float | int | np.float16 | np.float32 | np.float64 | np.int8 | np.int16 | np.int32 | np.int64
)
PixelValue: TypeAlias = np.uint8 | np.uint16


@doc(
    summary="Store a handful of pixel value stats for a particular ROI.",
    parameters=dict(
        mean_value="The mean pixel intensity in a ROI",
        sigma_value="The standard deviation of pixel intensity in a ROI",
        min_value="The minimum pixel value in a ROI",
        med_value="The median pixel value in a ROI",
        max_value="The maximum pixel value in a ROI",
        proj_mean="Mean of values in the max-z-projection",
        proj_sigma="Standard deviation of values in the max-z-projection",
        proj_min="Minimum of values in the max-z-projection",
        proj_med="Median of values in the max-z-projection",
        proj_max="Maximum of values in the max-z-projection",
        center_mean="Mean of values in the central z-slice",
        center_sigma="Standard deviation of values in the central z-slice",
        center_min="Minimum of values in the central z-slice",
        center_med="Median of values in the central z-slice",
        center_max="Maximum of values in the central z-slice",
    ),
)
@dataclasses.dataclass(kw_only=True, frozen=True)
class RegionalPixelStatistics:  # noqa: D101
    center_mean: float
    center_sigma: float
    center_min: float
    center_med: float
    center_max: float

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
            raise ValueError(f"To build {cls.__name__}, image must be 3D, not {len(shape)}D")
        num_planes = shape[0]
        round_z: int = int(round(central_z))
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
                raise ValueError(
                    f"[{lower_slice_bound}, {upper_slice_bound}) slice for image of {num_planes} z-slices"
                )
            logging.debug(oob_slice_msg)
        # Clip only here, so that the check above still sees a window that runs below plane 0.
        # Only the planes of the window are loaded, so the statistics below are plain numbers.
        central_plane_img = np.asarray(img[max(0, lower_slice_bound) : upper_slice_bound])

        return cls(
            center_mean=central_plane_img.mean(),
            center_sigma=central_plane_img.std(),
            center_min=central_plane_img.min(),
            center_med=np.median(central_plane_img),
            center_max=central_plane_img.max(),
        )


@doc(
    summary="Compute statistics over pixels from multiple channels, in a region centered on a point.",
    parameters=dict(
        img="Image in which to measure pixels",
        pt="Center of region to measure",
        channels="Channels of image in which to measure pixels",
        diameter="Size (width and height) of region around point in which to measure pixels",
        channel_column="Name for the field/column in which to store channel from which pixels were taken",
    ),
    returns="List of records, each mapping key/field to value",
    raises=dict(
        ValueError="If the diameter isn't positive, or the region lies entirely outside the image",
    ),
)
def compute_pixel_statistics(  # noqa: D103"
    img: PixelArray,
    pt: ImagePoint3D,
    *,
    channels: Iterable[ImagingChannel],
    diameter: int,
    channel_column: str,
) -> list[dict[str, Numeric]]:
    if diameter < 1:
        raise ValueError(f"Diameter of the region must be positive; got {diameter}")
    # Centre the region on the nearest pixel, rounding halves up; round() would round them to even.
    left: int = math.floor(pt.x + 0.5) - diameter // 2
    right: int = left + diameter
    top: int = math.floor(pt.y + 0.5) - diameter // 2
    bottom: int = top + diameter
    # Clip the region to the image, so that the bounds reported are those of the pixels measured.
    num_rows, num_cols = img.shape[-2:]
    y_min, y_max = max(0, top), min(bottom, num_rows)
    x_min, x_max = max(0, left), min(right, num_cols)
    if y_min >= y_max or x_min >= x_max:
        raise ValueError(
            f"Region x [{left}, {right}), y [{top}, {bottom}) around point ({pt.x}, {pt.y}) "
            f"lies outside the image of {num_cols} x {num_rows} pixels"
        )
    bounds: dict[str, int] = {
        "y_min_px": y_min,
        "y_max_px": y_max,
        "x_min_px": x_min,
        "x_max_px": x_max,
    }
    # Build up records, e.g. rows of data table/frame
    result: list[dict[str, Numeric]] = []
    for ch in channels:
        subimg = img[ch.get, :, y_min:y_max, x_min:x_max]
        stats = RegionalPixelStatistics.from_image(subimg, central_z=pt.z)
        result.append({channel_column: ch.get, **bounds, **stats.to_dict})
    return result
