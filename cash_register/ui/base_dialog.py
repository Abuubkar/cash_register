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
        # Keep hidden until layout + centering are complete to avoid
        # a brief default-sized window flash on some window managers.
        self.withdraw()
        self.title(title)
        self.result = None
        self.resizable(False, False)
        self.configure(bg=T.BG_APP)
        self.transient(parent)
        self.minsize(width, 0)

        self._build_chrome(width)
        self._build_body(self._body_frame)
        self._build_buttons(self._btn_frame)

        self.update_idletasks()
        self._center(parent)
        self.deiconify()
        self.lift()
        self.grab_set()
        self.wait_window()

    def _center(self, parent: tk.Misc) -> None:
        # Ensure both parent and dialog geometry are fully calculated.
        self.update_idletasks()
        # Ensure parent geometry is up-to-date before computing centering.
        parent.update_idletasks()

        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        # When withdrawn, some platforms report current size as 1x1.
        # Use requested size as a reliable source for true dialog dimensions.
        dialog_w = max(self.winfo_width(), self.winfo_reqwidth())
        dialog_h = max(self.winfo_height(), self.winfo_reqheight())

        if parent_w > 1 and parent_h > 1:
            x = parent.winfo_rootx() + (parent_w - dialog_w) // 2
            y = parent.winfo_rooty() + (parent_h - dialog_h) // 2
        else:
            # Fallback: center on the screen if parent geometry isn't ready.
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w - dialog_w) // 2
            y = (screen_h - dialog_h) // 2

        # Keep dialog fully visible.
        x = max(0, x)
        y = max(0, y)
        self.geometry(f"+{x}+{y}")

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
                                   pady=16)
        self._btn_frame.pack(fill="x")

    def _build_body(self, container: tk.Frame) -> None:
        """Override in subclass."""

    def _build_buttons(self, container: tk.Frame) -> None:
        """Default: Cancel + OK buttons. Override for custom layouts."""
        # Top half of container for errors, bottom for buttons
        self._error_var = tk.StringVar()
        self._error_lbl = tk.Label(container, textvariable=self._error_var,
                                   fg=T.BTN_DANGER, bg=T.BG_APP, font=T.FONT_SMALL,
                                   anchor="w", justify="left")
        
        self._btn_area = tk.Frame(container, bg=T.BG_APP)
        self._btn_area.pack(fill="x")
        
        ttk.Button(self._btn_area, text="Cancel", style="Secondary.TButton",
                   command=self.destroy).pack(side="right", padx=(10, 0))
        ttk.Button(self._btn_area, text="OK", style="Primary.TButton",
                   command=self._on_ok).pack(side="right")
        self.bind("<Return>", lambda _: self._on_ok())
        self.bind("<Escape>", lambda _: self.destroy())

    def _on_ok(self) -> None:
        """Override to validate and set self.result."""
        self.destroy()

    def show_error(self, message: str) -> None:
        """Display an inline error in the dialog."""
        self._error_var.set(message)
        if not self._error_lbl.winfo_ismapped():
            self._error_lbl.pack(side="top", fill="x", pady=(0, 10), before=self._btn_area)
            self.update_idletasks()

    # ── shared widget helpers ─────────────────────────────────────────────────

    def _label(self, parent, text: str, style: str = "body") -> tk.Label:
        font = {"body": T.FONT_BODY, "small": T.FONT_SMALL,
                "heading": T.FONT_HEADING}.get(style, T.FONT_BODY)
        color = T.TEXT_PRIMARY if style != "small" else T.TEXT_SECONDARY
        return tk.Label(parent, text=text, bg=T.BG_APP, fg=color,
                        font=font, anchor="w", justify="left")

    def _entry(self, parent, width: int = 28) -> ttk.Entry:
        # ttk.Entry natively manages padding to prevent text cursor overlapping border
        return ttk.Entry(parent, font=T.FONT_BODY, width=width)
