
from __future__ import annotations
import sys
import pytest
from pre_commit_hooks import check_line_length

@pytest.mark.parametrize('test_line',[
    "! Comment line",
    "! Very long comment line.............................................................................................................",
    "print *, 'Hello, World!' ! Inline comment",
    "print *, 'Hello, World!' ! Very long inline comment.................................................................................."])
def test_legal_file(tmpdir,test_line):
    fortran_code = "program test\n    {test_line}\nend program test"
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write(fortran_code)
        assert check_line_length.main(['f.py']) == 0

def test_illegal_file(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write("""
program hello
  print *, 'Very long print statement..................................................................................................'
end program hello""")
        assert check_line_length.main(['f.py']) == 1