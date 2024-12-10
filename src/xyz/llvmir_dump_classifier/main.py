from __future__ import annotations

import argparse
import glob
import os
import shutil

"""
classify llvm ir dump files
eg : `--print-after-all --ir-dump-directory=dump_llvmir`
```
dump_llvmir/7-e69643229fae63a4-module-compiler::SetConvergentAttrPass-after.ll
dump_llvmir/7-fa91abb78b3b04e5-function-545fd4683422dce9-InstCombinePass-after.ll
```
pattern: CurrentPassNumber-NameHash-Type-**Others**.ll
in `llvm/lib/Passes/StandardInstrumentations.cpp`
"""


def get_name_hash(fp: str):
    file = os.path.basename(fp)
    first_m = file.find("-", 0)
    second_m = file.find("-", first_m + 1)
    namehash = file[first_m + 1 : second_m]
    return namehash


def main(args):
    files = glob.glob(f"{args.input}/*.ll")
    if not files:
        print(f"no `{args.input}/*.ll` files found")
        return

    namehash_dict = {}
    for fp in files:
        namehash = get_name_hash(fp)
        if namehash not in namehash_dict:
            namehash_dict[namehash] = []
        namehash_dict[namehash].append(fp)

    for k, fps in namehash_dict.items():
        if args.dry_run:
            print(f"  mkdir -p {args.input}/{k}")
            print(f"  mv {args.input}/*-{k}-* {args.input}/{k}")
        else:
            for fp in fps:
                os.makedirs(f"{args.input}/{k}", exist_ok=True)
                shutil.move(fp, f"{args.input}/{k}/{os.path.basename(fp)}")


def cli():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "input",
        type=str,
        help="input file",
    )
    parse.add_argument(
        "--dry_run",
        action="store_true",
        default=False,
        help="dry_run",
    )

    _args = parse.parse_args()
    print(_args)

    main(_args)


if __name__ == "__main__":
    cli()
