from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .binary_file import BinaryFile
from .type_annotation import TypeAnnotation


@ome_dataclass
class FileAnnotation(TypeAnnotation):
    binary_file: BinaryFile = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
