"""Script to test functioning of ladder."""

from agent.base_agent import BaseAgent
from ladder.weighted_ladder import WeightedLadder
from battle_engine.coinflip import CoinFlipEngine


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


def test_match_basic():
    """Test that match functions properly."""
    # Set up variables
    lad = WeightedLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    # Add the players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Generate a match (should be ba1 and ba2)
    _ = lad.match_players()

    # Assert that players get removed from ladder
    assert not lad.available_players()
    assert lad.num_turns == 1


def test_run_game():
    """Test run_game functions properly."""
    # Set up variables
    ba1 = BaseAgent()
    ba2 = BaseAgent()
    cfe = CoinFlipEngine()
    lad = WeightedLadder(game=cfe)

    # Add players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Run the game
    lad.run_game()

    # Check that the ladder updated properly
    players = lad.get_players()

    player1 = players[0]
    player2 = players[1]

    # Only one elo value changes
    assert((player1.elo > 1000 and player2.elo == 1000) or
           (player1.elo == 1000 and player2.elo > 1000))

    # Someone won the game
    assert((player1.num_wins == 0 and player2.num_wins == 1) or
           (player1.num_wins == 1 and player2.num_wins == 0))

    # Someone lost the game
    assert((player1.num_losses == 0 and player2.num_losses == 1) or
           (player1.num_losses == 1 and player2.num_losses == 0))


def test_get_players_sorted():
    """Run get_players with sorted flag to true."""
    # Set up variables
    ba1 = BaseAgent()
    ba2 = BaseAgent()
    cfe = CoinFlipEngine()
    lad = WeightedLadder(cfe)

    # Add players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Run the game
    lad.run_game()

    # Check that the results are sorted in ascending elo
    players = lad.get_players(sort=True)

    player1 = players[0]
    player2 = players[1]

    assert player1.elo > player2.elo
    assert (player1.num_wins == 1 and player2.num_wins == 0)
    assert (player1.num_losses == 0 and player2.num_losses == 1)


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


def test_match_error():
    """Ensure RuntimeError is thrown when no players available to match."""
    lad = WeightedLadder()
    ba1 = BaseAgent(id_in="Ba1")

    # Error thrown when no players available
    try:
        lad.match_players()
        assert False
    except RuntimeError:
        pass

    # Error thrown when only one player available
    lad.add_player(ba1)
    try:
        lad.match_players()
        assert False
    except RuntimeError:
        pass

    # Originally enough players, but not enough afterwards
    for _ in range(2):
        lad.add_player(BaseAgent())

    try:
        lad.match_players()  # 3 players in pool
        lad.match_players()  # Only 1 player in pool
        assert False
    except RuntimeError:
        pass


test_match_basic()
test_match_func()
test_run_game()
test_get_players_sorted()
test_selection_size()
test_match_error()
