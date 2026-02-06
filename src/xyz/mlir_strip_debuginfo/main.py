from __future__ import annotations

import argparse
import logging
import re

RE_loc_def = re.compile(r"^\s*#loc[0-9A-Za-z_]*\s*=\s*loc\b")


def strip_loc_expr(line: str) -> str:
    if "loc(" not in line:
        return line

    out: list[str] = []
    i = 0
    while True:
        idx = line.find("loc(", i)
        if idx == -1:
            out.append(line[i:])
            break

        if idx > 0 and (line[idx - 1].isalnum() or line[idx - 1] == "_"):
            out.append(line[i : idx + 1])
            i = idx + 1
            continue

        segment = line[i:idx].rstrip(" \t")
        out.append(segment)

        j = idx
        depth = 0
        saw_paren = False
        while j < len(line):
            ch = line[j]
            if ch == "(":
                depth += 1
                saw_paren = True
            elif ch == ")":
                depth -= 1
                if saw_paren and depth == 0:
                    j += 1
                    break
            j += 1

        if j <= idx:
            i = idx + 1
            continue
        i = j

    return "".join(out)


def main(args):
    with open(args.input, "r") as fp:
        while True:
            aline = fp.readline()
            if not aline:
                break
            if RE_loc_def.match(aline):
                continue
            logging.info(strip_loc_expr(aline))


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
        help="output file",
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.strip_debuginfo.mlir"

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
