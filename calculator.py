import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x650")  # Размер окна для видимости всех элементов
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")  # Светлый фон

        # Центральная рамка для всех элементов
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(padx=30, pady=20, fill="both", expand=True)

        # Поле ввода/вывода
        self.entry = tk.Entry(self.main_frame, width=28, font=("Helvetica", 16), bd=0,
                              bg="#ffffff", fg="#000000", insertbackground="#000000",
                              relief="flat")
        self.entry.grid(row=0, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        # Поле истории с прокруткой
        self.history_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.history_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")
        self.history = tk.Text(self.history_frame, height=6, width=28, font=("Helvetica", 12),
                               bg="#ffffff", fg="#000000", state='disabled', bd=0)
        self.history.pack(side="left", fill="both")
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        # Привязка клавиш
        self.root.bind('<Key>', self.key_press)

        # Кнопки
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
                bg_color = "#d9d9d9" if button in '0123456789.' else "#ff9500"  # Светло-серый для цифр, оранжевый для операций
                fg_color = "#000000"  # Черный текст для контраста
                tk.Button(self.main_frame, text=button, width=5, height=2, font=("Helvetica", 12, "bold"),
                         bg=bg_color, fg=fg_color, activebackground="#bfbfbf" if button in '0123456789.' else "#cc7b00",
                         bd=0, relief="flat", command=cmd).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        # Кнопка очистки ввода
        tk.Button(self.main_frame, text="C", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.clear).grid(row=row, column=0, padx=5, pady=5)
        # Кнопка Backspace
        tk.Button(self.main_frame, text="⌫", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.backspace).grid(row=row, column=1, padx=5, pady=5)
        # Кнопка очистки истории
        tk.Button(self.main_frame, text="CH", width=5, height=2, font=("Helvetica", 12, "bold"),
                  bg="#ff3b30", fg="#000000", activebackground="#cc2e26", bd=0, relief="flat",
                  command=self.clear_history).grid(row=row, column=2, padx=5, pady=5)

    def click(self, char):
        if char == '=':
            try:
                expression = self.entry.get()
                # Заменяем пользовательские символы на Python-совместимые
                expression = (expression.replace('^', '**')
                                      .replace('√', 'math.sqrt')
                                      .replace('sin', 'math.sin')
                                      .replace('cos', 'math.cos')
                                      .replace('tan', 'math.tan')
                                      .replace('ln', 'math.log'))
                result = eval(expression, {"math": math})  # Безопасный eval
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(round(result, 6)))
                # Обновляем историю
                self.history.configure(state='normal')
                self.history.insert(tk.END, f"{expression.replace('**', '^').replace('math.', '')} = {result}\n")
                self.history.configure(state='disabled')
                self.history.see(tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
                self.clear()
        else:
            self.entry.insert(tk.END, char)

    def clear(self):
        self.entry.delete(0, tk.END)

    def backspace(self):
        current = self.entry.get()
        if current:
            self.entry.delete(len(current)-1, tk.END)

    def clear_history(self):
        self.history.configure(state='normal')
        self.history.delete(1.0, tk.END)
        self.history.configure(state='disabled')

    def key_press(self, event):
        key = event.char
        if key in '0123456789.+-*/%^()':
            self.click(key)
        elif key == '\r':  # Enter
            self.click('=')
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key.lower() == 'c':
            self.clear()
        elif key.lower() == 'h':  # Очистка истории по клавише 'h'
            self.clear_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()