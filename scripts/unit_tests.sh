# Script to run unit test files

if [ "'$*'" != "''" ]; then
    # If arguments provided, use them
    while [ "$1" != "" ]; do
        dir_name="tests/$1"
        find $dir_name -iname '*.py' ! -name "__init__.py"  -exec python3 -m {} \;
        shift;
    done;
else 
    # Default to test all modules
    MODULES=("agent_tests" "engine_tests" "ladder_tests" "misc_tests")
    ./scripts/unit_tests.sh "${MODULES[@]}"
fi;