import os
import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader, PdfWriter


def choose_input_file():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select input PDF",
        filetypes=[("PDF files", "*.pdf")],
    )
    root.destroy()
    return path


def choose_output_dir():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Select output folder")
    root.destroy()
    return path


def choose_chapters_file():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select chapters config file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    root.destroy()
    return path


def load_chapters(config_path):
    chapters = []
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            name, start, end = parts[0], int(parts[1]), int(parts[2])
            chapters.append((name, start, end))
    return chapters


def split_by_chapters(input_pdf, output_dir, chapters):
    """
    chapters = [
        ("chapter1.pdf", 0, 10),
        ("chapter2.pdf", 10, 25),
        ("chapter3.pdf", 25, 40),
    ]
    """
    reader = PdfReader(input_pdf)

    for name, start, end in chapters:
        writer = PdfWriter()

        for i in range(start, end):
            writer.add_page(reader.pages[i])

        out_path = os.path.join(output_dir, name)
        with open(out_path, "wb") as f:
            writer.write(f)

        print(f"Created: {out_path}")


# --- main ---
input_pdf = choose_input_file()
if not input_pdf:
    print("No input file selected.")
    exit()

output_dir = choose_output_dir()
if not output_dir:
    print("No output folder selected.")
    exit()

chapters_file = choose_chapters_file()
if not chapters_file:
    print("No chapters config file selected.")
    exit()

chapters = load_chapters(chapters_file)
split_by_chapters(input_pdf, output_dir, chapters)