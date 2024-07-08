from __future__ import annotations

import argparse
import logging
import shutil

"""
convert long lines into short lines

- support file input
- TODO: support stdio input
"""


def main(args):
    with open(args.input, "r") as fp:
        while True:
            aline = fp.readline()
            if not aline:
                break

            for mark in args.mark:
                aline = aline.replace(mark, f"\n{mark}")

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
    parse.add_argument(
        "--inplace",
        "-i",
        action="store_true",
        default=False,
        help="inplace mode",
    )
    parse.add_argument(
        "--mark",
        "-m",
        action="append",
        help='mark, `mark` -> `\\n + mark`. if no set, will be [" -", " --"]',
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.split"
    if not _args.mark:
        _args.mark = [" -", " --"]

    print(_args)

    file_handler = logging.FileHandler(_args.output, mode="w")
    file_handler.setLevel(logging.INFO)
    # manually deal terminator
    file_handler.terminator = ""
    logging.basicConfig(
        handlers=[file_handler], level=logging.INFO, format="%(message)s"
    )

    main(_args)

    if _args.inplace:
        shutil.move(_args.output, _args.input)


if __name__ == "__main__":
    cli()
