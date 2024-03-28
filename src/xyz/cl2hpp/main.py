import os
import argparse
import logging

""""
- opencl kernel code to hpp
- parse hpp to kernel code back(maybe in another tool), TODO
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


# {1, 1}
def gen_bracket_list(alist: list):
    ret = "{"
    # TODO: need a better loop
    for item in alist[:-1]:
        ret += f"{item}, "
    ret += f"{alist[-1]}"
    ret += "}"
    return ret


def encode_src(src: str, src_idx: int = 0):
    src_barr = bytearray(src.encode())
    src_barr = list(src_barr)
    logging.info(
        f"static char const file_{src_idx}[] = \n{gen_bracket_list(src_barr)};"
    )


def main(args):
    with open(args.input, "r") as fp:
        src = fp.read()
        logging.info(header)
        logging.info(f"// src file: {os.path.basename(args.input)}")
        logging.info(f"/*\n{src}\n*/")
        encode_src(src)
        logging.info(tail)


def cli():
    parse = argparse.ArgumentParser()
    # TODO: support multi inputs
    parse.add_argument(
        "input",
        type=str,
    )
    parse.add_argument(
        "--output",
        "-o",
        type=str,
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
