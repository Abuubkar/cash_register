# build_windows.ps1
# Run this script on a Windows machine to build CashRegister.exe
# Usage: Right-click this file → "Run with PowerShell"
#
# Output: dist\CashRegister.exe

Write-Host "=== Cash Register - Windows .exe Builder ===" -ForegroundColor Cyan

# Step 1 – Install PyInstaller
Write-Host "`n[1/2] Installing PyInstaller..." -ForegroundColor Yellow
pip install --upgrade pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip install failed. Make sure Python is on your PATH." -ForegroundColor Red
    exit 1
}

# Step 2 – Build executable
Write-Host "`n[2/2] Building CashRegister.exe..." -ForegroundColor Yellow
pyinstaller `
    --onefile `
    --windowed `
    --name "CashRegister" `
    --icon "edit_icon.ico" `
    --hidden-import tkinter `
    --hidden-import tkinter.ttk `
    --hidden-import tkinter.messagebox `
    --hidden-import tkinter.simpledialog `
    --clean `
    run.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Build failed. See messages above." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Build Complete! ===" -ForegroundColor Green
Write-Host "Your executable is at: dist\CashRegister.exe" -ForegroundColor Green
