@ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

title run Jenkins job remotely for given user
echo Enter 1st argument:jenkins user name Prateek, Neetu, Subham etc : casesensitive, 2nd : passwd: 3rd: Jenkins job Name
set user=%1
set passwd=%2
set jenJobName=%3
set s=""

C:
cd "C:\Users\Harsha\.jenkins\users\%user%_*"\
IF NOT EXIST statusJob.txt ( goto delmsg
)
else (  echo Waiting for you to start Jenkins job. )

:delmsg
echo Run not started.. Please start your run.

:check
call python D:\Users\Harsha\JenkinsAutomation\newJobStatus.py %user% %passwd% %jenJobName%>statusJob.txt

for /f "tokens=*" %%a in (statusJob.txt) do ( 
set s=%%a
)

if "%s%"=="BUILDING" (
goto BuildFile
 )

if "%s%"=="SUCCESS" (
goto NextFile
)
if "%s%"=="FAILURE" (
goto FailFile
)
if "%s%"=="ABORTED" (
goto AbortedFile
)


:waitloop
:: Wait for 5 to 50 seconds
    Set _seconds=0
	Set /a "_seconds=_seconds+5">nul
	PING -n %_seconds% 127.0.0.1>nul
goto check

:BuildFile
	echo Job is in build state
	goto waitloop 
	


:NextFile
    echo Jenkins Job started 
	PING -n 5 127.0.0.1>nul
	echo Job is a SUCCESS
	goto msg

:FailFile
	echo Jenkins Job started 
	PING -n 5 127.0.0.1>nul
	echo Job Failed 
	goto msg

:AbortedFile
	echo Jenkins Job started 
	PING -n 5 127.0.0.1>nul
	echo Job Aborted
	goto msg
:msg
    echo All Jenkins done

