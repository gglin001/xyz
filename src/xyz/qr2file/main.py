from __future__ import annotations

import argparse
import binascii
import glob
import os
import tarfile
from io import BytesIO

try:
    import zxingcpp
    from PIL import Image
except ImportError:
    raise ImportError("do `pip install pillow zxing-cpp` first")

"""
convert qr code to file
"""


def main(args):
    fps = glob.glob(f"{args.input}/qr_*.png")
    if not fps:
        raise FileNotFoundError("expect `{args.input}/qr_*.png`, but not found")
    fps = sorted(
        fps, key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0])
    )

    input_hex = ""
    for fp in fps:
        print(f"decoding from {fp} , curent len(input_hex): {len(input_hex)}")
        input_decode = zxingcpp.read_barcodes(Image.open(fp))
        if len(input_decode) != 1:
            raise Exception("decode failed, early exit")
        input_hex += input_decode[0].text
        # NOTE: add `\n` for hex strs, check `xyz.file2qr`
        if args.is_hex:
            input_hex += "\n"

    if args.is_hex:
        with open(args.output, "w") as fp_out:
            fp_out.write(input_hex)
    elif args.no_xz:
        input_bin = binascii.a2b_base64(input_hex)
        with open(args.output, "wb") as fp_out:
            fp_out.write(input_bin)
    else:
        input_bin = binascii.a2b_base64(input_hex)
        tar_buffer = BytesIO()
        tar_buffer.write(input_bin)
        tar_buffer.seek(0)
        # mode = 'r:gz'
        mode = "r:xz"
        # mode = 'r:bz2'
        tar = tarfile.open(fileobj=tar_buffer, mode=mode)
        tar.extractall(args.output)


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "input",
        type=str,
        help="input dir, expect `{args.input}/qr_*.png`",
    )
    parse.add_argument(
        "--output",
        "-o",
        type=str,
        default=".",
        help="output dir or file(--no_xz), default=`.`(dir)",
    )
    parse.add_argument(
        "--no_xz",
        action="store_true",
        default=False,
    )
    parse.add_argument(
        "--is_hex",
        "-hex",
        action="store_true",
        default=False,
        help="raw file is hex str, check `xyz.file2qr -hex`",
    )

    _args = parse.parse_args()

    if os.path.isdir(_args.output):
        if _args.is_hex:
            _args.output = f"{_args.output}/qr2file.hex"
        elif _args.no_xz:
            _args.output = f"{_args.output}/qr2file.unknown"

    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
