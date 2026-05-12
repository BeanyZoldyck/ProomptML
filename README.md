# PoomptML

An XML tag helper for writing prompts. Built with Python and customtkinter.

## What it does

PoomptML gives you a quick way to insert XML tags while writing prompts. Press `Ctrl+Space` to open a palette, type a tag name, and hit Enter. The app inserts `<tag></tag>` with your cursor positioned inside the opening and closing tags.

The editor is a plain text area with monospace font. Whatever you've written gets copied to your clipboard when you press `Shift+Enter` or `Ctrl+Enter`.

## Usage

- `Ctrl+Space` — open the tag palette
- `Enter` (in palette) — insert the tag and close the palette
- `Escape` — cancel
- `Shift+Enter` or `Ctrl+Enter` — copy entire editor contents to clipboard

If `Ctrl+Space` is captured by your IME or OS, change `TAG_PALETTE_SEQUENCE` at the top of `main.py` to something like `<Control-q>` or `<F2>`.

## Tag name rules

Tag names must start with a letter or underscore, followed by any combination of letters, numbers, dots, underscores, hyphens, or colons. So `role`, `context`, `examples`, `user_profile_1` are all valid.

## Running

```bash
python main.py
```

Requires Python 3.10+ and customtkinter (`pip install custom-tkinter`).
