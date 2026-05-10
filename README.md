# ProomptML

XML prompt generation for OpenCode. Write structured prompts fast.

There's also a Python GUI for clipboard-based workflows, but this is the main event.

## Install globally (all projects)

Copy two files to your OpenCode config directory:

```
~/.config/opencode/
├── commands/
│   └── xml.md
└── plugins/
    └── xml-prompt.js
```

Restart OpenCode. That's it — `/xml` works everywhere now.

## Install per-project

Either clone this repo and run OpenCode from inside it, or copy the `.opencode/` folder into your own project. OpenCode discovers plugins and commands automatically.

## Usage

Type `/xml` followed by your prompt parts:

```
/xml task build a REST API
context user management with roles and permissions
constraints Node.js only, use Express
output_format JSON responses
```

Submit (Shift+Enter between lines), and the plugin transforms it into:

```xml
<task>build a REST API</task>
<context>user management with roles and permissions</context>
<constraints>Node.js only, use Express</constraints>
<output_format>JSON responses</output_format>
```

Each line becomes a tag. The first word is the tag name, everything after is the content. Lines starting with `#` are ignored. A bare word with no content becomes a self-closing tag.

## How it works

- **`.opencode/commands/xml.md`** registers `/xml` as a valid command. Without it, OpenCode doesn't know the command exists.
- **`.opencode/plugins/xml-prompt.js`** hooks into `command.execute.before`. It takes the arguments (your raw text), splits by newline, wraps each line in XML tags, and mutates the parts array in place.

The plugin only activates for the `xml` command, so other commands pass through unchanged.

## Python GUI

`main.py` is a standalone XML editor using customtkinter. No OpenCode needed — paste the output anywhere.

```bash
pip install -r requirements.txt
python main.py
```

- `Ctrl+Space` opens a tag palette. Type a name, hit Enter — inserts `<tag></tag>` with the cursor inside.
- `Shift+Enter` or `Ctrl+Enter` copies the full editor content to your clipboard.

## File layout

```
.
├── .opencode/
│   ├── commands/
│   │   └── xml.md          # registers /xml command
│   └── plugins/
│       └── xml-prompt.js   # transforms arguments to XML tags
├── main.py                  # Python GUI (standalone)
└── requirements.txt
```
