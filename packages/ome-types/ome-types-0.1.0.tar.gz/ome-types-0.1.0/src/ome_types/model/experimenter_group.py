from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .experimenter_ref import ExperimenterRef
from .leader import Leader
from .simple_types import ExperimenterGroupID


@ome_dataclass
class ExperimenterGroup:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_ref: List[ExperimenterRef] = field(default_factory=list)
    id: Optional[ExperimenterGroupID] = None
    leader: List[Leader] = field(default_factory=list)
    name: Optional[str] = None
