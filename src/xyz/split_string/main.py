from __future__ import annotations

import argparse

"""
# TODO: WIP

convert long lines into short lines

- support file input
- support stdio input
- support setting splitter
"""


def main(args):
    pass


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

    main(_args)


if __name__ == "__main__":
    cli()
