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


def main(args):
    with open(args.input, "rb") as fp_in:
        input_buffer = BytesIO(fp_in.read())
    input_buffer.seek(0)

    if args.xz:
        tar_buffer = BytesIO()
        # mode = 'w:gz'
        mode = "w:xz"
        # mode = 'w:bz2'
        tar = tarfile.open(fileobj=tar_buffer, mode=mode)
        tarinfo = tarfile.TarInfo(args.input)
        tarinfo.size = len(input_buffer.getvalue())
        tar.addfile(tarinfo, input_buffer)
        tar.close()
        tar_buffer.seek(0)
        hex_bytes = binascii.hexlify(tar_buffer.read())
    else:
        hex_bytes = binascii.hexlify(input_buffer.read())
    print(f"len(hex_bytes) : {len(hex_bytes)}")

    for i in range(0, len(hex_bytes), args.seg):
        xx = hex_bytes[i : i + args.seg]
        fp = f"{args.output}/qr_{i}.png"
        print(f"created - {fp} , len {len(xx)}")
        qrcode.make(xx, version=args.qr_version).save(fp)


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "input",
        type=str,
    )
    parse.add_argument(
        "--output",
        "-o",
        type=str,
        help="output dir",
    )
    parse.add_argument(
        "-xz",
        action="store_false",
        default=True,
        help="do `tar cfJ` first",
    )
    parse.add_argument(
        "-seg",
        type=int,
        default=2300,
        help="segment size, default=2300, check qr code sepc forv more info",
    )
    parse.add_argument(
        "-qr_version",
        type=int,
        default=40,
        help="qr_version, default=40",
    )

    _args = parse.parse_args()
    if not _args.output:
        _args.output = f"{_args.input}.qr"
    if not _args.xz:
        raise NotImplementedError("-xz must be true")
    print(_args)

    os.makedirs(_args.output, exist_ok=True)

    main(_args)


if __name__ == "__main__":
    cli()
