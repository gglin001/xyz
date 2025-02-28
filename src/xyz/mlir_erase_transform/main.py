from __future__ import annotations

import argparse
import logging
import re

# TODO: is it enough ?
RE_start = re.compile(r"transform\.with_named_sequence")
RE_end = re.compile(r"transform\.yield")

# match case:
#
# module attributes {transform.with_named_sequence} {
#   transform.named_sequence @to_tile_forall(%arg0: !transform.any_op {transform.readonly}) {
#     %0 = transform.structured.match ops{["linalg.matmul"]} in %arg0 : (!transform.any_op) -> !transform.any_op
#     %tiled_op, %forall_op = transform.structured.tile_using_forall %0 tile_sizes [1, 8, 1] : (!transform.any_op) -> (!transform.any_op, !transform.any_op)
#     transform.yield
#   }
# }


def main(args):
    with open(args.input, "r") as fp:
        while True:
            aline = fp.readline()
            if not aline:
                break
            match_start = RE_start.search(aline)
            if not match_start:
                logging.info(f"{aline}")
            else:
                # drop lines
                while True:
                    aline = fp.readline()
                    if not aline:
                        break
                    match_end = RE_end.search(aline)
                    if match_end:
                        # TODO: deal non-stand formats
                        # read extra 2 lines
                        twolines = fp.readline().strip(" ").strip("\n")
                        twolines += fp.readline().strip(" ").strip("\n")
                        if twolines == "}}":
                            break
                        else:
                            raise NotImplementedError(f"unknown format: \n{twolines}")


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
        _args.output = f"{_args.input}.erase_transform.mlir"

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
