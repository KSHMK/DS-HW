@echo off
cd download
set windef="%ProgramFiles%\Windows Defender\MpCmdRun.exe"
set avp="%programfiles(x86)%\Kaspersky Lab\Kaspersky Anti-Virus 21.3\avp.exe"
set avast="%ProgramFiles%\AVAST Software\Avast\ashcmd.exe"
set clamav="%programfiles(x86)%\ClamWin\bin\clamscan.exe"

set mypath=%cd%
%mypath%\7za.exe e -y %1 -pinfected > nul


if exist %avp% (
    start "avp" /D %mypath% %avp% SCAN .\
    exit
) 
if exist %clamav% (
    start "clamav" /D %mypath% %clamav% clamscan.exe --database="C:\Program Files\ClamWin\db" .\
    exit
) 
if exist %windef%  (
    start "windef" /D %mypath% %windef% -Scan -ScanType QuickScan -ScanPath .\
    exit
)


