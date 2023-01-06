
from __future__ import annotations
import sys
import pytest
from pre_commit_hooks import detect_deprecated_symbols
import re

@pytest.mark.parametrize('test_line',[
    "print *, 'eq'",
    "print *, '.eq.'",
    'print *, ".eq."',
    "1 eq 2"])
def test_legal_symbols(tmpdir,test_line):
    fortran_code = f"program test\n    {test_line}\nend program test"
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write(fortran_code)
        assert detect_deprecated_symbols.main(['f.py'],symbols = [".eq."]) == 0

@pytest.mark.parametrize('test_line',[
    "1 .eq. 1",
    "print *, 'test'; 1 .eq. 1; print *, 'test';",
    'print *, "test"; 1 .eq. 1; print *, "test"',
    """print *, "test"; 1 .eq. 1; print *, 'test'"""])
def test_illegal_symbols(tmpdir,test_line):
    fortran_code = f"program test\n    {test_line}\nend program test"
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write(fortran_code)
        assert detect_deprecated_symbols.main(['f.py'],symbols = [".eq."]) == 1