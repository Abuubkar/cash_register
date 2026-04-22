"""
main_window.py — The application's main window.
Responsible for layout and event wiring only.
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from datetime import date as Date

from cash_register.core import theme as T


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cash Register")
        self.geometry("940x640")
        self.minsize(780, 520)
        self.configure(bg=T.BG_APP)
        self.resizable(True, True)

        self.on_set_date      = lambda d: None
        self.on_add_row       = lambda: None
        self.on_edit_row      = lambda: None
        self.on_delete_row    = lambda: None
        self.on_clear_data    = lambda: None

        self._selected_index = -1
        self._selected_tags = ()

        self._build_ui()

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

        tk.Label(bar, text="Cash Register",
                 bg=T.BG_HEADER, fg=T.TEXT_ON_HEADER,
                 font=T.FONT_TITLE).pack(side="left", padx=24, pady=12)

        self._header_date_var = tk.StringVar()
        tk.Label(bar, textvariable=self._header_date_var,
                 bg=T.BG_HEADER, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL).pack(side="right", padx=24)

    def _build_toolbar(self) -> None:
        bar = tk.Frame(self, bg=T.BG_TOOLBAR,
                       pady=T.TOOLBAR_PAD_Y, padx=T.TOOLBAR_PAD_X)
        bar.pack(fill="x")

        tk.Label(bar, text="Date:", bg=T.BG_TOOLBAR, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL).pack(side="left")

        self.date_var = tk.StringVar(value=str(Date.today()))

        date_btn = tk.Frame(bar, bg=T.INPUT_BG, bd=1, relief="solid", 
                            highlightbackground=T.INPUT_BORDER, highlightthickness=1, cursor="hand2")
        date_btn.pack(side="left", padx=(4, 4))
        
        lbl = tk.Label(date_btn, textvariable=self.date_var, font=T.FONT_BODY, bg=T.INPUT_BG, fg=T.TEXT_PRIMARY)
        lbl.pack(side="left", padx=(10, 4), pady=6)
        
        cal_cvs = tk.Canvas(date_btn, width=16, height=16, bg=T.INPUT_BG, highlightthickness=0, cursor="hand2")
        cal_cvs.pack(side="right", padx=(0, 10))
        cal_cvs.create_rectangle(2, 4, 14, 14, outline=T.TEXT_SECONDARY, width=1.5)
        cal_cvs.create_line(4, 2, 4, 6, fill=T.TEXT_SECONDARY, width=1.5, capstyle=tk.ROUND)
        cal_cvs.create_line(12, 2, 12, 6, fill=T.TEXT_SECONDARY, width=1.5, capstyle=tk.ROUND)
        cal_cvs.create_line(2, 8, 14, 8, fill=T.TEXT_SECONDARY, width=1.5)

        def open_picker(e):
            from cash_register.ui.date_picker import DatePickerDialog
            d = DatePickerDialog(self, initial_date=self.date_var.get())
            if d.result:
                self.on_set_date(d.result)
                
        lbl.bind("<Button-1>", open_picker)
        cal_cvs.bind("<Button-1>", open_picker)
        date_btn.bind("<Button-1>", open_picker)

        ttk.Button(bar, text="Clear Data", style="Secondary.TButton",
                   command=lambda: self.on_clear_data()).pack(side="right", padx=(0, 10))

        ttk.Button(bar, text="＋ Add Row", style="Secondary.TButton",
                   command=lambda: self.on_add_row()).pack(side="right", padx=(0, 20))

    def _build_table(self) -> None:
        frame = tk.Frame(self, bg=T.BG_APP)
        frame.pack(fill="both", expand=True, padx=16, pady=(16, 0))

        # Scrollbars
        self._v_scrollbar = ttk.Scrollbar(frame, orient="vertical")
        self._v_scrollbar.pack(side="right", fill="y")

        self._h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
        self._h_scrollbar.pack(side="bottom", fill="x")

        # Header Canvas (scrolls horizontally only)
        self._header_canvas = tk.Canvas(frame, bg=T.BG_APP, height=36, highlightthickness=0)
        self._header_canvas.pack(side="top", fill="x")

        # Table Canvas (scrolls both ways)
        self._canvas = tk.Canvas(frame, bg=T.BG_APP, highlightthickness=0)
        self._canvas.pack(side="top", fill="both", expand=True)

        # Wire vertical scroll
        self._v_scrollbar.config(command=self._canvas.yview)
        self._canvas.config(yscrollcommand=self._v_scrollbar.set)

        # Wire horizontal scroll (synchronized)
        def _on_hscroll(*args):
            self._header_canvas.xview(*args)
            self._canvas.xview(*args)
        
        self._h_scrollbar.config(command=_on_hscroll)
        self._header_canvas.config(xscrollcommand=self._h_scrollbar.set)
        self._canvas.config(xscrollcommand=self._h_scrollbar.set)

        # Header wrapper frame
        self._header_frame = tk.Frame(self._header_canvas, bg=T.ROW_FOOTER, height=36)
        self._header_window = self._header_canvas.create_window((0, 0), window=self._header_frame, anchor="nw")

        # Data rows frame
        self._scrollable_frame = tk.Frame(self._canvas, bg=T.BG_APP)
        self._canvas_window = self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")

        # Configure scroll regions and responsive width
        def _configure_widths(event):
            # Sum of columns is 960
            table_min_width = 960
            new_width = max(event.width, table_min_width)
            self._canvas.itemconfig(self._canvas_window, width=new_width)
            self._header_canvas.itemconfig(self._header_window, width=new_width)
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))
            self._header_canvas.configure(scrollregion=self._header_canvas.bbox("all"))

        self._canvas.bind("<Configure>", _configure_widths)
        self._scrollable_frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._header_frame.bind("<Configure>", lambda e: self._header_canvas.configure(scrollregion=self._header_canvas.bbox("all")))

        # Draw column headers
        for col_id, (label, w, minw, anchor) in T.TABLE_COLUMNS.items():
            cell = tk.Frame(self._header_frame, bg=T.ROW_FOOTER, width=w, height=36)
            cell.pack(side="left")
            cell.pack_propagate(False)
            lbl = tk.Label(cell, text=label, bg=T.ROW_FOOTER, fg=T.TEXT_SECONDARY, font=T.FONT_HEADING, anchor=anchor)
            lbl.pack(fill="both", expand=True, padx=8)

        # Mousewheel scrolling (OS-aware)
        def _on_mousewheel(event):
            if self.tk.call("tk", "windowingsystem") == "aqua":
                delta = int(-1 * event.delta)
            else:
                delta = int(-1 * (event.delta / 120))

            # Get current view
            first, last = self._canvas.yview()

            # Prevent scrolling above top
            if first <= 0 and delta < 0:
                return

            # Prevent scrolling below bottom
            if last >= 1 and delta > 0:
                return

            self._canvas.yview_scroll(delta, "units")

        def _on_h_mousewheel(event):
            if self.tk.call("tk", "windowingsystem") == "aqua":
                delta = int(-1 * event.delta)
            else:
                delta = int(-1 * (event.delta / 120))
            self._canvas.xview_scroll(delta, "units")
            self._header_canvas.xview_scroll(delta, "units")

        self._canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self._canvas.bind_all("<Shift-MouseWheel>", _on_h_mousewheel)

        # Pan scrolling (drag to scroll)
        def _on_pan_start(event):
            self._canvas.scan_mark(event.x, event.y)
            self._header_canvas.scan_mark(event.x, 0)

        def _on_pan_drag(event):
            self._canvas.scan_dragto(event.x, event.y, gain=1)
            # Synchronize header horizontal position manually during vertical/horizontal pan
            self._header_canvas.xview_moveto(self._canvas.xview()[0])

        # Bind pan to right-click (Button-2 or Button-3 depending on OS/Config)
        # On macOS trackpads, this is often a two-finger click or Ctrl+Click
        self._canvas.bind("<Button-2>", _on_pan_start)
        self._canvas.bind("<B2-Motion>", _on_pan_drag)
        self._canvas.bind("<Button-3>", _on_pan_start)
        self._canvas.bind("<B3-Motion>", _on_pan_drag)

        # Also allow panning with Button-1 (left click) on the canvas background
        self._canvas.bind("<Button-1>", _on_pan_start)
        self._canvas.bind("<B1-Motion>", _on_pan_drag)

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self, bg=T.BG_STATUS, height=32)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self._status_var = tk.StringVar(value="Ready")
        tk.Label(bar, textvariable=self._status_var,
                 bg=T.BG_STATUS, fg=T.TEXT_SECONDARY,
                 font=T.FONT_SMALL, anchor="w").pack(side="left", padx=24, pady=4)

    def get_selected_index(self) -> int:
        return self._selected_index

    def get_selected_tags(self) -> tuple:
        return self._selected_tags

    def set_status(self, message: str) -> None:
        self._status_var.set(message)

    def set_header_date(self, text: str) -> None:
        self._header_date_var.set(text)

    def refresh_table(self, state) -> None:
        from cash_register.utils.formatters import money, money_or_dash

        for widget in self._scrollable_frame.winfo_children():
            widget.destroy()

        opening  = state.opening_cash or 0.0
        cur_date = state.current_date or ""

        # Opening Balance
        self._add_row([cur_date, "Opening Balance", money(opening), "—", money(opening), ""], tags=("opening",), row_idx=-1)

        running = opening
        for i, tx in enumerate(state.rows):
            running += tx.cr - tx.dr
            tag = "odd" if i % 2 == 0 else "even"
            self._add_row([tx.date or cur_date, tx.name, money_or_dash(tx.cr), money_or_dash(tx.dr), money(running), ""], tags=(tag,), row_idx=i)

        # Footer row
        self._add_row(["", "Cash in Hand", money(state.total_cr), money(state.total_dr), money(state.cash_in_hand), ""], tags=("footer",), row_idx=-2)

    def _add_row(self, data, tags, row_idx):
        bg_color = T.ROW_OPENING if "opening" in tags else T.ROW_FOOTER if "footer" in tags else T.ROW_ODD if "odd" in tags else T.ROW_EVEN
        font = T.FONT_ITALIC if "opening" in tags else T.FONT_HEADING if "footer" in tags else T.FONT_BODY

        row_frame = tk.Frame(self._scrollable_frame, bg=bg_color, height=T.ROW_HEIGHT)
        row_frame.pack(fill="x")
        row_frame.pack_propagate(False)

        is_interactive = not ("opening" in tags or "footer" in tags)

        def on_enter(e):
            pass

        def on_leave(e):
            pass

        for i, (col_id, col_val) in enumerate(zip(T.TABLE_COLUMNS.keys(), data)):
            w = T.TABLE_COLUMNS[col_id][1]
            anchor = T.TABLE_COLUMNS[col_id][3]
            
            cell = tk.Frame(row_frame, bg=bg_color, width=w, height=T.ROW_HEIGHT)
            cell.pack(side="left")
            cell.pack_propagate(False)
            cell.bind("<Enter>", on_enter)
            cell.bind("<Leave>", on_leave)

            if col_id == "actions" and is_interactive:
                self._build_action_cell(cell, row_idx, tags)
            else:
                fg = T.TEXT_PRIMARY
                if col_id == "cr" and col_val != "—":
                    fg = T.TEXT_CR
                elif col_id == "dr" and col_val != "—":
                    fg = T.TEXT_DR
                
                lbl = tk.Label(cell, text=col_val, bg=bg_color, fg=fg, font=font, anchor=anchor)
                lbl.pack(fill="both", expand=True, padx=8)
                lbl.bind("<Enter>", on_enter)
                lbl.bind("<Leave>", on_leave)

        tk.Frame(self._scrollable_frame, bg=T.BORDER_LIGHT, height=1).pack(fill="x")

    def _build_action_cell(self, cell, row_idx, tags):
        # Keep action chips visually centered and balanced in each row.
        wrap = tk.Frame(cell, bg=cell["bg"])
        wrap.pack(expand=True)

        def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
            points = [
                x1 + radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1,
            ]
            return canvas.create_polygon(points, smooth=True, splinesteps=18, **kwargs)

        def make_chip(text, palette, cmd):
            font = tkfont.Font(font=T.FONT_HEADING)
            width = max(56, font.measure(text) + 24)
            height = 24
            radius = min(T.RADIUS_CHIP, height // 2)

            chip = tk.Canvas(
                wrap,
                width=width,
                height=height,
                bg=wrap["bg"],
                highlightthickness=0,
                bd=0,
                relief="flat",
                cursor="hand2",
            )
            draw_rounded_rect(
                chip,
                1,
                1,
                width - 1,
                height - 1,
                radius,
                fill=palette["bg"],
                outline=palette["border"],
                width=1,
                tags="chip_bg",
            )
            chip.create_text(
                width // 2,
                height // 2,
                text=text,
                fill=palette["fg"],
                font=T.FONT_HEADING,
                tags="chip_text",
            )
            chip.pack(side="left", padx=3)

            def on_enter(_):
                chip.itemconfigure("chip_bg", fill=palette["hover"])

            def on_leave(_):
                chip.itemconfigure("chip_bg", fill=palette["bg"])

            def on_press(_):
                chip.itemconfigure("chip_bg", fill=palette["pressed"])

            def on_release(_):
                chip.itemconfigure("chip_bg", fill=palette["hover"])

            def on_click(_):
                self._selected_index = row_idx
                self._selected_tags = tags
                cmd()

            chip.bind("<Enter>", on_enter)
            chip.bind("<Leave>", on_leave)
            chip.bind("<ButtonPress-1>", on_press)
            chip.bind("<ButtonRelease-1>", on_release)
            chip.bind("<Button-1>", on_click)
            return chip

        make_chip(
            "Edit",
            {
                "bg": T.CHIP_EDIT_BG,
                "hover": T.CHIP_EDIT_BG_HOVER,
                "pressed": T.CHIP_EDIT_BG_PRESSED,
                "fg": T.CHIP_EDIT_TEXT,
                "border": T.CHIP_EDIT_BORDER,
            },
            self.on_edit_row,
        )
        make_chip(
            "Delete",
            {
                "bg": T.CHIP_DELETE_BG,
                "hover": T.CHIP_DELETE_BG_HOVER,
                "pressed": T.CHIP_DELETE_BG_PRESSED,
                "fg": T.CHIP_DELETE_TEXT,
                "border": T.CHIP_DELETE_BORDER,
            },
            self.on_delete_row,
        )

