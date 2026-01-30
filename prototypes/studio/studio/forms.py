"""
BlackRoad Studio - Form Builder Engine

Manages form definitions with components:
Forms, Input, T_Field, Label, Radio, Checkbox, Submit, Name, Select
"""

import json
import os
from pathlib import Path


# ─── Component Types ───────────────────────────────────────────────

COMPONENT_TYPES = {
    "input": {"tag": "input", "attrs": ["name", "type", "placeholder", "required", "value"]},
    "t_field": {"tag": "textarea", "attrs": ["name", "rows", "cols", "placeholder", "required"]},
    "label": {"tag": "label", "attrs": ["for", "text"]},
    "radio": {"tag": "input[radio]", "attrs": ["name", "value", "options", "required"]},
    "checkbox": {"tag": "input[checkbox]", "attrs": ["name", "value", "checked"]},
    "submit": {"tag": "button[submit]", "attrs": ["text", "action"]},
    "name": {"tag": "input[name]", "attrs": ["first", "last", "placeholder", "required"]},
    "select": {"tag": "select", "attrs": ["name", "options", "placeholder", "required", "multiple"]},
}


class Component:
    """A single form component."""

    def __init__(self, ctype, **kwargs):
        if ctype not in COMPONENT_TYPES:
            raise ValueError(f"Unknown component type: {ctype}. Valid: {', '.join(COMPONENT_TYPES)}")
        self.ctype = ctype
        self.props = kwargs
        self.id = kwargs.get("name", f"{ctype}_{id(self) % 10000}")

    def to_dict(self):
        return {"type": self.ctype, "id": self.id, "props": self.props}

    @classmethod
    def from_dict(cls, data):
        c = cls(data["type"], **data.get("props", {}))
        c.id = data.get("id", c.id)
        return c

    def render_preview(self, width=48):
        """Render a terminal preview of this component."""
        ctype = self.ctype
        props = self.props

        if ctype == "label":
            text = props.get("text", "Label")
            return f"  {text}"

        if ctype == "input":
            ph = props.get("placeholder", "Enter text...")
            name = props.get("name", "field")
            req = " *" if props.get("required") else ""
            return f"  [{name}{req}]: [{ph:.<{width - len(name) - 8}}]"

        if ctype == "t_field":
            ph = props.get("placeholder", "Enter text...")
            rows = props.get("rows", 3)
            name = props.get("name", "textarea")
            lines = [f"  [{name}]:"]
            lines.append(f"  +{'-' * (width - 4)}+")
            for i in range(rows):
                content = ph if i == 0 else ""
                lines.append(f"  |{content:<{width - 4}}|")
            lines.append(f"  +{'-' * (width - 4)}+")
            return "\n".join(lines)

        if ctype == "radio":
            name = props.get("name", "option")
            options = props.get("options", ["Option 1", "Option 2"])
            lines = [f"  {name}:"]
            for opt in options:
                lines.append(f"    ( ) {opt}")
            return "\n".join(lines)

        if ctype == "checkbox":
            name = props.get("name", "check")
            value = props.get("value", name)
            checked = "[x]" if props.get("checked") else "[ ]"
            return f"  {checked} {value}"

        if ctype == "submit":
            text = props.get("text", "Submit")
            pad = (width - len(text) - 4) // 2
            return f"  {'.' * pad}[ {text} ]{'.' * pad}"

        if ctype == "name":
            return (
                f"  [First Name]: [{'.' * (width // 2 - 10)}]  "
                f"[Last Name]: [{'.' * (width // 2 - 10)}]"
            )

        if ctype == "select":
            name = props.get("name", "select")
            ph = props.get("placeholder", "Choose...")
            return f"  [{name}]: [ {ph} v ]"

        return f"  <{ctype}>"


class Form:
    """A complete form with ordered components."""

    def __init__(self, name="Untitled Form"):
        self.name = name
        self.components = []

    def add(self, component):
        self.components.append(component)
        return self

    def remove(self, index):
        if 0 <= index < len(self.components):
            return self.components.pop(index)
        return None

    def move(self, from_idx, to_idx):
        if 0 <= from_idx < len(self.components) and 0 <= to_idx < len(self.components):
            comp = self.components.pop(from_idx)
            self.components.insert(to_idx, comp)
            return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "components": [c.to_dict() for c in self.components],
        }

    @classmethod
    def from_dict(cls, data):
        form = cls(data.get("name", "Untitled"))
        for cd in data.get("components", []):
            form.add(Component.from_dict(cd))
        return form

    def render_preview(self, width=52):
        """Render a full terminal preview of the form."""
        lines = []
        border = "=" * width
        lines.append(f"  +{border}+")
        title = f" {self.name} "
        pad = (width - len(title)) // 2
        lines.append(f"  |{' ' * pad}{title}{' ' * (width - pad - len(title))}|")
        lines.append(f"  +{'-' * width}+")
        lines.append(f"  |{' ' * width}|")

        for comp in self.components:
            preview = comp.render_preview(width - 6)
            for pline in preview.split("\n"):
                # Strip leading spaces and re-pad inside the box
                clean = pline.strip()
                lines.append(f"  | {clean:<{width - 2}} |")
            lines.append(f"  |{' ' * width}|")

        lines.append(f"  +{border}+")
        return "\n".join(lines)

    def export_html(self):
        """Export as HTML form string."""
        parts = [f'<form name="{self.name}">']
        for comp in self.components:
            ct = comp.ctype
            p = comp.props

            if ct == "label":
                parts.append(f'  <label for="{p.get("for", "")}">{p.get("text", "")}</label>')

            elif ct == "input":
                req = " required" if p.get("required") else ""
                parts.append(
                    f'  <input type="{p.get("type", "text")}" '
                    f'name="{p.get("name", "")}" '
                    f'placeholder="{p.get("placeholder", "")}"{req} />'
                )

            elif ct == "t_field":
                req = " required" if p.get("required") else ""
                parts.append(
                    f'  <textarea name="{p.get("name", "")}" '
                    f'rows="{p.get("rows", 3)}" '
                    f'placeholder="{p.get("placeholder", "")}"{req}></textarea>'
                )

            elif ct == "radio":
                for opt in p.get("options", []):
                    parts.append(
                        f'  <label><input type="radio" name="{p.get("name", "")}" '
                        f'value="{opt}" /> {opt}</label>'
                    )

            elif ct == "checkbox":
                chk = " checked" if p.get("checked") else ""
                parts.append(
                    f'  <label><input type="checkbox" name="{p.get("name", "")}" '
                    f'value="{p.get("value", "")}"{chk} /> {p.get("value", "")}</label>'
                )

            elif ct == "submit":
                parts.append(f'  <button type="submit">{p.get("text", "Submit")}</button>')

            elif ct == "name":
                req = " required" if p.get("required") else ""
                parts.append(f'  <input type="text" name="first_name" placeholder="First Name"{req} />')
                parts.append(f'  <input type="text" name="last_name" placeholder="Last Name"{req} />')

            elif ct == "select":
                req = " required" if p.get("required") else ""
                mult = " multiple" if p.get("multiple") else ""
                parts.append(f'  <select name="{p.get("name", "")}" {req}{mult}>')
                if p.get("placeholder"):
                    parts.append(f'    <option value="">{p["placeholder"]}</option>')
                for opt in p.get("options", []):
                    parts.append(f'    <option value="{opt}">{opt}</option>')
                parts.append("  </select>")

        parts.append("</form>")
        return "\n".join(parts)


class FormStore:
    """Persist forms to disk as JSON."""

    def __init__(self, store_dir=None):
        if store_dir is None:
            store_dir = os.path.join(os.path.expanduser("~"), ".blackroad", "studio", "forms")
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def save(self, form):
        path = self.store_dir / f"{self._slug(form.name)}.json"
        path.write_text(json.dumps(form.to_dict(), indent=2))
        return str(path)

    def load(self, name):
        path = self.store_dir / f"{self._slug(name)}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return Form.from_dict(data)

    def list_forms(self):
        forms = []
        for f in sorted(self.store_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                forms.append(data.get("name", f.stem))
            except Exception:
                forms.append(f.stem)
        return forms

    def delete(self, name):
        path = self.store_dir / f"{self._slug(name)}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    def _slug(self, name):
        return name.lower().replace(" ", "_").replace("/", "_")
