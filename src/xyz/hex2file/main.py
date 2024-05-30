import argparse
import binascii
import tarfile

from io import BytesIO

"""
convert hex str to file
"""


def main(args):
    with open(args.input, "rb") as fp_in:
        input_hex = fp_in.read()
    input_bytes = binascii.a2b_hex(input_hex)

    if args.xz:
        tar_buffer = BytesIO()
        tar_buffer.write(input_bytes)
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
        "-xz",
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
