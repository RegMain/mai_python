import pytest
from toolkit.converter import convert


@pytest.mark.parametrize("from_unit, to_unit, value, expected_result", [
    ["km", "m", 100, 100000.0],
    ["m", "km", 5250.0, 5.25],
    ["f", "c", -40, -40.0],
    ["k", "c", 0, -273.15],
    ["kg", "g", 0.3223, 0.3223*1000.0]
])
def test_converter_positive(from_unit: str, to_unit: str, value: float, expected_result: float):
    assert convert(from_unit, to_unit, value, "") == expected_result
