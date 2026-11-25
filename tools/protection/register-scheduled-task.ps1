# Registers the daily ACES-Snapshot scheduled task (DLPM-001).
# ASCII-only: the Cyrillic user path is built at runtime from the environment.
$script = Join-Path $env:USERPROFILE "aces-os\tools\protection\aces-snapshot.ps1"
$action  = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Daily -At "03:30"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries
Register-ScheduledTask -TaskName "ACES-Snapshot" -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Write-Output "ACES-Snapshot task registered: $script @ 03:30 daily"
