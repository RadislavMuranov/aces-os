# ACES W4b - identity boundary for WA-1 (DLPM-002). ASCII only.
# Default action is status (read only).
# -Apply and -Rollback change the system and ask for confirmation.
# The agent identity must be a standard local user, never an administrator.

[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [string]$Repo,
    [string]$Vault = (Join-Path $env:USERPROFILE 'Documents\Obsidian Vault'),
    [string]$Stage = 'C:\ACES-Staging',
    [string]$AgentName = 'aces-agent',
    [string]$CodexGroup = 'CodexSandboxUsers',
    [switch]$Apply,
    [switch]$Codex,
    [switch]$RollbackCodex,
    [switch]$Rollback
)

$ErrorActionPreference = 'Stop'
if (-not $Repo) { $Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path }
$Repo = (Resolve-Path -LiteralPath $Repo).Path
$Vault = (Resolve-Path -LiteralPath $Vault).Path
$Agent = "$env:COMPUTERNAME\$AgentName"
$Spool = Join-Path $Stage 'audit\spool'
$Backup = Join-Path $Stage 'acl-backup'
$Mask = '(OI)(CI)(WD,AD,WEA,WA,DE,DC,WDAC,WO)'
$IsAdmin = (New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)

function Show-Acl([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { "absent: $Path"; return }
    $acl = Get-Acl -LiteralPath $Path
    "protected=$($acl.AreAccessRulesProtected) owner=$($acl.Owner)"
    foreach ($ace in $acl.Access) {
        "$($ace.AccessControlType) $($ace.IdentityReference) $($ace.FileSystemRights)"
    }
}

'identity=' + [Security.Principal.WindowsIdentity]::GetCurrent().Name
'elevated=' + $IsAdmin
'account=' + $(if (Get-LocalUser -Name $AgentName -ErrorAction SilentlyContinue) { 'present' } else { 'absent' })
'repo:'
Show-Acl $Repo
'vault:'
Show-Acl $Vault
'spool=' + (Test-Path -LiteralPath $Spool)

if ($Apply) {
    if (-not $IsAdmin) { throw 'elevated PowerShell required' }
    if ($PSCmdlet.ShouldProcess("$Repo and $Vault", "deny $Agent write and delete")) {
        if (-not (Get-LocalUser -Name $AgentName -ErrorAction SilentlyContinue)) {
            & net.exe user $AgentName '*' /add
            if ($LASTEXITCODE -ne 0) { throw 'net user failed' }
        }
        $AgentSid = (New-Object Security.Principal.NTAccount($Agent)).Translate(
            [Security.Principal.SecurityIdentifier]).Value
        $admin = @(Get-LocalGroupMember -SID 'S-1-5-32-544' -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq $Agent })
        if ($admin.Count) { throw "$Agent is an administrator; the boundary would not hold" }

        if (-not (Test-Path -LiteralPath $Backup)) { New-Item -ItemType Directory -Path $Backup -Force | Out-Null }
        foreach ($p in @($Repo, $Vault)) {
            $f = Join-Path $Backup ((Split-Path $p -Leaf) + '.sddl')
            if (-not (Test-Path -LiteralPath $f)) { Set-Content -LiteralPath $f -Value (Get-Acl -LiteralPath $p).Sddl }
        }
        New-Item -ItemType Directory -Force -Path $Spool | Out-Null

        Set-Content -LiteralPath (Join-Path $Repo '_w4b-delete-probe.tmp') -Value 'x'
        Set-Content -LiteralPath (Join-Path $Repo '_w4b-rename-probe.tmp') -Value 'x'

        & icacls $Stage /grant "${Agent}:(OI)(CI)M"
        & icacls $Repo  /deny  "${Agent}:$Mask"
        & icacls $Vault /deny  "${Agent}:$Mask"

        'applied. next: run tools\protection\w4b-probe.ps1 AS the agent; any ALLOWED line means FAIL'
    }
}

if ($Rollback) {
    if (-not $IsAdmin) { throw 'elevated PowerShell required' }
    foreach ($p in @($Repo, $Vault)) {
        $f = Join-Path $Backup ((Split-Path $p -Leaf) + '.sddl')
        if (Test-Path -LiteralPath $f) {
            $sd = New-Object System.Security.AccessControl.DirectorySecurity
            $sd.SetSecurityDescriptorSddlForm((Get-Content -LiteralPath $f -Raw))
            Set-Acl -LiteralPath $p -AclObject $sd
            "restored $p"
        } else {
            & icacls $p /remove:d $Agent
            "deny removed from $p (no backup found)"
        }
    }
    if (Get-LocalUser -Name $AgentName -ErrorAction SilentlyContinue) {
        & net.exe user $AgentName /delete
        if ($LASTEXITCODE -ne 0) { 'account delete blocked by an active logon; sign out and rerun' }
        else { "deleted $Agent" }
    }
    foreach ($n in '_w4b-created.tmp', '_w4b-delete-probe.tmp', '_w4b-rename-probe.tmp', '_w4b-renamed.tmp') {
        $p = Join-Path $Repo $n
        if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue }
    }
    "kept: $Stage"
}

if ($Codex) {
    if (-not $IsAdmin) { throw 'elevated PowerShell required' }
    if ($PSCmdlet.ShouldProcess($Vault, "deny $CodexGroup write and delete")) {
        $group = Get-LocalGroup -Name $CodexGroup -ErrorAction SilentlyContinue
        if (-not $group) { throw "Local group $CodexGroup not found" }
        $groupSid = $group.SID.Value
        $ownerSid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
        $token = @([Security.Principal.WindowsIdentity]::GetCurrent().Groups |
            ForEach-Object { $_.Value })
        if ($token -contains $groupSid) {
            throw "Current token contains $groupSid; denying it would lock the owner out"
        }

        if (-not (Test-Path -LiteralPath $Backup)) { New-Item -ItemType Directory -Path $Backup -Force | Out-Null }
        $backupFile = Join-Path $Backup 'vault-pre-codex.sddl'
        if (-not (Test-Path -LiteralPath $backupFile)) {
            Set-Content -LiteralPath $backupFile -Value (Get-Acl -LiteralPath $Vault).Sddl
        }
        'backup: ' + $backupFile

        $probe = Join-Path $Vault ('_w4b-owner-probe-' + [guid]::NewGuid().ToString('N') + '.tmp')
        $null = & icacls $Vault /inheritance:r /grant:r "*S-1-5-18:(OI)(CI)F" "*S-1-5-32-544:(OI)(CI)F" "*${ownerSid}:(OI)(CI)F"
        if ($LASTEXITCODE -ne 0) { throw ('grant failed; restore from ' + $backupFile) }
        Set-Content -LiteralPath $probe -Value 'x'
        Remove-Item -LiteralPath $probe -Force
        'owner-write: PASS'

        $null = & icacls $Vault /deny "*${groupSid}:$Mask"
        if ($LASTEXITCODE -ne 0) { throw ('deny failed; restore from ' + $backupFile) }
        Set-Content -LiteralPath $probe -Value 'x'
        Remove-Item -LiteralPath $probe -Force
        'owner-write-after-deny: PASS'
        'vault ACL:'
        Show-Acl $Vault
    }
}

if ($RollbackCodex) {
    if (-not $IsAdmin) { throw 'elevated PowerShell required' }
    $file = Join-Path $Backup 'vault-pre-codex.sddl'
    if (-not (Test-Path -LiteralPath $file)) { throw "No backup at $file" }
    $sd = New-Object System.Security.AccessControl.DirectorySecurity
    $sd.SetSecurityDescriptorSddlForm((Get-Content -LiteralPath $file -Raw))
    Set-Acl -LiteralPath $Vault -AclObject $sd
    "restored $Vault from $file"
}
