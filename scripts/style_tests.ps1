# Script to run code style tests

$modules =  "agent", "battle_engine", "ladder", "simulation", "stats", "tests"

foreach ($module in $modules) {
    Write-Output "Module: $module"
    Write-Output "## pycodestyle"
    pycodestyle $module
    Write-Output "## pydocstyle"
    pydocstyle $module
    Write-Output "## pylint"
    pylint $module --rcfile pylintrc
    Write-Output ""
}
