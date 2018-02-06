# Script to run code style tests

$modules = "agent", "battle_engine", "ladder", "simulation", "stats", "tests"

foreach ($module in $modules) {
    echo "Module: $module"
    echo "## pycodestyle"
    pycodestyle $module
    echo "## pydocstyle"
    pydocstyle $module
    echo "## pylint"
    pylint $module -d R0903 -s n
    echo ""
}
