from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .simple_types import (
    NonNegativeFloat,
    PercentFraction,
    PositiveFloat,
    UnitsLength,
)


@ome_dataclass
class TransmittanceRange:
    cut_in: Optional[PositiveFloat] = None
    cut_in_tolerance: Optional[NonNegativeFloat] = None
    cut_in_tolerance_unit: Optional[UnitsLength] = UnitsLength("nm")
    cut_in_unit: Optional[UnitsLength] = UnitsLength("nm")
    cut_out: Optional[PositiveFloat] = None
    cut_out_tolerance: Optional[NonNegativeFloat] = None
    cut_out_tolerance_unit: Optional[UnitsLength] = UnitsLength("nm")
    cut_out_unit: Optional[UnitsLength] = UnitsLength("nm")
    transmittance: Optional[PercentFraction] = None
