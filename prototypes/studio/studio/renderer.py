"""
BlackRoad Studio - Terminal Renderer

Renders the studio interface in the terminal, mirroring the visual IDE layout:
- Toolbar (top)
- Main canvas (center)
- Sidebar (right-style info)
- Status bar (bottom)
"""

import shutil


def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


# ─── Box Drawing ────────────────────────────────────────────────────

def box(title, content_lines, width=None):
    """Draw a box with title."""
    if width is None:
        width = min(get_terminal_width() - 4, 72)

    inner = width - 2
    lines = []
    lines.append(f"  +{'=' * inner}+")

    # Title bar
    t = f" {title} "
    pad = (inner - len(t)) // 2
    lines.append(f"  |{' ' * pad}{t}{' ' * (inner - pad - len(t))}|")
    lines.append(f"  +{'-' * inner}+")

    for line in content_lines:
        # Truncate if needed
        text = line[:inner - 2] if len(line) > inner - 2 else line
        lines.append(f"  | {text:<{inner - 2}} |")

    lines.append(f"  +{'=' * inner}+")
    return "\n".join(lines)


def toolbar(items, active=None):
    """Render a horizontal toolbar like the IDE tabs."""
    parts = []
    for item in items:
        if item == active:
            parts.append(f"[{item}]")
        else:
            parts.append(f" {item} ")
    bar = " | ".join(parts)
    width = min(get_terminal_width() - 4, len(bar) + 4)
    border = "-" * (width + 2)
    return f"  +{border}+\n  | {bar:<{width}} |\n  +{border}+"


def sidebar_panel(title, items, width=30):
    """Render a sidebar-style panel."""
    inner = width - 2
    lines = []
    lines.append(f"+{'-' * inner}+")
    t = f" {title} "
    pad = (inner - len(t)) // 2
    lines.append(f"|{' ' * pad}{t}{' ' * (inner - pad - len(t))}|")
    lines.append(f"+{'-' * inner}+")
    for item in items:
        text = item[:inner - 2] if len(item) > inner - 2 else item
        lines.append(f"| {text:<{inner - 2}} |")
    lines.append(f"+{'-' * inner}+")
    return "\n".join(lines)


def status_bar(left="", center="", right=""):
    """Render a bottom status bar."""
    width = min(get_terminal_width() - 4, 72)
    center_pad = (width - len(left) - len(right) - len(center)) // 2
    if center_pad < 1:
        center_pad = 1
    bar = f"{left}{' ' * center_pad}{center}{' ' * center_pad}{right}"
    bar = bar[:width]
    return f"  [{bar:<{width}}]"


def header():
    """Render the studio header/banner."""
    return """
  ____  _            _    ____                 _   ____  _             _ _
 | __ )| | __ _  ___| | _|  _ \\ ___   __ _  __| | / ___|| |_ _   _  __| (_) ___
 |  _ \\| |/ _` |/ __| |/ / |_) / _ \\ / _` |/ _` | \\___ \\| __| | | |/ _` | |/ _ \\
 | |_) | | (_| | (__|   <|  _ < (_) | (_| | (_| |  ___) | |_| |_| | (_| | | (_) |
 |____/|_|\\__,_|\\___|_|\\_\\_| \\_\\___/ \\__,_|\\__,_| |____/ \\__|\\__,_|\\__,_|_|\\___/

  Form Builder & Project Studio                                    v0.1.0
"""


def component_palette():
    """Show the component palette (toolbar items from the screenshot)."""
    items = ["Forms", "Input", "T_Field", "Label", "Radio", "Checkbox", "Submit", "Name", "Select"]
    return toolbar(items)


def splash():
    """Render the full splash screen mimicking the visual IDE."""
    lines = []
    lines.append(header())
    lines.append(component_palette())
    lines.append("")
    lines.append(box("Canvas", [
        "",
        "     Welcome to BlackRoad Studio CLI",
        "",
        "     The visual form builder, now in your terminal.",
        "     Build forms, preview them, and export to HTML.",
        "",
        "     Type 'help' to see available commands.",
        "     Type 'new' to create a new form.",
        "     Type 'demo' to see a sample form.",
        "",
    ]))
    lines.append("")
    lines.append(status_bar("READY", "BlackRoad Studio", "v0.1.0"))
    return "\n".join(lines)
