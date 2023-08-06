import tkinter as tk
import _tkinter
from huoyanlib import _raise_huoyanerror_tcl


def make_window(size_height, size_width, title):
    window = tk.Tk()
    try:
        window.title(title)
    except _tkinter.TclError:
        _raise_huoyanerror_tcl()

    try:
        window.geometry(str(size_height) + 'x' + str(size_width))
    except _tkinter.TclError:
        _raise_huoyanerror_tcl()



