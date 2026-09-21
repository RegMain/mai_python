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
    if token in ("+", "-", "*", "/"): return "Operator"
    if token.isdigit() or token in (".", ","): return "Operand"
    if token in ("(", ")"): return "Brace"
    if token.isspace(): return "Space"
    return "Unknown"

def check_priority(token) -> int:
    match token.value:
        case "*" | "/": return 2
        case "+" | "-": return 1 if token.is_binary else 3
    return 0

class Tokenizer:

    def tokenize(self, expression):
        while "  " in expression:
            expression = expression.replace("  ", " ")
        result: list = []
        new_token_flag = True
        for token in expression:
            match get_type(token):
                case "Operator":
                    if result:
                        match result[-1]:
                            case OperandToken():
                                result.append(OperatorToken(token, True))
                            case OperatorToken():
                                result.append(OperatorToken(token, False))
                            case BraceToken():
                                if result[-1].is_opening:
                                    result.append(OperatorToken(token, False))
                                else:
                                    result.append(OperatorToken(token, True))
                        new_token_flag = True

                    else:
                        result.append(OperatorToken(token, False))
                case "Operand":
                    if new_token_flag:
                        result.append(OperandToken(token.replace(",", "."), token in (",", ".")))
                        new_token_flag = False
                    elif isinstance(result[-1], OperandToken):
                        if token in (".", ","):
                            result[-1].is_float = True
                            result[-1].value += "."
                        else:
                            result[-1].value += token
                case "Brace":
                    result.append(BraceToken(token == "("))
                    new_token_flag = True
                case "Space":
                    new_token_flag = True
                    continue
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
            match token:
                case OperatorToken():
                    if i == len(tokens) - 1:
                        raise ExpressionSyntaxError(
                            "No operand for operator."
                        )

                    if not token.is_binary:
                        if token.value in ("*", "/"):
                            raise ExpressionSyntaxError(
                                "Two binary operators in a row."
                            )
                    else:
                        if (isinstance(tokens[i + 1], OperatorToken) and tokens[i + 1].is_binary):
                            raise ExpressionSyntaxError(
                                "Two binary operators in a row."
                            )
                        elif tokens[i + 1] == BraceToken(False):
                            raise ExpressionSyntaxError(
                                "No second operand for binary operator."
                            )
                case OperandToken():
                    try:
                        tmp: float = float(token.value)
                    except ValueError:
                        raise ExpressionSyntaxError(
                            "Invalid format of number."
                        )
                    if i != 0 and isinstance(tokens[i - 1], OperandToken):
                        raise ExpressionSyntaxError(
                            "No operator between two numbers."
                        )
                case BraceToken():
                    if token.is_opening:
                        brace_cnt += 1
                    else:
                        if isinstance(tokens[i - 1], OperatorToken) or tokens[i - 1] == BraceToken(True):
                            raise ExpressionSyntaxError(
                                "Empty braces were found."
                            )
                        brace_cnt -= 1
                        if brace_cnt < 0:
                            raise ExpressionSyntaxError(
                                "Braces do not match."
                            )

        if brace_cnt != 0:
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
                    if type(first_operand) == int and type(second_operand) == int and first_operand % second_operand == 0:
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
            match token:
                case OperandToken():
                    result.append(token)
                case OperatorToken():
                    while stack and isinstance(stack[-1], OperatorToken) and \
                    (check_priority(stack[-1]) > check_priority(token) or \
                        (token.is_binary and check_priority(stack[-1]) == check_priority(token))):
                        result.append(stack.pop())
                    stack.append(token)
                case BraceToken():
                    if token.is_opening:
                        stack.append(token)
                    else:
                        while stack and stack[-1] != BraceToken(True):
                            result.append(stack.pop())
                        if stack and stack[-1] == BraceToken(True):
                            stack.pop()
        while stack:
            result.append(stack.pop())

        return result

    def calculate_prn(self, formula: list) -> int | float:
        stack: list = []
        for token in formula:
            if isinstance(token, OperandToken):
                stack.append(float(token.value) if token.is_float else int(token.value))
            else:
                second_operand: int | float = stack.pop()
                first_operand: int | float = 0
                if token.is_binary:
                    first_operand = stack.pop()
                stack.append(self.perform_operation(token, first_operand, second_operand))

        if len(stack) == 1:
            return stack.pop()
        raise ExpressionSyntaxError("Something went wrong while calculating the expression.")

    def calculate_expression(self, tokens: list) -> int | float:
        return self.calculate_prn(self.tokens_to_prn(tokens))
