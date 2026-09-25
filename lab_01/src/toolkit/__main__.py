import argparse
import json
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError, ConverterError


def main():
    """
    Entry point. Gets expression from stdin, parses it and passes to converter/calculator
    """

    parser = argparse.ArgumentParser(
        prog="toolkit", description="CLI Toolkit: Calculator and Converter"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_calc = subparsers.add_parser(
        "calc",
        help="Syntax: calc <expression> | Calculates the given expressions' value",
    )
    parser_calc.add_argument("expression", type=str)
    parser_convert = subparsers.add_parser(
        "convert",
        help="Syntax: convert <value> --from=<unit1> --to<unit2> | Converts value from unit1 to unit2",
    )
    parser_convert.add_argument("value", type=str)
    parser_convert.add_argument("--from_unit", type=str)
    parser_convert.add_argument("--to_unit", type=str)
    parser_convert.add_argument("--config", type=str)
    args = parser.parse_args()
    try:
        match args.command:
            case "calc":
                result = calculate(args.expression)
                print(result)
                result_json = {"expression": args.expression, "result": result}
                # Loading data from history.json
                try:
                    with open("history.json") as history_file:
                        data = json.load(history_file)
                        data["calculations"].append(result_json)
                except FileNotFoundError:
                    data = {"calculations": [result_json]}
                # Saving data to history.json
                with open("history.json", "w") as history_file:
                    json.dump(data, history_file, indent=4)
            case "convert":
                if args.config:
                    config = args.config
                else:
                    config = ""
                try:
                    print(convert(args.from_unit, args.to_unit, args.value, config))
                except FileNotFoundError:
                    raise ConverterError(
                        "Either there's no configuration file or path to it is wrong.\n"
                    )
        sys.exit(0)
    except ToolkitError as exception:
        sys.stderr.write(f"Error: {exception}")
        sys.exit(2)


if __name__ == "__main__":
    main()
