from __future__ import annotations

import argparse
import logging

"""
# TODO: WIP

convert long lines into short lines

- support file input
- support stdio input
- support setting splitter
"""


def main(args):
    with open(args.input, "r") as fp:
        while True:
            aline = fp.readline()
            if not aline:
                break

            logging.info(f"{aline}")


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "input",
        type=str,
        help="input file",
    )
    parse.add_argument(
        "--output",
        "-o",
        type=str,
        help="output dir",
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.split"
    print(_args)

    file_handler = logging.FileHandler(_args.output, mode="w")
    file_handler.setLevel(logging.INFO)
    # manually deal terminator
    file_handler.terminator = ""
    logging.basicConfig(
        handlers=[file_handler], level=logging.INFO, format="%(message)s"
    )

    main(_args)


if __name__ == "__main__":
    cli()
