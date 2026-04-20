"""
controller.py — Application controller (presenter).
Owns all business logic. Knows about models and view; neither knows about each other.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import date as Date
from pathlib import Path

from cash_register.core.models import LedgerState
from cash_register.core.repository import LedgerRepository
from cash_register.ui.main_window import MainWindow
from cash_register.ui.dialogs import OpeningBalanceDialog, RowDialog
from cash_register.utils.formatters import money


class AppController:
    """
    Lifecycle:
        ctrl = AppController()
        ctrl.run()        ← starts Tk mainloop
    """

    def __init__(self):
        self._repo  = LedgerRepository()
        self._state = self._repo.load()

        self._view  = MainWindow()
        self._wire_view()

        from cash_register.ui.styles import apply_styles
        apply_styles(self._view)

        # first-run or resume
        if not self._state.is_initialised:
            self._view.after(150, self._first_run)
        else:
            self._sync_view()

    # ── wiring ────────────────────────────────────────────────────────────────

    def _wire_view(self) -> None:
        v = self._view
        v.on_set_date     = self._on_set_date
        v.on_add_row      = self._on_add_row
        v.on_edit_row     = self._on_edit_row
        v.on_delete_row   = self._on_delete_row

    # ── first run ─────────────────────────────────────────────────────────────

    def _first_run(self) -> None:
        dlg = OpeningBalanceDialog(self._view)
        amount = dlg.result if dlg.result is not None else 0.0

        self._state.opening_cash = amount
        self._state.current_date = str(Date.today())
        self._state.rows = []
        self._save()
        self._sync_view()
        self._view.set_status(
            f"Opening balance set to {money(amount)}")

    # ── date ──────────────────────────────────────────────────────────────────

    def _on_set_date(self) -> None:
        new_date = self._view.date_var.get().strip()
        if not new_date:
            messagebox.showwarning("Invalid Date", "Please enter a date.",
                                   parent=self._view)
            return

        old_date = self._state.current_date
        if new_date == old_date:
            messagebox.showinfo("Same Date",
                                "That is already the current date.",
                                parent=self._view)
            return

        closing = self._state.cash_in_hand
        confirmed = messagebox.askyesno(
            "Change Date",
            f"Switch to {new_date}?\n\n"
            f"All rows for '{old_date}' will be cleared.\n"
            f"Closing Cash in Hand ({money(closing)}) will become "
            f"the new opening balance.\n\nContinue?",
            parent=self._view,
        )
        if not confirmed:
            return

        self._state.roll_to_new_date(new_date)
        self._save()
        self._sync_view()
        self._view.set_status(
            f"Date set to {new_date}  |  Opening balance: {money(closing)}")

    # ── row CRUD ──────────────────────────────────────────────────────────────

    def _on_add_row(self) -> None:
        dlg = RowDialog(self._view, title="Add Transaction",
                        default_date=self._state.current_date or "")
        if dlg.result is None:
            return
        self._state.add_row(dlg.result)
        self._save()
        self._sync_view()
        self._view.set_status(f"Transaction added: {dlg.result.name}")

    def _on_edit_row(self) -> None:
        idx  = self._view.get_selected_index()
        tags = self._view.get_selected_tags()

        if idx < 0 or "opening" in tags or "footer" in tags:
            messagebox.showinfo(
                "Select a Row",
                "Please select a transaction row (not the opening or footer row).",
                parent=self._view)
            return

        existing = self._state.rows[idx]
        dlg = RowDialog(self._view, title="Edit Transaction",
                        tx=existing,
                        default_date=self._state.current_date or "")
        if dlg.result is None:
            return

        self._state.update_row(idx, dlg.result)
        self._save()
        self._sync_view()
        self._view.set_status(f"Transaction updated: {dlg.result.name}")

    def _on_delete_row(self) -> None:
        idx  = self._view.get_selected_index()
        tags = self._view.get_selected_tags()

        if idx < 0 or "opening" in tags or "footer" in tags:
            messagebox.showinfo(
                "Select a Row",
                "Please select a transaction row to delete.",
                parent=self._view)
            return

        name = self._state.rows[idx].name
        if not messagebox.askyesno("Delete Row",
                                    f"Delete '{name}'?",
                                    parent=self._view):
            return

        self._state.delete_row(idx)
        self._save()
        self._sync_view()
        self._view.set_status(f"Deleted: {name}")

    # ── internal helpers ──────────────────────────────────────────────────────

    def _save(self) -> None:
        self._repo.save(self._state)

    def _sync_view(self) -> None:
        """Push current state to the view."""
        cur_date = self._state.current_date or str(Date.today())
        self._view.date_var.set(cur_date)
        self._view.set_header_date(f"Today: {Date.today()}")
        self._view.refresh_table(self._state)
        self._view.set_status(
            f"Date: {cur_date}  |  "
            f"Opening: {money(self._state.opening_cash or 0)}  |  "
            f"Cash in Hand: {money(self._state.cash_in_hand)}  |  "
            f"Transactions: {len(self._state.rows)}"
        )

    # ── entry point ───────────────────────────────────────────────────────────

    def run(self) -> None:
        self._view.mainloop()
