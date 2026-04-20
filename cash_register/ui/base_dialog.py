"""
base_dialog.py — Reusable modal dialog base class.
All dialogs inherit from here to get consistent styling and behaviour.
"""

import tkinter as tk
from tkinter import ttk

from cash_register.core import theme as T


class BaseDialog(tk.Toplevel):
    """
    Centred, grab-set modal dialog.

    Subclasses implement:
        _build_body(container)  — add widgets to the content area
        _on_ok()                — validate and set self.result, then call self.destroy()

    self.result is None if the user cancels.
    """

    def __init__(self, parent: tk.Misc, title: str, width: int = 380):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.resizable(False, False)
        self.configure(bg=T.BG_APP)
        self.grab_set()
        self.transient(parent)

        self._build_chrome(width)
        self._build_body(self._body_frame)
        self._build_buttons(self._btn_frame)

        self.update_idletasks()
        self._center(parent)
        self.wait_window()

    def _center(self, parent: tk.Misc) -> None:
        pw = parent.winfo_rootx() + parent.winfo_width()  // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"+{pw - self.winfo_width()//2}+{ph - self.winfo_height()//2}")

    def _build_chrome(self, width: int) -> None:
        # thin coloured top strip
        top_strip = tk.Frame(self, bg=T.GUM_LEAF, height=4)
        top_strip.pack(fill="x")

        self._body_frame = tk.Frame(self, bg=T.BG_APP, padx=T.DIALOG_PAD_X,
                                    pady=T.DIALOG_PAD_Y)
        self._body_frame.pack(fill="both", expand=True)

        sep = tk.Frame(self, bg=T.BORDER_LIGHT, height=1)
        sep.pack(fill="x")

        self._btn_frame = tk.Frame(self, bg=T.BG_APP, padx=T.DIALOG_PAD_X,
                                   pady=12)
        self._btn_frame.pack(fill="x")

    def _build_body(self, container: tk.Frame) -> None:
        """Override in subclass."""

    def _build_buttons(self, container: tk.Frame) -> None:
        """Default: Cancel + OK buttons. Override for custom layouts."""
        ttk.Button(container, text="Cancel", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(container, text="OK", style="Primary.TButton",
                   command=self._on_ok).pack(side="right")
        self.bind("<Return>", lambda _: self._on_ok())
        self.bind("<Escape>", lambda _: self.destroy())

    def _on_ok(self) -> None:
        """Override to validate and set self.result."""
        self.destroy()

    # ── shared widget helpers ─────────────────────────────────────────────────

    def _label(self, parent, text: str, style: str = "body") -> tk.Label:
        font = {"body": T.FONT_BODY, "small": T.FONT_SMALL,
                "heading": T.FONT_HEADING}.get(style, T.FONT_BODY)
        color = T.TEXT_PRIMARY if style != "small" else T.TEXT_SECONDARY
        return tk.Label(parent, text=text, bg=T.BG_APP, fg=color,
                        font=font, anchor="w", justify="left")

    def _entry(self, parent, width: int = 28) -> tk.Entry:
        return tk.Entry(parent, font=T.FONT_BODY, width=width,
                        bg=T.INPUT_BG, fg=T.TEXT_PRIMARY,
                        insertbackground=T.TEXT_PRIMARY,
                        relief="solid", bd=T.BORDER_WIDTH,
                        highlightthickness=1,
                        highlightcolor=T.FERN,
                        highlightbackground=T.INPUT_BORDER)
