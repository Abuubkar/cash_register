# Cash Register — Business Logic & Requirements

## Overview

A single-user daily cash ledger desktop application.  
The user records credits and debits for a given date. The app tracks a running
**Cash in Hand** balance automatically. At end of day the user switches to a new
date; the closing balance carries forward as the next day's opening balance.

---

## Data Model

### Transaction
| Field  | Type   | Required | Notes                        |
|--------|--------|----------|------------------------------|
| date   | string | yes      | Display date for the row     |
| name   | string | yes      | Description / party name     |
| cr     | float  | no       | Credit amount (default 0.0)  |
| dr     | float  | no       | Debit amount  (default 0.0)  |

### LedgerState (the full app state)
| Field        | Type              | Notes                                      |
|--------------|-------------------|--------------------------------------------|
| opening_cash | float or null     | null only before first-run setup           |
| current_date | string or null    | The active working date                    |
| rows         | list[Transaction] | All transactions for the current date only |

---

## Core Calculations

```
cash_in_hand  = opening_cash + Σ(cr) − Σ(dr)
total_cr      = sum of all cr values in rows
total_dr      = sum of all dr values in rows
running_balance_at(i) = opening_cash + Σ(cr[0..i]) − Σ(dr[0..i])
```

- Cash in Hand is **always computed**, never stored or manually entered.
- Every transaction row shows its own running balance (not just the footer).

---

## Application States

### State 1 — Uninitialised (first run)
- `opening_cash` is `null`
- On launch: show **Opening Balance Dialog** immediately
- User enters a numeric amount (≥ 0)
- This becomes `opening_cash`; `current_date` is set to today; `rows` is empty
- State is persisted; app moves to **Active** state

### State 2 — Active (normal operation)
- `opening_cash` is set, `current_date` is set
- User can add, edit, delete transaction rows
- Table and status bar update after every change
- All changes are persisted immediately (no explicit Save button)

---

## Table Layout (per active date)

| Row       | Date        | Name             | CR              | DR              | Cash in Hand          |
|-----------|-------------|------------------|-----------------|-----------------|-----------------------|
| Row 1     | current date| Opening Balance  | opening_cash    | —               | opening_cash          |
| Row 2+    | current date| user input       | user input / —  | user input / —  | running balance       |
| Footer    | (blank)     | Cash in Hand     | Σ CR            | Σ DR            | final cash in hand    |

Rules:
- Row 1 (Opening Balance) is **read-only** — cannot be edited or deleted
- Footer row is **read-only** — computed only
- Zero CR or DR values display as `—` (dash), not `0.00`
- All amounts are displayed as `Rs X,XXX.XX`

---

## Date Change Flow

Trigger: user types a new date in the date field and clicks **Set Date**

```
1. Validate: new date must not be blank
2. Validate: new date must differ from current_date
3. Compute closing = cash_in_hand (current state)
4. Show confirmation dialog:
      "Switching to {new_date}.
       All rows for '{old_date}' will be cleared.
       Closing Cash in Hand (Rs X) becomes the new opening balance.
       Continue?"
5. If confirmed:
      opening_cash  ← closing
      current_date  ← new_date
      rows          ← []   (cleared)
6. Persist state
7. Refresh table and status bar
```

- The date format is free-form text (no calendar picker enforced)
- Previous transaction rows are **permanently deleted** — no history is kept

---

## Transaction — Add

1. User clicks **＋ Add Row**
2. **Row Dialog** opens pre-filled with `current_date`
3. User enters: Date, Name (required), CR (optional), DR (optional)
4. On Save:
   - Name must not be blank → show error if empty
   - CR must be a positive number or blank → show error if invalid
   - DR must be a positive number or blank → show error if invalid
   - Both CR and DR may be 0 (blank input treated as 0)
5. Append Transaction to `rows`
6. Persist and refresh table

---

## Transaction — Edit

1. User selects a transaction row (not Opening Balance, not Footer)
2. User clicks **✎ Edit**
3. **Row Dialog** opens pre-filled with existing values
4. Same validation as Add
5. Replace `rows[selected_index]` with updated Transaction
6. Persist and refresh table

Guard: if selection is Opening Balance row or Footer row → show info message, abort

---

## Transaction — Delete

1. User selects a transaction row (not Opening Balance, not Footer)
2. User clicks **✕ Delete**
3. Confirmation dialog: `"Delete '{name}'?"`
4. If confirmed: remove `rows[selected_index]`
5. Persist and refresh table

Guard: if selection is Opening Balance row or Footer row → show info message, abort

---

## Persistence

- Storage format: **JSON file** at `~/cash_register_data.json`
- Written after every mutation (add, edit, delete, date change, first-run)
- On launch, file is loaded; if missing or corrupt, a fresh `LedgerState` is created
- No explicit Save button — all changes are auto-saved

---

## Input Validation Rules

| Field  | Rule                                                        | Error message                          |
|--------|-------------------------------------------------------------|----------------------------------------|
| Name   | Must not be blank                                           | "Name / Description is required."     |
| CR     | Must be a positive number or blank (blank → 0)              | "Credit must be a positive number."   |
| DR     | Must be a positive number or blank (blank → 0)              | "Debit must be a positive number."    |
| Date   | Must not be blank (format not enforced)                     | "Please enter a date."                |
| Amount | Commas accepted (e.g. `1,234.56` parsed as `1234.56`)       | —                                      |
| Amount | Negative values rejected                                    | Covered by positive-number rule       |

---

## Status Bar

The status bar at the bottom of the window always shows:

```
Date: {current_date}  |  Opening: Rs X,XXX.XX  |  Cash in Hand: Rs X,XXX.XX  |  Transactions: N
```

Updated after every state change.

---

## Platform

| Requirement | Value              |
|-------------|--------------------|
| OS          | Windows 11, 64-bit |
| Runtime     | Python 3.8+        |
| Dependencies| None               |
| GUI toolkit | `tkinter` (stdlib) |

---

## Colour Palette — Shades of Fern

| Name         | Hex       | Used for                                      |
|--------------|-----------|-----------------------------------------------|
| Fern         | `#62b76a` | Primary buttons, selected row highlight       |
| Gum Leaf     | `#a9d6bb` | Title bar, table column headers               |
| Chinook      | `#a7e7b4` | Opening Balance row background                |
| Caper        | `#d2e9af` | Footer row, even rows, status bar background  |
| Chrome White | `#e3f2d4` | App background, toolbar, odd rows             |

All colour tokens are defined in `cash_register/core/theme.py`.  
No colour values appear anywhere else in the codebase.

---

## File Structure Reference

```
run.py                            ← entry point
cash_register/
  controller.py                   ← all business logic, wires view ↔ models
  core/
    theme.py                      ← colours, fonts, dimensions (edit here to retheme)
    models.py                     ← Transaction, LedgerState dataclasses + calculations
    repository.py                 ← JSON load/save
  ui/
    main_window.py                ← window layout and widget tree (view only)
    styles.py                     ← ttk style configuration
    base_dialog.py                ← reusable modal base class
    dialogs.py                    ← OpeningBalanceDialog, RowDialog
  utils/
    formatters.py                 ← money(), parse_amount(), money_or_dash()
```

---

## Change Guide for AI Editors

| What to change                        | File(s) to touch                          |
|---------------------------------------|-------------------------------------------|
| Any colour, font, or spacing          | `core/theme.py` only                      |
| Calculation logic (cash in hand etc.) | `core/models.py`                          |
| Add a new field to Transaction        | `core/models.py` → `ui/dialogs.py` → `ui/main_window.py` |
| Add a new button or menu item         | `ui/main_window.py` (add widget + slot) → `controller.py` (wire + implement) |
| Add a new dialog                      | `ui/dialogs.py` (subclass BaseDialog)     |
| Change storage format                 | `core/repository.py` only                 |
| Change status bar message             | `controller.py` → `_sync_view()`          |
| Change validation rules               | `ui/dialogs.py` → `_on_ok()`             |
| Change date-change confirmation text  | `controller.py` → `_on_set_date()`       |