echo "Running tests..."

# 
echo "Running agent_test.py"
python -m tests.agent_test

echo "Running elo_test.py"
python -m tests.elo_test
