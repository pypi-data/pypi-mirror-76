from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .basic_annotation import BasicAnnotation


@ome_dataclass
class TermAnnotation(BasicAnnotation):
    value: str = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
