from dataclasses import dataclass
from toolkit.errors import EmptyExpressionError, InvalidCharacterError
from toolkit.errors import ExpressionSyntaxError, DivisionByZeroError

class Token:
    pass

@dataclass
class OperandToken(Token):
    value: str
    is_float: bool

@dataclass
class OperatorToken(Token):
    value: str
    is_binary: bool

@dataclass
class BraceToken(Token):
    is_opening: bool

def get_type(token: str) -> str:
    if token in ("+", "-", "*", "/") or type(token) == OperatorToken: return "Operator"
    if token.isdigit() or token in (".", ",") or type(token) == OperandToken: return "Operand"
    if token in ("(", ")") or type(token) == BraceToken: return "Brace"
    return "Unknown"

def check_priority(token) -> int:
    match token:
        case "+" | "-": return 1
        case "*" | "/": return 2
    return 0

class Tokenizer:

    def tokenize(self, expression):
        expression = "".join(expression.split())
        result: list = []

        for token in expression:
            match get_type(token):
                case "Operator":
                    if result:
                        match get_type(result[-1]):
                            case "Operand":
                                result.append(OperatorToken(token, True))
                            case "Operator" | "Brace":
                                result.append(OperatorToken(token, False))
                    else:
                        result.append(OperatorToken(token, False))
                case "Operand":
                    if result and get_type(result[-1]) == "Operand":
                        result[-1].value += token
                    else:
                        result.append(OperandToken(token, False))
                case "Brace":
                    result.append(BraceToken(token == "("))
                case "Unknown":
                    raise InvalidCharacterError(
                        f"Unknown character: {token}."
                    )
        return result

class Validator:

    def validate(self, tokens: list):
        if not tokens:
            raise EmptyExpressionError(
                "Given expression is empty."
            )
        brace_cnt: int = 0
        for i in range(len(tokens)):
            token = tokens[i]
            match get_type(token):
                case "Operator":
                    if not token.is_binary:
                        if token in ("*", "/"):
                            raise ExpressionSyntaxError(
                                "Two binary operators in a row."
                            )
                        else:
                            if i != len(tokens) - 1:
                                if (get_type(tokens[i+1]) == "Operator"):
                                    raise ExpressionSyntaxError(
                                        "Two binary operators in a row."
                                    )
                            else:
                                raise ExpressionSyntaxError(
                                    "No second operand for binary operator."
                                )
                case "Operand":
                    try:
                        tmp: float = float(token) + int(token)
                    except ValueError:
                        raise ExpressionSyntaxError(
                            "Invalid format of number."
                        )
                case "Brace":
                    if token.is_opening:
                        brace_cnt += 1
                    else:
                        brace_cnt -= 1
                        if brace_cnt < 0:
                            raise ExpressionSyntaxError(
                                "Braces do not match."
                            )

class Calculator:

    def perform_operation(self, operator: OperatorToken, first_operand: int | float, second_operand: int | float) -> int | float:
        match operator.value:
            case "*": return first_operand * second_operand
            case "+": return first_operand + second_operand
            case "-": return first_operand - second_operand
            case "/":
                if second_operand:
                    if type(first_operand) == int and type(second_operand) == int:
                        return first_operand // second_operand
                    else:
                        return first_operand / second_operand
                else:
                    raise DivisionByZeroError(
                        "Division by zero is in given firmula"
                    )
        return -1

    def tokens_to_prn(self, tokens: list) -> list:
        result: list = []
        stack: list = []
        for token in tokens:
            match get_type(token):
                case "Operand":
                    result.append(token)
                case "Operator":
                    while stack and get_type(stack[-1]) == "Operator" and \
                    check_priority(stack[-1]) > check_priority(token) or \
                    token.is_binary and check_priority(stack[-1]) == check_priority(token):
                        result.append(stack.pop())
                    stack.append(token)
                case "Brace":
                    if token.is_opening:
                        stack.append(token)
                    else:
                        while stack and stack[-1] != BraceToken(False):
                            result.append(stack.pop())
                        if stack and stack[-1] == BraceToken(False):
                            stack.pop()
        while stack:
            result.append(stack.pop())

        return result[::-1]

    def calculate_prn(self, formula: list) -> int | float:
        stack: list = []
        for token in formula:
            if get_type(token) == "Operand":
                stack.append(float(token.value) if token.is_float else int(token.value))
            else:
                if token.is_binary:
                    second_operand: int | float = stack.pop()
                    first_operand: int | float = 0
                    if token.is_binary:
                        first_operand = stack.pop()
                    stack.append(self.perform_operation(token, first_operand, second_operand))

        if stack:
            return stack.pop()
        raise ExpressionSyntaxError("Something went wrong while calculating the expression.")

    def calculate_expression(self, tokens: list) -> int | float:
        return self.calculate_prn(self.tokens_to_prn(tokens))
