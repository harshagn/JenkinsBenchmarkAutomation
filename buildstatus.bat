REM @ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

title run Jenkins job remotely for given user
echo Enter 1st argument:jenkins user name Prateek, Neetu, Subham etc : casesensitive, 2nd : passwd: 3rd: Jenkins job Name
set user=%1
set passwd=%2
set jenJobName=%3
C:
cd "C:\Users\Harsha\.jenkins\users\%user%_*"
call python D:\Users\Harsha\JenkinsAutomation\newJobStatus.py %user% %passwd% %jenJobName%>statusJob.txt