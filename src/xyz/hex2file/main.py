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
        print(f"len(input_hex) : {len(input_hex)}")
    input_bin = binascii.unhexlify(input_hex)

    if args.no_xz:
        tar_buffer = BytesIO()
        tar_buffer.write(input_bin)
        tar_buffer.seek(0)
        # mode = 'r:gz'
        mode = "r:xz"
        # mode = 'r:bz2'
        tar = tarfile.open(fileobj=tar_buffer, mode=mode)
        tar.extractall(args.output)
    else:
        with open(args.output, "wb") as fp_out:
            fp_out.write(input_bin)


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
        "--no_xz",
        action="store_true",
        default=False,
    )

    _args = parse.parse_args()
    if not _args.output:
        _args.output = f"." if _args.no_xz else f"{_args.input}.unknown"
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
