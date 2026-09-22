from dataclasses import dataclass
from toolkit.errors import ImcompatibleUnitsError, UnknownUnitError
from toolkit.errors import InvalidValueError

@dataclass
class Unit:
    unit: str
    value: float

@dataclass
class LengthUnit(Unit):
    
    def get_value_in_si(self) -> float:
        match self.unit:
            case "mm": return self.value / 1000
            case "cm": return self.value / 100
            case "m": return self.value * 1.0
            case "km": return self.value * 1000.0
            case _: raise UnknownUnitError(
                f"Unknown how to convert from unit {self.unit} to m.\n"
            )
            
    def get_value_in_unit(self, unit: str) -> float:
        value_in_si: float = self.get_value_in_si()
        match unit:
            case "mm": return value_in_si * 1000.0
            case "cm": return value_in_si * 100.0
            case "m": return value_in_si * 1.0
            case "km": return value_in_si / 1000
            case _: raise UnknownUnitError(
                f"Unknown how to convert unit to {unit}.\n"
            )
            
@dataclass
class MassUnit(Unit):
    
    def get_value_in_si(self) -> float:
        match self.unit:
            case "g": return self.value / 1000
            case "kg": return self.value * 1.0
            case _: raise UnknownUnitError(
                f"Unknown how to convert from unit {self.unit} to kg.\n"
            )
    
    def get_value_in_unit(self, unit: str) -> float:
        value_in_si: float = self.get_value_in_si()
        match unit:
            case "g": return value_in_si * 1000.0
            case "kg": return value_in_si * 1.0
            case _: raise UnknownUnitError(
                f"Unknown how to convert unit to {unit}.\n"
            )

@dataclass
class TemperatureUnit(Unit):
    
    def get_value_in_si(self) -> float:
        match self.unit:
            case "k": return self.value - 273.15
            case "c": return self.value * 1.0
            case "f": return (self.value * 5 - 160) / 9
            case _: raise UnknownUnitError(
                f"Unknown how to convert from unit {self.unit} to celsius.\n"
            )

    def get_value_in_unit(self, unit: str) -> float:
        value_in_si: float = self.get_value_in_si()
        match unit:
            case "k": return value_in_si + 273.15
            case "c": return value_in_si * 1.0
            case "f": return value_in_si * 1.8 + 32
            case _: raise UnknownUnitError(
                f"Unknown how to convert unit to {unit}.\n"
            )

class Converter:

    def get_type(self, unit: str) -> str:
        if unit in ("mm", "cm", "m", "km"):
            return "Length"
        if unit in ("g", "kg"):
            return "Mass"
        if unit in ("c", "f", "k"):
            return "Temperature"
        raise UnknownUnitError(
            f"Type of {unit} is unknown.\n"
        )

    def convert_from_to(self, from_unit: str, to_unit: str, value: string) -> float:
        from_unit_type: str = self.get_type(from_unit)
        to_unit_type: str = self.get_type(to_unit)

        try:
            value = float(value)
        except ValueError:
            raise InvalidValueError(
                "Given value is not a number.\n"
            )
        
        if from_unit_type != to_unit_type:
            raise ImcompatibleUnitsError(
                f"Type of --to={to_unit} unit is different from type of --from={from_unit} unit.\n"
            )
        
        match from_unit_type:
            case "Length":
                given_unit: LengthUnit = LengthUnit(from_unit, value)
            case "Mass":
                given_unit: MassUnit = MassUnit(from_unit, value)
            case "Temperature":
                ABSOLUTE_ZERO: TemperatureUnit = TemperatureUnit("k", 0)
                if value < ABSOLUTE_ZERO.get_value_in_unit(from_unit):
                    raise InvalidValueError(
                        "Temperature can't be below absolute zero (0 Kelvin).\n"
                    )
                given_unit: TemperatureUnit = TemperatureUnit(from_unit, value)
                
        return given_unit.get_value_in_unit(to_unit)
        
def convert(from_unit: str, to_unit: str, value: float) -> float:
    converter = Converter()
    return converter.convert_from_to(from_unit, to_unit, value)
        
