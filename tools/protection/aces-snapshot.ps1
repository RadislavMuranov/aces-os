# ACES Snapshot - three-store data-loss protection (DLPM-001).
# Archives the aces-os repo (git bundle + tree archive) to E:\ACES-Backups,
# rotates old snapshots, and appends a line to the Obsidian snapshot log.
# Exit codes: 0 = OK, non-zero = failure (logged to snapshot-errors.log).

$ErrorActionPreference = "Stop"
# Paths are derived at runtime (script location + user profile) so the file
# stays pure ASCII and immune to PowerShell 5.1 ANSI/BOM encoding issues.
$Repo   = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Backup = "E:\ACES-Backups\aces-os\snapshots"
$Spool  = "C:\ACES-Staging\audit\spool"
$ObsLog = Join-Path $env:USERPROFILE "Documents\Obsidian Vault\02-Evidence-and-Verification\records\aces-os-snapshot-log.md"
$Keep   = 30

$Stamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
$Dest  = Join-Path $Backup $Stamp
New-Item -ItemType Directory -Path $Dest -Force | Out-Null

try {
  # 1. Git bundle: all refs, self-contained, verifiable.
  # git writes progress to stderr; with EAP=Stop PowerShell 5.1 turns that
  # into a terminating error, so native calls run with EAP=Continue locally.
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  & git -C $Repo bundle create (Join-Path $Dest "aces-os.bundle") --all 2>&1 | Out-Null
  $createOk = ($LASTEXITCODE -eq 0)
  & git -C $Repo bundle verify (Join-Path $Dest "aces-os.bundle") 2>&1 | Out-Null
  $verifyOk = ($LASTEXITCODE -eq 0)
  $ErrorActionPreference = $prev
  if (-not $createOk) { throw "git bundle create failed" }
  if (-not $verifyOk) { throw "git bundle verify failed" }

  # 2. Working tree archive (includes uncommitted files).
  Compress-Archive -Path (Join-Path $Repo "*") -DestinationPath (Join-Path $Dest "worktree.zip") -Force

  # 2b. Staging audit spool (WA-1 uncommitted ledger segment). Archived so the
  #     audit trail survives independently of the staging zone.
  $spoolNote = "spool: absent"
  if (Test-Path $Spool) {
    $spoolFiles = @(Get-ChildItem $Spool -File -Recurse -ErrorAction SilentlyContinue)
    if ($spoolFiles.Count -eq 0) {
      $spoolNote = "spool: empty"
    } else {
      try {
        Compress-Archive -Path (Join-Path $Spool "*") -DestinationPath (Join-Path $Dest "staging-spool.zip") -Force
        $spoolNote = "spool: staging-spool.zip ($($spoolFiles.Count) files)"
      } catch {
        $spoolNote = "spool: WARN not archived - $($_.Exception.Message)"
        Add-Content (Join-Path $Backup "snapshot-errors.log") "$Stamp - spool archive failed: $($_.Exception.Message)"
      }
    }
  }

  # 3. Manifest with checksums (recursive; relative paths).
  $files = Get-ChildItem $Dest -File -Recurse
  $manifest = foreach ($f in $files) {
    $h = (Get-FileHash $f.FullName -Algorithm SHA256).Hash
    "$h  $($f.FullName.Substring($Dest.Length + 1).Replace('\', '/'))"
  }
  $manifest | Set-Content (Join-Path $Dest "manifest.sha256")

  # 4. Rotation: keep newest $Keep snapshots.
  Get-ChildItem $Backup -Directory | Sort-Object Name -Descending |
    Select-Object -Skip $Keep | Remove-Item -Recurse -Force

  # 5. Obsidian record.
  $line = "- $Stamp - snapshot OK: bundle verified, worktree.zip + manifest.sha256 written to $Dest; $spoolNote"
  if (-not (Test-Path $ObsLog)) {
    "# aces-os snapshot log (DLPM-001)`n$line" | Set-Content $ObsLog
  } else {
    Add-Content $ObsLog $line
  }
  Write-Output $line
  exit 0
} catch {
  $msg = "$Stamp - SNAPSHOT FAILED: $($_.Exception.Message)"
  Add-Content (Join-Path $Backup "snapshot-errors.log") $msg
  Write-Error $msg
  exit 1
}
