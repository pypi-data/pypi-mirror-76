from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .simple_types import Hex40


class Compression(Enum):
    BZIP2 = "bzip2"
    NONE = "none"
    ZLIB = "zlib"


@ome_dataclass
class External:
    href: str
    sha1: Hex40
    compression: Optional[Compression] = Compression("none")
