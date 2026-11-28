# ACES W4b probe - runs AS the agent identity, never as the owner. ASCII only.
# Reads the request JSON, measures its own token by SID, attempts the four
# durable mutations, writes the report JSON.
# Exit: 0 = ISOLATED, 1 = NON_ISOLATED, 2 = INVALID (premise not met).

param(
    [Parameter(Mandatory = $true)][string]$RequestFile,
    [Parameter(Mandatory = $true)][string]$ReportFile
)

$ErrorActionPreference = 'Continue'
$req = Get-Content -LiteralPath $RequestFile -Raw | ConvertFrom-Json

function Try-Attempt([scriptblock]$Action) {
    try { & $Action; return 'ALLOWED' } catch { return 'DENIED' }
}

$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$sid = $id.User.Value
$name = $id.Name
$groupSids = @($id.Groups | ForEach-Object { $_.Value })
$adminGroup = ($groupSids -contains 'S-1-5-32-544')
$integrity = 'UNKNOWN'
try {
    foreach ($line in @(& "$env:SystemRoot\System32\whoami.exe" /groups 2>$null)) {
        if ($line -match 'S-1-16-(\d+)') { $integrity = 'S-1-16-' + $matches[1]; break }
    }
} catch {}
$principal = New-Object Security.Principal.WindowsPrincipal($id)
$elevated = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

$priv = [ordered]@{}
$privOut = @(& "$env:SystemRoot\System32\whoami.exe" /priv 2>$null)
foreach ($p in 'SeRestorePrivilege', 'SeBackupPrivilege', 'SeTakeOwnershipPrivilege', 'SeSecurityPrivilege', 'SeDebugPrivilege') {
    $priv[$p] = $(if (@($privOut -match ('\b' + $p + '\b')).Count) { 'PRESENT' } else { 'ABSENT' })
}

$prem = [ordered]@{
    overwrite = (Test-Path -LiteralPath $req.paths.overwrite)
    delete = (Test-Path -LiteralPath $req.paths.delete)
    rename = (Test-Path -LiteralPath $req.paths.rename)
    engine = (Test-Path -LiteralPath $req.engine)
}

$attempts = [ordered]@{}
$attempts.create = $(if (Test-Path -LiteralPath $req.paths.create) { 'PREMISE_FAILED' } else {
    Try-Attempt { [IO.File]::WriteAllText($req.paths.create, 'created') } })
$attempts.overwrite = $(if ($prem.overwrite) {
    Try-Attempt { [IO.File]::WriteAllText($req.paths.overwrite, 'TAMPERED') } } else { 'PREMISE_FAILED' })
$attempts.delete = $(if ($prem.delete) {
    Try-Attempt { [IO.File]::Delete($req.paths.delete) } } else { 'PREMISE_FAILED' })
$attempts.rename = $(if ($prem.rename) {
    Try-Attempt { [IO.File]::Move($req.paths.rename, $req.paths.rename_to) } } else { 'PREMISE_FAILED' })

$staging = [ordered]@{ write = 'DENIED'; read = 'DENIED'; delete = 'DENIED' }
$stagingFile = Join-Path $req.staging_root 'ok.txt'
try {
    [IO.File]::WriteAllText($stagingFile, 'ok')
    $staging.write = 'ALLOWED'
    if ([IO.File]::ReadAllText($stagingFile) -eq 'ok') { $staging.read = 'ALLOWED' }
    [IO.File]::Delete($stagingFile)
    if (-not (Test-Path -LiteralPath $stagingFile)) { $staging.delete = 'ALLOWED' }
} catch {}

$engine = [ordered]@{ ran = $false; exit = -1; canonical_delta = -1; spool_delta = -1 }
if ($prem.engine) {
    $beforeCanon = @(Get-Content -LiteralPath $req.canonical -ErrorAction SilentlyContinue).Count
    $beforeSpool = @(Get-Content -LiteralPath $req.spool -ErrorAction SilentlyContinue).Count
    $env:ACES_HOOK_JOURNAL = $req.canonical
    $env:ACES_HOOK_SPOOL = $req.spool
    $env:ACES_WA_MODE = 'enforce'
    $payload = [ordered]@{
        event = 'PreToolUse'
        tool_name = 'Write'
        tool_input = [ordered]@{
            file_path = (Join-Path $req.target_root '_w4b_engine_probe.tmp')
            content = 'x'
        }
    } | ConvertTo-Json -Depth 4 -Compress
    try {
        $payload | & node $req.engine 2>$null | Out-Null
        $engine.exit = $LASTEXITCODE
        $engine.ran = $true
    } catch {}
    if ($engine.ran) {
        $afterCanon = @(Get-Content -LiteralPath $req.canonical -ErrorAction SilentlyContinue).Count
        $afterSpool = @(Get-Content -LiteralPath $req.spool -ErrorAction SilentlyContinue).Count
        $engine.canonical_delta = $afterCanon - $beforeCanon
        $engine.spool_delta = $afterSpool - $beforeSpool
    }
}

$effects = [ordered]@{
    create_absent = -not (Test-Path -LiteralPath $req.paths.create)
    overwrite_changed = $false
    delete_present = (Test-Path -LiteralPath $req.paths.delete)
    rename_old_present = (Test-Path -LiteralPath $req.paths.rename)
    rename_new_present = (Test-Path -LiteralPath $req.paths.rename_to)
}
if (Test-Path -LiteralPath $req.paths.overwrite) {
    $effects.overwrite_changed = ((Get-Content -LiteralPath $req.paths.overwrite -Raw).Trim() -eq 'TAMPERED')
}

$identityMatch = ($sid -eq $req.expected_sid)
$procOwner = 'UNKNOWN'
$parentPid = -1
try {
    $proc = Get-CimInstance Win32_Process -Filter ("ProcessId=" + $PID) -ErrorAction Stop
    $parentPid = $proc.ParentProcessId
    $own = Invoke-CimMethod -InputObject $proc -MethodName GetOwnerSid -ErrorAction Stop
    if ($own.Sid) { $procOwner = $own.Sid }
} catch {}

$denied = $true
foreach ($k in 'create', 'overwrite', 'delete', 'rename') {
    if ($attempts[$k] -ne 'DENIED') { $denied = $false }
}
if (-not $premOk) { $denied = $false }

$privClean = $true
foreach ($p in 'SeRestorePrivilege', 'SeBackupPrivilege', 'SeTakeOwnershipPrivilege', 'SeSecurityPrivilege', 'SeDebugPrivilege') {
    if ($priv[$p] -ne 'ABSENT') { $privClean = $false }
}

$verdict = 'NON_ISOLATED'
$code = 1
if (-not ($prem.overwrite -and $prem.delete -and $prem.rename)) {
    $verdict = 'INVALID'
    $code = 2
} elseif ($identityMatch -and (-not $adminGroup) -and (-not $elevated) -and
    ($integrity -match '^S-1-16-(4096|8192|8448)$') -and $privClean -and $denied) {
    $verdict = 'ISOLATED'
    $code = 0
}

if ($req.mode -eq 'selfcheck') {
    foreach ($p in @($req.paths.create, $req.paths.rename_to)) {
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue }
    }
}

$report = [ordered]@{
    nonce = $req.nonce
    mode = $req.mode
    probe_sha256 = $req.probe_sha256
    pid = $PID
    started_utc = $req.started_utc
    finished_utc = (Get-Date).ToUniversalTime().ToString('o')
    token = [ordered]@{
        sid = $sid
        name = $name
        integrity = $integrity
        elevated = $elevated
        admin_group = $adminGroup
    }
    process = [ordered]@{
        owner_sid = $procOwner
        parent_pid = $parentPid
    }
    privileges = $priv
    premises = $prem
    attempts = $attempts
    staging = $staging
    effects = $effects
    engine = $engine
    identity_match = $identityMatch
    verdict = $verdict
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportFile -Encoding UTF8
$report | ConvertTo-Json -Depth 8
exit $code
