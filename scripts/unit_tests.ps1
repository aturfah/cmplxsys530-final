Write-Output "Running tests..."

# Run Agent Tests
Write-Output "Running base_agent_test.py"
python -m tests.agent_tests.base_agent_test
Write-Output "Completed!"

Write-Output "Running rps_agent_test.py"
python -m tests.agent_tests.rps_agent_test
Write-Output "Completed!"

# Run tests on Basic Coin Flip Engine
Write-Output "Running coinflip_test.py"
python -m tests.engine_tests.coinflip_test
Write-Output "Completed!"

Write-Output "Running base_ladder_test.py"
python -m tests.ladder_tests.base_ladder_test
Write-Output "Completed!"

Write-Output "Running random_ladder_test.py"
python -m tests.ladder_tests.random_ladder_test
Write-Output "Completed!"

Write-Output "Running weighted_ladder_test.py"
python -m tests.ladder_tests.weighted_ladder_test
Write-Output "Completed!"

# Run tests on Elo calculations
Write-Output "Running elo_test.py"
python -m tests.misc_tests.elo_test
Write-Output "Completed!"
