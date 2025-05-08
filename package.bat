@echo off
echo FileSynapse AI - Packaging Script

:: Cleanup
echo Cleaning up...
if exist FileSynapseAI-Package rmdir /s /q FileSynapseAI-Package
if exist FileSynapseAI-Package.zip del /f /q FileSynapseAI-Package.zip

:: Create package directory
echo Creating package directory...
mkdir FileSynapseAI-Package

:: Copy files
echo Copying files...
copy FileSynapseAI.exe FileSynapseAI-Package\
copy KULLANIM.md FileSynapseAI-Package\
copy LICENSE FileSynapseAI-Package\
copy README.md FileSynapseAI-Package\
copy logo_256.ico FileSynapseAI-Package\
copy category_mappings.json FileSynapseAI-Package\
copy settings.json FileSynapseAI-Package\
copy SUMMARY.md FileSynapseAI-Package\
copy FIX_SUMMARY.md FileSynapseAI-Package\

:: Create logs directory
echo Creating logs directory...
mkdir FileSynapseAI-Package\logs

echo Package created successfully!
echo Package location: FileSynapseAI-Package

echo Done!
pause 