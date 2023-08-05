from dataclasses import field
from enum import Enum
from typing import List, Optional, cast

from ome_types.dataclasses import ome_dataclass

from .affine_transform import AffineTransform
from .annotation_ref import AnnotationRef
from .simple_types import Color, NonNegativeInt, ShapeID, UnitsLength


class FontStyle(Enum):
    BOLD = "Bold"
    BOLD_ITALIC = "BoldItalic"
    ITALIC = "Italic"
    NORMAL = "Normal"


class FontFamily(Enum):
    CURSIVE = "cursive"
    FANTASY = "fantasy"
    MONOSPACE = "monospace"
    SANSSERIF = "sans-serif"
    SERIF = "serif"


class FillRule(Enum):
    EVEN_ODD = "EvenOdd"
    NON_ZERO = "NonZero"


@ome_dataclass
class Shape:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    fill_color: Optional[Color] = None
    fill_rule: Optional[FillRule] = None
    font_family: Optional[FontFamily] = None
    font_size: Optional[NonNegativeInt] = None
    font_size_unit: Optional[UnitsLength] = UnitsLength("pt")
    font_style: Optional[FontStyle] = None
    id: Optional[ShapeID] = None
    locked: Optional[bool] = None
    stroke_color: Optional[Color] = None
    stroke_dash_array: Optional[str] = None
    stroke_width: Optional[float] = None
    stroke_width_unit: Optional[UnitsLength] = UnitsLength("pixel")
    text: Optional[str] = None
    the_c: Optional[NonNegativeInt] = None
    the_t: Optional[NonNegativeInt] = None
    the_z: Optional[NonNegativeInt] = None
    transform: Optional[AffineTransform] = None
