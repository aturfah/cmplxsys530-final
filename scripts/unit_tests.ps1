Write-Output "Running tests..."

# Run Agent Tests
Write-Output "Running agent_test.py"
python -m tests.base_agent_test
Write-Output "Completed!"

# Run tests on Elo calculations
Write-Output "Running elo_test.py"
python -m tests.elo_test
Write-Output "Completed!"

# Run tests on Basic Coin Flip Engine
Write-Output "Running coinflip_test.py"
python -m tests.coinflip_test
Write-Output "Completed!"

Write-Output "Running base_ladder_test.py"
python -m tests.base_ladder_test
Write-Output "Completed!"

Write-Output "Running random_ladder_test.py"
python -m tests.random_ladder_test
Write-Output "Completed!"

Write-Output "Running weighted_ladder_test.py"
python -m tests.weighted_ladder_test
Write-Output "Completed!"

Write-Output "Running rps_agent_test.py"
python -m tests.rps_agent_test
Write-Output "Completed!"