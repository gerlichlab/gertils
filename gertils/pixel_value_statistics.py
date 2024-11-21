"""Tools for taking statistics over pixel values"""

import dataclasses
import logging
from collections.abc import Iterable
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from numpydoc_decorator import doc  # type: ignore[import]

from .geometry import ImagePoint3D, ZCoordinate
from .types import ImagingChannel

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
    mean_value: float
    sigma_value: float
    min_value: float
    med_value: float
    max_value: float
    proj_mean: float
    proj_sigma: float
    proj_min: float
    proj_med: float
    proj_max: float
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
        cls, img: npt.NDArray[PixelValue], central_z: ZCoordinate
    ) -> "RegionalPixelStatistics":
        """Compute stats for the given region (defined by whole given image)."""
        if len(img.shape) != 3:  # noqa: PLR2004
            raise ValueError(f"To build {cls.__name__}, image must be 3D, not {len(img.shape)}D")
        round_z: int = int(round(central_z))
        if round_z < 0:
            raise ValueError(
                f"Cannot extract pixel values from negative z-slice. ({round_z}, from {central_z})"
            )
        if round_z == img.shape[0] and central_z < img.shape[0]:
            logging.warning(
                f"Rounding central_z down from {central_z} to comply with z-depth of {img.shape[0]}"  # noqa: G004
            )
            round_z = int(central_z)
        elif round_z >= img.shape[0]:
            raise ValueError(
                f"Cannot extract pixel values from z-slice ({round_z}, from {central_z}) for image with {img.shape[0]} z-slice(s)."
            )

        central_plane_img = img[round_z]
        maxproj = np.max(img, axis=0)

        return cls(
            mean_value=img.mean(),
            sigma_value=img.std(),
            min_value=img.min(),
            med_value=np.median(img),  # type: ignore[arg-type]
            max_value=img.max(),
            proj_mean=maxproj.mean(),
            proj_sigma=maxproj.std(),
            proj_min=maxproj.min(),
            proj_med=np.median(maxproj),
            proj_max=maxproj.max(),
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
        signal_column="Name for the field/column in which to store channel from which pixels were taken",
    ),
    returns="List of records, each mapping key/field to value",
)
def compute_pixel_statistics(  # noqa: D103
    img: npt.NDArray[PixelValue],
    pt: ImagePoint3D,
    *,
    channels: Iterable[ImagingChannel],
    diameter: int,
    signal_column: str,
) -> list[dict[str, Numeric]]:
    left: int = round(pt.x - diameter / 2)
    right: int = left + diameter
    top: int = round(pt.y - diameter / 2)
    bottom: int = top + diameter
    bounds: dict[str, int] = {
        "y_min_px": top,
        "y_max_px": bottom,
        "x_min_px": left,
        "x_max_px": right,
    }
    # Build up records, e.g. rows of data table/frame
    result: list[dict[str, Numeric]] = []
    for ch in channels:
        subimg = img[ch.get, :, max(0, top) : bottom, max(0, left) : right]
        stats = RegionalPixelStatistics.from_image(subimg, central_z=pt.z)
        result.append({signal_column: ch.get, **bounds, **stats.to_dict})
    return result
