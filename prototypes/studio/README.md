# BlackRoad Studio CLI

The visual form builder & project studio, converted to a terminal interface.

## Quick Start

```bash
# Interactive mode
python -m studio.cli

# Show demo form
python -m studio.cli demo

# Show component palette
python -m studio.cli palette
```

## Commands

| Command | Description |
|---------|-------------|
| `new [name]` | Create a new form |
| `add <type>` | Add component (input, t_field, label, radio, checkbox, submit, name, select) |
| `remove <index>` | Remove component by index |
| `preview` | Preview the current form in terminal |
| `components` | List all components |
| `save [name]` | Save form to disk |
| `load <name>` | Load a saved form |
| `list` | List saved forms |
| `export [--output file]` | Export as HTML |
| `delete <name>` | Delete a saved form |
| `palette` | Show available component types |
| `demo` | Show a demo contact form |

## Interactive Mode

Run without arguments to enter interactive mode:

```
studio [Contact Form]> add label text=Email
studio [Contact Form]> add input name=email placeholder=you@example.com required=true
studio [Contact Form]> add submit text="Send"
studio [Contact Form]> preview
studio [Contact Form]> export form.html
```
