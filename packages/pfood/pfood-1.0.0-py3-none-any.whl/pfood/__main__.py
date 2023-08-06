#!/usr/bin/env python3

import argparse
import sys

from pfood import meta
from pfood.pfood_main import PFood


def main() -> None:
    parser = argparse.ArgumentParser(prog=meta.name, description=meta.description)

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="number of food that will be shown (default: 1).",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.name} {meta.version}",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_const",
        const="list",
        dest="action",
        help="list all foods and end program.",
    )

    args = parser.parse_args()

    try:
        food = PFood()
        if args.action == "list":
            food.print_all()
        else:
            food.print_random(args.count)
    except:
        sys.exit(f"\n\033[31m" + "Unknown error occurred" + f"\033[30m")


if __name__ == "__main__":
    main()
