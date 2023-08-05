from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from ome_types.dataclasses import ome_dataclass

from .annotation import Annotation
from .boolean_annotation import BooleanAnnotation
from .comment_annotation import CommentAnnotation
from .dataset import Dataset
from .double_annotation import DoubleAnnotation
from .experiment import Experiment
from .experimenter import Experimenter
from .experimenter_group import ExperimenterGroup
from .file_annotation import FileAnnotation
from .folder import Folder
from .image import Image
from .instrument import Instrument
from .list_annotation import ListAnnotation
from .long_annotation import LongAnnotation
from .plate import Plate
from .project import Project
from .rights import Rights
from .roi import ROI
from .screen import Screen
from .simple_types import UniversallyUniqueIdentifier
from .tag_annotation import TagAnnotation
from .term_annotation import TermAnnotation
from .timestamp_annotation import TimestampAnnotation
from .xml_annotation import XMLAnnotation

_annotation_types: Dict[str, type] = {
    "boolean_annotation": BooleanAnnotation,
    "comment_annotation": CommentAnnotation,
    "double_annotation": DoubleAnnotation,
    "file_annotation": FileAnnotation,
    "list_annotation": ListAnnotation,
    "long_annotation": LongAnnotation,
    "tag_annotation": TagAnnotation,
    "term_annotation": TermAnnotation,
    "timestamp_annotation": TimestampAnnotation,
    "xml_annotation": XMLAnnotation,
}


@ome_dataclass
class BinaryOnly:
    metadata_file: str
    uuid: UniversallyUniqueIdentifier


@ome_dataclass
class OME:
    binary_only: Optional[BinaryOnly] = None
    creator: Optional[str] = None
    datasets: List[Dataset] = field(default_factory=list)
    experimenter_groups: List[ExperimenterGroup] = field(default_factory=list)
    experimenters: List[Experimenter] = field(default_factory=list)
    experiments: List[Experiment] = field(default_factory=list)
    folders: List[Folder] = field(default_factory=list)
    images: List[Image] = field(default_factory=list)
    instruments: List[Instrument] = field(default_factory=list)
    plates: List[Plate] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    rights: Optional[Rights] = None
    rois: List[ROI] = field(default_factory=list)
    screens: List[Screen] = field(default_factory=list)
    structured_annotations: List[Annotation] = field(default_factory=list)
    uuid: Optional[UniversallyUniqueIdentifier] = None

    @validator("structured_annotations", pre=True, each_item=True)
    def validate_structured_annotations(
        cls, value: Union[Annotation, Dict[Any, Any]]
    ) -> Annotation:
        if isinstance(value, Annotation):
            return value
        elif isinstance(value, dict):
            try:
                _type = value.pop("_type")
            except KeyError:
                raise ValueError(
                    "dict initialization requires _type"
                ) from None
            try:
                annotation_cls = _annotation_types[_type]
            except KeyError:
                raise ValueError(
                    f"unknown Annotation type '{_type}'"
                ) from None
            return annotation_cls(**value)
        else:
            raise ValueError("invalid type for annotation values")
