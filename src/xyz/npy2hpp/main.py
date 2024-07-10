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

dtype_to_ctype = {
    np.dtype(np.int32): "int",
    np.dtype(np.uint32): "unsigned int",
    np.dtype(np.float32): "float",
    np.dtype(np.int8): "char",
    np.dtype(np.uint8): "unsigned char",
}


# {1, 1}
def _gen_bracket_list(alist: list):
    ret = "{"
    for item in alist[:-1]:
        ret += f"{item}, "
    ret += f"{alist[-1]}"
    ret += "}"
    return ret


# {0x1, 0x1}
def _gen_bracket_list_in_hex(alist: list):
    ret = "{"
    for item in alist[:-1]:
        ret += f"{hex(item)}, "
    ret += f"{hex(alist[-1])}"
    ret += "}"
    return ret


def _encode_src(arr: npt.NDArray, args):
    name: str = args.name
    code = f"// shape={arr.shape}, dtype={arr.dtype}, size={arr.size}"
    logging.info(code)
    code = f"#define {name.upper()}__SIZE {arr.size}"
    logging.info(code)

    arr_list = arr.flatten().tolist()
    ctype = dtype_to_ctype[arr.dtype]
    if args.hex:
        content = _gen_bracket_list_in_hex(arr_list)
    else:
        content = _gen_bracket_list(arr_list)
    code = f"static {ctype} const {name}[] =\n{content};"
    logging.info(code)


def main(args):
    if args.in_bin:
        arr = np.fromfile(args.input)
    else:
        arr = np.load(args.input)

    if args.u8:
        arr = arr.view(np.uint8)

    logging.info(header)
    _encode_src(arr, args)
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
        "-n",
        type=str,
        help="name of target array, default set to input filename",
    )
    parse.add_argument(
        "--in_bin",
        action="store_true",
        default=False,
        help="input file is a bin",
    )
    parse.add_argument(
        "--hex",
        action="store_true",
        default=False,
        help="use hex or not",
    )
    parse.add_argument(
        "--u8",
        action="store_true",
        default=False,
        help="use u8(uint8) or not",
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
