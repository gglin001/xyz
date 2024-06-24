from __future__ import annotations

import argparse
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
    new_history = []
    with open(args.input, "r") as fp_in:
        while True:
            aline = fp_in.readline()
            if not aline:
                break
            if is_one_line_history(aline):
                new_history.append(aline)

    if os.path.exists(args.output):
        backup_path = f"{args.output}.backup_{int(time.time())}"
        shutil.move(args.output, backup_path)

    with open(args.output, "w") as fp_out:
        fp_out.write("\n".join(new_history))


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
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
