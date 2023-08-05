from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass


class Compression(Enum):
    BZIP2 = "bzip2"
    NONE = "none"
    ZLIB = "zlib"


@ome_dataclass
class BinData:
    value: str
    big_endian: bool
    length: int
    compression: Optional[Compression] = Compression("none")
