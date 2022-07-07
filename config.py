import tkinter as tk
from tkinter import Tk, ttk

class Config(tk.Toplevel):
    def __init__(self, root, config_dict):
        super().__init__()
        self.root = root
        self.config_dict = config_dict
        self.interval = config_dict['interval']
        # root の位置を調べるにゃ
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        self.geometry('+%s+%s' % (int(root_x) + 50, int(root_y + 50)))
        self.title('表示の設定')
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.g_frm = ttk.Frame(self, padding=10)
        self.g_frm.grid(column=0, row=0,
            sticky=tk.E+tk.W+tk.N+tk.S)

