#! /usr/bin/env python3
from typing import Optional, Sequence, IO
import argparse
from . import util
import re 

def detect_deprecated_symbols(filename: str, buffer: IO[str], symbols: Sequence[str]=None) -> int:

    symbols_ = ['.'+s+'.' for s in ['eq','ne','lt','gt','le','ge']] if symbols is None else \
               symbols
    fortran_code = util.remove_comments(buffer.read())
    culprits = {}
    string_locations = util.fetch_string_locations(fortran_code)
    for symbol in symbols_:
        for match in re.finditer(re.escape(symbol), fortran_code):
            if string_locations:
                in_string = False
                for loc in string_locations:
                    if match.start()>=loc[0] and match.start()+len(match.group())<=loc[1]:
                        in_string = True; break
                if in_string: continue
            line_nr = fortran_code[:match.start()].count("\n")
            culprits[line_nr]=[symbol] if line_nr not in culprits.keys() else culprits[line_nr].append(symbol)

    if culprits:
        print(f"Illegal symbol{'s' if len(culprits)>1 else ''} {filename}:")
        for line_nr, deprecated_symbols in dict(sorted(culprits.items())).items():
            print(f'    Line {line_nr}: contains {deprecated_symbols[0] if len(deprecated_symbols)==1 else deprecated_symbols}')
        return 1
    return 0

def main(argv: Optional[Sequence[str]] = None, **kwargs) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    return util.iterate_over_files(args.filenames, detect_deprecated_symbols, **kwargs)