# Script to run unit test files

if [ "'$*'" != "''" ]; then
    # If arguments provided, use them
    while [ "$1" != "" ]; do
        echo "$1";
        shift;
    done;
else 
    # Default to test all modules
    MODULES=("agent_tests" "engine_tests" "ladder_tests" "misc_tests")
    ./scripts/unit_tests.sh "${MODULES[@]}"
fi;