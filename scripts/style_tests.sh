# Script to run code style tests


if [ "'$*'" != "''" ]; then
    # If arguments provided, use them
    while [ "$1" != "" ]; do
        echo "Received: ${1}" && shift;
    done;
else 
    # Default to test all modules
    MODULES=("agent" "battle_engine" "interface" "ladder" "file_manager" "pokemon_helpers" "scripts" "simulation" "stats" "tests")
    ./scripts/style_tests.sh  "${MODULES[@]}"
fi;