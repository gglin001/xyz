from __future__ import annotations

import argparse
import binascii
import os
import tarfile
from io import BytesIO

try:
    import qrcode
except ImportError:
    raise ImportError("do `pip install qrcode` first")

"""
convert file to qr code
"""

# TODO: can we support bigger `-seg` size
# TODO: replace `qrcode` with `zxing-cpp`


def main(args):
    with open(args.input, "rb") as fp_in:
        input_buffer = BytesIO(fp_in.read())
    input_buffer.seek(0)

    if args.is_hex:
        hex_bytes = input_buffer.read()
        # NOTE: clean `\n` for hex strs
        hex_bytes = hex_bytes.replace(b"\n", b"")
    elif args.no_xz:
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

    for i in range(0, len(hex_bytes), args.segment_size):
        xx = hex_bytes[i : i + args.segment_size]
        fp = f"{args.output}/qr_{i}.png"
        print(f"created - {fp} , len {len(xx)}")
        qrcode.make(xx, version=args.qr_version).save(fp)


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
        help="output dir",
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
        help="segment size, default=2300, check qr code sepc for more info",
    )
    parse.add_argument(
        "--qr_version",
        type=int,
        default=40,
        help="qr_version, default=40",
    )
    parse.add_argument(
        "--is_hex",
        "-hex",
        action="store_true",
        default=False,
        help="file is hex str(lines from `file2hex`)",
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.qr"

    print(_args)

    os.makedirs(_args.output, exist_ok=True)

    main(_args)


if __name__ == "__main__":
    cli()
