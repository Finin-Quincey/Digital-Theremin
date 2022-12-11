@echo off
echo Flashing current file to Pico...
echo Deleting main.py
ampy rm /main.py
echo Writing %~1 as main.py
ampy put "%~1" "main.py"
echo Upload done