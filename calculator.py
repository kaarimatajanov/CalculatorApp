import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Entry widget to display input/output
        self.entry = tk.Entry(root, width=20, font=("Arial", 16), bd=5, insertwidth=2,
                              bg="#ffffff", fg="#000000")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        button_list = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row = 1
        col = 0
        for button in button_list:
            cmd = lambda x=button: self.click(x)
            bg_color = "#d9d9d9" if button in '0123456789.' else "#ff9500"  # Orange for operators
            tk.Button(self.root, text=button, width=5, height=2, font=("Arial", 14),
                     bg=bg_color, fg="#000000", activebackground="#bfbfbf",
                     command=cmd).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Clear button
        tk.Button(self.root, text="C", width=5, height=2, font=("Arial", 14),
                  bg="#ff3b30", fg="#ffffff", activebackground="#cc2e26",
                  command=self.clear).grid(row=row, column=col, padx=5, pady=5)
        # Backspace button
        tk.Button(self.root, text="⌫", width=5, height=2, font=("Arial", 14),
                  bg="#ff3b30", fg="#ffffff", activebackground="#cc2e26",
                  command=self.backspace).grid(row=row, column=col+1, padx=5, pady=5)

    def click(self, char):
        if char == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except:
                messagebox.showerror("Error", "Invalid input")
                self.clear()
        else:
            self.entry.insert(tk.END, char)

    def clear(self):
        self.entry.delete(0, tk.END)

    def backspace(self):
        current = self.entry.get()
        if current:
            self.entry.delete(len(current)-1, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()