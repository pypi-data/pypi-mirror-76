from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .folder_ref import FolderRef
from .image_ref import ImageRef
from .roi_ref import ROIRef
from .simple_types import FolderID


@ome_dataclass
class Folder:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    folder_ref: List[FolderRef] = field(default_factory=list)
    id: Optional[FolderID] = None
    image_ref: List[ImageRef] = field(default_factory=list)
    name: Optional[str] = None
    roi_ref: List[ROIRef] = field(default_factory=list)
