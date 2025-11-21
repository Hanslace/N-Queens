# main.py
import tkinter as tk
from gui.interface import AppUI
import sys

def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
