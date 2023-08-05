from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import FilterSetID


@ome_dataclass
class FilterSetRef(Reference):
    id: Optional[FilterSetID] = None
