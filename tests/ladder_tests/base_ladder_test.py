"""Test for functions of BaseLadder."""

from agent.base_agent import BaseAgent
from battle_engine.coinflip import CoinFlipEngine
from ladder.base_ladder import BaseLadder
from tests.ladder_tests.ladder_test_helpers import mock_match_func


def test_add():
    """Basic test for ladder add_player method."""
    lad = BaseLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    assert len(lad.player_pool) == 2


def test_duplicate_add():
    """Test that same player cannot exist twice on ladder."""
    lad = BaseLadder()
    ba1 = BaseAgent()
    lad.add_player(ba1)

    lad.num_turns = 50

    lad.add_player(ba1)
    assert lad.player_pool[0][1] == 50
    assert len(lad.player_pool) == 1


def test_available_players():
    """Test that available players picks out players not in games."""
    lad = BaseLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    # No players are in games, so all available
    lad.add_player(ba1)
    lad.add_player(ba2)
    assert len(lad.available_players()) == 2

    # One player is taken
    ba1.in_game = True
    available_players = lad.available_players()
    assert len(available_players) == 1
    assert available_players[0] == (ba2, 0)


def test_match_basic():
    """Test that match functions properly."""
    # Set up variables
    lad = BaseLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    # Use fake match function
    lad.match_func = mock_match_func

    # Add the players to the ladder
    lad.add_player(ba1)
    lad.add_player(ba2)

    # Generate a match (should be ba1 and ba2)
    _ = lad.match_players()

    # Assert that players get removed from player pool
    assert not lad.available_players()
    assert lad.num_turns == 1
    for player, _ in lad.player_pool:
        assert player.in_game


def test_match_error():
    """Ensure RuntimeError is thrown when no players available to match."""
    lad = BaseLadder()
    ba1 = BaseAgent(id_in="Ba1")
    lad.match_func = mock_match_func

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


def test_run_game():
    """Test run_game functions properly."""
    # Set up variables
    ba1 = BaseAgent()
    ba2 = BaseAgent()
    cfe = CoinFlipEngine()
    lad = BaseLadder(game=cfe)
    lad.match_func = mock_match_func

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
    lad = BaseLadder(game=cfe)
    lad.match_func = mock_match_func

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


test_add()
test_duplicate_add()
test_available_players()
test_match_basic()
test_match_error()
test_run_game()
test_get_players_sorted()
