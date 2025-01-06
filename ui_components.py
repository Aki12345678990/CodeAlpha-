import tkinter as tk
from colors import Colors

def create_button(parent, text, command, color, **kwargs):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Helvetica", 12),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief=tk.FLAT,
        padx=20,
        pady=10,
        cursor="hand2",
        **kwargs
    )

def create_label(parent, text, size=12, bold=False):
    font_weight = "bold" if bold else "normal"
    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", size, font_weight),
        bg=Colors.BACKGROUND,
        fg=Colors.TEXT
    )