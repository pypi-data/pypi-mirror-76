from datetime import datetime
from typing import Optional, cast

from ome_types.dataclasses import ome_dataclass

from .image_ref import ImageRef
from .simple_types import NonNegativeInt, UnitsLength, WellSampleID


@ome_dataclass
class WellSample:
    index: NonNegativeInt
    id: Optional[WellSampleID] = None
    image_ref: Optional[ImageRef] = None
    position_x: Optional[float] = None
    position_x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    position_y: Optional[float] = None
    position_y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    timepoint: Optional[datetime] = None
