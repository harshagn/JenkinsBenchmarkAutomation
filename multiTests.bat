REM @ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

title Iterate files
set destDir=%1
echo The Input file path set is: %destDir%

set user=%2
set ucreds=
echo The User is set to: %user%

call python D:\Users\Harsha\JenkinsAutomation\uMap.py %user%>D:\Users\Harsha\JenkinsAutomation\creds-%user%.txt
REM Above returns the user's jenkin token ID which is pre-created for a given user in Jenkins for Matrix-based multi-user access 

for /f "tokens=1-2 delims==" %%a in (D:\Users\Harsha\JenkinsAutomation\creds-%user%.txt) do (
set ucreds=%%a
)
del D:\Users\Harsha\JenkinsAutomation\creds-%user%.txt
echo  The Jenkins User token credential set is : %ucreds%


REM truncating any previous value of Benchmark variable
set app=
D:
cd D:\Users\Harsha\JenkinsAutomation\
dir /b /a-d %destDir%\test*_%user%.dat > D:\Users\Harsha\JenkinsAutomation\fileList.txt
for /f %%g in (D:\Users\Harsha\JenkinsAutomation\fileList.txt) do (
REM start of for1 loop
del %destDir%\Res\test.dat
del %destDir%\..\run.xml
copy %destDir%\%%g %destDir%\Res\test.dat
REM If user specific testcases file is not present then exit
REM IF EXIST %destDir%\Res\test.dat ( goto usrmsg 
REM )
C:
del "C:\Users\Harsha\.jenkins\workspace\startPipeline\Automation_Kit_Ver1.2-JenkinsAutomation\benchmark-automation-master"\run.xml
D:
cd "D:\Users\Harsha\JenkinsAutomation\"
copy D:\Users\Harsha\JenkinsAutomation\run-orig.xml D:\Users\Harsha\JenkinsAutomation\run.xml
call python D:\Users\Harsha\JenkinsAutomation\text_file_to_xml.py D:\Users\Harsha\JenkinsAutomation\run.xml
copy D:\Users\Harsha\JenkinsAutomation\run.xml "C:\Users\Harsha\.jenkins\workspace\startPipeline\Automation_Kit_Ver1.2-JenkinsAutomation\benchmark-automation-master"\
REM cd D:\Users\Harsha\JenkinsAutomation\..\
"C:\Program Files\Git\mingw64\bin"\curl -X POST http://10.2.128.101:8585/job/winsTransfer/build?token=callCurl --user %user%:%ucreds%
REM  userCreds is "jenkins user:jenkins-user-token generated for winsTransfer jenkins routing Job"

REM JobTask.bat file is called to get status of started above Jenkins Job i.e. searched from below app variable
REM Read the data line from the file
for /f "tokens=1-2 delims=\=" %%a in (%destDir%\Res\test.dat) do (
)  
if %%a==Benchmark set app=%%bJob
REM start & end of for2 loop 

C:
cd "C:\Users\Harsha\.jenkins\users\%user%_*"\
IF NOT EXIST statusJob.txt ( goto delmsg
)
else ( echo Waiting for Pipeline to start Jenkins job. )

:delmsg
echo Run not started.. Please wait Jenkins Pipeline to start your run.

:check
call python D:\Users\Harsha\JenkinsAutomation\newJobStatus.py %user% "cpu2017" !app!>statusJob.txt

for /f "tokens=*" %%a in ("C:\Users\Harsha\.jenkins\users\%user%_*"\statusJob.txt) do (     
REM start of for3 loop
echo Waiting for TestCase %%g to start 
goto waitloop



if exist D:\Users\Harsha\JenkinsAutomation\InprocessFiles\ (
if "%%a"=="BUILDING" (
echo Job is Building
goto BuildFile
 )

if "%%a"=="SUCCESS" (
echo Job is SUCCESS
goto NextFile
)
if "%%a"=="FAILURE" (
echo Job Failed
goto FailFile
)
if "%%a"=="ABORTED" (
echo Job Aborted
goto AbortedFile
)
else ( goto msg)
) 
REM End of main IF exist statement above 

:waitloop
:: Wait for 50 seconds
    Set _seconds=0
	Set /a "_seconds=_seconds+50">nul
	PING -n %_seconds% 127.0.0.1>nul
goto check

:BuildFile
 	D:
	cd D:\Users\Harsha\JenkinsAutomation\
	move %destDir%\%%g D:\Users\Harsha\JenkinsAutomation\InprocessFiles\>nul
	REM dir /b /a-d D:\Users\Harsha\JenkinsAutomation\
	echo TestCase %%g is in build state
	goto waitloop 


:NextFile
	echo TestCase %%g is SUCCESSFULLY completed
	D:
	move D:\Users\Harsha\JenkinsAutomation\InprocessFiles\%%g D:\Users\Harsha\JenkinsAutomation\completedFiles\
	goto check

:FailFile
	echo TestCase %%g Failed 
	D:
	cd D:\Users\Harsha\JenkinsAutomation\
	move D:\Users\Harsha\JenkinsAutomation\InprocessFiles\%%g D:\Users\Harsha\JenkinsAutomation\FailedFiles\
	goto check

:AbortedFile
	echo TestCase %%g Aborted
	D:
	cd D:\Users\Harsha\JenkinsAutomation\
	move D:\Users\Harsha\JenkinsAutomation\InprocessFiles\%%g D:\Users\Harsha\JenkinsAutomation\AbortedFiles\
	goto check
		)
   )
REM end of for3 loop 
)
REM end of for1 loop
:msg
    echo All Jenkins jobs are completed
:usrmsg
    echo User Logged in and corressponding user's testcases test.dat files do not match
REM timeout /t  /nobreak > NUL
REM PAUSE
