call conda activate gis_env

@echo off
cd /d "%~dp0\.\Python_Src"

python csv_address_geocoder.py

pause