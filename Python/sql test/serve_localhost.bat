REM start server, restart when changes in files are detected
rem activate vows
pserve development.ini --reload

REM if server crashes, wait for user to press button
pause

REM restart this batch script
serve_local.bat