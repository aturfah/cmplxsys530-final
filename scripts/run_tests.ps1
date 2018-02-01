echo "Running tests..."

# Run Agent Tests
echo "Running agent_test.py"
python -m tests.agent_test
echo "Completed!"

# Run tests on Elo calculations
echo "Running elo_test.py"
python -m tests.elo_test
echo "Completed!"

# Run tests on Basic Coin Flip Engine
echo "Running coinflip_test.py"
python -m tests.coinflip_test
echo "Completed!"