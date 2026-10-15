$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$folder = Join-Path $root 'build/import-tests'
New-Item -ItemType Directory -Force $folder | Out-Null
$template = Join-Path $root 'deployment/settings.example.json'
$global:ConciergeTestCalls = [System.Collections.Generic.List[object]]::new()
function Invoke-FakePac {
    $global:ConciergeTestCalls.Add(@($args))
    $global:LASTEXITCODE = 0
}
function Assert-Rejected([scriptblock]$Action) {
    $before = $global:ConciergeTestCalls.Count
    $rejected = $false
    try { & $Action } catch { $rejected = $true }
    if (-not $rejected -or $global:ConciergeTestCalls.Count -ne $before) { throw 'Invalid input reached PAC or was accepted.' }
}
$settings = Get-Content -LiteralPath $template -Raw | ConvertFrom-Json
foreach ($value in $settings.EnvironmentVariables) {
    $value.Value = if ($value.SchemaName -eq 'cr9b0_CalendarId') { 'test-primary-calendar-id' } elseif ($value.SchemaName -eq 'cr9b0_CalendarMailbox') { 'executive@example.com' } else { 'assistant@example.com' }
}
foreach ($value in $settings.ConnectionReferences) { $value.ConnectionId = 'test-connection-id' }
$file = Join-Path $folder 'settings.json'
$settings | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $file -Encoding utf8
$builtPackage = Join-Path $root 'build/ZavaExMMeetingConcierge.zip'
$builtChecksum = Join-Path $root 'build/SHA256SUMS.txt'
Assert-Rejected { & "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'https://poc.example.com' -SettingsFile $template -Pac Invoke-FakePac }
Assert-Rejected { & "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'http://poc.example.com' -SettingsFile $file -Pac Invoke-FakePac }
Assert-Rejected { & "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'https://poc.example.com' -SettingsFile $file -PackagePath $builtPackage -Pac Invoke-FakePac }
$wrongChecksum = Join-Path $folder 'wrong-checksum.txt'
('0' * 64) + '  ZavaExMMeetingConcierge.zip' | Set-Content -LiteralPath $wrongChecksum
Assert-Rejected { & "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'https://poc.example.com' -SettingsFile $file -PackagePath $builtPackage -ChecksumFile $wrongChecksum -Pac Invoke-FakePac }
& "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'https://poc.example.com' -SettingsFile $file -PackagePath $builtPackage -ChecksumFile $builtChecksum -ValidateOnly -Pac Invoke-FakePac
if ($global:ConciergeTestCalls.Count -ne 0) { throw 'Validation contacted a tenant.' }
& "$PSScriptRoot/import-solution.ps1" -EnvironmentUrl 'https://poc.example.com' -SettingsFile $file -PackagePath $builtPackage -ChecksumFile $builtChecksum -Pac Invoke-FakePac
if ($global:ConciergeTestCalls.Count -ne 2 -or $global:ConciergeTestCalls[0][0] -ne 'org' -or $global:ConciergeTestCalls[1][1] -ne 'import') { throw 'Unexpected PAC sequence.' }
foreach ($call in $global:ConciergeTestCalls) {
    if ($call -notcontains '--environment' -or $call -notcontains 'https://poc.example.com/') { throw 'Target environment must be explicit.' }
}
if ($global:ConciergeTestCalls[1] -notcontains '--settings-file' -or $global:ConciergeTestCalls[1] -contains '--activate-plugins') { throw 'Unsafe import arguments.' }
foreach ($path in Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.ps1') {
    $parseErrors = $null; $tokens = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($path.FullName, [ref]$tokens, [ref]$parseErrors)
    if ($parseErrors.Count) { throw $parseErrors }
}
Remove-Variable -Name ConciergeTestCalls -Scope Global
Write-Output 'Import input, checksum, explicit target, and PowerShell syntax checks passed with fake PAC. No tenant calls were made.'
