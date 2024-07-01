from __future__ import annotations

import argparse
import logging
import os
import pathlib
import shutil
import time

"""
- clean `~/.zsh_history`
- keep <= `--n_lines` of history
"""


def main(args):
    is_full = False
    lines: list[str] = []
    with open(args.input, "r") as fp_in:
        while True:
            try:
                aline = fp_in.readline()
            except Exception as _:
                # `readline()` may fail, just skip, related history will be discard
                print("skiped a times `.readline()`")
                pass

            if not aline:
                if len(lines) <= args.n_lines + 1:
                    for line in lines:
                        logging.info(line)
                break

            lines.append(aline)

            # TODO: is it robust enough?
            if len(lines) > 1 and lines[-1].startswith(": "):
                is_full = True

            if is_full:
                if len(lines) <= args.n_lines + 1:
                    for line in lines[:-1]:
                        logging.info(line)
                is_full = False
                lines = [lines[-1]]


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
    parse.add_argument(
        "--n_lines",
        "-n",
        type=int,
        default=2,
        help="keep <= n lines of history",
    )

    _args = parse.parse_args()
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
