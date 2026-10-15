param([string]$Pac = 'pac', [string]$OutputPath)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
[xml]$manifest = Get-Content -LiteralPath (Join-Path $root 'solution/unpacked/Other/Solution.xml') -Raw
$version = [string]$manifest.ImportExportXml.SolutionManifest.Version
if (-not $OutputPath) { $OutputPath = Join-Path $root ('build/ZavaExMMeetingConcierge_' + $version.Replace('.', '_') + '_unmanaged.zip') }
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Force (Split-Path $OutputPath -Parent) | Out-Null
& $Pac solution pack --folder (Join-Path $root 'solution/unpacked') --zipfile $OutputPath --packagetype Unmanaged
if ($LASTEXITCODE -ne 0) { throw 'Pack failed' }
Write-Output "Package: $OutputPath"
