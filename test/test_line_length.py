
from __future__ import annotations
import sys
import pytest
from pre_commit_hooks import line_length_checker

# skip_win32 = pytest.mark.skipif(
#     sys.platform == 'win32',
#     reason='case conflicts between directories and files',
# )

def test_legal_file(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write("""
program hello
  ! Comment line
  ! Very long comment line.............................................................................................................
  print *, 'Hello, World!' ! Inline comment
  print *, 'Hello, World!' ! Very long inline comment..................................................................................
end program hello""")
        assert line_length_checker.main(['f.py']) == 0

def test_illegal_file(tmpdir):
    with tmpdir.as_cwd():
        tmpdir.join('f.py').write("""
program hello
  print *, 'Very long print statement..................................................................................................'
end program hello""")
        assert line_length_checker.main(['f.py']) == 1
