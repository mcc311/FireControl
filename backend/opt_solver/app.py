import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
import xlwings as xw
from os import getcwd
from utils import open_with_os
from solver import load_matrix, get_policy, policy_mode, sheet_name
import time

class App:
    def __init__(self, root):
        # setting title
        root.title("Fire Control")
        # setting window size
        width = 520
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.filename = getcwd()

        self.GLabel_532_var = tk.StringVar()
        self.GLabel_532_var.set(getcwd())
        GLabel_532 = tk.Label(root, textvariable=self.GLabel_532_var)
        ft = tkFont.Font(family='Times', size=12)
        GLabel_532["font"] = ft
        GLabel_532["fg"] = "#333333"
        GLabel_532["justify"] = "right"
        GLabel_532.place(x=40, y=60, width=500, height=30)

        # Buttons
        GButton_710 = ttk.Button(root)
        GButton_710["text"] = "編輯檔案"
        GButton_710.place(x=30, y=90, width=100, height=25)
        GButton_710["command"] = self.GButton_710_command

        GButton_712 = ttk.Button(root)
        GButton_712["text"] = "選擇檔案"
        GButton_712.place(x=30, y=60, width=100, height=30)
        GButton_712["command"] = self.GButton_712_command

        GButton_713 = ttk.Button(root)
        GButton_713["text"] = "計算"
        GButton_713.place(x=250, y=90, width=70, height=25)
        GButton_713["command"] = self.GButton_713_command

        GButton_714 = ttk.Button(root)
        GButton_714["text"] = "初始化"
        GButton_714.place(x=140, y=90, width=100, height=25)
        GButton_714["command"] = self.clear_buttom_command

        alpha_key = ["威脅度重視度","價值重視度","彈藥成本重視度","毀傷度重視度"]
        self.entries = {key: ttk.Entry(root) for key in alpha_key}
        for idx, (key, entry) in enumerate(self.entries.items()):
            ttk.Label(root, text=key).place(x=370, y=260+idx*45)
            entry.place(x=370, y=280+idx*45, width=40)

        self.chk_policy = {value: tk.BooleanVar() for key, value in policy_mode.items()}
        self.policy_text = {value: tk.StringVar() for key, value in policy_mode.items()}
        for key, value in self.policy_text.items():
            self.policy_text[key].set(key)
        checkbox_policy = [tk.Checkbutton(root, textvariable=self.policy_text[key], var=chk) for key, chk in self.chk_policy.items()]
        for i, checkbox in enumerate(checkbox_policy):
            checkbox.place(x=350, y=150+i*20)
        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.place(x=30, y=150, width=300, height=300)


    def GButton_710_command(self):
        open_with_os(self.filename)

    def GButton_712_command(self):
        self.filename = fd.askopenfilename(initialdir=getcwd())
        self.GLabel_532_var.set(self.filename)

        
    def GButton_713_command(self):
        self.wb = xw.Book(self.filename)
        self.ws = self.wb.sheets[sheet_name['main']]
        enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix = load_matrix(filepath=self.filename)
        x = 7
        self.ws.range("A7:T65565").delete()
        for mode, chk in self.chk_policy.items():
            if chk.get():
                start = time.time()
                self.ws.range(f"A{x}").value = f'{mode}:'
                # self.ws.range(f"A{x}:20").api.Borders(9).LineStyle = 1
                # self.ws.range(f"A{x}:20").api.Borders(9).we
                x += 1
                policy, _ = get_policy(enemies, weapons, t_matrix, q_matrix, v_matrix, u_matrix, mode)
                end = time.time()
                time_cost = end-start
                self.policy_text[mode].set(f'{mode} {time_cost:.2f} s')
                for _, row in policy.iterrows():
                    self.ws.range(f"A{x}").value = row.values
                    x += 1
        self.wb.save()

    def clear_buttom_command(self):
        for key, value in self.policy_text.items():
            self.policy_text[key].set(key)

        self.wb = xw.Book(self.filename)
        self.ws = self.wb.sheets[sheet_name['main']]
        self.ws.range("A7:T65565").delete()
        sheets_cat = ['t', 'v', 'q', 'u']
        for cat in sheets_cat:
            df_sht = self.wb.sheets[sheet_name[f'{cat}_default']]
            sht = self.wb.sheets[sheet_name[f'{cat}_sheet']]
            sht.range("A1:W12").value = df_sht.range("A1:W12").value

        
        self.wb.save()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
