from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class AffineTransform:
    a00: float
    a01: float
    a02: float
    a10: float
    a11: float
    a12: float
