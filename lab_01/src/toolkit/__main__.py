import sys
import argparse

from toolkit.calculator import calculate

def main():
    parser = argparse.ArgumentParser(
        prog = "toolkit",
        description = "CLI Toolkit: Calculator and Converter"
    )
    subcommands = parser.add_subparsers(dest = "command", required = True)
if __name__ == "__main__":
    main()
