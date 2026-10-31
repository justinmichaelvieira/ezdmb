$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand {
    Param
    (
        [Parameter(Mandatory = $true)] [string] $FilePath,
        [Parameter(Mandatory = $true)] [string[]] $Arguments,
        [Parameter(Mandatory = $true)] [string] $Description
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python 3.13 or later and the Windows Python launcher are required."
}

$versionOutput = (& py -3 -c "import sys; print('.'.join(map(str, sys.version_info[:3])))") -join ""
if ($LASTEXITCODE -ne 0 -or $versionOutput -notmatch '^\d+\.\d+\.\d+$') {
    throw "Could not determine the version of Python selected by the py launcher."
}

$pythonVersion = [version]$versionOutput
if ($pythonVersion -lt [version]"3.13.0") {
    throw "Python 3.13 or later is required; found Python $pythonVersion."
}

$repoRoot = $PSScriptRoot
$venvDirectory = Join-Path $repoRoot ".venv"
$venvPython = Join-Path $venvDirectory "Scripts\python.exe"

Invoke-CheckedCommand -FilePath "py" -Arguments @("-3", "-m", "venv", $venvDirectory) -Description "Creating the virtual environment"
Invoke-CheckedCommand -FilePath $venvPython -Arguments @("-m", "pip", "install", "--upgrade", "pip") -Description "Upgrading pip"
Invoke-CheckedCommand -FilePath $venvPython -Arguments @("-m", "pip", "install", $repoRoot) -Description "Installing ezdmb and its dependencies"

Write-Host "Development environment ready."
Write-Host "Activate it with: .\.venv\Scripts\Activate.ps1"
Write-Host "To run the current source, set PYTHONPATH to '$repoRoot\src' and run the virtualenv Python with -m ezdmb."
