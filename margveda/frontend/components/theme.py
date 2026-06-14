ACCENT = "#27e0ff"
ACCENT_2 = "#8b5cf6"
BG = "#070b18"
CARD = "rgba(15, 23, 42, 0.84)"
BORDER = "rgba(148, 163, 184, 0.22)"
TEXT = "#e5f4ff"
MUTED = "#94a3b8"
SUCCESS = "#34d399"
DANGER = "#fb7185"


GLOBAL_STYLE = {
    "font_family": "Inter, ui-sans-serif, system-ui, sans-serif",
    "background": BG,
    "color": TEXT,
}


def panel_style() -> dict:
    return {
        "background": CARD,
        "border": f"1px solid {BORDER}",
        "border_radius": "8px",
        "box_shadow": "0 24px 80px rgba(0, 0, 0, 0.35)",
    }


def input_style() -> dict:
    return {
        "background": "#0f172a",
        "border": f"1px solid {BORDER}",
        "border_radius": "8px",
        "color": TEXT,
        "height": "44px",
        "width": "100%",
    }


def button_style() -> dict:
    return {
        "background": f"linear-gradient(135deg, {ACCENT}, {ACCENT_2})",
        "border_radius": "8px",
        "color": "#020617",
        "font_weight": "800",
        "height": "44px",
        "width": "100%",
    }
