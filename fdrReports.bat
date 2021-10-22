@ECHO OFF
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

title FDR report generator
REM source directory containing the FDR automation kit and input SPECPU2017 rsf, txt files i.e. D:\Users\Harsha\JenkinsAutomation\SPECCPUFDR-Automation_phase3_icx
set autoKitPath=%1
echo Input files path is set to %autoKitPath%
set maxFreq=%2
echo maxFreq of the SKU is set to %maxFreq%
set memConfig=%3
echo memConfigory configuration string is set to %memConfig%
set userID=%4
echo user ID is set to %userID%
set TuneCom=%5
echo Tuning comment string is set to %TuneCom%
D:
cd %autoKitPath%
REM copy result\CPU2017*.txt %autoKitPath%\
REM copy result\CPU2017*.rsf %autoKitPath%\
call python %autoKitPath%\makeFDR_new.py %maxFreq% %memConfig% %userID% %TuneCom%