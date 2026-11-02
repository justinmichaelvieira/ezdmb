$ErrorActionPreference = "Stop"

# Elevate privileges of current WindowsIdentity, if necessary
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    Start-Process -FilePath "PowerShell.exe" -Verb RunAs -WorkingDirectory $pwd -ArgumentList $arguments
    exit;
}

$tempFolder = $env:TEMP

# Turn on log of this scripts console output.
# See: https://stackoverflow.com/a/60663349/106625
$logPath = Join-Path $tempFolder "ezdmb-install.log"
Start-Transcript -Path $logPath -Force

# Use TLS1.2 instead of TLS1.0 for http requests, if available.
# Works around compatibility issue with TLS 1.2 servers and
# defaulted TLS 1.0 in Powershell v1 & v2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12

# Via: https://stackoverflow.com/a/4647985/106625
function Write-ColorOutput($ForegroundColor) {
    # save the current color
    $fc = $host.UI.RawUI.ForegroundColor

    # set the new color
    $host.UI.RawUI.ForegroundColor = $ForegroundColor

    # output
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }

    # restore the original color
    $host.UI.RawUI.ForegroundColor = $fc
}

function PauseForAnyKey ($message)
{
    # Powershell ISE needs an assembly loaded for this to work
    if ($psISE) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show("$message")
    }
    else {
        Write-Host "$message" -ForegroundColor Yellow
        $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

function FailInstall($message) {
    Write-ColorOutput red "INSTALL FAILED - $message"
    Stop-Transcript
    PauseForAnyKey "Press any key to close this window..."
    exit 1
}

function Get-PythonVersion {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
        return $null
    }

    $versionOutput = & py -3 -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" 2>$null
    if ($LASTEXITCODE -ne 0 -or $versionOutput -notmatch '^\d+\.\d+\.\d+$') {
        return $null
    }

    return [version]$versionOutput
}

function Invoke-PythonCommand {
    Param
    (
        [Parameter(Mandatory = $true)] [string[]] $PythonArguments,
        [Parameter(Mandatory = $true)] [string] $Description
    )

    & py -3 @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        FailInstall "$Description failed with exit code $LASTEXITCODE."
    }
}

function AttemptDownload {
    Param
    (
        [Parameter(Mandatory = $true)] [object] $client,
        [Parameter(Mandatory = $true)] [string] $fileSource,
        [Parameter(Mandatory = $true)] [string] $fileDestination
    )
    Try {
        $client.DownloadFile($fileSource,  $fileDestination)
    }
    catch [System.Net.WebException] {
        Write-ColorOutput red ("INSTALL FAILED - Error occurred during download of $fileDestination.")
        If ($_.Exception.Response.StatusCode.value__) {
            $statusCode = ($_.Exception.Response.StatusCode.value__ ).ToString().Trim()
            Write-ColorOutput red ($statusCode)
        }
        If  ($_.Exception.Message) {
            $message = ($_.Exception.Message).ToString().Trim();
            Write-ColorOutput red ($message)
        }

        FailInstall "Download of $fileDestination failed."
    }
}

# The application requires Python 3.13 or later. This is the latest 3.13
# release with an official Windows installer.
$pyVersion = "3.13.17"
$minimumPythonVersion = [version]"3.13.0"
$pyExe = "python-$pyVersion-amd64.exe"
$pyExeSource = "https://www.python.org/ftp/python/$pyVersion/$pyExe"
$pyExeDestination = Join-Path $tempFolder $pyExe
$appInstallerExe = Join-Path $PSScriptRoot "ezdmb_setup.exe"

# Set up download client object
$client = New-Object System.Net.WebClient

if (-not [Environment]::Is64BitOperatingSystem) {
    FailInstall "64-bit Windows is required because the PySide6 runtime has no 32-bit Windows package."
}

Write-ColorOutput yellow "Checking for Python 3.13 or later."
$pythonVersion = Get-PythonVersion
if ($null -eq $pythonVersion -or $pythonVersion -lt $minimumPythonVersion) {
    if (-not (Test-Path -Path $pyExeDestination -PathType Leaf)) {
        AttemptDownload -client $client -fileSource $pyExeSource -fileDestination $pyExeDestination
    }
    else {
        Write-ColorOutput blue "$pyExe found; skipping download."
    }

    $pythonInstaller = Start-Process -FilePath $pyExeDestination -Wait -NoNewWindow -PassThru -ArgumentList @(
        "/quiet",
        "InstallAllUsers=1",
        "PrependPath=1",
        "Include_test=0",
        "Include_pip=1",
        "Include_launcher=1"
    )
    if ($pythonInstaller.ExitCode -notin @(0, 3010)) {
        FailInstall "Python $pyVersion installer exited with code $($pythonInstaller.ExitCode)."
    }

    $pythonVersion = Get-PythonVersion
}

if ($null -eq $pythonVersion -or $pythonVersion -lt $minimumPythonVersion) {
    FailInstall "Python 3.13 or later was not available after installation."
}

Write-ColorOutput green "Using Python $pythonVersion."
Invoke-PythonCommand -PythonArguments @("-m", "ensurepip", "--upgrade") -Description "Bootstrapping pip"
Invoke-PythonCommand -PythonArguments @("-m", "pip", "install", "--upgrade", "pip") -Description "Upgrading pip"

# Installing ezdmb also installs PySide6 and the other declared application dependencies.
Invoke-PythonCommand -PythonArguments @("-m", "pip", "install", "--upgrade", "--force-reinstall", "ezdmb") -Description "Installing ezdmb and its dependencies"

$runtimeCheck = "import importlib; [importlib.import_module(name) for name in ('ezdmb', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets', 'PySide6.QtPdf', 'PySide6.QtPdfWidgets', 'PySide6.QtWebEngineWidgets', 'PySide6.QtSvg')]"
& py -3 -c $runtimeCheck
if ($LASTEXITCODE -ne 0) {
    FailInstall "The ezdmb or PySide6 runtime modules could not be imported."
}

if (-not (Test-Path -Path $appInstallerExe -PathType Leaf)) {
    FailInstall "The Windows setup executable was not found at $appInstallerExe."
}

$appInstaller = Start-Process -FilePath $appInstallerExe -Wait -NoNewWindow -PassThru
if ($appInstaller.ExitCode -ne 0) {
    FailInstall "The Windows setup executable exited with code $($appInstaller.ExitCode)."
}

Write-ColorOutput green "Installation completed. Log: $logPath"
Stop-Transcript
