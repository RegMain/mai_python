class ToolkitError(Exception):
    pass

class CalculatorError(ToolkitError):
    pass

class EmptyExpressionError(CalculatorError):
    pass

class InvalidCharacterError(CalculatorError):
    pass

class ExpressionSyntaxError(CalculatorError):
    pass

class DivisionByZeroError(CalculatorError):
    pass

class ConverterError(ToolkitError):
    pass

class UnknownUnitError(ConverterError):
    pass

class IncompatibleUnitsError(ConverterError):
    pass

class InvalidValueError(ConverterError):
    pass
