from dataclasses import dataclass
import json
from pathlib import Path

from toolkit.calculator import calculate
from toolkit.errors import IncompatibleUnitsError, InvalidValueError, UnknownUnitError, ConfigSyntaxError, CalculatorError


@dataclass
class Quantity:
    unit: str
    value: float
            
class Converter:

    config: dict

    def __init__(self, config: dict):
        self.config = config

    def get_type(self, unit: str) -> str:
        if "type" in self.config[unit]:
            return self.config[unit]["type"]
        raise ConfigSyntaxError(
            f"Type of {unit} is not in configuration file.\n"
        )

    def convert_to_standart_units(self, quantity: Quantity) -> float:
        if "x" not in self.config[quantity.unit]["to_standart_expression"]:
            raise ConfigSyntaxError(
                f"Variable (x) is not in to_standart_expression for unit {quantity.unit}.\n"
            )
        result: float = calculate(self.config[quantity.unit]["to_standart_expression"].replace("x", str(quantity.value)))
        if "min_value" in self.config[quantity.unit] and result < self.config[quantity.unit]["min_value"]:
            raise InvalidValueError(
                "Value is lower than minimum of its' type.\n"
            )
        if "max_value" in self.config[quantity.unit] and result > self.config[quantity.unit]["max_value"]:
            raise InvalidValueError(
                "Value is higher than maximum of its' type.\n"
            )
        return result
    def convert_to_some_unit(self, quantity: Quantity, to_unit: str) -> float:
        quantity_value_in_standart: float = self.convert_to_standart_units(quantity)
        if "x" not in self.config[to_unit]["from_standart_expression"]:
            raise ConfigSyntaxError(
                f"Variable (x) is not in from_standart_expression for unit {to_unit}.\n"
            )
        return calculate(self.config[to_unit]["from_standart_expression"].replace("x", str(quantity_value_in_standart)))

    def convert_from_to(self, from_unit: str, to_unit: str, value: str) -> float:
        if from_unit not in self.config or to_unit not in self.config:
            raise UnknownUnitError(
                "At least one of units is unknown.\n"
            )
        from_unit_type: str = self.get_type(from_unit)
        to_unit_type: str = self.get_type(to_unit)
        try:
            value = float(value)
        except ValueError:
            raise InvalidValueError(
                "Given value is not a number.\n"
            )
        if from_unit_type != to_unit_type:
            raise IncompatibleUnitsError(
                f"Type of unit {to_unit} is different from type of unit {from_unit}.\n"
            )
        if "to_standart_expression" not in self.config[from_unit] or "from_standart_expression" not in self.config[to_unit]:
            raise ConfigSyntaxError(
                f"Unknown how to convert from unit {from_unit} to unit {to_unit}.\n"
            )
        quantity: Quantity = Quantity(from_unit, value)
        try:
            return self.convert_to_some_unit(quantity, to_unit)
        except CalculatorError:
            raise ConfigSyntaxError(
                "Given expressions in configuration file are not valid.\n"
            )
        
def convert(from_unit: str, to_unit: str, value: float, config_path: str = "") -> float:
    if not config_path:
        config_path = Path(__file__).resolve().parent / "converter.json"
    with open(config_path, "r") as config:
        converter = Converter(json.load(config))
        return converter.convert_from_to(from_unit, to_unit, value)
