"""
main_window.py — The application's main window.
Responsible for layout and event wiring only.
All business logic is delegated to the controller.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date as Date

from cash_register.core import theme as T


class MainWindow(tk.Tk):
    """
    Pure view layer. Exposes:
        - Observables / StringVars the controller can read
        - Public methods the controller calls to update the UI
        - Callback slots the controller binds to
    """

    def __init__(self):
        super().__init__()
        self.title("Cash Register")
        self.geometry("940x640")
        self.minsize(780, 520)
        self.configure(bg=T.BG_APP)
        self.resizable(True, True)

        # ── public callback slots (controller binds these) ────────────────────
        self.on_set_date      = lambda: None
        self.on_add_row       = lambda: None
        self.on_edit_row      = lambda: None
        self.on_delete_row    = lambda: None

        self._build_ui()

    # ── build ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._build_title_bar()
        self._build_toolbar()
        tk.Frame(self, bg=T.BORDER_MID, height=1).pack(fill="x")
        self._build_table()
        self._build_status_bar()

    def _build_title_bar(self) -> None:
        bar = tk.Frame(self, bg=T.BG_HEADER, height=T.TITLE_BAR_H)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="🌿  Cash Register",
                 bg=T.BG_HEADER, fg=T.TEXT_ON_HEADER,
                 font=T.FONT_TITLE).pack(side="left", padx=20, pady=12)

        # today's date displayed on the right of the header
        self._header_date_var = tk.StringVar()
        tk.Label(bar, textvariable=self._header_date_var,
                 bg=T.BG_HEADER, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL).pack(side="right", padx=20)

    def _build_toolbar(self) -> None:
        bar = tk.Frame(self, bg=T.BG_TOOLBAR,
                       pady=T.TOOLBAR_PAD_Y, padx=T.TOOLBAR_PAD_X)
        bar.pack(fill="x")

        # date entry group
        tk.Label(bar, text="Date:", bg=T.BG_TOOLBAR, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL).pack(side="left")

        self.date_var = tk.StringVar(value=str(Date.today()))
        self._date_entry = tk.Entry(bar, textvariable=self.date_var,
                                    font=T.FONT_BODY, width=13,
                                    bg=T.INPUT_BG, fg=T.TEXT_PRIMARY,
                                    insertbackground=T.TEXT_PRIMARY,
                                    relief="solid", bd=1,
                                    highlightthickness=1,
                                    highlightcolor=T.FERN,
                                    highlightbackground=T.INPUT_BORDER)
        self._date_entry.pack(side="left", padx=(4, 4), ipady=4)

        ttk.Button(bar, text="Set Date", style="Primary.TButton",
                   command=lambda: self.on_set_date()).pack(side="left", padx=(0, 20))

        ttk.Button(bar, text="＋ Add Row", style="Secondary.TButton",
                   command=lambda: self.on_add_row()).pack(side="right", padx=(0, 20))

    def _build_table(self) -> None:
        frame = tk.Frame(self, bg=T.BG_APP)
        frame.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        # columns — hidden "idx" column carries the row index back to controller
        vis_cols = list(T.TABLE_COLUMNS.keys())
        all_cols = vis_cols + ["_idx"]

        self.tree = ttk.Treeview(frame, columns=all_cols,
                                 show="headings", selectmode="browse")

        for col_id, (label, width, minw, anchor) in T.TABLE_COLUMNS.items():
            self.tree.heading(col_id, text=label)
            self.tree.column(col_id, width=width, minwidth=minw, anchor=anchor)

        # hide the index column
        self.tree.heading("_idx", text="")
        self.tree.column("_idx", width=0, minwidth=0, stretch=False)

        # row tags
        self.tree.tag_configure("opening",
            background=T.ROW_OPENING,
            font=T.FONT_ITALIC,
            foreground=T.TEXT_PRIMARY)
        self.tree.tag_configure("footer",
            background=T.ROW_FOOTER,
            font=T.FONT_HEADING,
            foreground=T.TEXT_PRIMARY)
        self.tree.tag_configure("odd",  background=T.ROW_ODD)
        self.tree.tag_configure("even", background=T.ROW_EVEN)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview,
                            style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind("<ButtonRelease-1>", self._on_tree_click)

    def _on_tree_click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
            
        col = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        columns = self.tree["columns"]
        try:
            col_idx = int(col.replace('#', '')) - 1
            col_name = columns[col_idx]
        except Exception:
            return

        if col_name == "actions":
            tags = self.tree.item(item, "tags")
            if "opening" in tags or "footer" in tags:
                return

            self.tree.selection_set(item)
            bbox = self.tree.bbox(item, col)
            if bbox:
                x, y, w, h = bbox
                if event.x < x + w / 2:
                    self.on_edit_row()
                else:
                    self.on_delete_row()

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self, bg=T.BG_STATUS, height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self._status_var = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self._status_var,
                 bg=T.BG_STATUS, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL, anchor="w").pack(side="left", padx=12, pady=4)

    # ── public API for the controller ─────────────────────────────────────────

    def get_selected_index(self) -> int:
        """Return the data index of the selected row, or -1."""
        sel = self.tree.selection()
        if not sel:
            return -1
        vals = self.tree.item(sel[0], "values")
        try:
            return int(vals[-1])   # _idx column
        except (IndexError, ValueError):
            return -1

    def get_selected_tags(self) -> tuple:
        sel = self.tree.selection()
        if not sel:
            return ()
        return self.tree.item(sel[0], "tags")

    def set_status(self, message: str) -> None:
        self._status_var.set(message)

    def set_header_date(self, text: str) -> None:
        self._header_date_var.set(text)

    def refresh_table(self, state) -> None:
        """Rebuild the treeview from a LedgerState."""
        from cash_register.utils.formatters import money, money_or_dash

        for item in self.tree.get_children():
            self.tree.delete(item)

        opening  = state.opening_cash or 0.0
        cur_date = state.current_date or ""

        # Row 1 — opening balance
        self.tree.insert("", "end",
            values=(cur_date, "Opening Balance",
                    money(opening), "—",
                    money(opening), "", -1),
            tags=("opening",))

        # Transaction rows
        running = opening
        for i, tx in enumerate(state.rows):
            running += tx.cr - tx.dr
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end",
                values=(tx.date or cur_date,
                        tx.name,
                        money_or_dash(tx.cr),
                        money_or_dash(tx.dr),
                        money(running),
                        "✎   ✕",
                        i),
                tags=(tag,))

        # Footer row
        self.tree.insert("", "end",
            values=("", "Cash in Hand",
                    money(state.total_cr),
                    money(state.total_dr),
                    money(state.cash_in_hand),
                    "",
                    -2),
            tags=("footer",))
