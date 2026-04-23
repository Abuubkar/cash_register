#!/usr/bin/env python3
import sys
import re
import os

VERSION_FILE = os.path.join("cash_register", "version.py")

def bump_version(part):
    if not os.path.exists(VERSION_FILE):
        print(f"Error: {VERSION_FILE} not found.")
        sys.exit(1)

    with open(VERSION_FILE, "r") as f:
        content = f.read()

    match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("Error: Could not find version string in version.py")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)

    new_version = f"{major}.{minor}.{patch}"
    new_content = re.sub(r'__version__ = ".*"', f'__version__ = "{new_version}"', content)

    with open(VERSION_FILE, "w") as f:
        f.write(new_content)

    print(f"Version bumped to {new_version}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    
    bump_version(sys.argv[1].lower())
