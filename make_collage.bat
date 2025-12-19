@echo off
setlocal

rem Запуск локального скрипта склейки коллажа из PNG в этой же папке.
rem Все параметры передаются дальше в make_collage.py.

set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%make_collage.py" %*

endlocal
