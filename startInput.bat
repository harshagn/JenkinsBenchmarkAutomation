@ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM title check Jenkins job status
REM D:
REM cd D:\Users\Harsha\JenkinsAutomation\
REM start /B jobTask.bat

:check
for /f "tokens=*" %%a in (D:\Users\Harsha\JenkinsAutomation\statusJob.txt) do (
REM set line=%%a
REM echo %line%
REM :test
if "%%a"=="BUILDING" (
echo Job is Building
goto wait
)
if "%%a"=="SUCCESS" (
echo Job is SUCCESS
goto msg
)
if "%%a"=="FAILURE" (
echo Job Failed
goto msg
)
if "%%a"=="ABORTED" (
echo Job Aborted
goto msg
)

:wait
:: Wait for 10 seconds
    Set _seconds=0
	Set /a "_seconds=_seconds+20">nul
	PING -n %_seconds% 127.0.0.1>nul
goto check
)
:msg
echo Jenkins Job completed
	
REM 	python newJobStatus.py "jadmin:1143d5f11534e322b69317346f80e43177" test
REM 	type statusJob.txt | find "BUILDING" | more +2