import pytest
from toolkit.converter import convert


@pytest.mark.parametrize("from_unit, to_unit, value, expected_result", [
    # Required
    ("Mm", "m", 1000, 1.0),
    ("KG", "g", 1.5, 1500.0),
    ("c", "F", 0, 32.0),
    ("c", "k", -273.15, 0),

    ("km", "m", 100, 100000.0),
    ("M", "km", 5250.0, 5.25),
    ("f", "c", -40, -40.0),
    ("k", "C", 0, -273.15),
    ("kG", "g", 0.3223, 0.3223*1000.0)
])
def test_converter_positive(from_unit: str, to_unit: str, value: float, expected_result: float):
    assert convert(from_unit, to_unit, value, "") == expected_result
