from __future__ import annotations

import argparse
import logging
import os

try:
    import numpy as np
    import numpy.typing as npt
except ImportError:
    raise ImportError("do `pip install numpy` first")


""""
- numpy saved npy to hpp
- TODO: deal alignment
"""

header = r"""
// auto generated from xyz.npy2hpp.
#pragma once

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
def _gen_bracket_list(alist: list):
    ret = "{"
    for item in alist[:-1]:
        ret += f"{item}, "
    ret += f"{alist[-1]}"
    ret += "}"
    return ret


def _encode_src(arr: npt.NDArray, name: str):
    src_barr = bytearray(arr.tobytes())
    src_barr = list(src_barr)
    logging.info(
        f"static unsigned char const {name}[] =\n{_gen_bracket_list(src_barr)};"
    )


def main(args):
    arr = np.load(args.input)

    logging.info(header)
    _encode_src(arr, args.name)
    logging.info(tail)


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
    parse.add_argument(
        "--name",
        type=str,
        help="name of target array, default set to input filename",
    )

    _args = parse.parse_args()

    if not os.path.exists(_args.input):
        raise FileNotFoundError(_args.input)
    if not _args.output:
        _args.output = f"{_args.input}.hpp"
    if not _args.name:
        _args.name = os.path.splitext(os.path.basename(_args.input))[0]
    print(_args)

    file_handler = logging.FileHandler(_args.output, mode="w")
    file_handler.setLevel(logging.INFO)
    logging.basicConfig(
        handlers=[file_handler], level=logging.INFO, format="%(message)s"
    )

    main(_args)


if __name__ == "__main__":
    cli()
