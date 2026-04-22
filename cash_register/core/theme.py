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
BG_APP        = "#fdfbf7"            # warm cream app background
BG_TOOLBAR    = "#ffffff"            # pure white for toolbar
BG_HEADER     = "#ffffff"            # clean top header
BG_STATUS     = "#ffffff"            # status bar at bottom

# table rows
ROW_ODD       = "#ffffff"            # pure white
ROW_EVEN      = "#faf8f2"            # warm beige for striping
ROW_OPENING   = "#f8f7f2"            # warmer opening balance row
ROW_FOOTER    = "#f5f2eb"            # warm sand footer row
ROW_SELECTED  = "#f2efe4"            # warm selected row highlight
ROW_HOVER     = "#f9f7f0"            # subtle warm hover

# text
TEXT_PRIMARY   = "#11181c"           # near-black for modern high-contrast reading
TEXT_SECONDARY = "#687076"           # slate gray for labels, hints
TEXT_ON_ACCENT = "#ffffff"           # white text on accent buttons
TEXT_ON_HEADER = "#11181c"           # dark on header
TEXT_CR        = "#107c10"           # premium emerald green for credits
TEXT_DR        = "#d13438"           # clean modern red for debits

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
FONT_HEADING  = (FONT_FAMILY, 12, "bold")
FONT_BODY     = (FONT_FAMILY, 11)
FONT_SMALL    = (FONT_FAMILY, 12)
FONT_ITALIC   = (FONT_FAMILY, 11, "italic")
FONT_MONO     = ("Consolas", 10)

# ── Dimensions ────────────────────────────────────────────────────────────────
TITLE_BAR_H   = 60
TOOLBAR_PAD_X = 24
TOOLBAR_PAD_Y = 16
ROW_HEIGHT    = 48                    # taller rows for better breathing room with larger fonts
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
    "date":         ("Date",          100,  80, "center"),
    "name":         ("Name",          240,  100, "w"),
    "cr":           ("Credit (CR)",   150,  100, "e"),
    "dr":           ("Debit (DR)",    150,  100, "e"),
    "cash_in_hand": ("Cash in Hand",  170,  110, "e"),
    "actions":      ("Action",        150,  120, "center"),
}
