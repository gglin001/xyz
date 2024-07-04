from __future__ import annotations

import argparse
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


def gen_array(arg: str) -> npt.NDArray:
    arg = arg.strip('"').strip("'")

    # `-i i32=1` / `-i 1`
    if "x" not in arg:
        if "=" in arg:
            le, ri = arg.split("=")
            dtype = type_to_dtype[le]
            value = np.array(ri, dtype=dtype)
            return value
        else:
            value = np.array(eval(arg))
            return value

    # `-i 2x2xi32=1`
    le, ri = arg.split("=")
    ll = le.split("x")
    shape = [int(x) for x in ll[:-1]]
    dtype = type_to_dtype[ll[-1]]
    value = np.array(ri, dtype=dtype)
    arr = np.zeros(shape=shape, dtype=dtype)
    arr = arr + value

    # TODO: `-i "2x2xi32=1 2 3 4"` ?
    # TODO: `-i "2x2xi32=[[1 2][3 4]]"` ?
    # TODO: `-i "2x2xi32=@some/file.bin"` ?
    # TODO: `-i 2x2xi32=#json/string` ?

    return arr


def main(args):
    arr = gen_array(args.input)

    if args.output == "-":
        print(f"shape={arr.shape}, dtype={arr.dtype}", file=sys.stdout)
        if arr.shape:
            np.savetxt(sys.stdout, arr)
        else:
            np.savetxt(sys.stdout, arr.reshape([1]))
    else:
        np.save(args.output, arr)


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--input",
        "-i",
        type=str,
        help="input, eg: `-i=2x2xi32=1`, `-i=`3.14`, `-i=i32=`3.14`",
    )
    parse.add_argument(
        "--output",
        "-o",
        type=str,
        default="-",
        help="output file, default: `sys.stdout`",
    )

    _args = parse.parse_args()

    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
