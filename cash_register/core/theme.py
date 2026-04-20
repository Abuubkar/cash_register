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
FERN          = "#2a9d8f"    # slightly cleaner modern green accent
FERN_DARK     = "#21867a"    # hover/pressed state for primary buttons
GUM_LEAF      = "#e9f5f0"    # soft near-white green for backgrounds
CHINOOK       = "#dcedec"    # opening row highlight, very subtle
CAPER         = "#f4f9f7"    # footer / even rows
CHROME_WHITE  = "#fafcfb"    # app background / odd rows

# ── Derived / semantic colours ─────────────────────────────────────────────────
# backgrounds
BG_APP        = "#fcfdfc"            # main app background (clean off-white)
BG_TOOLBAR    = "#ffffff"            # pure white for toolbar
BG_HEADER     = "#ffffff"            # clean top header
BG_STATUS     = "#ffffff"            # status bar at bottom

# table rows
ROW_ODD       = "#ffffff"            # pure white
ROW_EVEN      = "#fafbfb"            # barely off-white for striping
ROW_OPENING   = "#f2f8f6"            # opening balance row
ROW_FOOTER    = "#f7f9f9"            # totals footer row
ROW_SELECTED  = "#eaf5f3"            # selected row highlight background
ROW_HOVER     = "#f4faf8"            # NEW: row hover color

# text
TEXT_PRIMARY   = "#11181c"           # near-black for modern high-contrast reading
TEXT_SECONDARY = "#687076"           # slate gray for labels, hints
TEXT_ON_ACCENT = "#ffffff"           # white text on accent buttons
TEXT_ON_HEADER = "#11181c"           # dark on header

# borders
BORDER_LIGHT  = "#e6e8eb"            # subtle row dividers
BORDER_MID    = "#dfe3e6"            # panel borders

# buttons
BTN_PRIMARY       = FERN
BTN_PRIMARY_HOVER = FERN_DARK
BTN_SECONDARY     = "#f1f3f5"        # light gray for secondary actions
BTN_SECONDARY_HVR = "#e9ecef"
BTN_DANGER        = "#e5484d"        # modern destructive red
BTN_DANGER_HOVER  = "#ce2c31"

# inline action chips used in table rows
CHIP_EDIT_BG          = "#f1f8f5"
CHIP_EDIT_BG_HOVER    = "#e4f2ec"
CHIP_EDIT_BG_PRESSED  = "#d8ece3"
CHIP_EDIT_TEXT         = "#1e7b6e"
CHIP_EDIT_BORDER       = "#cde1d8"

CHIP_DELETE_BG         = "#fff5f5"
CHIP_DELETE_BG_HOVER   = "#feeaea"
CHIP_DELETE_BG_PRESSED = "#fddfdf"
CHIP_DELETE_TEXT       = "#c73a3f"
CHIP_DELETE_BORDER     = "#f2cdcf"

# entry / input fields
INPUT_BG      = "#ffffff"
INPUT_BORDER  = BORDER_MID

# ── Typography ────────────────────────────────────────────────────────────────
# Use Segoe UI as reliable system font, but with modern weights
FONT_FAMILY   = "Segoe UI"

FONT_TITLE    = (FONT_FAMILY, 18, "bold")
FONT_HEADING  = (FONT_FAMILY, 11, "bold")
FONT_BODY     = (FONT_FAMILY, 10)
FONT_SMALL    = (FONT_FAMILY,  9)
FONT_ITALIC   = (FONT_FAMILY, 10, "italic")
FONT_MONO     = ("Consolas", 10)

# ── Dimensions ────────────────────────────────────────────────────────────────
TITLE_BAR_H   = 60
TOOLBAR_PAD_X = 24
TOOLBAR_PAD_Y = 16
ROW_HEIGHT    = 42                    # taller rows for better breathing room
BORDER_WIDTH  = 1
DIALOG_PAD_X  = 32
DIALOG_PAD_Y  = 24
BTN_PAD       = (16, 10)

# Corner radii by component type (single source of truth for rounding)
RADIUS_BUTTON = 10
RADIUS_CHIP   = 999
RADIUS_INPUT  = 8
CORNER_RADIUS = RADIUS_INPUT

# ── Table column config ────────────────────────────────────────────────────────
# Each entry: (header_label, width, min_width, anchor)
TABLE_COLUMNS = {
    "date":         ("Date",          110,  80, "center"),
    "name":         ("Name",          230,  100, "w"),
    "cr":           ("Credit (CR)",   130,  80, "e"),
    "dr":           ("Debit (DR)",    130,  80, "e"),
    "cash_in_hand": ("Cash in Hand",  150,  90, "e"),
    "actions":      ("Action",        140,  110, "center"),
}
