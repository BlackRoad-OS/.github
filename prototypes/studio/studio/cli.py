#!/usr/bin/env python3
"""
BlackRoad Studio CLI

The visual form builder & project studio as a terminal interface.

Usage:
    python -m studio.cli                    # Interactive mode
    python -m studio.cli new "My Form"      # Create a new form
    python -m studio.cli add <type>         # Add component to current form
    python -m studio.cli preview            # Preview current form
    python -m studio.cli list               # List saved forms
    python -m studio.cli export <name>      # Export form to HTML
    python -m studio.cli demo               # Show demo form
    python -m studio.cli palette            # Show component palette
"""

import sys
import argparse

from .forms import Component, Form, FormStore, COMPONENT_TYPES
from .renderer import (
    header, component_palette, splash, box, toolbar,
    sidebar_panel, status_bar
)


# ─── State ──────────────────────────────────────────────────────────

_current_form = None
_store = FormStore()


def _get_form():
    global _current_form
    if _current_form is None:
        _current_form = Form("Untitled Form")
    return _current_form


# ─── Commands ───────────────────────────────────────────────────────

def cmd_new(args):
    """Create a new form."""
    global _current_form
    name = " ".join(args.name) if args.name else "Untitled Form"
    _current_form = Form(name)
    print(f"\n  Created new form: {name}")
    print(f"  Use 'add <type>' to add components.")
    print(f"  Components: {', '.join(COMPONENT_TYPES.keys())}\n")


def cmd_add(args):
    """Add a component to the current form."""
    form = _get_form()
    ctype = args.type.lower() if args.type else None

    if not ctype:
        print("\n  Usage: add <type> [--name NAME] [--placeholder TEXT] ...")
        print(f"  Types: {', '.join(COMPONENT_TYPES.keys())}\n")
        return

    if ctype not in COMPONENT_TYPES:
        print(f"\n  Unknown component: {ctype}")
        print(f"  Valid types: {', '.join(COMPONENT_TYPES.keys())}\n")
        return

    # Build props from extra args
    props = {}
    if args.name_attr:
        props["name"] = args.name_attr
    if args.placeholder:
        props["placeholder"] = args.placeholder
    if args.text:
        props["text"] = args.text
    if args.options:
        props["options"] = [o.strip() for o in args.options.split(",")]
    if args.required:
        props["required"] = True
    if args.rows:
        props["rows"] = int(args.rows)
    if args.value:
        props["value"] = args.value

    # Defaults
    if ctype == "label" and "text" not in props:
        props["text"] = props.get("name", "Label")
    if ctype == "submit" and "text" not in props:
        props["text"] = "Submit"
    if ctype == "radio" and "options" not in props:
        props["options"] = ["Option 1", "Option 2", "Option 3"]
    if ctype == "select" and "options" not in props:
        props["options"] = ["Choice 1", "Choice 2", "Choice 3"]

    comp = Component(ctype, **props)
    form.add(comp)

    print(f"\n  Added {ctype} to '{form.name}'")
    print(f"  Components: {len(form.components)}")
    print(f"\n  Preview:")
    print(comp.render_preview())
    print()


def cmd_remove(args):
    """Remove a component by index."""
    form = _get_form()
    if args.index is None:
        print("\n  Usage: remove <index>")
        print(f"  Form has {len(form.components)} components (0-indexed)\n")
        return

    removed = form.remove(args.index)
    if removed:
        print(f"\n  Removed {removed.ctype} from position {args.index}\n")
    else:
        print(f"\n  Invalid index: {args.index}\n")


def cmd_preview(args):
    """Preview the current form."""
    form = _get_form()
    if not form.components:
        print("\n  Form is empty. Use 'add <type>' to add components.\n")
        return
    print()
    print(form.render_preview())
    print()


def cmd_list(args):
    """List all saved forms."""
    forms = _store.list_forms()
    if not forms:
        print("\n  No saved forms. Use 'save' to save the current form.\n")
        return

    print()
    print(box("Saved Forms", [f"  {i+1}. {f}" for i, f in enumerate(forms)]))
    print()


def cmd_save(args):
    """Save the current form."""
    form = _get_form()
    if args.name:
        form.name = " ".join(args.name)
    path = _store.save(form)
    print(f"\n  Saved '{form.name}' to {path}\n")


def cmd_load(args):
    """Load a saved form."""
    global _current_form
    if not args.name:
        print("\n  Usage: load <form-name>\n")
        return

    name = " ".join(args.name)
    form = _store.load(name)
    if form:
        _current_form = form
        print(f"\n  Loaded '{form.name}' ({len(form.components)} components)\n")
    else:
        print(f"\n  Form '{name}' not found. Use 'list' to see saved forms.\n")


def cmd_export(args):
    """Export form as HTML."""
    form = _get_form()
    if not form.components:
        print("\n  Form is empty. Nothing to export.\n")
        return

    html = form.export_html()

    if args.output:
        with open(args.output, "w") as f:
            f.write(html)
        print(f"\n  Exported to {args.output}\n")
    else:
        print()
        print(box("HTML Export", html.split("\n")))
        print()


def cmd_palette(args):
    """Show the component palette."""
    print()
    print(component_palette())
    print()
    print("  Available Components:")
    print("  " + "-" * 50)
    for name, info in COMPONENT_TYPES.items():
        attrs = ", ".join(info["attrs"][:4])
        print(f"    {name:<12} <{info['tag']}>  attrs: {attrs}")
    print()


def cmd_demo(args):
    """Show a demo form."""
    form = Form("Contact Us")
    form.add(Component("label", text="Get in Touch", **{"for": "email"}))
    form.add(Component("name", required=True))
    form.add(Component("input", name="email", type="email", placeholder="your@email.com", required=True))
    form.add(Component("input", name="phone", type="tel", placeholder="(555) 123-4567"))
    form.add(Component("select", name="subject", placeholder="Select a topic...",
                        options=["General Inquiry", "Support", "Partnership", "Feedback"]))
    form.add(Component("t_field", name="message", placeholder="Your message here...", rows=4, required=True))
    form.add(Component("radio", name="priority", options=["Low", "Medium", "High"]))
    form.add(Component("checkbox", name="newsletter", value="Subscribe to newsletter"))
    form.add(Component("submit", text="Send Message"))

    print()
    print(form.render_preview())
    print()
    print(status_bar(f"Components: {len(form.components)}", form.name, "DEMO"))
    print()


def cmd_components(args):
    """List components in the current form."""
    form = _get_form()
    if not form.components:
        print(f"\n  '{form.name}' has no components.\n")
        return

    print()
    print(f"  {form.name}")
    print("  " + "=" * 40)
    for i, comp in enumerate(form.components):
        props_str = ", ".join(f"{k}={v}" for k, v in list(comp.props.items())[:3])
        print(f"  {i:3}. [{comp.ctype:<10}] {props_str}")
    print()
    print(f"  Total: {len(form.components)} components")
    print()


def cmd_delete(args):
    """Delete a saved form."""
    if not args.name:
        print("\n  Usage: delete <form-name>\n")
        return
    name = " ".join(args.name)
    if _store.delete(name):
        print(f"\n  Deleted '{name}'\n")
    else:
        print(f"\n  Form '{name}' not found.\n")


# ─── Interactive Mode ───────────────────────────────────────────────

def cmd_interactive(args):
    """Launch interactive studio mode."""
    global _current_form

    print(splash())

    while True:
        form = _get_form()
        prompt_text = f"  studio [{form.name}]> "

        try:
            raw = input(prompt_text).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye!")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        rest = parts[1:]

        if cmd in ("quit", "exit", "q"):
            print("  Goodbye!")
            break

        elif cmd == "help":
            _show_help()

        elif cmd == "new":
            name = " ".join(rest) if rest else "Untitled Form"
            _current_form = Form(name)
            print(f"\n  Created: {name}\n")

        elif cmd == "add":
            if not rest:
                print(f"\n  Usage: add <type> [key=value ...]\n  Types: {', '.join(COMPONENT_TYPES)}\n")
                continue
            ctype = rest[0].lower()
            if ctype not in COMPONENT_TYPES:
                print(f"\n  Unknown: {ctype}. Types: {', '.join(COMPONENT_TYPES)}\n")
                continue
            props = _parse_inline_props(rest[1:], ctype)
            comp = Component(ctype, **props)
            form.add(comp)
            print(f"\n  + {ctype}")
            print(comp.render_preview())
            print()

        elif cmd == "remove" or cmd == "rm":
            if rest and rest[0].isdigit():
                removed = form.remove(int(rest[0]))
                if removed:
                    print(f"\n  Removed {removed.ctype} at index {rest[0]}\n")
                else:
                    print(f"\n  Invalid index\n")
            else:
                print("\n  Usage: remove <index>\n")

        elif cmd in ("preview", "view", "show"):
            if form.components:
                print()
                print(form.render_preview())
                print()
            else:
                print("\n  Form is empty.\n")

        elif cmd in ("components", "list-components", "lc"):
            if form.components:
                print()
                for i, c in enumerate(form.components):
                    props_str = ", ".join(f"{k}={v}" for k, v in list(c.props.items())[:3])
                    print(f"  {i:3}. [{c.ctype:<10}] {props_str}")
                print()
            else:
                print("\n  No components.\n")

        elif cmd == "save":
            if rest:
                form.name = " ".join(rest)
            path = _store.save(form)
            print(f"\n  Saved: {path}\n")

        elif cmd == "load":
            if not rest:
                print("\n  Usage: load <name>\n")
                continue
            name = " ".join(rest)
            loaded = _store.load(name)
            if loaded:
                _current_form = loaded
                print(f"\n  Loaded: {loaded.name} ({len(loaded.components)} components)\n")
            else:
                print(f"\n  Not found: {name}\n")

        elif cmd == "list" or cmd == "ls":
            forms = _store.list_forms()
            if forms:
                print()
                for i, f in enumerate(forms):
                    print(f"  {i+1}. {f}")
                print()
            else:
                print("\n  No saved forms.\n")

        elif cmd == "export":
            if not form.components:
                print("\n  Form is empty.\n")
                continue
            html = form.export_html()
            if rest:
                with open(rest[0], "w") as f:
                    f.write(html)
                print(f"\n  Exported to {rest[0]}\n")
            else:
                print()
                for line in html.split("\n"):
                    print(f"  {line}")
                print()

        elif cmd == "delete" or cmd == "del":
            if rest:
                name = " ".join(rest)
                if _store.delete(name):
                    print(f"\n  Deleted: {name}\n")
                else:
                    print(f"\n  Not found: {name}\n")
            else:
                print("\n  Usage: delete <name>\n")

        elif cmd == "palette":
            print()
            print(component_palette())
            print()

        elif cmd == "demo":
            _ns = argparse.Namespace()
            cmd_demo(_ns)

        elif cmd == "rename":
            if rest:
                form.name = " ".join(rest)
                print(f"\n  Renamed to: {form.name}\n")
            else:
                print("\n  Usage: rename <new name>\n")

        elif cmd == "clear":
            form.components.clear()
            print("\n  Cleared all components.\n")

        elif cmd == "move":
            if len(rest) >= 2 and rest[0].isdigit() and rest[1].isdigit():
                if form.move(int(rest[0]), int(rest[1])):
                    print(f"\n  Moved {rest[0]} -> {rest[1]}\n")
                else:
                    print("\n  Invalid indices.\n")
            else:
                print("\n  Usage: move <from> <to>\n")

        elif cmd == "status":
            print()
            print(status_bar(
                f"Form: {form.name}",
                f"Components: {len(form.components)}",
                f"Saved: {len(_store.list_forms())}"
            ))
            print()

        else:
            print(f"\n  Unknown command: {cmd}")
            print("  Type 'help' for available commands.\n")


def _show_help():
    """Show interactive help."""
    print()
    print(box("Studio Commands", [
        "",
        "  Form Management:",
        "    new [name]         Create a new form",
        "    save [name]        Save current form",
        "    load <name>        Load a saved form",
        "    list / ls          List saved forms",
        "    delete <name>      Delete a saved form",
        "    rename <name>      Rename current form",
        "",
        "  Components:",
        "    add <type> [...]   Add component (key=value props)",
        "    remove <index>     Remove component by index",
        "    move <from> <to>   Reorder components",
        "    components / lc    List components in form",
        "    clear              Remove all components",
        "    palette            Show component types",
        "",
        "  Display:",
        "    preview / view     Preview the form",
        "    demo               Show demo form",
        "    export [file]      Export as HTML",
        "    status             Show status bar",
        "",
        "  General:",
        "    help               Show this help",
        "    quit / exit        Exit studio",
        "",
    ]))
    print()


def _parse_inline_props(parts, ctype):
    """Parse inline key=value props from interactive mode."""
    props = {}
    for part in parts:
        if "=" in part:
            key, val = part.split("=", 1)
            if key == "options":
                props[key] = [v.strip() for v in val.split(",")]
            elif key == "required":
                props[key] = val.lower() in ("true", "1", "yes")
            elif key == "checked":
                props[key] = val.lower() in ("true", "1", "yes")
            elif key == "rows":
                props[key] = int(val)
            else:
                props[key] = val
        else:
            # Positional: first positional is name/text depending on type
            if ctype == "label":
                props.setdefault("text", part)
            elif ctype == "submit":
                props.setdefault("text", part)
            else:
                props.setdefault("name", part)

    # Defaults
    if ctype == "label" and "text" not in props:
        props["text"] = "Label"
    if ctype == "submit" and "text" not in props:
        props["text"] = "Submit"
    if ctype == "radio" and "options" not in props:
        props["options"] = ["Option 1", "Option 2", "Option 3"]
    if ctype == "select" and "options" not in props:
        props["options"] = ["Choice 1", "Choice 2", "Choice 3"]

    return props


# ─── Main Entry ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BlackRoad Studio - Form Builder & Project Studio CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           Interactive mode
  %(prog)s new "Contact Form"        Create a new form
  %(prog)s add input --name email    Add an input component
  %(prog)s preview                   Preview the current form
  %(prog)s export --output form.html Export to HTML
  %(prog)s demo                      Show a demo form
  %(prog)s palette                   Show component palette
  %(prog)s list                      List saved forms
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # new
    new_p = subparsers.add_parser("new", help="Create a new form")
    new_p.add_argument("name", nargs="*", help="Form name")

    # add
    add_p = subparsers.add_parser("add", help="Add a component")
    add_p.add_argument("type", nargs="?", help="Component type")
    add_p.add_argument("--name-attr", "-n", help="Component name attribute")
    add_p.add_argument("--placeholder", "-p", help="Placeholder text")
    add_p.add_argument("--text", "-t", help="Label/button text")
    add_p.add_argument("--options", "-o", help="Comma-separated options")
    add_p.add_argument("--required", "-r", action="store_true", help="Required field")
    add_p.add_argument("--rows", help="Textarea rows")
    add_p.add_argument("--value", "-v", help="Value")

    # remove
    rm_p = subparsers.add_parser("remove", help="Remove a component")
    rm_p.add_argument("index", type=int, nargs="?", help="Component index")

    # preview
    subparsers.add_parser("preview", help="Preview the current form")

    # components
    subparsers.add_parser("components", help="List components in form")

    # save
    save_p = subparsers.add_parser("save", help="Save the current form")
    save_p.add_argument("name", nargs="*", help="Form name")

    # load
    load_p = subparsers.add_parser("load", help="Load a saved form")
    load_p.add_argument("name", nargs="*", help="Form name")

    # list
    subparsers.add_parser("list", help="List saved forms")

    # export
    export_p = subparsers.add_parser("export", help="Export form as HTML")
    export_p.add_argument("--output", "-o", help="Output file path")

    # delete
    del_p = subparsers.add_parser("delete", help="Delete a saved form")
    del_p.add_argument("name", nargs="*", help="Form name")

    # palette
    subparsers.add_parser("palette", help="Show component palette")

    # demo
    subparsers.add_parser("demo", help="Show demo form")

    args = parser.parse_args()

    commands = {
        "new": cmd_new,
        "add": cmd_add,
        "remove": cmd_remove,
        "preview": cmd_preview,
        "components": cmd_components,
        "save": cmd_save,
        "load": cmd_load,
        "list": cmd_list,
        "export": cmd_export,
        "delete": cmd_delete,
        "palette": cmd_palette,
        "demo": cmd_demo,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        cmd_interactive(args)


if __name__ == "__main__":
    main()
