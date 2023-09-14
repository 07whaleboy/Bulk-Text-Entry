@echo off
cls
setlocal enabledelayedexpansion

:: Initialize variables
set /a num=0
set /a lines_per_second=0
set /a total_lines=0

:: Create 'Output' directory if it doesn't exist
if not exist Output (
    md Output
)

:: Prompt for filename and content
:start
echo This program will generate any amount of any word or phrase in a text file.
echo What would you like the file to be called? This will automatically add a .txt extension.
set /p name=

cls
echo What's the word or phrase you want to generate in this file?
set /p contents=

:: Prompt for the number of instances
:instances
cls
echo How many times do you want to generate "%contents%" in "%name%.txt"?
set /p instances=

:: Check if instances is a number
setlocal enabledelayedexpansion
set "temp=!instances!"
for /f "delims=0123456789" %%i in ("!temp!") do (
    if "%%i" neq "" (
        cls
        echo %instances% is not a number. Please input a number.
        pause
        goto instances
    )
)
endlocal

cls
echo This program will start generating "!contents!" in "%name%.txt" "%instances%" times when you press any key.
pause >nul
goto generate

:generate
:: Start the timer
for /f "tokens=1-3 delims=:.," %%a in ("%time%") do (
    set "start_time=%%a%%b%%c"
)

:loop
>>"Output\%name%.txt" echo(!contents!
set /a num+=1
set /a total_lines+=1
echo !num!

:: Calculate lines per second
for /f "tokens=1-3 delims=:.," %%a in ("%time%") do (
    set "current_time=%%a%%b%%c"
)
set /a elapsed_time=current_time-start_time

if !elapsed_time! gtr 0 (
    set /a lines_per_second=total_lines/elapsed_time
) else (
    set /a lines_per_second=0
)

if !num! lss %instances% (
    goto loop
) else (
    :: Stop the timer and calculate the time taken
    for /f "tokens=1-3 delims=:.," %%a in ("%time%") do (
        set "end_time=%%a%%b%%c"
    )
    set /a elapsed_time=end_time-start_time

    if !elapsed_time! gtr 0 (
        set /a lines_per_second=total_lines/elapsed_time
    ) else (
        set /a lines_per_second=0
    )

    echo Completed in !elapsed_time! seconds, with an average of !lines_per_second! lines per second.
    echo Press any key to exit...
    pause >nul
    exit /b