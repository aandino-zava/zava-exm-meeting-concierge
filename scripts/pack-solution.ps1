param([string]$Pac = 'pac')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
New-Item -ItemType Directory -Force (Join-Path $root 'build') | Out-Null
& $Pac solution pack --folder (Join-Path $root 'solution/unpacked') --zipfile (Join-Path $root 'build/ZavaExMMeetingConcierge-unmanaged.zip') --packagetype Unmanaged
if ($LASTEXITCODE -ne 0) { throw 'Pack failed' }
