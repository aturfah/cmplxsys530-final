""" Base agent class """
from uuid import uuid4


class Base_Agent():
    def __init__(self, id_in=None):
        """ Initialize a new agent """
        if id_in is None:
            self.id = uuid4()
        else:
            self.id = id_in
        self.elo = 1000
        self.num_wins = 0
        self.num_losses = 0

    def hello(self):
        """ Test Method """
        print("Hello from base_agent {}".format(self.id))

    def win_loss_ratio(self):
        """ Get W/L Ratio for Agent """
        if self.num_losses == 0:
            return None
        return self.num_wins / self.num_losses
    
    def make_move(self):
        raise NotImplementedError