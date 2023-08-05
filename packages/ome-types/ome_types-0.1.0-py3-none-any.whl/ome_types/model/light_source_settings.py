from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .settings import Settings
from .simple_types import (
    LightSourceID,
    PercentFraction,
    PositiveFloat,
    UnitsLength,
)


@ome_dataclass
class LightSourceSettings(Settings):
    attenuation: Optional[PercentFraction] = None
    id: Optional[LightSourceID] = None
    wavelength: Optional[PositiveFloat] = None
    wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")
