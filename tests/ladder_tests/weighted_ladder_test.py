"""Script to test functioning of ladder."""

from agent.base_agent import BaseAgent
from ladder.weighted_ladder import WeightedLadder

def test_match_func():
    """Test the match_func to make sure it works."""
    # Set up variables
    lad = WeightedLadder()
    ba1 = BaseAgent(id_in="Ba1")
    ba2 = BaseAgent(id_in="Ba2")

    # Make the elo score higher
    ba1.elo = 1500
    ba2.elo = 1400

    # Add the higher ranked players
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Add the rest of the agents (ranked lower)
    for i in range(3, 11):
        lad.add_player(BaseAgent(id_in="Ba{}".format(i)))

    # Try matching the higher ranked players together
    match1, match2 = lad.match_players()
    while (match1.id is not ba1.id) and (match1.id is not ba2.id):
        match1, match2 = lad.match_players()

    # Higher elo players got matched together
    assert (match2.id == ba1.id or match2.id == ba2.id)


def test_selection_size():
    """Test that selection size works properly."""
    # Initialization
    lad = WeightedLadder()
    assert lad.selection_size == 1

    # Populate ladder
    base_player = BaseAgent()
    base_player.elo = 1030
    for ind in range(15):
        new_player = BaseAgent()
        new_player.elo = 1000 + ind
        lad.add_player(new_player)

    # Only getting pool of one player
    lad.selection_size = 1
    assert len(lad.get_candidate_matches(base_player)) == 1
    assert lad.get_candidate_matches(base_player)[0][0].elo == 1014

    # Pool of normal size, get five best players
    lad.selection_size = 5
    assert len(lad.get_candidate_matches(base_player)) == 5
    max_elo = 1014
    for pair in lad.get_candidate_matches(base_player):
        assert pair[0].elo == max_elo
        max_elo -= 1

    # Pool of unreasonable size, just get max number of players
    lad.selection_size = 5000
    assert len(lad.get_candidate_matches(base_player)) == 15


test_match_func()
test_selection_size()
