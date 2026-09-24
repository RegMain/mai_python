import pytest
from toolkit.calculator import calculate


@pytest.mark.parametrize("expression, expected_result", [
    # Operators' priority
    ("1+2*3/1", eval("1+2*3/1")),
    ("5*7-3/2+58%4-21+3*10", eval("5*7-3/2+58%4-21+3*10")),
    # Support for unar minus
    ("1*-3+7", eval("1*-3+7")),
    ("-31*391+301-1949/-2", eval("-31*391+301-1949/-2")),
    # Ignoring spaces
    ("1 + 2 * 3 / 1", eval("1 + 2 * 3 / 1")),
    # Calculating rational numbers
    ("1 / 2 / 3", eval("1 / 2 / 3")),
    ("84 / 103 + 91 % 138 - 313/122223", eval("84 / 103 + 91 % 138 - 313/122223")),
    ("1/10 + 2/10", eval("1/10 + 2/10")),
    # Support for unar plus
    ("+3 * 5 - 10 / 3", eval("+3 * 5 - 10 / 3")),
    # Support for floating point / comma numbers
    # Note: Python doesn't support floating comma
    ("0.3134+0,13130003-1*0.5", eval("0.3134+0.13130003-1*0.5")),
    ("3.1415926+2.718281828", eval("3.1415926+2.718281828")),
    # Priority of operations with braces
    ("(13-31)*(31/3)-(9335-1929)/39--1", eval("(13-31)*(31/3)-(9335-1929)/39--1")),
    ("(1+3)*(4*5)-(10//5+3)", eval("(1+3)*(4*5)-(10//5+3)")),
    # Too many spaces
    (" ( 7 * 10)  + 12    -3 *(3 + 10 ) ", eval(" ( 7 * 10)  + 12    -3 *(3 + 10 ) "))
])
def test_calculator_positive(expression: str, expected_result: float):
    assert float(calculate(expression)) == float(expected_result)
