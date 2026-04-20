====================================================
  Cash Register — Windows 11 Desktop App
====================================================

SETUP (one time)
----------------
  pip install openpyxl

HOW TO RUN
----------
  python run.py

====================================================
  PROJECT STRUCTURE
====================================================

run.py                          <- Entry point — run this

cash_register/
  controller.py                 <- All app logic; wires view <-> models

  core/
    theme.py                    <- ALL colours, fonts, sizes here
    models.py                   <- Data classes (Transaction, LedgerState)
    repository.py               <- Disk read/write (JSON)

  ui/
    main_window.py              <- Main window layout (view only)
    base_dialog.py              <- Reusable modal dialog base class
    dialogs.py                  <- OpeningBalanceDialog, RowDialog
    styles.py                   <- All ttk style configuration

  utils/
    formatters.py               <- money(), parse_amount(), etc.
    exporter.py                 <- Excel export logic

====================================================
  HOW TO MAKE COMMON EDITS
====================================================

Change any colour / font / size
  -> Edit  cash_register/core/theme.py  only.

Add a new dialog
  -> Subclass BaseDialog in cash_register/ui/dialogs.py

Add a new button
  -> Add widget in main_window.py
  -> Add callback slot: self.on_my_action = lambda: None
  -> Wire in controller.py: v.on_my_action = self._on_my_action

Change storage backend
  -> Replace cash_register/core/repository.py

====================================================
  COLOUR PALETTE — Shades of Fern
====================================================
  fern          #62b76a   Primary buttons, selected rows
  gum leaf      #a9d6bb   Title bar, table header
  chinook       #a7e7b4   Opening balance row
  caper         #d2e9af   Footer row, even rows, status bar
  chrome white  #e3f2d4   App background, odd rows
====================================================
