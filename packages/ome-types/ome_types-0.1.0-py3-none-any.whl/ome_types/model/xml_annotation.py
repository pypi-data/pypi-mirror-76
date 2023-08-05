from dataclasses import field
from typing import Any, List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .text_annotation import TextAnnotation


@ome_dataclass
class XMLAnnotation(TextAnnotation):
    value: Any = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
