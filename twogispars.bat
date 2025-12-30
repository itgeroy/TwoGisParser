@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║                   Парсер 2GIS                    ║
echo ╚══════════════════════════════════════════════════╝
echo.

echo.
echo Устанавливаем зависимости...
pip install sv-ttk
pip install pyinstaller
pip install googletrans
pip install playwright
pip install openpyxl

echo.
echo Собираем EXE...
pyinstaller --clean --noconfirm ^
--name="2GIS_Parser" ^
--onefile ^
--windowed ^
--icon="static/icon.ico" ^
--add-data="static;static" ^
--hidden-import="sv_ttk" ^
gui_main.py

echo.
pause