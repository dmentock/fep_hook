
from pre_commit_hooks import util

def test_remove_comments(tmpdir):
    fortran_code = f"program test\n    !test comment\n    test_line !test_comment inline\nend program test"
    assert util.remove_comments(fortran_code) == 'program test\n    \n    test_line \nend program test'

def test_fetch_string_locations(tmpdir):
    assert util.fetch_string_locations("'1 == 1'") == [(0, 7)]
    assert util.fetch_string_locations('"1 == 1"') == [(0, 7)]
    assert util.fetch_string_locations("""'1 == 1'\n"2==2" """) == [(0, 7), (9, 14)]
    assert util.fetch_string_locations("""write(*, '(*(a))') "error: failed to read: '", trim(arg), "'" """) == \
            [(9, 16), (19, 44), (58, 60)]
