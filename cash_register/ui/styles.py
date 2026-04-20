"""
styles.py — Configure all ttk styles once.
Import and call apply_styles(root) before building any UI.
"""

from tkinter import ttk
from cash_register.core import theme as T


def apply_styles(root) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Input Fields ──────────────────────────────────────────────────────────
    style.configure("TEntry",
        insertcolor=T.TEXT_PRIMARY,
        fieldbackground=T.INPUT_BG,
        foreground=T.TEXT_PRIMARY,
        cursor="ibeam"
    )

    # ── Treeview (main table) ─────────────────────────────────────────────────
    style.configure("Treeview",
        background=T.ROW_ODD,
        foreground=T.TEXT_PRIMARY,
        fieldbackground=T.ROW_ODD,
        rowheight=T.ROW_HEIGHT,
        font=T.FONT_BODY,
        borderwidth=0,
        relief="flat",
    )
    style.configure("Treeview.Heading",
        background=T.BG_HEADER,
        foreground=T.TEXT_ON_HEADER,
        font=T.FONT_HEADING,
        relief="flat",
        padding=(8, 6),
    )
    style.map("Treeview",
        background=[("selected", T.ROW_SELECTED)],
        foreground=[("selected", T.TEXT_ON_ACCENT)],
    )
    style.map("Treeview.Heading",
        background=[("active", T.GUM_LEAF)],
    )

    # ── Primary button (fern green) ───────────────────────────────────────────
    style.configure("Primary.TButton",
        background=T.BTN_PRIMARY,
        foreground=T.TEXT_ON_ACCENT,
        font=T.FONT_HEADING,
        relief="flat",
        padding=T.BTN_PAD,
        borderwidth=0,
        focusthickness=0,
        cursor="hand2",
    )
    style.map("Primary.TButton",
        background=[("active", T.BTN_PRIMARY_HOVER),
                    ("pressed", T.BTN_PRIMARY_HOVER)],
    )

    # ── Secondary button (muted) ──────────────────────────────────────────────
    style.configure("Secondary.TButton",
        background=T.BTN_SECONDARY,
        foreground=T.TEXT_PRIMARY,
        font=T.FONT_BODY,
        relief="flat",
        padding=T.BTN_PAD,
        borderwidth=0,
        focusthickness=0,
        cursor="hand2",
    )
    style.map("Secondary.TButton",
        background=[("active", T.BTN_SECONDARY_HVR),
                    ("pressed", T.BTN_SECONDARY_HVR)],
    )

    # ── Danger button (delete / destructive) ──────────────────────────────────
    style.configure("Danger.TButton",
        background=T.BTN_DANGER,
        foreground=T.TEXT_ON_ACCENT,
        font=T.FONT_BODY,
        relief="flat",
        padding=T.BTN_PAD,
        borderwidth=0,
        focusthickness=0,
        cursor="hand2",
    )
    style.map("Danger.TButton",
        background=[("active", T.BTN_DANGER_HOVER),
                    ("pressed", T.BTN_DANGER_HOVER)],
    )

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure("Vertical.TScrollbar",
        background=T.CAPER,
        troughcolor=T.CHROME_WHITE,
        arrowcolor=T.TEXT_SECONDARY,
        relief="flat",
        borderwidth=0,
    )
