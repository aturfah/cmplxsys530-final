from agent.base_agent import Base_Agent

ba1 = Base_Agent()
ba1.hello()

ba1.num_wins = 50
print(ba1.win_loss_ratio())
ba1.num_losses = 12
print(ba1.win_loss_ratio())