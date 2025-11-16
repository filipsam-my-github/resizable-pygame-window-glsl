@echo off
echo Installing required packages...
pip uninstall pygame
pip install pygame-ce moderngl pyautogui

echo.
echo Installation complete!
echo Running the demo...
python demo.py

pause