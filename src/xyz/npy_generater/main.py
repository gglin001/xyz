from __future__ import annotations

import argparse
import os
import sys

try:
    import numpy as np
    import numpy.typing as npt
except ImportError:
    raise ImportError("do `pip install numpy` first")


""""
- numpy generater from args
- TODO: support full args from `iree-run-module`
"""


"""
note:

scalar value
e.g.: --input="3.14"

buffer:
[shape]xtype=[value]
e.g.: --input="2x2xi32=1 2 3 4"
2x2xi32=[[1 2][3 4]]
2x2xi32=@some/file.bin
"""


type_to_dtype = {
    "i32": np.dtype(np.int32),
    "int32": np.dtype(np.int32),
    "i64": np.dtype(np.int64),
    "int64": np.dtype(np.int64),
    "i8": np.dtype(np.int8),
    "u8": np.dtype(np.uint8),
    "f32": np.dtype(np.float32),
    "f64": np.dtype(np.float64),
}


def parse_input(arg: str) -> tuple[3]:
    # TODO: support `--input="2x2xi32=1"` only for now

    arg = arg.strip('"').strip("'")
    left, right = arg.split("=")

    le = left.split("x")
    shape = [int(x) for x in le[:-1]]
    dtype = type_to_dtype[le[-1]]
    value = np.array(right, dtype=dtype)
    return (shape, dtype, value)


def main(args):
    shape, dtype, value = parse_input(args.input)
    arr = np.array(value, shape=shape, dtype=dtype)
    np.save(args.output, arr)


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--input",
        "-i",
        type=str,
        help="inputs",
    )
    parse.add_argument(
        "--output",
        "-o",
        # required=True,
        type=str,
        help="output file",
    )

    _args = parse.parse_args()

    # _args = parse.parse_args(
    #     [
    #         '--input="2x2xi32=1"',
    #     ]
    # )

    print(_args)
    if not _args.output:
        _args.output = sys.stdout

    main(_args)


if __name__ == "__main__":
    cli()
