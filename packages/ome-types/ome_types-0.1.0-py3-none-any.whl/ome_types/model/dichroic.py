from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import DichroicID


@ome_dataclass
class Dichroic(ManufacturerSpec):
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    id: Optional[DichroicID] = None
