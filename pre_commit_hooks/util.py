from typing import Sequence, Callable, Any, Dict, Optional, Union, Literal, Tuple, IO, List

def iterate_over_files(filenames: Sequence[str], func: Callable[[str, IO[str], Optional[Dict[str, Any]]], int], **kwargs) -> int:
    retv = 0
    for filename in filenames:
        with open(filename, 'r') as f:
            retv = func(filename, f, **kwargs)
    return retv

def remove_comments(buffer: str, character: str = None) -> str:
    character_ = '!' if character is None else character
    return "\n".join([line.split(character_)[0] for line in buffer.split("\n")])

def fetch_string_locations(code: str) -> List[Tuple[int,int]]:

    in_string: Union[bool,Literal["'",'"']] = False
    string_occurrences = []
    string_start = None
    for i, c in enumerate(code):
        if in_string:
            if c == in_string: # c is either ' or " and closes the current string
                string_occurrences.append((string_start, i))
                in_string = False
        elif c in ["'", '"']:
            string_start = i
            in_string = c
    return string_occurrences