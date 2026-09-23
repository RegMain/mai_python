import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main():
    parser = argparse.ArgumentParser(
        prog = "toolkit",
        description = "CLI Toolkit: Calculator and Converter"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_calc = subparsers.add_parser("calc", help="Syntax: calc <expression> | Calculates the given expressions' value")
    parser_calc.add_argument("expression", type=str)
    parser_convert = subparsers.add_parser("convert", help="Syntax: convert <value> --from=<unit1> --to<unit2> | Converts value from unit1 to unit2")
    parser_convert.add_argument("value", type=str)
    parser_convert.add_argument("--from_unit", type=str)
    parser_convert.add_argument("--to_unit", type=str)
    args = parser.parse_args()
    try:
        match args.command:
            case "calc":
                print(calculate(args.expression))
            case "convert":
                print(convert(args.from_unit.lower(), args.to_unit.lower(), args.value))
        sys.exit(0)
    except ToolkitError as exception:
        sys.stderr.write(f"Error: {exception}")
        sys.exit(2)
        
if __name__ == "__main__":
    main()
