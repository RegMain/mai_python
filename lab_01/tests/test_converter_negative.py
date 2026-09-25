import pytest
from toolkit.converter import convert
from toolkit.errors import IncompatibleUnitsError, InvalidValueError, UnknownUnitError


def test_required_1():
    with pytest.raises(InvalidValueError):
        convert("k", "c", -1)


def test_required_2():
    with pytest.raises(IncompatibleUnitsError):
        convert("kg", "m", 1)


def test_unknown_unit_1():
    with pytest.raises(UnknownUnitError):
        convert("km", "ft", 10)


def test_unknown_unit_2():
    with pytest.raises(UnknownUnitError):
        convert("c", "r", 5.3)


def test_incompatible_units_1():
    with pytest.raises(IncompatibleUnitsError):
        convert("c", "g", 3.14)


def test_incompatible_units_2():
    with pytest.raises(IncompatibleUnitsError):
        convert("m", "kg", 103)


def test_invalid_value_1():
    with pytest.raises(InvalidValueError):
        convert("m", "km", "something")


def test_invalid_value_2():
    with pytest.raises(InvalidValueError):
        convert("c", "f", -500)
