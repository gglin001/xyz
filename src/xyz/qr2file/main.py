import argparse
import binascii
import tarfile
import os
import glob

from io import BytesIO

try:
    from PIL import Image
    import zxingcpp
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
    input_bin = binascii.unhexlify(input_hex)

    if args.xz:
        tar_buffer = BytesIO()
        tar_buffer.write(input_bin)
        tar_buffer.seek(0)
        # mode = 'r:gz'
        mode = "r:xz"
        # mode = 'r:bz2'
        tar = tarfile.open(fileobj=tar_buffer, mode=mode)
        tar.extractall(args.output)
    else:
        raise NotImplementedError("args.xz must be true")


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
    )
    parse.add_argument(
        "--xz",
        action="store_false",
        default=True,
        help="do `tar cfJ` first",
    )

    _args = parse.parse_args()
    if not _args.output:
        _args.output = f"."
    if not _args.xz:
        raise NotImplementedError("-xz must be true")
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
