REM clear junctions, then start dropbox
REM 2012.05.08 Ioannis Filippidis, jfilippidis@gmail.com

rem @ECHO OFF
rem CLS

rem clear shortcuts
cd C:\
cd C:\Dropbox
junctions.py -d
junction -s

rem start dropbox
cd "C:\Documents and Settings\Ioannis Filippidis\Application Data\Dropbox\bin"
run "C:\Documents and Settings\Ioannis Filippidis\Application Data\Dropbox\bin\Dropbox.exe" /home

pause

