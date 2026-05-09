[CmdletBinding()]
param(
  [string]$WorkspaceRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $WorkspaceRoot

$inside = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0 -or $inside.Trim() -ne "true") {
  throw "Dieser Befehl muss im Git-Workspace ausgeführt werden."
}

Write-Host "Creating local workspace folders..."

$directories = @(
  "00_project-control\roadmap",
  "01_docs\setup",
  "01_docs\references",
  "02_external",
  "03_tools\releases",
  "04_private_roms",
  "05_builds",
  "06_patches",
  "07_scripts\bootstrap",
  "07_scripts\build",
  "08_tests\setup",
  "08_tests\build",
  "08_tests\hma",
  "08_tests\randomizer",
  "08_tests\ironmon",
  "08_tests\smoke",
  "08_tests\release"
)

foreach ($dir in $directories) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "Checking Git..."
git --version

Write-Host "Checking working tree..."
git status --short --ignored

Write-Host ""
Write-Host "Workspace bootstrap complete."
Write-Host "No external repos cloned."
Write-Host "No ROMs, saves, builds, or tool binaries touched."
Write-Host ""
Write-Host "Manual local files still required later:"
Write-Host "- legal private FireRed ROM in 04_private_roms/"
Write-Host "- local tool releases in 03_tools/releases/"
Write-Host "- generated builds in 05_builds/"
