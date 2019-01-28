# Delete all log files
Remove-Item "logs\*.*" | Where-Object { ! $_.PSIsContainer }