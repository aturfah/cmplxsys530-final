"""Testing file for TeamReader."""

from file_manager.team_reader import TeamReader


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
    tr_proc = TeamReader(prefix="unit_test")

    tr_proc.process_files()
    assert tr_proc.teams
    assert len(tr_proc.teams[0]) == 3


def test_teams():
    """Test that teams are read in properly."""
    tr_proc = TeamReader(prefix="cb_spinda.txt")
    tr_proc.process_files()
    processed_spinda = tr_proc.teams[0][0]

    # Test that it is a spinda
    assert processed_spinda.name == "spinda"

    # Test that moves read properly
    assert len(processed_spinda.moves) == 4

    # EVs
    assert processed_spinda.evs["hp"] == 252
    assert not processed_spinda.evs["speed"]

    # Stats calculated correctly
    assert processed_spinda.attack == 240
    assert processed_spinda.speed == 156
    assert processed_spinda.hp == 324


test_init()
test_process()
test_teams()
