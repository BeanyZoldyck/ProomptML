"""
PoomptML — XML prompt helper.
Ctrl+Space: tag palette. Enter in palette: insert <tag></tag>, caret inside.
Shift+Enter / Ctrl+Enter: copy full editor to clipboard.
Alternate shortcut if Ctrl+Space is captured by IME/OS: change TAG_PALETTE_SEQUENCE below.
"""

from __future__ import annotations

import re
import tkinter as tk

import customtkinter as ctk

# If Ctrl+Space is captured globally, try e.g. "<Control-q>" or "<F2>".
TAG_PALETTE_SEQUENCE = "<Control-space>"

TAG_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:\-]*$")


def _mono_font(size: int = 14) -> ctk.CTkFont:
    return ctk.CTkFont(family="Consolas", size=size)


class TagPalette(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, app: "PoomptApp") -> None:
        super().__init__(master)
        self.app = app
        self.title("Insert tag")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.transient(master)

        self._frame = ctk.CTkFrame(self, corner_radius=12)
        self._frame.pack(fill="both", expand=True, padx=12, pady=12)

        self._hint = ctk.CTkLabel(
            self._frame,
            text="Tag name (Enter to insert, Esc to cancel)",
            font=ctk.CTkFont(size=12),
        )
        self._hint.pack(anchor="w", pady=(0, 6))

        self._entry = ctk.CTkEntry(self._frame, width=280, placeholder_text="e.g. role")
        self._entry.pack(fill="x")

        self._error = ctk.CTkLabel(
            self._frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        )
        self._error.pack(anchor="w", pady=(6, 0))

        self._entry.bind("<Return>", self._on_submit)
        self._entry.bind("<Escape>", self._on_cancel)
        self.protocol("WM_DELETE_WINDOW", self._close)

        self.bind("<Escape>", self._on_cancel)

    def open_at_editor(self) -> None:
        self._error.configure(text="")
        self._entry.delete(0, "end")
        self.update_idletasks()
        self.geometry(
            f"+{self.master.winfo_rootx() + 48}+{self.master.winfo_rooty() + 48}"
        )
        self.deiconify()
        self.lift()
        self._entry.focus_set()

    def _on_submit(self, _event: tk.Event | None = None) -> str | None:
        raw = self._entry.get().strip()
        if not TAG_NAME_RE.match(raw):
            self._error.configure(
                text="Invalid XML name (use letter/_ first, then alnum . - _ :)"
            )
            return "break"
        self.app.insert_tag_at_cursor(raw)
        self._close()
        return "break"

    def _on_cancel(self, _event: tk.Event | None = None) -> str | None:
        self._close()
        return "break"

    def _close(self) -> None:
        self.withdraw()
        try:
            self.app.focus_text()
        except tk.TclError:
            pass


class PoomptApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("PoomptML")
        self.geometry("720x480")
        self.minsize(480, 320)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        mono = _mono_font(14)
        self._text = ctk.CTkTextbox(
            self,
            font=mono,
            wrap="none",
            corner_radius=10,
            border_width=1,
        )
        self._text.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))

        self._status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        self._status.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        self._status_after_id: str | None = None
        self._tag_palette = TagPalette(self, self)
        self._tag_palette.withdraw()

        tw = self._text._textbox  # noqa: SLF001 — planned integration with Tk Text
        tw.bind(TAG_PALETTE_SEQUENCE, self._open_tag_palette)
        tw.bind("<Shift-Return>", self._copy_all)
        tw.bind("<Control-Return>", self._copy_all)

        self.bind(TAG_PALETTE_SEQUENCE, self._open_tag_palette_root)

    def focus_text(self) -> None:
        self._text.focus_set()

    def _open_tag_palette_root(self, event: tk.Event) -> str | None:
        if event.widget is self:
            return self._open_tag_palette(event)
        return None

    def _open_tag_palette(self, _event: tk.Event) -> str | None:
        self._tag_palette.open_at_editor()
        return "break"

    def insert_tag_at_cursor(self, name: str) -> None:
        tw = self._text._textbox  # noqa: SLF001
        opening = f"<{name}>"
        closing = f"</{name}>"
        chunk = f"{opening}{closing}"
        idx = tw.index("insert")
        tw.insert(idx, chunk)
        inner = f"{idx}+{len(opening)}c"
        tw.mark_set("insert", inner)
        tw.see("insert")

    def _copy_all(self, _event: tk.Event) -> str | None:
        body = self._text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(body)
        self.update()
        self._flash_status("Copied to clipboard")
        return "break"

    def _flash_status(self, message: str, ms: int = 1500) -> None:
        self._status.configure(text=message)
        if self._status_after_id:
            self.after_cancel(self._status_after_id)
        self._status_after_id = self.after(ms, self._clear_status)

    def _clear_status(self) -> None:
        self._status.configure(text="")
        self._status_after_id = None


def main() -> None:
    app = PoomptApp()
    app.mainloop()


if __name__ == "__main__":
    main()
