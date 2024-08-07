from __future__ import annotations

import argparse
import binascii
import os
import tarfile
from io import BytesIO

"""
convert hex str to file
"""


def main(args):
    with open(args.input, "rb") as fp_in:
        input_hex = fp_in.read()
        # strip final newline
        input_hex = input_hex.strip(b"\n")
        print(f"len(input_hex) : {len(input_hex)}")
    input_bin = binascii.a2b_base64(input_hex)

    if args.no_xz:
        with open(args.output, "wb") as fp_out:
            fp_out.write(input_bin)
    else:
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
        help="input file",
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

    _args = parse.parse_args()

    if os.path.isdir(_args.output):
        if _args.no_xz:
            _args.output = f"{_args.output}/hex2file.unknown"

    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
