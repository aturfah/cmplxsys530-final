# Script to run unit test files

if (!$args) {
    $tests = "agent_tests", "engine_tests", "ladder_tests", "misc_tests"
} else {
    $tests = $args
}


foreach ($test_batch in $tests) {
    $dir_name = "tests/" + $test_batch
    Get-ChildItem $dir_name -Filter *.py | ForEach-Object {
        Write-Output "Running $($test_batch)/$($_.Name)"
        python -m "tests.$($test_batch).$($_.BaseName)"
    }
    Write-Output ""
}
