from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import AnnotationID


@ome_dataclass
class AnnotationRef(Reference):
    id: Optional[AnnotationID] = None
