echo "Running tests..."

# Run Agent Tests
echo "Running agent_test.py"
python -m tests.base_agent_test
echo "Completed!"

# Run tests on Elo calculations
echo "Running elo_test.py"
python -m tests.elo_test
echo "Completed!"

# Run tests on Basic Coin Flip Engine
echo "Running coinflip_test.py"
python -m tests.coinflip_test
echo "Completed!"

echo "Running ladder_test.py"
python -m tests.ladder_test
echo "Completed!"

echo "Running rps_agemt_test.py"
python -m tests.rps_agent_test
echo "Completed!"