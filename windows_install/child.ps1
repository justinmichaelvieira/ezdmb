Set-PSDebug -Trace 1

# Elevate privileges of current WindowsIdentity, if necessary
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$pwd'; & '$PSCommandPath';`"";
    exit;
}

# Use TLS1.2 instead of TLS1.0 by default for http requests, if available.
# This works around connection/compatibility issues with some webservers that
# force TLS 1.2, and early versions of Powershell.
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

$tempFolder = $env:TEMP

# Log file. Via: https://stackoverflow.com/a/60663349/106625
$logPath = "$tempFolder\ezdmb-install.log"
Start-Transcript -Path "$logPath"

# Package cloud repository to use, and token used to give read-only access to the repo
$pcRepo = "ezdmb"
$pcRepoToken = "" // FIXME
$depsRepo = "ezdmbwindeps"
$depsRepoToken = "" // FIXME

# Python version expected (used to verify installed successfully)
$pyVersion = "3.10.4"

$pyExeDestination = "$tempFolder\\$pyExe"
$appWheelFileDestination = "$tempFolder\\$appWheelFile"
$depsWheelFileDestination = "$tempFolder\\$depsWheelFile"

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

# If python3 found in script dir, copy it to tmp folder.
CopyToTempIfExistsInScriptDir($pyExe)

# If python3 not previously copied or downloaded directly into tmp folder
# download it directly to tmp folder.
if (-not(Test-Path -Path  $pyExeDestination -PathType Leaf)) {
    AttemptDownload -client $client -fileSource $pyExeSource -fileDestination $pyExeDestination
}
else {
    Write-ColorOutput blue ("$pyExe found; Skipping download.")
}

# Start python intaller
Start-Process $pyExeDestination -Wait -NoNewWindow -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1"

# Reload env vars, so we can use python and pip correctly
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
    Write-ColorOutput red ("*******************************************************")
    Write-ColorOutput red ("ERROR: Python $pyVersion did not install correctly.")
    Write-ColorOutput red ("Try installing Python $pyVersion manually, then re-run this script.")
    Write-ColorOutput red ("*******************************************************\n")

    Stop-Transcript

    PauseForAnyKey "Press any key to close this window..."
    exit 1
}

# Download deps python package from PackageCloud, if wheel file not existing in script dir
CopyToTempIfExistsInScriptDir($depsWheelFile)
if (-not(Test-Path -Path $depsWheelFileDestination -PathType Leaf)) {
    Write-ColorOutput blue ("$depsWheelFile not in script dir; Getting ezdmbwindeps package off dist server...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install ezdmbwindeps --no-cache-dir --force-reinstall --index-url=https://`"$depsRepoToken`":@packagecloud.io/ezdmb/`"$depsRepo`"/pypi/simple"
}
else {
    Write-ColorOutput blue ("$depsWheelFileDestination found; Executing wheel found in script directory...")
    Start-Process "py" -Wait -NoNewWindow -ArgumentList "-m pip install --no-cache-dir --force-reinstall `"$depsWheelFileDestination`""
}
