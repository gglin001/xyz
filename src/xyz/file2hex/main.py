from __future__ import annotations

import argparse
import binascii
import os
import tarfile
from io import BytesIO

"""
convert file to hex str
"""


def main(args):
    with open(args.input, "rb") as fp_in:
        input_buffer = BytesIO(fp_in.read())
    input_buffer.seek(0)

    if args.no_xz:
        hex_bytes = binascii.b2a_base64(input_buffer.read())
    else:
        tar_buffer = BytesIO()
        # mode = 'w:gz'
        mode = "w:xz"
        # mode = 'w:bz2'
        tar = tarfile.open(fileobj=tar_buffer, mode=mode)
        tarinfo = tarfile.TarInfo(os.path.basename(args.input))
        tarinfo.size = len(input_buffer.getvalue())
        tar.addfile(tarinfo, input_buffer)
        tar.close()
        tar_buffer.seek(0)
        hex_bytes = binascii.b2a_base64(tar_buffer.read())
    print(f"len(hex_bytes) : {len(hex_bytes)}")

    with open(args.output, "w") as fp_out:
        hex_str = hex_bytes.decode()
        for i in range(0, len(hex_str), args.segment_size):
            fp_out.write(hex_str[i : i + args.segment_size])
            fp_out.write("\n")


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
        "--no_xz",
        action="store_true",
        default=False,
    )
    parse.add_argument(
        "--segment_size",
        "-seg",
        type=int,
        default=2300,
        help="segment size, default=2300, check file2qr more info",
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.hex"
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
