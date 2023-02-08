import os
import tkinter as tk
from tkinter import filedialog

def read_file_path(file_restriction = ''):
    root = tk.Tk()
    root.withdraw()
    root.update()

    if 'txt' in file_restriction:
        return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    else:
        return filedialog.askopenfilename()

def create_new_file_path():
    root = tk.Tk()
    root.withdraw()
    root.update()

    return filedialog.asksaveasfilename()


def check_input(ui):
    if ui.upper() == 'Q':
        print('Quitting...')
        return True
    return False

def read_from_file(path):
    with open(os.path.join(path), 'r') as file:
        return file.read()

def get_msg(ui):
    if ui == '':
        path = read_file_path()
        return read_from_file(path)
    else:
        return ui