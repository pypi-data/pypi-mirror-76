from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import FilterID


@ome_dataclass
class FilterRef(Reference):
    id: Optional[FilterID] = None
