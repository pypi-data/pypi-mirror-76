from typing import Optional

from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class ManufacturerSpec:
    lot_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
