# ACES W4b probe - run AS the agent identity, never as the owner. ASCII only.
# Every line is evidence; any ALLOWED on ev:create/overwrite/delete/rename means FAIL.

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$out = 'C:\ACES-Staging\audit\w4b-probe.txt'
$lines = New-Object System.Collections.Generic.List[string]
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$lines.Add('identity=' + $id.Name)

$priv = @((& "$env:SystemRoot\System32\whoami.exe" /priv) | ForEach-Object {
    if ($_ -match '^\s*(Se\w+Privilege)\s') { $matches[1] }
})
foreach ($p in 'SeRestorePrivilege', 'SeBackupPrivilege', 'SeTakeOwnershipPrivilege', 'SeSecurityPrivilege') {
    $lines.Add('priv:' + $p + '=' + $(if ($priv -contains $p) { 'PRESENT' } else { 'ABSENT' }))
}
try {
    $adm = @(Get-LocalGroupMember -SID 'S-1-5-32-544' -ErrorAction Stop |
        Where-Object { $_.Name -eq $id.Name })
    $lines.Add('administrators=' + $(if ($adm.Count) { 'MEMBER' } else { 'ABSENT' }))
} catch {
    $lines.Add('administrators=UNKNOWN')
}

function Try-Step([string]$name, [string]$target, [scriptblock]$action) {
    if ($target -and -not (Test-Path -LiteralPath $target)) {
        $lines.Add($name + '=N/A(target-absent)')
        return
    }
    try { & $action; $lines.Add($name + '=ALLOWED') }
    catch { $lines.Add($name + '=DENIED') }
}

$del = Join-Path $repo '_w4b-delete-probe.tmp'
$ren = Join-Path $repo '_w4b-rename-probe.tmp'

Try-Step 'ev:read' '' { [void][IO.File]::ReadAllText((Join-Path $repo '.claude\hooks\aces-hook-engine.mjs')) }
Try-Step 'ev:create' '' { [IO.File]::WriteAllText((Join-Path $repo '_w4b-created.tmp'), 'x') }
Try-Step 'ev:overwrite' $del { [IO.File]::WriteAllText($del, 'y') }
Try-Step 'ev:delete' $del { [IO.File]::Delete($del) }
Try-Step 'ev:rename' $ren { [IO.File]::Move($ren, (Join-Path $repo '_w4b-renamed.tmp')) }
Try-Step 'ev:staging' '' {
    New-Item -ItemType Directory -Force -Path 'C:\ACES-Staging\work' | Out-Null
    [IO.File]::WriteAllText('C:\ACES-Staging\work\w4b-probe.txt', 'x')
}

try {
    $spool = 'C:\ACES-Staging\audit\spool\journal.tsv'
    $before = @(Get-Content -LiteralPath $spool -ErrorAction SilentlyContinue).Count
    $req = '{"event":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"README.md","content":"x"}}'
    $req | & node (Join-Path $repo '.claude\hooks\aces-hook-engine.mjs') | Out-Null
    $after = @(Get-Content -LiteralPath $spool -ErrorAction SilentlyContinue).Count
    $lines.Add('ev:engine=RAN')
    $lines.Add('ev:spool-delta=' + ($after - $before))
} catch {
    $lines.Add('ev:engine=ERROR')
    $lines.Add('ev:spool-delta=0')
}

$lines | Set-Content -LiteralPath $out -Encoding ascii
Get-Content -LiteralPath $out
