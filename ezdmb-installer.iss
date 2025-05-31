; ezdmb Windows Installer Innosetup build

[Setup] 
AppName=ezdmb
AppVerName=ezdmb v0.9.5
ChangesEnvironment=yes
DefaultDirName={commonpf}\ezdmb
DefaultGroupName=ezdmb
OutputBaseFilename=ezdmb_x64
OutputDir=./work
PrivilegesRequired=admin

; Logs for all installer runs will collect in %TEMP/Setup Log <date> #<number of setup runs today>.txt
SetupLogging=yes

; Disables default "use previous optional task selections" feature of Innosetup installers
UsePreviousTasks=no

[Tasks]
Name: autostart; Description: "&Add Shortcut to Start Up for All Users"; GroupDescription: "Run at Startup:"

[Files]
Source: artifacts\.version; DestDir: {commonpf}\ezdmb; Flags: ignoreversion recursesubdirs uninsrestartdelete
Source: artifacts\icon.ico; DestDir: {commonpf}\ezdmb; Flags: uninsrestartdelete
; Source: artifacts\dmb_config.json; DestDir: {commonpf}\ezdmb; Flags: onlyifdoesntexist uninsrestartdelete
; TODO: INCLUDE EXES BELOW
; Source: ezdmb-x64.exe; DestDir: "{commonpf}\ezdmb"; DestName: ezdmb.exe; Check: IsWin64; Flags: uninsrestartdelete
; Source: ezdmb-x32.exe; DestDir: "{commonpf}\ezdmb"; DestName: ezdmb.exe; Check: "not IsWin64"; Flags: uninsrestartdelete

[Dirs]
Name: {commonappdata}\ezdmb; Flags: uninsneveruninstall

[Icons]
Name: "{commondesktop}\Run ezdmb"; Filename: "{cmd}"; Parameters: " /C ""{app}\ezdmb.exe"""; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico
Name: "{group}\Run ezdmb"; Filename: "{cmd}"; Parameters: "/C ""{app}\ezdmb.exe"" ezdmb"; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico
Name: "{commonstartup}\Run ezdmb"; Filename: "{cmd}"; Parameters: " /C ""{app}\ezdmb.exe"" ezdmb"; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico; Tasks: autostart

[Run]
; Copy log, so %TEMP%/ezdmb_setup.log always contains log entries from the last installer run.
Filename: "{cmd}"; WorkingDir: "{%TEMP}"; Parameters: "/d /c start "" "" /b cmd /d /c ""timeout 1 >NUL & del ezdmb_setup.log 2>NUL & copy /y """"""{log}"""""" ezdmb_setup.log"""; Flags: runhidden

[InstallDelete]
; Remove autostart shortcut, if it exists (during reinstall/upgrade), and user unchecked the autostart option in install gui
Type: files; Name: "{commonstartup}\Run ezdmb.lnk"; Check: DeleteAutostartNecessary()

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{commonpf}\ezdmb"; \
    Check: NeedsAddPath('{commonpf}\ezdmb')

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(
    HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result :=
    (Pos(';' + UpperCase(Param) + ';', ';' + UpperCase(OrigPath) + ';') = 0) and
    (Pos(';' + UpperCase(Param) + '\;', ';' + UpperCase(OrigPath) + ';') = 0); 
end;

function DeleteAutostartNecessary(): boolean;
begin
  Result := (not WizardIsTaskSelected('autostart')) and (FileExists(ExpandConstant('{commonstartup}\Run ezdmb.lnk')));
end;
