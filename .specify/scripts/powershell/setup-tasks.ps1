#!/usr/bin/env pwsh

# Prepare the tasks phase for the current feature (PowerShell)
#
# Validates that the feature directory and plan.md exist, resolves the active
# tasks-template through the Spec Kit template stack (overrides > presets >
# extensions > core) and reports the documents available under FEATURE_DIR.
#
# Usage: ./setup-tasks.ps1 [OPTIONS]
#
# OPTIONS:
#   -Json               Output in JSON format
#   -Help, -h           Show help message

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Output @"
Usage: setup-tasks.ps1 [OPTIONS]

Prepare the tasks phase for the current feature.

OPTIONS:
  -Json               Output in JSON format
  -Help, -h           Show this help message

EXAMPLES:
  .\setup-tasks.ps1 -Json
  .\setup-tasks.ps1

"@
    exit 0
}

# Source common functions
. "$PSScriptRoot/common.ps1"

# Get feature paths and validate branch
$paths = Get-FeaturePathsEnv

if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT)) {
    exit 1
}

# Validate prerequisites
if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
    Write-Output "ERROR: Feature directory not found: $($paths.FEATURE_DIR)"
    Write-Output "Run the specify phase first to create the feature structure."
    exit 1
}

if (-not (Test-Path $paths.IMPL_PLAN -PathType Leaf)) {
    Write-Output "ERROR: plan.md not found in $($paths.FEATURE_DIR)"
    Write-Output "Run the plan phase first to create the implementation plan."
    exit 1
}

# Resolve the active tasks template (empty string when none is installed)
$tasksTemplate = Resolve-Template -TemplateName 'tasks-template' -RepoRoot $paths.REPO_ROOT
if (-not $tasksTemplate -or -not (Test-Path $tasksTemplate -PathType Leaf)) {
    $tasksTemplate = ''
}

# Build list of available documents
$docs = @()

if (Test-Path $paths.RESEARCH) { $docs += 'research.md' }
if (Test-Path $paths.DATA_MODEL) { $docs += 'data-model.md' }

# Check contracts directory (only if it exists and has files)
if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue | Select-Object -First 1)) {
    $docs += 'contracts/'
}

if (Test-Path $paths.QUICKSTART) { $docs += 'quickstart.md' }

# Output results
if ($Json) {
    [PSCustomObject]@{
        FEATURE_DIR    = $paths.FEATURE_DIR
        TASKS_TEMPLATE = $tasksTemplate
        AVAILABLE_DOCS = $docs
    } | ConvertTo-Json -Compress
} else {
    Write-Output "FEATURE_DIR:$($paths.FEATURE_DIR)"
    Write-Output "TASKS_TEMPLATE:$tasksTemplate"
    Write-Output "AVAILABLE_DOCS:"

    Test-FileExists -Path $paths.RESEARCH -Description 'research.md' | Out-Null
    Test-FileExists -Path $paths.DATA_MODEL -Description 'data-model.md' | Out-Null
    Test-DirHasFiles -Path $paths.CONTRACTS_DIR -Description 'contracts/' | Out-Null
    Test-FileExists -Path $paths.QUICKSTART -Description 'quickstart.md' | Out-Null
}
