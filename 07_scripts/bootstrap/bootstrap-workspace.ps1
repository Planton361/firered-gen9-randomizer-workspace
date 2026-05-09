# bootstrap-workspace.ps1

$ErrorActionPreference = "Stop"

Write-Host "Creating local workspace folders..."

$dirs = @(
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

$dirs | ForEach-Object {
  New-Item -ItemType Directory -Path $_ -Force | Out-Null
}

Write-Host "Checking Git..."
git --version

Write-Host "Checking working tree..."
git status --short --ignored

Write-Host ""
Write-Host "Manual local files still required later:"
Write-Host "- legal private FireRed ROM in 04_private_roms/"
Write-Host "- local tool releases in 03_tools/releases/"
Write-Host "- generated builds in 05_builds/"
