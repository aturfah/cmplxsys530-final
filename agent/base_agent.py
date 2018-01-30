""" Base agent class """
from uuid import uuid4


class Base_Agent():
    def __init__(self, id_in=None):
        if id_in is None:
            self.id = uuid4()
        else:
            self.id = id_in
        self.elo = 1000
        self.num_wins = 0
        self.num_losses = 0

    def hello(self):
        print("Hello from base_agent {}".format(self.id))
        
    