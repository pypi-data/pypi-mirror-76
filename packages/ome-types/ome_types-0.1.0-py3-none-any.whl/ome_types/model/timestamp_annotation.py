from dataclasses import field
from datetime import datetime
from typing import List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .basic_annotation import BasicAnnotation


@ome_dataclass
class TimestampAnnotation(BasicAnnotation):
    value: datetime = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
