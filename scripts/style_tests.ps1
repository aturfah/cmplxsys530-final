# Script to run code style tests

if (!$args) {
    $modules = "agent", "battle_engine", "interface", "ladder", "log_manager", "pokemon_helpers", "simulation", "stats", "tests"
}
else {
    $modules = $args
}
    

foreach ($module in $modules) {
    Write-Output "Module: $module"
    Write-Output "## pycodestyle"
    pycodestyle $module --max-line-length 100
    Write-Output "## pydocstyle"
    pydocstyle $module
    Write-Output "## pylint"
    pylint $module --rcfile pylintrc
    Write-Output ""
}
