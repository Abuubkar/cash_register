"""
dialogs.py — Concrete application dialogs.
Each dialog inherits BaseDialog and only contains domain-specific logic.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from cash_register.core.models import Transaction
from cash_register.core import theme as T
from cash_register.ui.base_dialog import BaseDialog
from cash_register.utils.formatters import parse_amount


class OpeningBalanceDialog(BaseDialog):
    """Ask the user for their initial cash in hand (first-run only)."""

    def __init__(self, parent: tk.Misc):
        super().__init__(parent, title="Set Opening Balance", width=360)

    def _build_body(self, container: tk.Frame) -> None:
        self._label(container,
                    "Welcome! Enter your current Cash in Hand\n"
                    "to set the opening balance.",
                    style="body").pack(anchor="w", pady=(12, 10))

        self._label(container, "Opening Cash in Hand (Rs)",
                    style="small").pack(anchor="w")
        self._e_amount = self._entry(container)
        self._e_amount.pack(fill="x", pady=(2, 12), ipady=5)
        self._e_amount.focus_set()

    def _on_ok(self) -> None:
        try:
            self.result = parse_amount(self._e_amount.get())
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Amount",
                                 "Please enter a valid positive number.",
                                 parent=self)


class RowDialog(BaseDialog):
    """Add or edit a transaction row."""

    def __init__(self, parent: tk.Misc, title: str,
                 tx: Optional[Transaction] = None,
                 default_date: str = ""):
        self._tx           = tx
        self._default_date = default_date
        super().__init__(parent, title=title, width=400)

    def _build_body(self, container: tk.Frame) -> None:
        def row(label_text: str, entry_hint: str = "") -> tk.Entry:
            self._label(container, label_text, style="small").pack(anchor="w", pady=(8, 1))
            e = self._entry(container)
            if entry_hint:
                e.insert(0, entry_hint)
            e.pack(fill="x", ipady=5)
            return e

        name_val = (self._tx.name if self._tx else "")
        cr_val   = (str(self._tx.cr) if self._tx and self._tx.cr else "")
        dr_val   = (str(self._tx.dr) if self._tx and self._tx.dr else "")

        self._e_name = row("Name / Description", name_val)
        self._e_cr   = row("Credit (CR)  —  leave blank if none", cr_val)
        self._e_dr   = row("Debit (DR)   —  leave blank if none", dr_val)

        self._e_name.focus_set()

    def _build_buttons(self, container: tk.Frame) -> None:
        from tkinter import ttk
        ttk.Button(container, text="Cancel", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(container, text="Save", style="Primary.TButton",
                   command=self._on_ok).pack(side="right")
        self.bind("<Return>", lambda _: self._on_ok())
        self.bind("<Escape>", lambda _: self.destroy())

    def _on_ok(self) -> None:
        name = self._e_name.get().strip()
        if not name:
            messagebox.showerror("Required",
                                 "Name / Description is required.", parent=self)
            return
        try:
            cr = parse_amount(self._e_cr.get())
        except ValueError:
            messagebox.showerror("Invalid Credit",
                                 "Credit must be a positive number.", parent=self)
            return
        try:
            dr = parse_amount(self._e_dr.get())
        except ValueError:
            messagebox.showerror("Invalid Debit",
                                 "Debit must be a positive number.", parent=self)
            return

        date_val = self._tx.date if self._tx else self._default_date
        self.result = Transaction(
            date=date_val,
            name=name, cr=cr, dr=dr,
        )
        self.destroy()
