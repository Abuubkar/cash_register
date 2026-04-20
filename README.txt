====================================================
  Cash Register - Desktop App (Windows 11 / 64-bit)
====================================================

REQUIREMENTS
------------
Python 3.8+ (64-bit)  — https://www.python.org/downloads/
  (tkinter is included with Python on Windows)

Install the only extra library needed:
  pip install openpyxl

HOW TO RUN
----------
  python cash_register.py

Or double-click cash_register.py if .py files are
associated with Python on your system.

DATA STORAGE
------------
Your data is saved automatically to:
  C:\Users\<YourName>\cash_register_data.json

No database needed — all data persists between sessions.

FEATURES
--------
  • First launch: enter your opening Cash in Hand
  • Add transactions (Name, CR, DR) per day
  • Cash in Hand auto-calculated in every row
  • Change date → clears rows, carries closing balance forward
  • Edit or delete any transaction row
  • Export to a formatted Excel (.xlsx) file

OPTIONAL: CREATE A SHORTCUT
----------------------------
Right-click cash_register.py → Send to → Desktop (create shortcut)
====================================================
