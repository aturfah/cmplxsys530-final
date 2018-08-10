"""Testing file for TeamReader."""

from log_manager.team_reader import TeamReader

def test_init():
    """Test initialization method for TeamReader."""
    # Check that reading files works properly
    tr_reg = TeamReader()
    tr_pre = TeamReader(prefix="p")
    tr_suf = TeamReader(suffix="q")

    assert tr_reg.team_files
    assert not tr_pre.team_files
    assert not tr_suf.team_files

def test_process():
    """Test processing of a text file."""
    tr_proc = TeamReader()

    tr_proc.process_files()
    assert tr_proc.teams
    assert len(tr_proc.teams[0]) == 3

test_init()
test_process()
