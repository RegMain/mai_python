import pytest
from toolkit.calculator import calculate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    ExpressionSyntaxError,
    InvalidCharacterError,
)


def test_empty_expression_1():
    with pytest.raises(EmptyExpressionError):
        calculate("")

def test_invalid_character_1():
    with pytest.raises(InvalidCharacterError):
        calculate("1 + 2 + 3 + 10 + C")

def test_invalid_expression_1():
    with pytest.raises(ExpressionSyntaxError):
        calculate("10 - +")

def test_division_by_zero_1():
    with pytest.raises(DivisionByZeroError):
        calculate("3 / 0")

def test_empty_expression_2():
    with pytest.raises(EmptyExpressionError):
        calculate("       ")

def test_invalid_character_2():
    with pytest.raises(InvalidCharacterError):
        calculate("10 & 3 * (7 - 3)")

def test_invalid_expression_2():
    with pytest.raises(ExpressionSyntaxError):
        calculate("43*/5")

def test_division_by_zero_2():
    with pytest.raises(DivisionByZeroError):
        calculate("10 / (10 - 10)")
