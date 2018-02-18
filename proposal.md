# Model Proposal for _[Project Name]_

_Ali Turfah_

* Course ID: CMPLXSYS 530,
* Course Title: Computer Modeling of Complex Systems
* Term: Winter, 2018



&nbsp; 

### Goal 
*****
 
The goal of this project is to create a model of the Pokemon Showdown (PS) metagame. The primary results of interest are the emergent strategies that correspond to "high-ladder" play. <br/>
Ideally this will be done by building up from the rules simpler turn-based games (Rock/Paper/Scissors) with varying strategies.

&nbsp;  
### Justification
****
_Short explanation on why you are using ABM_
ABMs were chosen to model this system because it allows for control at the level of the player, in individual games, and analysis of the results at the metagame level.

&nbsp; 
### Main Micro-level Processes and Macro-level Dynamics of Interest
****

_Short overview of the key processes and/or relationships you are interested in using your model to explore. Will likely be something regarding emergent behavior that arises from individual interactions_

The Micro-level process is how the game plays out. In the case of Rock/Paper/Scissors, it is which move the players cast. In the case of pokemon, it is the decisions made at each turn by the players. 
&nbsp; 
The Macro-level process of interest is which strategies tend to dominate and the trends in dominant strategies. Since PS matches players based on Elo ranking (as opposed to randomly), another feature of interest is how that affects metagame development/which strategies dominate.

## Model Outline
****
&nbsp; 
### 1) Environment
_The environment will be the "ladder", or the matchmaking service that pairs players for a battle. There will be two types of ladders, one that pairs players based on Elo Ranking and another that pairs them randomly. The ladder is also responsible for updating player scores after a game is completed._

#### Properties
<ul>
<li><i>player_pool</i>: List of players availible to play.</li>
<li><i>game</i>: GameEngine specifying game to be played.</li>
<li><i>k_value</i>: K value to use in updating Elo scores.</li>
<li><i>num_turns</i>: Number of games that have been played.</li>
</ul>

#### Function to match players (base_ladder.py)
```python
def match_players(self):
    """Return a pair of players to play."""
    # Select a random player
    player_ind = randint(low=0, high=len(self.player_pool))
    player = self.player_pool[player_ind][0]
    del self.player_pool[player_ind]

    # Select that player's opponent (based on waiting function)
    opponent_pair = sorted(self.player_pool,
                            key=lambda val: self.match_func(player, val),
                            reverse=True)[0]
    opponent = opponent_pair[0]
    opponent_ind = self.player_pool.index(opponent_pair)
    del self.player_pool[opponent_ind]

    self.num_turns += 1
    return (player, opponent)
```

#### Random Ladder Weighting function (random_ladder.py)
```python
def match_func(self, player1, player2_pair):
    """
    Return random value as a match weighting.

    Since players will be sorted this random value, it is
    equivalent to randomly choosing an opponent.

    :param player1: BaseAgent
        The player who is being matched
    :param player2: (BaseAgent, int)
        The candidate player & turns waiting pair for a  match
    """
    return rand()
```

#### Weighted Ladder Weighting function (weighted_ladder.py)
```python
def match_func(self, player1, player2_pair):
    """
    Calculate the match score for two players.

    Players with similar elo rankings should be matched together.
    In addition, players who have been waiting for a long time should
    get to play sooner.

    Functional form is <Turns_waiting>/abs(<Difference in Elo scores>)

    :param player1: BaseAgent
        The player who is being matched
    :param player2: (BaseAgent, int)
        The candidate player & turns waiting pair for a  match
    """
    elo_factor = 1/max(abs(player1.elo - player2_pair[0].elo), 1)
    turn_factor = max((self.num_turns - player2_pair[1]), 1)

    return elo_factor*turn_factor
```

#### Update player rankings (base_ladder.py)
```python
def update_players(self, winner, loser):
    """
    Update values for winner and loser.

    :param winner: BaseAgent
        Player who won
    :param loser: BaseAgent
        Player who lost
    """
    new_winner_elo = elo(winner, loser, 1, self.k_value)
    new_loser_elo = elo(loser, winner, 0, self.k_value)
    winner.elo = new_winner_elo
    winner.num_wins += 1
    loser.elo = new_loser_elo
    loser.num_losses += 1
```

#### Run a game (base_ladder.py)
```python
def run_game(self):
    """Match players and run a game."""
    player, opp = self.match_players()
    player_copy = deepcopy(player)
    opp_copy = deepcopy(opp)

    outcome = self.game_engine.run(player, opp)

    if outcome == 1:
        self.update_players(player, opp)
    else:
        self.update_players(opp, player)

    self.add_player(player)
    self.add_player(opp)

    return (outcome, player_copy, opp_copy)
```

&nbsp; 

### 2) Agents
 
 _Description of the "agents" in the system. Things to specify *if they apply*:_
 
* _List of agent-owned variables (e.g. age, heading, ID, etc.)_
* _List of agent-owned methods/procedures (e.g. move, consume, reproduce, die, etc.)_


```python
# Include first pass of the code you are thinking of using to construct your agents
# This may be a set of "turtle-own" variables and a command in the "setup" procedure, a list, an array, or Class constructor
# Feel free to include any agent methods/procedures you have so far. Filling in with pseudocode is ok! 
# NOTE: If using Netlogo, remove "python" from the markdown at the top of this section to get a generic code block
```

&nbsp; 

### 3) Action and Interaction 
 
**_Interaction Topology_**

_Description of the topology of who interacts with whom in the system. Perfectly mixed? Spatial proximity? Along a network? CA neighborhood?_
 
**_Action Sequence_**

_What does an agent, cell, etc. do on a given turn? Provide a step-by-step description of what happens on a given turn for each part of your model_

1. Step 1
2. Step 2
3. Etc...

&nbsp; 
### 4) Model Parameters and Initialization

_Describe and list any global parameters you will be applying in your model._

_Describe how your model will be initialized_

_Provide a high level, step-by-step description of your schedule during each "tick" of the model_

&nbsp; 

### 5) Assessment and Outcome Measures

_What quantitative metrics and/or qualitative features will you use to assess your model outcomes?_

&nbsp; 

### 6) Parameter Sweep

_What parameters are you most interested in sweeping through? What value ranges do you expect to look at for your analysis?_
