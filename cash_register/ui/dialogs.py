"""
dialogs.py — Concrete application dialogs.
Each dialog inherits BaseDialog and only contains domain-specific logic.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List

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
            val = parse_amount(self._e_amount.get())
            if val < 0:
                self.show_error("Please enter a valid positive number.")
                return
            self.result = val
            self.destroy()
        except ValueError:
            self.show_error("Please enter a valid positive number.")


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

        self._e_name = row("Name", name_val)
        self._e_cr   = row("Credit (CR)  —  leave blank if none", cr_val)
        self._e_dr   = row("Debit (DR)   —  leave blank if none", dr_val)

        self._e_name.focus_set()

    def _on_ok(self) -> None:
        self._error_var.set("")
        name = self._e_name.get().strip()
        if not name:
            self.show_error("Name is required.")
            return

        try:
            cr = parse_amount(self._e_cr.get())
            if cr < 0:
                self.show_error("Credit must be a positive number.")
                return
        except ValueError:
            self.show_error("Credit must be a positive number.")
            return

        try:
            dr = parse_amount(self._e_dr.get())
            if dr < 0:
                self.show_error("Debit must be a positive number.")
                return
        except ValueError:
            self.show_error("Debit must be a positive number.")
            return

        date_val = self._tx.date if self._tx else self._default_date
        self.result = Transaction(
            date=date_val,
            name=name, cr=cr, dr=dr,
        )
        self.destroy()


class ConfirmDialog(BaseDialog):
    """
    Custom styled yes/no confirmation dialog.

    Usage::

        dlg = ConfirmDialog(
            parent,
            title="Change Date",
            headline="Switch to 2026-04-24?",
            details=[
                "All rows for '2026-04-20' will be cleared.",
                "Closing Cash in Hand (Rs 99,999.00) will become the new opening balance.",
            ],
            confirm_label="Confirm",
        )
        if dlg.result:   # True = confirmed
            ...
    """

    def __init__(
        self,
        parent: tk.Misc,
        title: str,
        headline: str,
        details: list,
        confirm_label: str = "Confirm",
    ):
        self._headline      = headline
        self._details       = details
        self._confirm_label = confirm_label
        super().__init__(parent, title=title, width=400)

    # ------------------------------------------------------------------

    def _build_body(self, container: tk.Frame) -> None:
        # Headline
        tk.Label(
            container,
            text=self._headline,
            bg=T.BG_APP,
            fg=T.TEXT_PRIMARY,
            font=T.FONT_HEADING,
            anchor="w",
            justify="left",
            wraplength=360,
        ).pack(anchor="w", pady=(12, 10))

        # Detail lines
        for line in self._details:
            tk.Label(
                container,
                text=line,
                bg=T.BG_APP,
                fg=T.TEXT_SECONDARY,
                font=T.FONT_BODY,
                anchor="w",
                justify="left",
                wraplength=360,
            ).pack(anchor="w", pady=(0, 4))

    def _build_buttons(self, container: tk.Frame) -> None:
        btn_area = tk.Frame(container, bg=T.BG_APP)
        btn_area.pack(fill="x")

        ttk.Button(
            btn_area,
            text="Cancel",
            style="Secondary.TButton",
            command=self.destroy,
        ).pack(side="right", padx=(10, 0))

        ttk.Button(
            btn_area,
            text=self._confirm_label,
            style="Primary.TButton",
            command=self._on_ok,
        ).pack(side="right")

        self.bind("<Return>", lambda _: self._on_ok())
        self.bind("<Escape>", lambda _: self.destroy())

    def _on_ok(self) -> None:
        self.result = True
        self.destroy()
