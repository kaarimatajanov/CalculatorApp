import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x500")  # Increased height for history
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Entry widget to display input/output
        self.entry = tk.Entry(root, width=20, font=("Arial", 16), bd=5, insertwidth=2,
                              bg="#ffffff", fg="#000000")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.entry.focus_set()

        # History display
        self.history = tk.Text(root, height=5, width=25, font=("Arial", 12),
                               bg="#e6e6e6", fg="#000000", state='disabled')
        self.history.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        # Bind keyboard events
        self.root.bind('<Key>', self.key_press)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        button_list = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row = 2
        col = 0
        for button in button_list:
            cmd = lambda x=button: self.click(x)
            bg_color = "#d9d9d9" if button in '0123456789.' else "#ff9500"
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
                expression = self.entry.get()
                result = eval(expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                # Update history
                self.history.configure(state='normal')
                self.history.insert(tk.END, f"{expression} = {result}\n")
                self.history.configure(state='disabled')
                self.history.see(tk.END)
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

    def key_press(self, event):
        key = event.char
        if key in '0123456789.+-*/':
            self.click(key)
        elif key == '\r':  # Enter key
            self.click('=')
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key.lower() == 'c':
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()