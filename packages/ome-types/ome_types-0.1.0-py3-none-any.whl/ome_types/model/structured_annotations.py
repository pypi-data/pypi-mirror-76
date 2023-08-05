from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .boolean_annotation import BooleanAnnotation
from .comment_annotation import CommentAnnotation
from .double_annotation import DoubleAnnotation
from .file_annotation import FileAnnotation
from .list_annotation import ListAnnotation
from .long_annotation import LongAnnotation
from .map_annotation import MapAnnotation
from .tag_annotation import TagAnnotation
from .term_annotation import TermAnnotation
from .timestamp_annotation import TimestampAnnotation
from .xml_annotation import XMLAnnotation


@ome_dataclass
class StructuredAnnotations:
    boolean_annotations: Optional[BooleanAnnotation] = None
    comment_annotations: Optional[CommentAnnotation] = None
    double_annotations: Optional[DoubleAnnotation] = None
    file_annotations: Optional[FileAnnotation] = None
    list_annotations: Optional[ListAnnotation] = None
    long_annotations: Optional[LongAnnotation] = None
    map_annotations: Optional[MapAnnotation] = None
    tag_annotations: Optional[TagAnnotation] = None
    term_annotations: Optional[TermAnnotation] = None
    timestamp_annotations: Optional[TimestampAnnotation] = None
    xml_annotations: Optional[XMLAnnotation] = None
