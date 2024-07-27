Set-PSDebug -Trace 1

# Elevate privileges, if necessary
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$pwd'; & '$PSCommandPath';`"";
    exit;
}

# Python version expected (used to verify installed successfully)
$pyVersion = "3.10.4"

# Package cloud repository to use, and token used to give read-only access to the repo
$pcRepo = "ezdmb"
$pcRepoToken = "<your-token-here>"
$depsRepo = "ezdmbwindeps"
$depsRepoToken = "<your-token-here>"
$appWheelFile = "ezdmb-0.9.1-py3-none-any.whl"
$depsWheelFile = "ezdmbwindeps-1.0.0-py3-none-any.whl"

# Destination paths of each file we download
$pyExeDestination = "$tempFolder\\$pyExe"
$appWheelFileDestination = "$tempFolder\\$appWheelFile"
$depsWheelFileDestination = "$tempFolder\\$depsWheelFile"
$tempFolder = $env:TEMP

# Use TLS1.2 instead of TLS1.0 by default for http requests, if available
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12

# Log file. See: https://stackoverflow.com/a/60663349/106625
$logPath = "$tempFolder\ezdmb-install.log"
Start-Transcript -Path "$logPath"

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

# Pick the right py exe, based on OS bit depth
if ((Get-WmiObject win32_operatingsystem | Select-Object osarchitecture).osarchitecture -like "64*") {
    # 64bit-windows-only code here
    Write-ColorOutput green ("Using 64bit python.")
    $pyExe = "python-$pyVersion-amd64.exe"
}
else {
    # 32bit-windows-only code here
    Write-ColorOutput green ("Using 32bit python.")
    $pyExe = "python-$pyVersion-i386.exe"
}

# Delete any files in the temp dir which may be incomplete or updated in install folder
if (Test-Path $pyExeDestination) { Remove-Item -Path $pyExeDestination }
if (Test-Path $appWheelFileDestination) { Remove-Item -Path $appWheelFileDestination }
if (Test-Path $depsWheelFileDestination) { Remove-Item -Path $depsWheelFileDestination }

# Set up download client object
$client = New-Object System.Net.WebClient

function PauseForAnyKey ($message)
{
    # Powershell ISE needs an assembly loaded for this to work
    if ($psISE) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.MessageBox]::Show("$message")
    }
    else {
        Write-Host "$message" -ForegroundColor Yellow
        $x = $host.ui.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

function CopyToTempIfExistsInScriptDir {
    Param
    (
        [Parameter(Mandatory = $true)] [string] $installerFile,
        [Parameter(Mandatory = $false)] [string] $tempFolder = $env:TEMP
    )

    if (Test-Path -Path "$PSScriptRoot\\$installerFile" -PathType Leaf) {
        Copy-Item "$PSScriptRoot\\$installerFile" -Destination "$tempFolder\\$installerFile"
        Write-ColorOutput blue ("$installerFile found in install folder; Copying to $tempFolder.")
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

        PauseForAnyKey "Press any key to close this window..."
        exit 1
    }
}

# Download (if necessary) and Install python3
CopyToTempIfExistsInScriptDir($pyExe)
if (-not(Test-Path -Path  $pyExeDestination -PathType Leaf)) {
    AttemptDownload -client $client -fileSource $pyExeSource -fileDestination $pyExeDestination
}
else {
    Write-ColorOutput blue ("$pyExe found; Skipping download.")
}
Start-Process $pyExeDestination -Wait -NoNewWindow -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1"

# Reload env vars
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Upgrade pip and install wheel library if python installed successfully.
# If python not installed successfully, exit with error.
py -V | Tee-Object -Variable cmdOutput
if ($cmdOutput -Match "$pyVersion") {
    # Install pip
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m ensurepip --upgrade"

    # Install python "wheel" binary format package
    Start-Process "py" -Wait -NoNewWindow -ArgumentList " -m pip install wheel"
} else {
    Stop-Transcript

    Write-ColorOutput red ("*******************************************************")
    Write-ColorOutput red ("ERROR: Python $pyVersion did not install correctly.")
    Write-ColorOutput red ("Try running $pyExe (unzipped as part of offline")
    Write-ColorOutput red ("installer, OR in the %TEMP% directory) as Administrator,")
    Write-ColorOutput red ("and make sure that py launcher (in the list of Optional")
    Write-ColorOutput red ("Features) is checked, next to: for all users (requires")
    Write-ColorOutput red ("elevation).")
    Write-ColorOutput red ("*******************************************************\n")

    PauseForAnyKey "Press any key to close this window..."
    exit 1
}

# Download deps python package, if wheel file not existing in script dir
CopyToTempIfExistsInScriptDir($depsWheelFile)
if (-not(Test-Path -Path $depsWheelFileDestination -PathType Leaf)) {
    Write-ColorOutput blue ("$depsWheelFile not in script dir; Getting ezdmbwindeps package off dist server...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install ezdmbwindeps --no-cache-dir --force-reinstall --index-url=https://`"$depsRepoToken`":@packagecloud.io/ezdmb/`"$depsRepo`"/pypi/simple"
}
else {
    Write-ColorOutput blue ("$depsWheelFileDestination found; Executing wheel found in script directory...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install --no-cache-dir --force-reinstall `"$depsWheelFileDestination`""
}

# Execute the ezdmbwindeps dependency bootstrapper package
Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m ezdmbwindeps `"$env:TEMP`""

CopyToTempIfExistsInScriptDir($appWheelFile)
# Download ezdmb python package from PackageCloud, if wheel file not existing in script dir
if (-not(Test-Path -Path $appWheelFileDestination -PathType Leaf)) {
    Write-ColorOutput blue ("$appWheelFile not in script dir; Getting ezdmb package off dist server...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install ezdmb --no-cache-dir --force-reinstall --index-url=https://`"$pcRepoToken`":@packagecloud.io/ezdmb/`"$pcRepo`"/pypi/simple"
}
else {
    Write-ColorOutput blue ("$appWheelFile found; Executing wheel found in script directory...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install --no-cache-dir --force-reinstall `"$appWheelFileDestination`""
}

# Execute the ezdmb python bootstrapper package
Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m ezdmb"

Write-ColorOutput green ("Installation script completed. Installation log is available at: $logPath")
Stop-Transcript
