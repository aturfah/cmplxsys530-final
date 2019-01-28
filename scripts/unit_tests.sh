# Script to run unit test files

if [ "'$*'" != "''" ]; then
    # If arguments provided, use them
    while [ "$1" != "" ]; do
        dir_name="tests/$1"
        files=$(find $dir_name -iname '*.py' ! -name "__init__.py");
        for file_name in $(echo $files | tr " " "\n");do
            temp_var=${file_name////.}
            temp_var=${temp_var/.py/ }
            python3 -m $temp_var
        done
        shift;
    done;
else 
    # Default to test all modules
    MODULES=("agent_tests" "engine_tests" "ladder_tests" "misc_tests")
    ./scripts/unit_tests.sh "${MODULES[@]}"
fi;