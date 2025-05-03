import tkinter as tk
from tkinter import messagebox
from viewmodel import CalculatorViewModel

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleCalculatorMVVM")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.viewmodel = CalculatorViewModel()
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(padx=30, pady=20, fill="both", expand=True)

        self.entry = tk.Entry(self.main_frame, width=28, font=("Helvetica", 16), bd=0,
                              bg="#ffffff", fg="#000000", insertbackground="#000000",
                              relief="flat")
        self.entry.grid(row=0, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        self.history_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.history_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")
        self.history = tk.Text(self.history_frame, height=6, width=28, font=("Helvetica", 12),
                               bg="#ffffff", fg="#000000", state='disabled', bd=0)
        self.history.pack(side="left", fill="both")
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        self.root.bind('<Key>', self.key_press)
        self.create_buttons()

    def create_buttons(self):
        button_list = [
            ('sin', 'cos', 'tan', 'ln', '%'),
            ('7', '8', '9', '/', '^'),
            ('4', '5', '6', '*', '√'),
            ('1', '2', '3', '-', '('),
            ('0', '.', '=', '+', ')')
        ]

        row = 2
        for button_row in button_list:
            col = 0
            for button in button_row:
                cmd = lambda x=button: self.click(x)
                bg_color = "#d9d9d9" if button in '0123456789.' else "#ff9500"
                fg_color = "#000000"
                tk.Button(self.main_frame, text=button, width=5, height=2, font=("Helvetica", 12, "bold"),
                         bg=bg_color, fg=fg_color, activebackground="#bfbfbf" if button in '0123456789.' else "#cc7b00",
                         bd=0, relief="flat", command=cmd).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        tk.Button(self.main_frame, text="C", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.clear).grid(row=row, column=0, padx=5, pady=5)
        tk.Button(self.main_frame, text="⌫", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.backspace).grid(row=row, column=1, padx=5, pady=5)
        tk.Button(self.main_frame, text="CH", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.clear_history).grid(row=row, column=2, padx=5, pady=5)

    def click(self, char):
        if char == '=':
            result = self.viewmodel.evaluate()
            self.update_entry()
            self.update_history()
            if self.viewmodel.get_error():
                messagebox.showerror("Ошибка", f"Недопустимый ввод: {self.viewmodel.get_error()}")
        else:
            self.viewmodel.append_input(char)
            self.update_entry()

    def clear(self):
        self.viewmodel.clear()
        self.update_entry()

    def backspace(self):
        self.viewmodel.backspace()
        self.update_entry()

    def clear_history(self):
        self.viewmodel.clear_history()
        self.update_history()

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.viewmodel.expression)

    def update_history(self):
        self.history.configure(state='normal')
        self.history.delete(1.0, tk.END)
        self.history.insert(tk.END, self.viewmodel.get_history())
        self.history.configure(state='disabled')
        self.history.see(tk.END)

    def key_press(self, event):
        key = event.char
        if key in '0123456789.+-*/%^()':
            self.click(key)
        elif key == '\r':
            self.click('=')
        elif key == '\x08':
            self.backspace()
        elif key.lower() == 'c':
            self.clear()
        elif key.lower() == 'h':
            self.clear_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()