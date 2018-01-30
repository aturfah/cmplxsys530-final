""" Functions to compute new elo values for a player """

def expected(player1, player2):
    """ Expected score of player1 vs player2 given elo rankings """
    return 1 / (1 + 10 ** ((player2.elo - player1.elo) / 400))

def elo(player1, player2, outcome, k=32):
    """ Calculate new elo score given outcome of match"""
    exp = expected(player1, player2)
    return player1.elo + k * (outcome - exp)