from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .reagent import Reagent
from .reference import Reference
from .simple_types import PlateID, ScreenID


@ome_dataclass
class PlateRef(Reference):
    id: Optional[PlateID] = None


@ome_dataclass
class Screen:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    id: Optional[ScreenID] = None
    name: Optional[str] = None
    plate_ref: List[PlateRef] = field(default_factory=list)
    protocol_description: Optional[str] = None
    protocol_identifier: Optional[str] = None
    reagent_set_description: Optional[str] = None
    reagent_set_identifier: Optional[str] = None
    reagents: List[Reagent] = field(default_factory=list)
    type: Optional[str] = None
