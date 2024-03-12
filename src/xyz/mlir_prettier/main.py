import argparse
import re
import logging

RE_dense = re.compile(r"dense\<\"0x[A-Z0-9]*\"\>")


# TODO: is it robust enough?
def generate_one(type_str: str):
    type_str_clean = type_str.replace("tensor", "").replace("vector", "")
    if "i" in type_str_clean:
        return 1
    elif "f" in type_str_clean:
        return 1.0
    else:
        raise Exception(f"unknown type: {type_str}")


def main(args):
    with open(args.input, "r") as fp:
        while True:
            aline = fp.readline()
            if not aline:
                break
            match = RE_dense.search(aline)
            if match and len(match.group(0)) > args.threshold:
                le, ri = match.span(0)
                logging.info(
                    f"{aline[:le]}dense<{generate_one(aline[ri:])}>{aline[ri:-1]} // NOTE: mlir_prettier.py applied"
                )
            else:
                # last char is '\n'
                logging.info(aline[:-1])


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
        "--threshold",
        "-t",
        type=int,
        default=79,
    )

    _args = parse.parse_args()
    if not _args.output:
        _args.output = f"{_args.input}.pretty.mlir"
    print(_args)

    file_handler = logging.FileHandler(_args.output, mode="w")
    file_handler.setLevel(logging.INFO)
    # file_handler.terminator = ""
    logging.basicConfig(
        handlers=[file_handler], level=logging.INFO, format="%(message)s"
    )

    main(_args)


if __name__ == "__main__":
    cli()
