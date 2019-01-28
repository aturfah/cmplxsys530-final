# Script to run code style tests

if [ "'$*'" != "''" ]; then
    # If arguments provided, use them
    while [ "$1" != "" ]; do
        echo "Module: ${1}";
        echo "## pycodestyle";
        pycodestyle ${1} --max-line-length 100
        echo "## pydocstyle";
        pydocstyle ${1}
        echo "## pylint";
        pylint ${1} --rcfile pylintrc
        echo ""
        shift;
    done;
else 
    # Default to test all modules
    MODULES=("agent" "battle_engine" "interface" "ladder" "file_manager" "pokemon_helpers" "scripts" "simulation" "stats" "tests")
    ./scripts/style_tests.sh "${MODULES[@]}"
fi;