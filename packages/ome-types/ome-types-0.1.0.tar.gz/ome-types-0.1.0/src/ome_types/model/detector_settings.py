from typing import Optional, cast

from ome_types.dataclasses import ome_dataclass

from .settings import Settings
from .simple_types import (
    Binning,
    DetectorID,
    PositiveInt,
    UnitsElectricPotential,
    UnitsFrequency,
)


@ome_dataclass
class DetectorSettings(Settings):
    binning: Optional[Binning] = None
    gain: Optional[float] = None
    id: Optional[DetectorID] = None
    integration: Optional[PositiveInt] = None
    offset: Optional[float] = None
    read_out_rate: Optional[float] = None
    read_out_rate_unit: Optional[UnitsFrequency] = UnitsFrequency("MHz")
    voltage: Optional[float] = None
    voltage_unit: Optional[UnitsElectricPotential] = UnitsElectricPotential(
        "V"
    )
    zoom: Optional[float] = None
