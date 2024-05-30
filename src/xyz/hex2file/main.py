import argparse
import binascii
import tarfile
import os

from io import BytesIO

"""
convert hex str to file
"""


def main(args):
    with open(args.input, "rb") as fp_in:
        input_hex = fp_in.read()
        print(f"len(input_hex) : {len(input_hex)}")
    input_bin = binascii.unhexlify(input_hex)

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
        help="output dir or file(--no_xz)",
    )
    parse.add_argument(
        "--no_xz",
        action="store_true",
        default=False,
    )

    _args = parse.parse_args()

    if not _args.output:
        _args.output = f"{_args.input}.unknown" if _args.no_xz else f"."
    if _args.no_xz and os.path.isdir(_args.output):
        _args.output = f"{_args.output}/hex2file.unknown"
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
