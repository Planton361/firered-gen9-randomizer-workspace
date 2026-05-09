[CmdletBinding()]
param(
  [string]$ExpectedOriginContains = "Planton361/firered-gen9-randomizer-workspace"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$inside = git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0 -or $inside.Trim() -ne "true") {
  throw "Dieser Befehl muss im Git-Workspace ausgeführt werden."
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()

$origin = ""
try {
  $origin = (git remote get-url origin).Trim()
} catch {
  throw "Remote 'origin' fehlt."
}

$upstream = ""
try {
  $upstream = (git remote get-url upstream).Trim()
} catch {
  $upstream = ""
}

Write-Host "Current branch: $branch"
Write-Host "origin: $origin"

if ($upstream.Length -gt 0) {
  Write-Host "upstream: $upstream"
} else {
  Write-Host "upstream: <not configured>"
}

if ($origin -notlike "*$ExpectedOriginContains*") {
  throw "origin zeigt nicht auf das erwartete Workspace-Repo: $ExpectedOriginContains"
}

Write-Host ""
Write-Host "Configured remotes:"
git remote -v

Write-Host ""
Write-Host "Remote check passed."
