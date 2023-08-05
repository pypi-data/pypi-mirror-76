from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .dichroic_ref import DichroicRef
from .filter_ref import FilterRef


@ome_dataclass
class LightPath:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    dichroic_ref: Optional[DichroicRef] = None
    emission_filter_ref: List[FilterRef] = field(default_factory=list)
    excitation_filter_ref: List[FilterRef] = field(default_factory=list)
