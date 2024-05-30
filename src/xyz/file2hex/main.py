import argparse
import binascii
import tarfile

from io import BytesIO

"""
convert file to hex str
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

    with open(args.output, "w") as fp_out:
        fp_out.write(hex_bytes.decode())


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
        _args.output = f"{_args.input}.hex"
    if not _args.xz:
        raise NotImplementedError("-xz must be true")
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
