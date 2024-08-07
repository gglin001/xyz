from __future__ import annotations

import argparse
import logging
import os

""""
- opencl kernel code to hpp
- TODO: parse hpp to kernel code back(maybe in another tool)
- TODO: add example
"""

header = r"""
// auto generated from xyz.cl2hpp.
#pragma once

#include <stddef.h>
#include <stdint.h>

#if __cplusplus
extern "C" {
#endif // __cplusplus
"""

tail = r"""
#if __cplusplus
}
#endif // __cplusplus
"""


# {1, 1, 0}
def _gen_bracket_list(alist: list):
    ret = "{"
    for item in alist:
        ret += f"{item}, "
    # always append a zero
    ret += f"{0}"
    ret += "}"
    return ret


def _encode_src(src: str, src_idx: int = 0):
    src_barr = bytearray(src.encode())
    src_barr = list(src_barr)
    logging.info(
        f"static char const file_{src_idx}[] =\n{_gen_bracket_list(src_barr)};"
    )


def main(args):
    with open(args.input, "r") as fp:
        src = fp.read()
        src_idx = 0
        logging.info(header)
        logging.info(f"// src file: {os.path.basename(args.input)}")
        logging.info(rf"""
#if __cplusplus
static char const file_{src_idx}[] = R"(
{src}
)";
#else""")
        _encode_src(src, src_idx)
        logging.info(r"""
#endif""")
        logging.info(tail)


def cli():
    parse = argparse.ArgumentParser()
    # TODO: support multi inputs
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
        _args.output = f"{_args.input}.hpp"

    print(_args)

    file_handler = logging.FileHandler(_args.output, mode="w")
    file_handler.setLevel(logging.INFO)
    logging.basicConfig(
        handlers=[file_handler], level=logging.INFO, format="%(message)s"
    )

    main(_args)


if __name__ == "__main__":
    cli()
