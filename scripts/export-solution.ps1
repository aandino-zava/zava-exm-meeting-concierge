param([Parameter(Mandatory=$true)][string]$EnvironmentUrl, [string]$Pac = 'pac')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$zip = Join-Path $root 'solution/exports/ZavaExMMeetingConcierge_1_0_0_0_unmanaged.zip'
& $Pac org who --environment $EnvironmentUrl
if ($LASTEXITCODE -ne 0) { throw 'Environment identity check failed' }
& $Pac solution export --name ZavaCalendarGovernancePOC --path $zip --managed false --environment $EnvironmentUrl --overwrite
if ($LASTEXITCODE -ne 0) { throw 'Export failed' }
& $Pac solution unpack --zipfile $zip --folder (Join-Path $root 'solution/unpacked') --packagetype Unmanaged --allowDelete --allowWrite
if ($LASTEXITCODE -ne 0) { throw 'Unpack failed' }
