from __future__ import annotations

import argparse
import logging
import os
import pathlib
import shutil
import time

"""
clean `~/.zsh_history`
"""


def is_one_line_history(aline: str) -> bool:
    if aline.startswith(": ") and not aline.endswith("\\"):
        return True
    return False


def main(args):
    with open(args.input, "r") as fp_in:
        while True:
            try:
                aline = fp_in.readline()
            except Exception as _:
                # `readline()` may fail, just skip
                print("skiped a times `.readline()`")
                pass

            if not aline:
                break

            # TODO: add an option for keeping multi lines
            # TODO: support multi lines history(each line ends with `\`)
            if is_one_line_history(aline):
                logging.info(aline)


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--input",
        "-i",
        type=str,
        default=f"{pathlib.Path.home()}/.zsh_history",
        help="input file",
    )
    parse.add_argument(
        "--output",
        "-o",
        default=f"{pathlib.Path.home()}/.zsh_history",
        type=str,
        help="output dir",
    )

    _args = parse.parse_args()
    # _args = parse.parse_args(
    #     [
    #         "-i=./_demos/zsh_history.backup",
    #         "-o=./_demos/zsh_history",
    #     ]
    # )

    print(_args)
    if os.path.exists(_args.output):
        backup_path = f"{_args.output}.backup_{int(time.time())}"
        shutil.move(_args.output, backup_path)

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
