from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .experimenter_group_ref import ExperimenterGroupRef
from .experimenter_ref import ExperimenterRef
from .image_ref import ImageRef
from .simple_types import DatasetID


@ome_dataclass
class Dataset:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_group_ref: Optional[ExperimenterGroupRef] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    id: Optional[DatasetID] = None
    image_ref: List[ImageRef] = field(default_factory=list)
    name: Optional[str] = None
