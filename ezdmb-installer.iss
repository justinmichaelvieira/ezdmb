; ezdmb Windows Installer Innosetup build

[Setup] 
AppName=ezdmb
AppVerName=ezdmb v0.9.40
ChangesEnvironment=yes
DefaultDirName={commonpf}\ezdmb
DefaultGroupName=ezdmb
OutputBaseFilename=ezdmb_setup
OutputDir=.
PrivilegesRequired=admin

; Logs for all installer runs will collect in %TEMP/Setup Log <date> #<number of setup runs today>.txt
SetupLogging=yes

; Disables default "use previous optional task selections" feature of Innosetup installers
UsePreviousTasks=no

[Tasks]
Name: autostart; Description: "&Add Shortcut to Start Up for All Users"; GroupDescription: "Run at Startup:"

[Files]
Source: artifacts\.version; DestDir: {commonpf}\ezdmb; Flags: ignoreversion uninsrestartdelete
Source: artifacts\style.css; DestDir: {commonpf}\ezdmb; Flags: ignoreversion uninsrestartdelete
Source: artifacts\icon.ico; DestDir: {commonpf}\ezdmb; Flags: ignoreversion uninsrestartdelete

[Dirs]
Name: {commonappdata}\ezdmb; Flags: uninsneveruninstall

[Icons]
Name: "{commondesktop}\Run ezdmb"; Filename: "{cmd}"; Parameters: " /C ""py -m ezdmb"""; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico; AfterInstall: SetElevationBit('{commondesktop}\Run ezdmb.lnk')
Name: "{group}\Run ezdmb"; Filename: "{cmd}"; Parameters: "/C ""py -m ezdmb"""; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico; AfterInstall: SetElevationBit('{group}\Run ezdmb.lnk')
Name: "{commonstartup}\Run ezdmb"; Filename: "{cmd}"; Parameters: " /C ""py -m ezdmb"""; WorkingDir: "{app}\"; IconFilename: {app}\icon.ico; Tasks: autostart; AfterInstall: SetElevationBit('{commonstartup}\Run ezdmb.lnk')

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

procedure SetElevationBit(Filename: string);
var
  Buffer: string;
  Stream: TStream;
begin
  Filename := ExpandConstant(Filename);
  Log('Setting elevation bit for ' + Filename);

  Stream := TFileStream.Create(FileName, fmOpenReadWrite);
  try
    Stream.Seek(21, soFromBeginning);
    SetLength(Buffer, 1);
    Stream.ReadBuffer(Buffer, 1);
    Buffer[1] := Chr(Ord(Buffer[1]) or $20);
    Stream.Seek(-1, soFromCurrent);
    Stream.WriteBuffer(Buffer, 1);
  finally
    Stream.Free;
  end;
end;