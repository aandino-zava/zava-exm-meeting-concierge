param(
    [Parameter(Mandatory=$true)][uri]$EnvironmentUrl,
    [Parameter(Mandatory=$true)][string]$SettingsFile,
    [string]$Pac = 'pac',
    [string]$PackagePath,
    [string]$ChecksumFile,
    [switch]$ValidateOnly
)
$ErrorActionPreference = 'Stop'
if ($EnvironmentUrl.Scheme -ne 'https' -or $EnvironmentUrl.AbsolutePath -ne '/' -or $EnvironmentUrl.Query -or $EnvironmentUrl.Fragment -or $EnvironmentUrl.UserInfo) {
    throw 'Use the target Dataverse HTTPS organization URL without a path or credentials.'
}
$root = Split-Path $PSScriptRoot -Parent
$settings = Get-Content -LiteralPath $SettingsFile -Raw | ConvertFrom-Json
$template = Get-Content -LiteralPath (Join-Path $root 'deployment/settings.example.json') -Raw | ConvertFrom-Json
foreach ($required in $template.EnvironmentVariables) {
    $values = @($settings.EnvironmentVariables | Where-Object SchemaName -eq $required.SchemaName)
    if ($values.Count -ne 1 -or [string]::IsNullOrWhiteSpace([string]$values[0].Value)) { throw "Provide one value for $($required.SchemaName)." }
    if ($required.SchemaName -ne 'cr9b0_CalendarId' -and $values[0].Value -notmatch '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') {
        throw "Provide a single email address for $($required.SchemaName)."
    }
}
foreach ($required in $template.ConnectionReferences) {
    $values = @($settings.ConnectionReferences | Where-Object LogicalName -eq $required.LogicalName)
    if ($values.Count -ne 1 -or [string]::IsNullOrWhiteSpace([string]$values[0].ConnectionId) -or $values[0].ConnectorId -ne $required.ConnectorId) {
        throw "Provide a target connection ID and matching connector for $($required.LogicalName)."
    }
}
if ([bool]$PackagePath -ne [bool]$ChecksumFile) { throw 'Supply PackagePath and ChecksumFile together.' }
if ($PackagePath) {
    $archive = (Resolve-Path -LiteralPath $PackagePath).Path
    $checksumText = (Get-Content -LiteralPath $ChecksumFile -Raw).Trim()
    $checksumMatch = [regex]::Match($checksumText, '^([a-fA-F0-9]{64})  ' + [regex]::Escape([System.IO.Path]::GetFileName($archive)) + '$')
    if (-not $checksumMatch.Success) { throw 'Checksum file must contain one SHA-256 entry for the selected package.' }
    $expectedHash = $checksumMatch.Groups[1].Value.ToLowerInvariant()
} else {
    $provenance = Get-Content -LiteralPath (Join-Path $root 'solution/provenance.json') -Raw | ConvertFrom-Json
    $archive = Join-Path $root ('solution/' + $provenance.export_archive)
    $expectedHash = $provenance.archive_sha256
}
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedHash) { throw 'Package checksum differs from the expected SHA-256.' }
if ($ValidateOnly) { Write-Output 'Settings and package checksum passed. No tenant connection was made.'; return }
& $Pac org who --environment $EnvironmentUrl.AbsoluteUri
if ($LASTEXITCODE -ne 0) { throw 'Target environment check failed' }
& $Pac solution import --path $archive --settings-file (Resolve-Path -LiteralPath $SettingsFile).Path --environment $EnvironmentUrl.AbsoluteUri --async
if ($LASTEXITCODE -ne 0) { throw 'Import failed. Inspect the import log before retrying.' }
Write-Output 'Import command completed. Verify both flows remain off, set the rule, configure agent authentication, and follow docs/deployment.md before enabling the POC.'
