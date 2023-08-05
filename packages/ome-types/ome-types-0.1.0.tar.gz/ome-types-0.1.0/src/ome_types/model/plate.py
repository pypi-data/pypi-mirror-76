from dataclasses import field
from typing import List, Optional, cast

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .plate_acquisition import PlateAcquisition
from .simple_types import (
    NamingConvention,
    NonNegativeInt,
    PlateID,
    PositiveInt,
    UnitsLength,
)
from .well import Well


@ome_dataclass
class Plate:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    column_naming_convention: Optional[NamingConvention] = None
    columns: Optional[PositiveInt] = None
    description: Optional[str] = None
    external_identifier: Optional[str] = None
    field_index: Optional[NonNegativeInt] = None
    id: Optional[PlateID] = None
    name: Optional[str] = None
    plate_acquisitions: List[PlateAcquisition] = field(default_factory=list)
    row_naming_convention: Optional[NamingConvention] = None
    rows: Optional[PositiveInt] = None
    status: Optional[str] = None
    well_origin_x: Optional[float] = None
    well_origin_x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    well_origin_y: Optional[float] = None
    well_origin_y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    wells: List[Well] = field(default_factory=list)
