#! /usr/bin/env python3

from typing import Sequence, Optional, IO
import argparse
from . import util

MAX_LINE_LENGTH = 132

def verify_line_length(filename, buffer: IO[str], limit: int = None) -> int:

    limit_ = MAX_LINE_LENGTH if limit is None else \
             limit
    fortran_code = util.remove_comments(buffer.read())
    culprits = []
    for i, line in enumerate(fortran_code.split("\n")):
        if len(line) > limit_: culprits.append({"line_nr":i+1, "content":line})
    if culprits:
        print(f"Illegal line length{'s' if len(culprits)>1 else ''} for {filename}:")
        for line in culprits:
            print(f'    Line {line["line_nr"]} too long: {len(line["content"])} > {limit_}')
        return 1
    return 0

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    return util.iterate_over_files(args.filenames, verify_line_length)


