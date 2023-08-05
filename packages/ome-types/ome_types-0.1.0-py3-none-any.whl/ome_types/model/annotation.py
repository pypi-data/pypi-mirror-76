from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import AnnotationID, ExperimenterID


@ome_dataclass
class Annotation:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    annotator: Optional[ExperimenterID] = None
    description: Optional[str] = None
    id: Optional[AnnotationID] = None
    namespace: Optional[str] = None
