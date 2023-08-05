from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import ExperimenterID


@ome_dataclass
class Experimenter:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    email: Optional[str] = None
    first_name: Optional[str] = None
    id: Optional[ExperimenterID] = None
    institution: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    user_name: Optional[str] = None
