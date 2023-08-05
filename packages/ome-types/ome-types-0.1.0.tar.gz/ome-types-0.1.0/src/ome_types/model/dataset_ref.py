from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import DatasetID


@ome_dataclass
class DatasetRef(Reference):
    id: Optional[DatasetID] = None
