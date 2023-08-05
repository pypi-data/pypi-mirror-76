from typing import Optional

from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class Rights:
    rights_held: Optional[str] = None
    rights_holder: Optional[str] = None
