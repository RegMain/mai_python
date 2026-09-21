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

def token_get_type(token):
        if token in ("+", "-", "*", "/"): return "Operator"
        if token.isdigit() or token in (".", ","): return "Operand"
        if token in ("(", ")"): return "Brace"
        return "Unknown"

class Tokenizator:

    def tokenize(expression):
        expression = "".join(expression.split())
        result: list[Token] = []
        
        for token in expression:
            match token_get_type(token):
                case "Operator":
                    if result:
                        match token_get_type(result[-1]):
                            case "Operand" | "Brace":
                                result.append(OperatorToken(token, True))
                            case "Operato":
                                result.append(OperatorToken(token, False))
                    else:
                        result.append(OperatorToken(token, False))
                case "Operand":
                    if result and token_get_type(token) == "Operand":
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

    def validate(tokens):
        if not tokens:
            raise EmptyExpressionError(
                "Given expression is empty."
            )
        brace_cnt: int = 0
        for i in range(len(tokens)):
            token = tokens[i]
            match token_get_type(token):
                case "Operator":
                    if not token.is_binary:
                        if token in ("*", "/"):
                            raise ExpressionSyntaxError(
                                "Two binary operators in a row."
                            )
                        else:
                            if i != len(tokens) - 1:
                                if (token_get_type(tokens[i+1]) == "Operator"):
                                    raise ExpressionSyntaxError(
                                        "Two binary operators in a row."
                                    )
                            else:
                                raise ExpressionSyntaxError(
                                    "No second operand for binary operator."
                                )
                    else:
                        pass
                    
                case "Operand":
                    try:
                        if token.is_float:
                            tmp: float = float(token)
                        else:
                            tmp: int = int(token)
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
    pass
