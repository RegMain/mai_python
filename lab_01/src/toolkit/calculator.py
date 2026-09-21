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

class Tokenizator:

    def get_type(token):
        if token in ("+", "-", "*", "/"): return "Operator"
        if token.isdigit() or token in (".", ","): return "Operand"
        if token in ("(", ")"): return "Brace"
        return "Unknown"

    def tokenize(self, expression):
        expression = "".join(expression.split())
        result: list[Token] = []
        
        for token in expression:
            match (self.get_type(Token)):
                case "Operator":
                    if result:
                        match str(type(result[-1])):
                            case "OperandToken" | "BraceToken":
                                result.append(OperatorToken(token, True))
                            case "OperatorToken":
                                result.append(OperatorToken(token, False))
                    else:
                        result.append(OperatorToken(token, False))
                case "Operand":
                    if result and str(type(result[-1])) == "OperandToken":
                        result[-1].value += token
                    else:
                        result.append(OperandToken(token, False))
                case "BraceToken":
                    result.append(BraceToken(token == "("))
                case "Unknown":
                    raise InvalidCharacterError(
                        f"Unknown character: {token}"
                    )
        return result
    
class Validator:
    pass

class Calculator:
    pass
