param([Parameter(Mandatory=$true)][string]$EnvironmentUrl, [string]$Pac = 'pac')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$staging = Join-Path $root 'build/live-export'
New-Item -ItemType Directory -Force $staging | Out-Null
$zip = Join-Path $staging 'live-unmanaged.zip'
& $Pac org who --environment $EnvironmentUrl
if ($LASTEXITCODE -ne 0) { throw 'Environment identity check failed' }
$manifestPath = Join-Path $root 'solution/unpacked/Other/Solution.xml'
[xml]$manifest = Get-Content -LiteralPath $manifestPath -Raw
$solutionName = [string]$manifest.ImportExportXml.SolutionManifest.UniqueName
if ([string]::IsNullOrWhiteSpace($solutionName)) { throw 'Solution name is missing from the native manifest' }
& $Pac solution export --name $solutionName --path $zip --managed false --environment $EnvironmentUrl --overwrite
if ($LASTEXITCODE -ne 0) { throw 'Export failed' }
& $Pac solution unpack --zipfile $zip --folder (Join-Path $staging 'unpacked') --packagetype Unmanaged --allowDelete --allowWrite
if ($LASTEXITCODE -ne 0) { throw 'Unpack failed' }
Write-Output 'Live export staged in build/live-export. Review it before replacing portable source or a release package.'
