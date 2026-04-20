"""
theme.py — Single source of truth for the entire visual design.

Palette: Shades of Fern
  fern         #62b76a   – primary accent / buttons
  gum_leaf     #a9d6bb   – header background
  chinook      #a7e7b4   – opening row highlight
  caper        #d2e9af   – footer / even rows
  chrome_white #e3f2d4   – app background / odd rows

To retheme the whole app, only edit this file.
"""

# ── Fern palette ──────────────────────────────────────────────────────────────
FERN          = "#62b76a"
FERN_DARK     = "#4a9452"   # hover/pressed state for primary buttons
GUM_LEAF      = "#a9d6bb"
CHINOOK       = "#a7e7b4"
CAPER         = "#d2e9af"
CHROME_WHITE  = "#e3f2d4"

# ── Derived / semantic colours ─────────────────────────────────────────────────
# backgrounds
BG_APP        = CHROME_WHITE          # main window background
BG_TOOLBAR    = "#f0f8ec"             # toolbar strip (slightly lighter than app bg)
BG_HEADER     = GUM_LEAF             # title bar
BG_STATUS     = CAPER                # status bar at bottom

# table rows
ROW_ODD       = "#ffffff"            # clean white for odd rows
ROW_EVEN      = CHROME_WHITE         # very light fern tint for even rows
ROW_OPENING   = CHINOOK              # opening balance row
ROW_FOOTER    = CAPER                # totals footer row
ROW_SELECTED  = FERN                 # selected row highlight

# text
TEXT_PRIMARY   = "#1e3a22"           # dark forest green — main readable text
TEXT_SECONDARY = "#3d6642"           # mid-green — labels, hints
TEXT_ON_ACCENT = "#ffffff"           # white — text on fern buttons
TEXT_ON_HEADER = "#1e3a22"           # dark on gum-leaf header

# borders
BORDER_LIGHT  = "#c5ddb5"            # subtle row dividers
BORDER_MID    = "#a9d6bb"            # panel borders

# buttons
BTN_PRIMARY       = FERN
BTN_PRIMARY_HOVER = FERN_DARK
BTN_SECONDARY     = "#c8e6c0"        # muted fern for secondary actions
BTN_SECONDARY_HVR = "#b5d9a8"
BTN_DANGER        = "#c0392b"
BTN_DANGER_HOVER  = "#962d22"

# entry / input fields
INPUT_BG      = "#ffffff"
INPUT_BORDER  = BORDER_MID

# ── Typography ────────────────────────────────────────────────────────────────
FONT_FAMILY   = "Segoe UI"

FONT_TITLE    = (FONT_FAMILY, 14, "bold")
FONT_HEADING  = (FONT_FAMILY, 10, "bold")
FONT_BODY     = (FONT_FAMILY, 10)
FONT_SMALL    = (FONT_FAMILY,  9)
FONT_ITALIC   = (FONT_FAMILY, 10, "italic")
FONT_MONO     = ("Consolas", 10)

# ── Dimensions ────────────────────────────────────────────────────────────────
TITLE_BAR_H   = 54
TOOLBAR_PAD_X = 16
TOOLBAR_PAD_Y = 10
ROW_HEIGHT    = 34
BORDER_WIDTH  = 1
DIALOG_PAD_X  = 24
DIALOG_PAD_Y  = 8
BTN_PAD       = (14, 8)
CORNER_RADIUS = 4     # used in custom widgets if needed

# ── Table column config ────────────────────────────────────────────────────────
# Each entry: (header_label, width, min_width, anchor)
TABLE_COLUMNS = {
    "date":         ("Date",          110,  80, "center"),
    "name":         ("Name",          230,  100, "w"),
    "cr":           ("Credit (CR)",   130,  80, "e"),
    "dr":           ("Debit (DR)",    130,  80, "e"),
    "cash_in_hand": ("Cash in Hand",  150,  90, "e"),
}
