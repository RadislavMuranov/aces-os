# ACES W4b - identity boundary for WA-1 (DLPM-002). ASCII only.
# -Status   read only: account, ACLs, backups, last verdict
# -SelfCheck read only durable zones: ACL roundtrip and detector negative
# -Apply    elevated: create agent, back up ACLs, restrict durable zones
# -Verify   elevated: run the probe AS the agent, then check post state yourself
# -Rollback elevated: restore saved ACLs, delete the agent, verify
# -RollbackCodex elevated: restore the Vault ACL saved before the Codex deny
# -Codex    elevated: deny the Codex group write on the Vault (already applied)

param(
    [string]$Repo,
    [string]$Vault = (Join-Path $env:USERPROFILE 'Documents\Obsidian Vault'),
    [string]$Stage = 'C:\ACES-Staging',
    [string]$AgentName = 'aces-agent',
    [string]$CodexGroup = 'CodexSandboxUsers',
    [switch]$Apply,
    [switch]$Verify,
    [switch]$Rollback,
    [switch]$RollbackCodex,
    [switch]$SelfCheck
)

$ErrorActionPreference = 'Stop'
if (-not $Repo) { $Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path }
$Repo = (Resolve-Path -LiteralPath $Repo).Path
$Vault = (Resolve-Path -LiteralPath $Vault).Path
$Agent = "$env:COMPUTERNAME\$AgentName"
$BackupDir = Join-Path $Repo 'tools\protection\acl-backup'
$VerifyRoot = Join-Path $Stage 'verify'
$Spool = Join-Path $Stage 'audit\spool'
$WriteMask = 'WD,AD,WEA,WA,DE,DC,WDAC,WO'
$SystemSid = 'S-1-5-18'
$AdminsSid = 'S-1-5-32-544'
$UsersSid = 'S-1-5-32-545'
$BackupOpsSid = 'S-1-5-32-551'

function Test-Admin {
    $w = New-Object Security.Principal.WindowsPrincipal(
        [Security.Principal.WindowsIdentity]::GetCurrent())
    $w.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Get-SidValue([string]$Name) {
    (New-Object Security.Principal.NTAccount($Name)).Translate(
        [Security.Principal.SecurityIdentifier]).Value
}

function Get-AclText([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'absent' }
    $a = Get-Acl -LiteralPath $Path
    $out = @('protected=' + $a.AreAccessRulesProtected)
    foreach ($x in $a.Access) {
        $s = '?'
        try { $s = $x.IdentityReference.Translate(
            [Security.Principal.SecurityIdentifier]).Value } catch {}
        $out += ($x.AccessControlType.ToString() + '|' + $s + '|' +
            [string]$x.FileSystemRights + '|' + $x.IsInherited)
    }
    ($out | Sort-Object) -join "`n"
}

function Get-AclHash([string]$Path) {
    $sha = [Security.Cryptography.SHA256]::Create()
    $b = [Text.Encoding]::UTF8.GetBytes((Get-AclText $Path))
    ([BitConverter]::ToString($sha.ComputeHash($b))).Replace('-', '')
}

function Test-Ace([string]$Path, [string]$SidValue, [string]$Type) {
    $acl = Get-Acl -LiteralPath $Path
    foreach ($x in $acl.Access) {
        $s = ''
        try { $s = $x.IdentityReference.Translate(
            [Security.Principal.SecurityIdentifier]).Value } catch {}
        if ($x.AccessControlType.ToString() -eq $Type -and $s -eq $SidValue) { return $true }
    }
    $false
}

function Show-Acl([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { 'absent ' + $Path; return }
    $a = Get-Acl -LiteralPath $Path
    'protected=' + $a.AreAccessRulesProtected + ' owner=' + $a.Owner
    foreach ($x in $a.Access) {
        $s = '?'
        try { $s = $x.IdentityReference.Translate(
            [Security.Principal.SecurityIdentifier]).Value } catch {}
        $x.AccessControlType.ToString() + ' ' + $s + ' ' +
            [string]$x.FileSystemRights + ' inh=' + $x.IsInherited
    }
}

function Assert-Targets {
    if (-not (Test-Path -LiteralPath (Join-Path $Repo '.git'))) {
        throw ('not a repo root: ' + $Repo)
    }
    if (-not (Test-Path -LiteralPath (Join-Path $Repo '.claude\hooks\aces-hook-engine.mjs'))) {
        throw ('engine missing under ' + $Repo)
    }
    foreach ($p in @($Repo, $Vault)) {
        if ($p.TrimEnd('\') -eq [IO.Path]::GetPathRoot($p).TrimEnd('\')) {
            throw ('refusing drive root: ' + $p)
        }
    }
}

function Save-Sddl([string]$Path, [string]$Name) {
    if (-not (Test-Path -LiteralPath $BackupDir)) {
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    }
    $sddlFile = Join-Path $BackupDir ($Name + '.pre-w4b.sddl')
    $hashFile = Join-Path $BackupDir ($Name + '.pre-w4b.sha256')
    if (Test-Path -LiteralPath $sddlFile) { return $sddlFile }
    Set-Content -LiteralPath $sddlFile -Value (Get-Acl -LiteralPath $Path).Sddl -Encoding ascii
    Set-Content -LiteralPath $hashFile -Value (Get-AclHash $Path) -Encoding ascii
    $sddlFile
}

function Restore-Sddl([string]$Path, [string]$Name) {
    $sddlFile = Join-Path $BackupDir ($Name + '.pre-w4b.sddl')
    $hashFile = Join-Path $BackupDir ($Name + '.pre-w4b.sha256')
    if (-not (Test-Path -LiteralPath $sddlFile)) { return $false }
    if (-not (Test-Path -LiteralPath $hashFile)) { return $false }
    $expected = (Get-Content -LiteralPath $hashFile -Raw).Trim()
    $sddl = (Get-Content -LiteralPath $sddlFile -Raw).Trim()
    $sd = New-Object System.Security.AccessControl.DirectorySecurity
    $sd.SetSecurityDescriptorSddlForm($sddl)
    Set-Acl -LiteralPath $Path -AclObject $sd
    ((Get-AclHash $Path) -eq $expected)
}

function Test-StageRestored {
    $hashFile = Join-Path $BackupDir 'stage.pre-w4b.sha256'
    if (-not (Test-Path -LiteralPath $hashFile)) { return $false }
    $expected = (Get-Content -LiteralPath $hashFile -Raw).Trim()
    ((Get-AclHash $Stage) -eq $expected)
}

function Set-ZoneAcl([string]$Path, [string]$AgentSidValue, [string]$AgentRights) {
    $ownerSid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $null = & icacls $Path /inheritance:r
    if ($LASTEXITCODE -ne 0) { throw ('inheritance failed: ' + $Path) }
    $null = & icacls $Path /grant:r "*${SystemSid}:(OI)(CI)F" "*${AdminsSid}:(OI)(CI)F" `
        "*${ownerSid}:(OI)(CI)F" "*${AgentSidValue}:(OI)(CI)$AgentRights"
    if ($LASTEXITCODE -ne 0) { throw ('grant failed: ' + $Path) }
}

function Set-AgentDeny([string]$Path, [string]$AgentSidValue) {
    $null = & icacls $Path /deny "*${AgentSidValue}:(OI)(CI)($WriteMask)"
    if ($LASTEXITCODE -ne 0) { throw ('deny failed: ' + $Path) }
}

function Set-GroupDeny([string]$Path, [string]$GroupSidValue) {
    $null = & icacls $Path /deny "*${GroupSidValue}:(OI)(CI)($WriteMask)"
    if ($LASTEXITCODE -ne 0) { throw ('group deny failed: ' + $Path) }
}

function Get-BuildHash {
    $probe = Join-Path $PSScriptRoot 'w4b-probe.ps1'
    $a = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
    $b = (Get-FileHash -LiteralPath $probe -Algorithm SHA256).Hash
    'boundary=' + $a + ';probe=' + $b
}

function Get-AgentState {
    $u = Get-LocalUser -Name $AgentName -ErrorAction SilentlyContinue
    if (-not $u) { return [ordered]@{ present = $false } }
    $sid = $u.SID.Value
    $admins = @(Get-LocalGroupMember -SID $AdminsSid -ErrorAction SilentlyContinue |
        Where-Object { $_.SID.Value -eq $sid })
    $backup = @(Get-LocalGroupMember -SID $BackupOpsSid -ErrorAction SilentlyContinue |
        Where-Object { $_.SID.Value -eq $sid })
    [ordered]@{
        present = $true
        name = $u.Name
        sid = $sid
        enabled = $u.Enabled
        admins = ($admins.Count -gt 0)
        backup = ($backup.Count -gt 0)
    }
}

function Show-AgentAce([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'absent' }
    $st = Get-AgentState
    if (-not $st.present) { return 'agent-absent' }
    $acl = Get-Acl -LiteralPath $Path
    $rows = @($acl.Access | Where-Object {
        try { $_.IdentityReference.Translate(
            [Security.Principal.SecurityIdentifier]).Value -eq $st.sid } catch { $false }
    })
    if (-not $rows.Count) { return 'no-ace' }
    (($rows | ForEach-Object {
        $_.AccessControlType.ToString() + ':' + [string]$_.FileSystemRights
    }) -join ',')
}

function Get-CodexDeny([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'absent' }
    $codexSid = $null
    try { $codexSid = Get-SidValue "$env:COMPUTERNAME\$CodexGroup" } catch { return 'n/a' }
    $acl = Get-Acl -LiteralPath $Path
    @($acl.Access | Where-Object {
        $_.AccessControlType -eq 'Deny' -and
        $_.IdentityReference.Translate(
            [Security.Principal.SecurityIdentifier]).Value -eq $codexSid
    }).Count
}

function Show-Status {
    'identity=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name
    'elevated=' + (Test-Admin)
    'build=' + (Get-BuildHash)
    $st = Get-AgentState
    'agent.present=' + $st.present
    if ($st.present) {
        'agent.sid=' + $st.sid
        'agent.enabled=' + $st.enabled
        'agent.admins=' + $st.admins
        'agent.backupops=' + $st.backup
    }
    foreach ($z in @(@('repo', $Repo), @('vault', $Vault), @('stage', $Stage))) {
        '--- zone ' + $z[0] + ' ---'
        Show-Acl $z[1]
        'agent.ace=' + (Show-AgentAce $z[1])
        'aclhash=' + (Get-AclHash $z[1])
        if ($z[0] -ne 'repo') { 'codex.deny.count=' + (Get-CodexDeny $z[1]) }
        'backup.' + $z[0] + '=' + (Test-Path -LiteralPath (Join-Path $BackupDir ($z[0] + '.pre-w4b.sddl')))
    }
    $last = @(Get-ChildItem -LiteralPath $VerifyRoot -Filter 'report.json' -Recurse -File -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1)
    if ($last.Count) {
        $r = Get-Content -LiteralPath $last[0].FullName -Raw | ConvertFrom-Json
        'last.verdict=' + $r.verdict
        'last.nonce=' + $r.nonce
        'last.started=' + $r.started_utc
        'last.build=' + $r.build
        $same = ($r.verdict -eq 'PASS') -and
            ($r.build -eq (Get-BuildHash)) -and
            ($r.acl_after.repo -eq (Get-AclHash $Repo)) -and
            ($r.acl_after.vault -eq (Get-AclHash $Vault)) -and
            ($r.acl_after.stage -eq (Get-AclHash $Stage))
        if ($same) { 'BOUNDARY=ENFORCED_AS_OF ' + $r.started_utc } else { 'BOUNDARY=ADVISORY' }
    } else {
        'last.verdict=none'
        'BOUNDARY=ADVISORY'
    }
}

function Invoke-Apply {
    if (-not (Test-Admin)) { throw 'elevated PowerShell required' }
    Assert-Targets
    $answer = Read-Host 'Type APPLY to restrict the durable zones'
    if ($answer -ne 'APPLY') { 'aborted'; return }

    $st = Get-AgentState
    if (-not $st.present) {
        & net.exe user $AgentName '*' /add
        if ($LASTEXITCODE -ne 0) { throw 'net user failed' }
        'account: created'
        $st = Get-AgentState
    }
    if (-not $st.present) { throw 'account missing after create' }
    'agent.sid=' + $st.sid
    if ($st.admins) { throw 'agent is in Administrators; abort' }
    if ($st.backup) { throw 'agent is in Backup Operators; abort' }
    if (-not $st.enabled) { throw 'agent is disabled; abort' }

    $member = @(Get-LocalGroupMember -SID $UsersSid -ErrorAction SilentlyContinue |
        Where-Object { $_.SID.Value -eq $st.sid })
    if (-not $member.Count) {
        Add-LocalGroupMember -SID $UsersSid -Member $AgentName
        'agent: added to Users'
    }

    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    New-Item -ItemType Directory -Force -Path $VerifyRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $Spool | Out-Null
    $null = & icacls $VerifyRoot /grant "${Agent}:(OI)(CI)M"
    $null = & icacls $Spool /grant "${Agent}:(OI)(CI)M"

    $bRepo = Save-Sddl $Repo 'repo'
    $bVault = Save-Sddl $Vault 'vault'
    $bStage = Save-Sddl $Stage 'stage'
    'backup.repo=' + $bRepo + ' sha256=' + ((Get-Content -LiteralPath (Join-Path $BackupDir 'repo.pre-w4b.sha256') -Raw).Trim())
    'backup.vault=' + $bVault + ' sha256=' + ((Get-Content -LiteralPath (Join-Path $BackupDir 'vault.pre-w4b.sha256') -Raw).Trim())
    'backup.stage=' + $bStage + ' sha256=' + ((Get-Content -LiteralPath (Join-Path $BackupDir 'stage.pre-w4b.sha256') -Raw).Trim())

    # The staging root is not modified: the agent already has inherited write
    # access there, and the backup store now lives in the repository instead.
    Set-ZoneAcl $Repo $st.sid 'RX'
    Set-AgentDeny $Repo $st.sid
    Set-ZoneAcl $Vault $st.sid 'RX'
    Set-AgentDeny $Vault $st.sid

    $codexSid = $null
    try { $codexSid = Get-SidValue "$env:COMPUTERNAME\$CodexGroup" } catch {}
    if ($codexSid -and -not (Get-CodexDeny $Vault)) {
        Set-GroupDeny $Vault $codexSid
        'codex.deny=' + $codexSid
    }

    '--- repo ---'
    Show-Acl $Repo
    '--- vault ---'
    Show-Acl $Vault
    '--- stage ---'
    Show-Acl $Stage
    'BOUNDARY=UNVERIFIED'
    'next=-Verify'
}

function Invoke-Rollback {
    if (-not (Test-Admin)) { throw 'elevated PowerShell required' }
    $answer = Read-Host 'Type ROLLBACK to restore the saved ACLs and delete the agent'
    if ($answer -ne 'ROLLBACK') { 'aborted'; return }

    $res = @()
    $res += [pscustomobject]@{ zone = 'repo'; ok = (Restore-Sddl $Repo 'repo') }
    $res += [pscustomobject]@{ zone = 'vault'; ok = (Restore-Sddl $Vault 'vault') }
    $res += [pscustomobject]@{ zone = 'stage'; ok = (Test-StageRestored) }
    foreach ($r in $res) { $(if ($r.ok) { 'PASS' } else { 'FAIL' }) + ' restore ' + $r.zone }
    $bad = @($res | Where-Object { -not $_.ok })
    if ($bad.Count) { 'ROLLBACK=FAIL'; 'account kept for retry'; exit 1 }

    $st = Get-AgentState
    if ($st.present) {
        $null = & icacls $VerifyRoot /remove:g $Agent /T /C /Q 2>$null
        $null = & icacls $Spool /remove:g $Agent /T /C /Q 2>$null
        $left = 0
        foreach ($t in @($VerifyRoot, $Spool)) {
            if (Test-Ace $t $st.sid 'Allow') { $left++ }
            if (Test-Ace $t $st.sid 'Deny') { $left++ }
        }
        'tool.aces.left=' + $left
        if ($left) { 'ROLLBACK=FAIL'; 'account kept: stale ACEs in staging'; exit 1 }
        & net.exe user $AgentName /delete
        if ($LASTEXITCODE -ne 0) { 'ROLLBACK=FAIL delete'; exit 1 }
    }
    $gone = -not (Get-LocalUser -Name $AgentName -ErrorAction SilentlyContinue)
    'agent.absent=' + $gone
    foreach ($f in @(Get-ChildItem -LiteralPath $Repo -Filter '_w4b_*' -File -ErrorAction SilentlyContinue)) {
        Remove-Item -LiteralPath $f.FullName -Force -ErrorAction SilentlyContinue
        'removed=' + $f.Name
    }
    'ROLLBACK=' + $(if ($gone) { 'PASS' } else { 'FAIL' })
    'kept=' + $Stage
}

function Invoke-RollbackCodex {
    if (-not (Test-Admin)) { throw 'elevated PowerShell required' }
    $file = Join-Path $BackupDir 'vault-pre-codex.sddl'
    if (-not (Test-Path -LiteralPath $file)) { $file = Join-Path $Stage 'acl-backup\vault-pre-codex.sddl' }
    if (-not (Test-Path -LiteralPath $file)) { throw ('no backup ' + $file) }
    $answer = Read-Host 'Type CODEX to restore the Vault ACL saved before the Codex deny'
    if ($answer -ne 'CODEX') { 'aborted'; return }
    $sddl = (Get-Content -LiteralPath $file -Raw).Trim()
    $sd = New-Object System.Security.AccessControl.DirectorySecurity
    $sd.SetSecurityDescriptorSddlForm($sddl)
    Set-Acl -LiteralPath $Vault -AclObject $sd
    'sddl.equal=' + ((Get-Acl -LiteralPath $Vault).Sddl -eq $sddl)
    'codex.deny.count=' + (Get-CodexDeny $Vault)
    Show-Acl $Vault
}


function Invoke-Verify {
    if (-not (Test-Admin)) { throw 'elevated PowerShell required' }
    Assert-Targets
    $st = Get-AgentState
    if (-not $st.present) { throw 'agent absent; run -Apply' }
    if ($st.admins) { throw 'agent is an administrator' }
    if ($st.backup) { throw 'agent is in Backup Operators' }
    if (-not $st.enabled) { throw 'agent is disabled' }

    $aRepo = Show-AgentAce $Repo
    $aVault = Show-AgentAce $Vault
    $aStage = Show-AgentAce $Stage
    if ($aRepo -notmatch 'Deny') { throw ('repo deny missing: ' + $aRepo) }
    if ($aVault -notmatch 'Deny') { throw ('vault deny missing: ' + $aVault) }
    if ($aStage -match 'Deny') { throw ('stage must not deny: ' + $aStage) }

    $probeSrc = Join-Path $PSScriptRoot 'w4b-probe.ps1'
    $runner = $probeSrc
    $runnerHash = (Get-FileHash -LiteralPath $runner -Algorithm SHA256).Hash

    $nonce = [guid]::NewGuid().ToString('N')
    $caseDir = Join-Path $VerifyRoot ('w4b-' + $nonce)
    New-Item -ItemType Directory -Force -Path $caseDir | Out-Null
    $reqFile = Join-Path $caseDir 'request.json'
    $repFile = Join-Path $caseDir 'agent-report.json'
    $ownerRep = Join-Path $BackupDir ('verify-' + $nonce + '.json')

    $pCreate = Join-Path $Repo ('_w4b_' + $nonce + '_create.tmp')
    $pOver = Join-Path $Repo ('_w4b_' + $nonce + '_overwrite.tmp')
    $pDelete = Join-Path $Repo ('_w4b_' + $nonce + '_delete.tmp')
    $pRename = Join-Path $Repo ('_w4b_' + $nonce + '_rename.tmp')
    $pRenTo = Join-Path $Repo ('_w4b_' + $nonce + '_renamed.tmp')
    foreach ($p in @($pCreate, $pRenTo)) {
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force }
    }
    Set-Content -LiteralPath $pOver -Value 'ORIGINAL' -Encoding ascii
    Set-Content -LiteralPath $pDelete -Value 'KEEP' -Encoding ascii
    Set-Content -LiteralPath $pRename -Value 'KEEP' -Encoding ascii

    $overHash = (Get-FileHash -LiteralPath $pOver -Algorithm SHA256).Hash
    $canonical = Join-Path $Repo '.claude\hooks\journal.tsv'
    $spool = Join-Path $Stage 'audit\spool\journal.tsv'
    $canonHash = (Get-FileHash -LiteralPath $canonical -Algorithm SHA256).Hash
    $spoolCount = @(Get-Content -LiteralPath $spool -ErrorAction SilentlyContinue).Count
    $aclRepo = Get-AclHash $Repo
    $aclVault = Get-AclHash $Vault
    $aclStage = Get-AclHash $Stage

    $request = [ordered]@{
        nonce = $nonce
        mode = 'verify'
        expected_sid = $st.sid
        expected_name = $Agent
        target_root = $Repo
        staging_root = $caseDir
        engine = (Join-Path $Repo '.claude\hooks\aces-hook-engine.mjs')
        canonical = $canonical
        spool = $spool
        probe_sha256 = $runnerHash
        started_utc = (Get-Date).ToUniversalTime().ToString('o')
        paths = [ordered]@{
            create = $pCreate
            overwrite = $pOver
            delete = $pDelete
            rename = $pRename
            rename_to = $pRenTo
        }
    }
    $request | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reqFile -Encoding UTF8
    'runner.sha256=' + $runnerHash

    $argLine = '-NoProfile -ExecutionPolicy Bypass -File "' + $runner + '" -RequestFile "' + $reqFile + '" -ReportFile "' + $repFile + '"'
    try {
        $cred = Get-Credential -UserName $Agent -Message 'Password for the agent identity'
        if (-not $cred) { throw 'no credential' }
        Start-Process -FilePath 'powershell.exe' -Credential $cred -ArgumentList $argLine -WindowStyle Hidden -Wait | Out-Null
        'launch=Start-Process'
    } catch {
        'launch=runas-fallback'
        $short = $runner
        try {
            $fso = New-Object -ComObject Scripting.FileSystemObject
            $short = $fso.GetFile($runner).ShortPath
        } catch {}
        $cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -File ' + $short + ' -RequestFile ' + $reqFile + ' -ReportFile ' + $repFile
        & cmd.exe /c ('runas /user:' + $Agent + ' "' + $cmd + '"')
    }

    $deadline = (Get-Date).AddSeconds(180)
    while (-not (Test-Path -LiteralPath $repFile) -and (Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 500
    }

    $postCreate = Test-Path -LiteralPath $pCreate
    $postOverText = ''
    if (Test-Path -LiteralPath $pOver) { $postOverText = (Get-Content -LiteralPath $pOver -Raw).Trim() }
    $postOverHash = ''
    if (Test-Path -LiteralPath $pOver) { $postOverHash = (Get-FileHash -LiteralPath $pOver -Algorithm SHA256).Hash }
    $postDelete = Test-Path -LiteralPath $pDelete
    $postRenameOld = Test-Path -LiteralPath $pRename
    $postRenameNew = Test-Path -LiteralPath $pRenTo
    $postCanonHash = (Get-FileHash -LiteralPath $canonical -Algorithm SHA256).Hash
    $postSpoolCount = @(Get-Content -LiteralPath $spool -ErrorAction SilentlyContinue).Count

    $rep = $null
    if (Test-Path -LiteralPath $repFile) {
        try { $rep = Get-Content -LiteralPath $repFile -Raw | ConvertFrom-Json } catch { $rep = $null }
    }

    $C = New-Object System.Collections.Generic.List[object]
    $add = { param($n, $ok, $d)
        $C.Add([pscustomobject]@{ name = $n; ok = [bool]$ok; detail = [string]$d }) }

    & $add 'report.present' ($null -ne $rep) $repFile
    & $add 'post.create_absent' (-not $postCreate) ([string]$postCreate)
    & $add 'post.overwrite_unchanged' (($postOverHash -eq $overHash) -and ($postOverText -eq 'ORIGINAL')) $postOverHash
    & $add 'post.delete_present' ($postDelete) ([string]$postDelete)
    & $add 'post.rename_old_present' ($postRenameOld) ([string]$postRenameOld)
    & $add 'post.rename_new_absent' (-not $postRenameNew) ([string]$postRenameNew)
    & $add 'post.canonical_unchanged' ($postCanonHash -eq $canonHash) $postCanonHash.Substring(0, 16)
    & $add 'post.spool_grew' (($postSpoolCount - $spoolCount) -ge 1) ([string]($postSpoolCount - $spoolCount))
    & $add 'post.acl_repo_unchanged' ((Get-AclHash $Repo) -eq $aclRepo) 'hash'
    & $add 'post.acl_vault_unchanged' ((Get-AclHash $Vault) -eq $aclVault) 'hash'
    & $add 'post.acl_stage_unchanged' ((Get-AclHash $Stage) -eq $aclStage) 'hash'

    if ($rep) {
        & $add 'report.nonce' ($rep.nonce -eq $nonce) ([string]$rep.nonce)
        & $add 'report.probe_sha256' ($rep.probe_sha256 -eq $runnerHash) ([string]$rep.probe_sha256)
        & $add 'report.token_sid' ($rep.token.sid -eq $st.sid) ([string]$rep.token.sid)
        & $add 'report.owner_sid' ($rep.process.owner_sid -eq $st.sid) ([string]$rep.process.owner_sid)
        & $add 'report.not_elevated' ($rep.token.elevated -eq $false) ([string]$rep.token.elevated)
        & $add 'report.no_admin_group' ($rep.token.admin_group -eq $false) ([string]$rep.token.admin_group)
        & $add 'report.integrity' ($rep.token.integrity -match '^S-1-16-(4096|8192|8448)$') ([string]$rep.token.integrity)
        foreach ($p in 'SeRestorePrivilege', 'SeBackupPrivilege', 'SeTakeOwnershipPrivilege', 'SeSecurityPrivilege', 'SeDebugPrivilege') {
            & $add ('report.priv.' + $p) ($rep.privileges.$p -eq 'ABSENT') ([string]$rep.privileges.$p)
        }
        foreach ($k in 'overwrite', 'delete', 'rename') {
            & $add ('report.premise.' + $k) ($rep.premises.$k -eq $true) ([string]$rep.premises.$k)
        }
        foreach ($k in 'create', 'overwrite', 'delete', 'rename') {
            & $add ('report.attempt.' + $k) ($rep.attempts.$k -eq 'DENIED') ([string]$rep.attempts.$k)
        }
        foreach ($k in 'write', 'read', 'delete') {
            & $add ('report.staging.' + $k) ($rep.staging.$k -eq 'ALLOWED') ([string]$rep.staging.$k)
        }
        & $add 'report.engine.ran' ($rep.engine.ran -eq $true) ([string]$rep.engine.ran)
        & $add 'report.engine.canonical_delta' ($rep.engine.canonical_delta -eq 0) ([string]$rep.engine.canonical_delta)
        & $add 'report.engine.spool_delta' ($rep.engine.spool_delta -ge 1) ([string]$rep.engine.spool_delta)
    }

    $fail = @($C | Where-Object { -not $_.ok })
    foreach ($x in $C) {
        $(if ($x.ok) { 'PASS' } else { 'FAIL' }) + ' ' + $x.name + ' :: ' + $x.detail
    }
    $verdict = $(if ($fail.Count) { 'FAIL' } else { 'PASS' })
    'W4B=' + $verdict
    if ($verdict -eq 'PASS') {
        'BOUNDARY=ENFORCED_AS_OF ' + (Get-Date).ToUniversalTime().ToString('o')
        foreach ($p in @($pOver, $pDelete, $pRename, $pRenTo)) {
            if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue }
        }
    } else {
        'BOUNDARY=ADVISORY'
        'kept=' + $Repo
    }

    $out = [ordered]@{
        started_utc = $request.started_utc
        finished_utc = (Get-Date).ToUniversalTime().ToString('o')
        nonce = $nonce
        build = (Get-BuildHash)
        verdict = $verdict
        agent = $st
        acl_after = [ordered]@{
            repo = (Get-AclHash $Repo)
            vault = (Get-AclHash $Vault)
            stage = (Get-AclHash $Stage)
        }
        checks = @($C)
        agent_report = $rep
    }
    $out | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ownerRep -Encoding UTF8
    'owner.report=' + $ownerRep
    if ($fail.Count) { exit 1 }
}

$GuestsSid = 'S-1-5-32-546'

function Invoke-SelfCheck {
    Assert-Targets
    $nonce = [guid]::NewGuid().ToString('N')
    $root = Join-Path $Stage ('selfcheck-' + $nonce)
    $target = Join-Path $root 'case-target'
    $stagingDir = Join-Path $root 'case-staging'
    $aclDir = Join-Path $root 'acl'
    New-Item -ItemType Directory -Force -Path $target, $stagingDir, $aclDir | Out-Null
    $R = New-Object System.Collections.Generic.List[object]
    $chk = { param($n, $ok)
        $R.Add([pscustomobject]@{ name = $n; ok = [bool]$ok }) }

    $before = (Get-Acl -LiteralPath $aclDir).Sddl
    $beforeHash = Get-AclHash $aclDir
    $ownerSid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $null = & icacls $aclDir /inheritance:r /grant:r "*${SystemSid}:(OI)(CI)F" `
        "*${AdminsSid}:(OI)(CI)F" "*${ownerSid}:(OI)(CI)F" "*${GuestsSid}:(OI)(CI)RX"
    $sd = New-Object System.Security.AccessControl.DirectorySecurity
    $sd.SetSecurityDescriptorSddlForm($before)
    Set-Acl -LiteralPath $aclDir -AclObject $sd
    & $chk 'acl.sddl_roundtrip' ((Get-Acl -LiteralPath $aclDir).Sddl -eq $before)
    & $chk 'acl.hash_roundtrip' ((Get-AclHash $aclDir) -eq $beforeHash)

    $child = Join-Path $aclDir 'child'
    New-Item -ItemType Directory -Force -Path $child | Out-Null
    $beforeChild = Get-AclHash $child
    Set-ZoneAcl $aclDir $GuestsSid 'M'
    Set-AgentDeny $aclDir $GuestsSid
    $afterChild = Get-AclHash $child
    $hasDeny = Test-Ace $child $GuestsSid 'Deny'
    & $chk 'acl.child_inherits' (($afterChild -ne $beforeChild) -and $hasDeny)
    $sd2 = New-Object System.Security.AccessControl.DirectorySecurity
    $sd2.SetSecurityDescriptorSddlForm($before)
    Set-Acl -LiteralPath $aclDir -AclObject $sd2
    & $chk 'acl.child_restored' ((Get-AclHash $child) -eq $beforeChild)

    $posFile = Join-Path $stagingDir 'pos.txt'
    Set-Content -LiteralPath $posFile -Value 'x' -Encoding ascii
    & $chk 'owner.create' (Test-Path -LiteralPath $posFile)
    & $chk 'owner.read' ((Get-Content -LiteralPath $posFile -Raw).Trim() -eq 'x')
    Remove-Item -LiteralPath $posFile -Force
    & $chk 'owner.delete' (-not (Test-Path -LiteralPath $posFile))

    $reqFile = Join-Path $root 'request.json'
    $repFile = Join-Path $root 'report.json'
    $canon = Join-Path $root 'canonical.tsv'
    $spool = Join-Path $root 'spool.tsv'
    Set-Content -LiteralPath $canon -Value '' -Encoding ascii
    Set-Content -LiteralPath $spool -Value '' -Encoding ascii
    $del = Join-Path $target 'delete.tmp'
    $ovr = Join-Path $target 'overwrite.tmp'
    $ren = Join-Path $target 'rename.tmp'
    Set-Content -LiteralPath $del -Value 'KEEP' -Encoding ascii
    Set-Content -LiteralPath $ovr -Value 'ORIGINAL' -Encoding ascii
    Set-Content -LiteralPath $ren -Value 'KEEP' -Encoding ascii

    $req = [ordered]@{
        nonce = $nonce
        mode = 'selfcheck'
        expected_sid = $GuestsSid
        expected_name = 'none'
        target_root = $target
        staging_root = $stagingDir
        engine = (Join-Path $Repo '.claude\hooks\aces-hook-engine.mjs')
        canonical = $canon
        spool = $spool
        probe_sha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'w4b-probe.ps1') -Algorithm SHA256).Hash
        started_utc = (Get-Date).ToUniversalTime().ToString('o')
        paths = [ordered]@{
            create = (Join-Path $target 'create.tmp')
            overwrite = $ovr
            delete = $del
            rename = $ren
            rename_to = (Join-Path $target 'renamed.tmp')
        }
    }
    $req | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reqFile -Encoding UTF8

    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'w4b-probe.ps1') `
        -RequestFile $reqFile -ReportFile $repFile | Out-Null
    $probeExit = $LASTEXITCODE
    $pr = $null
    if (Test-Path -LiteralPath $repFile) {
        $pr = Get-Content -LiteralPath $repFile -Raw | ConvertFrom-Json
    }

    & $chk 'detector.report' ($null -ne $pr)
    & $chk 'detector.exit1' ($probeExit -eq 1)
    & $chk 'detector.non_isolated' ($pr.verdict -eq 'NON_ISOLATED')
    & $chk 'detector.identity_mismatch' (-not $pr.identity_match)
    & $chk 'detector.admin_member' ($pr.token.admin_group -eq $true)
    & $chk 'detector.elevated' ($pr.token.elevated -eq $true)
    & $chk 'detector.create_allowed' ($pr.attempts.create -eq 'ALLOWED')
    if ($pr) {
        'engine.ran=' + $pr.engine.ran
        'engine.exit=' + $pr.engine.exit
        'engine.canonical_delta=' + $pr.engine.canonical_delta
        'engine.spool_delta=' + $pr.engine.spool_delta
    }
    & $chk 'engine.canonical_delta1' ($pr.engine.canonical_delta -eq 1)
    & $chk 'engine.spool_delta0' ($pr.engine.spool_delta -eq 0)

    $fail = @($R | Where-Object { -not $_.ok })
    foreach ($x in $R) { $(if ($x.ok) { 'PASS' } else { 'FAIL' }) + ' ' + $x.name }
    'SELFCHECK=' + $(if ($fail.Count) { 'FAIL' } else { 'PASS' })
    'BOUNDARY=ADVISORY'
    if ($fail.Count) { 'kept=' + $root } else { Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue }
    if ($fail.Count) { exit 1 }
    exit 0
}

if ($Apply) { Invoke-Apply; return }
if ($Verify) { Invoke-Verify; return }
if ($Rollback) { Invoke-Rollback; return }
if ($RollbackCodex) { Invoke-RollbackCodex; return }
if ($SelfCheck) { Invoke-SelfCheck; return }
Show-Status
