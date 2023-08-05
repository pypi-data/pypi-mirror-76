from typing import Optional, cast

from ome_types.dataclasses import ome_dataclass

from .simple_types import NonNegativeInt, UniversallyUniqueIdentifier


@ome_dataclass
class UUID:
    file_name: str
    value: UniversallyUniqueIdentifier


@ome_dataclass
class TiffData:
    first_c: Optional[NonNegativeInt] = cast(NonNegativeInt, 0)
    first_t: Optional[NonNegativeInt] = cast(NonNegativeInt, 0)
    first_z: Optional[NonNegativeInt] = cast(NonNegativeInt, 0)
    ifd: Optional[NonNegativeInt] = cast(NonNegativeInt, 0)
    plane_count: Optional[NonNegativeInt] = None
    uuid: Optional[UUID] = None
