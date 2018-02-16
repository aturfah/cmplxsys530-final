# Script to run code style tests

if (!$args) {
    $modules =  "agent", "battle_engine", "ladder", "simulation", "stats", "tests", "log_manager"
} else {
    $modules = $args
}
    

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
