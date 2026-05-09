[CmdletBinding()]
param(
  [switch]$AllowMain
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$inside = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0 -or $inside.Trim() -ne "true") {
  throw "Dieser Befehl muss im Git-Workspace ausgeführt werden."
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
$failures = New-Object System.Collections.Generic.List[string]

if ($branch -eq "main" -and -not $AllowMain) {
  $failures.Add("Aktueller Branch ist main. Für Änderungen bitte Arbeitsbranch verwenden.")
}

$forbiddenDirs = @(
  "04_private_roms/",
  "05_builds/",
  "03_tools/releases/"
)

$forbiddenExtensions = @(
  ".gba", ".gb", ".gbc",
  ".sav", ".srm",
  ".state", ".ss0", ".ss1",
  ".zip", ".7z",
  ".exe", ".dll", ".jar"
)

function Normalize-RepoPath {
  param([string]$Path)
  return ($Path -replace "\\", "/").Trim('"')
}

function Test-ForbiddenPath {
  param([string]$Path)

  $normalized = Normalize-RepoPath $Path

  foreach ($dir in $forbiddenDirs) {
    if ($normalized.StartsWith($dir, [System.StringComparison]::OrdinalIgnoreCase)) {
      return $true
    }
  }

  $ext = [System.IO.Path]::GetExtension($normalized).ToLowerInvariant()
  if ($forbiddenExtensions -contains $ext) {
    return $true
  }

  if ($normalized -match "(^|/)\.env($|\.|/)") {
    return $true
  }

  return $false
}

$tracked = git ls-files
foreach ($file in $tracked) {
  if (Test-ForbiddenPath $file) {
    $failures.Add("Verbotene Datei ist getrackt: $file")
  }
}

$statusLines = git status --porcelain=v1 -uall
foreach ($line in $statusLines) {
  if ([string]::IsNullOrWhiteSpace($line)) {
    continue
  }

  if ($line.Length -lt 4) {
    continue
  }

  $path = $line.Substring(3).Trim()
  if ($path -match " -> ") {
    $path = ($path -split " -> ")[-1]
  }
  $path = $path.Trim('"')

  if (Test-ForbiddenPath $path) {
    $failures.Add("Verbotene Datei erscheint im Git-Status: $path")
  }
}

Write-Host "Branch: $branch"
Write-Host "Git status:"
git status --short

if ($failures.Count -gt 0) {
  Write-Host ""
  Write-Host "Sicherheitscheck fehlgeschlagen:"
  foreach ($failure in $failures) {
    Write-Host "- $failure"
  }
  exit 1
}

Write-Host ""
Write-Host "Git safety check passed."
