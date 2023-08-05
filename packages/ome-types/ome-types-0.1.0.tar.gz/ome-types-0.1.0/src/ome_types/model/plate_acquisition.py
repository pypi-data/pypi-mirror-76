from dataclasses import field
from datetime import datetime
from typing import List, Optional, cast

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import PlateAcquisitionID, PositiveInt
from .well_sample_ref import WellSampleRef


@ome_dataclass
class PlateAcquisition:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    end_time: Optional[datetime] = None
    id: Optional[PlateAcquisitionID] = None
    maximum_field_count: Optional[PositiveInt] = None
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    well_sample_ref: List[WellSampleRef] = field(default_factory=list)
