param([string]$Pac = 'pac', [string]$OutputPath)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $OutputPath) { $OutputPath = Join-Path $root 'build/ZavaExMMeetingConcierge.zip' }
$OutputPath = [System.IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Force (Split-Path $OutputPath -Parent) | Out-Null
& $Pac solution pack --folder (Join-Path $root 'solution/unpacked') --zipfile $OutputPath --packagetype Unmanaged
if ($LASTEXITCODE -ne 0) { throw 'Pack failed' }
$hash = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA256).Hash.ToLowerInvariant()
[System.IO.File]::WriteAllText((Join-Path (Split-Path $OutputPath -Parent) 'SHA256SUMS.txt'), $hash + '  ' + [System.IO.Path]::GetFileName($OutputPath) + "`n", [System.Text.UTF8Encoding]::new($false))
Write-Output "Package: $OutputPath"
