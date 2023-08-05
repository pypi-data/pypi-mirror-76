from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ImageID


@ome_dataclass
class ImageRef(Reference):
    id: Optional[ImageID] = None
