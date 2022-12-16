#! /usr/bin/env python3

import sys
from typing import Iterable, Sequence, Optional, IO
import argparse

MAX_LINE_LENGTH = 132

def verify_line_length(buffer: IO[bytes] ,limit: int = None) -> Iterable[str]:
    limit_ = MAX_LINE_LENGTH if limit is None else limit
    culprits = []
    for i, line in enumerate(list(buffer)):
        line = line.decode().strip()
        if len(line.split('!')[0]) > limit_: culprits.append({"line_nr":i, "content":line})
    return culprits


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        with open(filename, 'rb+') as f:
            ret_for_file = verify_line_length(f)
            if ret_for_file:
                retv = 1
                print(f"Illegal line length(s) for {filename}:")
                for line in ret_for_file:
                    print(f'    Line at {line["line_nr"]} too long: {len(line["content"])} > {MAX_LINE_LENGTH}')
    return retv