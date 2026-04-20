import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date, timedelta

from cash_register.core import theme as T
from cash_register.ui.base_dialog import BaseDialog


class DatePickerDialog(BaseDialog):
    """A clean, modern popup calendar to pick a date."""

    def __init__(self, parent: tk.Misc, initial_date: str = ""):
        self.selected_date = None
        self.initial_date_str = initial_date
        
        # Parse initial_date or use today
        try:
            if initial_date:
                # Expecting 'YYYY-MM-DD'
                y, m, d = map(int, initial_date.split("-"))
                self.current_view = date(y, m, 1)
                self.chosen_year = y
                self.chosen_month = m
                self.chosen_day = d
            else:
                raise ValueError
        except Exception:
            today = date.today()
            self.current_view = date(today.year, today.month, 1)
            self.chosen_year = today.year
            self.chosen_month = today.month
            self.chosen_day = today.day

        super().__init__(parent, title="Select Date", width=340)

    def _build_buttons(self, container: tk.Frame) -> None:
        self._btn_area = tk.Frame(container, bg=T.BG_APP)
        self._btn_area.pack(fill="x")
        
        ttk.Button(
            self._btn_area,
            text="Cancel",
            style="Secondary.TButton",
            command=self.destroy,
        ).pack(side="right", padx=(10, 0))

        # Keep this button mounted to preserve dialog height.
        self.btn_set_date = ttk.Button(
            self._btn_area,
            text="Set Date",
            style="Primary.TButton",
            command=self._on_ok,
        )
        self.btn_set_date.pack(side="right")
            
        self.bind("<Return>", lambda _: self._on_ok())
        self.bind("<Escape>", lambda _: self.destroy())

    def _on_ok(self) -> None:
        chosen_date_str = f"{self.chosen_year:04d}-{self.chosen_month:02d}-{self.chosen_day:02d}"
        if chosen_date_str == self.initial_date_str:
            self.destroy()
            return
        self.result = chosen_date_str
        self.destroy()

    def _build_body(self, container: tk.Frame) -> None:
        # We will dynamically recreate the calendar inner parts.
        self.header_frame = tk.Frame(container, bg=T.BG_APP)
        self.header_frame.pack(fill="x", pady=(0, 16))

        # Prev button
        prev_btn = tk.Label(self.header_frame, text="◀", font=T.FONT_HEADING, 
                            bg=T.BG_APP, fg=T.TEXT_SECONDARY, cursor="hand2")
        prev_btn.pack(side="left", padx=8)
        prev_btn.bind("<Button-1>", lambda e: self._add_months(-1))

        # Month/Year label
        self.month_lbl = self._label(self.header_frame, "", style="heading")
        self.month_lbl.pack(side="left", expand=True)

        # Next button
        next_btn = tk.Label(self.header_frame, text="▶", font=T.FONT_HEADING, 
                            bg=T.BG_APP, fg=T.TEXT_SECONDARY, cursor="hand2")
        next_btn.pack(side="right", padx=8)
        next_btn.bind("<Button-1>", lambda e: self._add_months(1))

        # Calendar grid
        self.grid_frame = tk.Frame(container, bg=T.BG_APP)
        self.grid_frame.pack(fill="both", expand=True)

        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1, uniform="cal")

        self._render_calendar()

    def _add_months(self, delta: int):
        month = self.current_view.month - 1 + delta
        year = self.current_view.year + month // 12
        month = month % 12 + 1
        self.current_view = date(year, month, 1)
        self._render_calendar()

    def _render_calendar(self):
        # Clear old grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        year = self.current_view.year
        month = self.current_view.month

        # Current Month Name
        month_name = calendar.month_name[month]
        self.month_lbl.config(text=f"{month_name} {year}")

        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for c, d in enumerate(days):
            tk.Label(self.grid_frame, text=d, font=T.FONT_SMALL, 
                     bg=T.BG_APP, fg=T.TEXT_SECONDARY, anchor="center").grid(row=0, column=c, pady=(0, 8), sticky="nsew")

        cal = calendar.monthcalendar(year, month)
        today = date.today()

        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    continue  # empty day
                
                # Check if it's the currently chosen day
                is_selected = (day == self.chosen_day and 
                               month == self.chosen_month and 
                               year == self.chosen_year and self.chosen_day != 0) 
                
                bg_color = T.BG_APP
                fg_color = T.TEXT_PRIMARY
                
                if is_selected:
                    bg_color = T.FERN
                    fg_color = T.TEXT_ON_ACCENT
                elif day == today.day and month == today.month and year == today.year:
                    fg_color = T.FERN_DARK

                lbl = tk.Label(self.grid_frame, text=str(day), width=3, height=1,
                               font=T.FONT_BODY, bg=bg_color, fg=fg_color, cursor="hand2", anchor="center")
                lbl.grid(row=r, column=c, padx=2, pady=2, sticky="nsew", ipady=2)
                
                # Hover effects
                def on_enter(e, l=lbl, bg=bg_color):
                    if bg != T.FERN: 
                        l.config(bg=T.ROW_HOVER)
                def on_leave(e, l=lbl, bg=bg_color):
                    l.config(bg=bg)
                
                lbl.bind("<Enter>", on_enter)
                lbl.bind("<Leave>", on_leave)
                lbl.bind("<Button-1>", lambda e, d=day, m=month, y=year: self._select_date(y, m, d))

        # Keep button mounted for stable dialog height.

    def _select_date(self, year, month, day):
        self.chosen_year = year
        self.chosen_month = month
        self.chosen_day = day
        self._render_calendar()
