from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import ReagentID


@ome_dataclass
class Reagent:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    id: Optional[ReagentID] = None
    name: Optional[str] = None
    reagent_identifier: Optional[str] = None
