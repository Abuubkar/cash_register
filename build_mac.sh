#!/bin/bash

# build_mac.sh
# Run this script on a Mac to build CashRegister.app
# Usage: chmod +x build_mac.sh && ./build_mac.sh
#
# Output: dist/CashRegister.app

echo "=== Cash Register - macOS .app Builder ==="

# Step 1 – Install Build Dependencies
echo -e "\n[1/2] Installing build dependencies..."
pip install --upgrade pyinstaller Pillow
if [ $? -ne 0 ]; then
    echo "ERROR: pip install failed. Make sure Python is installed."
    exit 1
fi

# Step 2 – Build executable
echo -e "\n[2/2] Building CashRegister.app..."

# Extract version from cash_register/version.py
VERSION=$(grep '__version__ =' cash_register/version.py | cut -d '"' -f 2)
if [ -z "$VERSION" ]; then
    VERSION="unknown"
fi

# Note: On Mac, --windowed creates a .app bundle. 
# We use --onedir (default) instead of --onefile as it's the standard for .app bundles.
pyinstaller \
    --onedir \
    --windowed \
    --name "CashRegister-v$VERSION" \
    --icon "edit_icon.png" \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import tkinter.messagebox \
    --hidden-import tkinter.simpledialog \
    --clean \
    run.py


if [ $? -ne 0 ]; then
    echo -e "\nERROR: Build failed. See messages above."
    exit 1
fi

echo -e "\n=== Build Complete! ==="
echo "Your application is at: dist/CashRegister-v$VERSION.app"
