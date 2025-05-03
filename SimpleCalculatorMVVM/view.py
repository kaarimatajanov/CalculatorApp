import tkinter as tk
from tkinter import messagebox, font
from viewmodel import CalculatorViewModel
from PIL import Image, ImageTk
import pygame
import os

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleCalculatorMVVM")
        self.root.geometry("500x750")  # Увеличена высота для видимости всех кнопок
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.viewmodel = CalculatorViewModel()
        self.resources = {}
        self.setup_resources()
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_resources(self):
        # Статическая загрузка
        try:
            # Иконка окна
            self.root.iconbitmap("SimpleCalculatorMVVM/resources/icon.ico")

            # Логотип
            self.resources['logo'] = ImageTk.PhotoImage(
                Image.open("SimpleCalculatorMVVM/resources/logo.png").resize((60, 60), Image.Resampling.LANCZOS)
            )

            # Шрифт
            self.resources['custom_font'] = font.Font(family="Helvetica", size=12, weight="bold")

            # Курсоры
            self.resources['button_cursor'] = "hand2"
            self.resources['entry_cursor'] = "xterm"

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки ресурсов: {str(e)}")

        # Динамическая загрузка звука
        try:
            pygame.mixer.init()
            self.resources['sound'] = None
            self.load_sound()
        except Exception as e:
            print(f"Ошибка инициализации звука: {str(e)}")

        # Динамическая загрузка анимации (опционально)
        self.resources['gif_frames'] = []
        self.resources['gif_index'] = 0
        try:
            gif_path = "SimpleCalculatorMVVM/resources/animation.gif"
            if os.path.exists(gif_path):
                gif = Image.open(gif_path)
                self.resources['gif_delay'] = gif.info.get('duration', 100) / 1000
                frame = 0
                while True:
                    try:
                        gif.seek(frame)
                        self.resources['gif_frames'].append(
                            ImageTk.PhotoImage(gif.copy().resize((100, 50), Image.Resampling.LANCZOS))
                        )
                        frame += 1
                    except EOFError:
                        break
        except Exception as e:
            print(f"Ошибка загрузки GIF: {str(e)}")

    def load_sound(self):
        if not self.resources['sound']:
            try:
                sound_path = "SimpleCalculatorMVVM/resources/click.wav"
                if os.path.exists(sound_path):
                    self.resources['sound'] = pygame.mixer.Sound(sound_path)
                    print("Звук успешно загружен")
                else:
                    print("Файл click.wav не найден")
            except Exception as e:
                print(f"Ошибка загрузки звука: {str(e)}")

    def setup_ui(self):
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="О программе", command=self.show_about_dialog)
        file_menu.add_command(label="Очистить", command=self.clear)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)

        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Логотип
        logo_label = tk.Label(self.main_frame, image=self.resources['logo'], bg="#f0f0f0")
        logo_label.grid(row=0, column=0, columnspan=5, pady=5)

        # Поле ввода
        self.entry = tk.Entry(self.main_frame, width=28, font=("Helvetica", 16),
                              bd=0, bg="#ffffff", fg="#000000", insertbackground="#000000",
                              relief="flat", cursor=self.resources['entry_cursor'])
        self.entry.grid(row=1, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        # История
        self.history_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.history_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")
        self.history = tk.Text(self.history_frame, height=6, width=28, font=("Helvetica", 12),
                               bg="#ffffff", fg="#000000", state='disabled', bd=0)
        self.history.pack(side="left", fill="both")
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        # Анимация (только если есть GIF)
        if self.resources['gif_frames']:
            self.animation_label = tk.Label(self.main_frame, bg="#f0f0f0")
            self.animation_label.grid(row=3, column=0, columnspan=5, pady=10)
            self.update_animation()

        self.root.bind('<Key>', self.key_press)
        self.create_buttons()

    def update_animation(self):
        if self.resources['gif_frames']:
            self.resources['gif_index'] = (self.resources['gif_index'] + 1) % len(self.resources['gif_frames'])
            self.animation_label.config(image=self.resources['gif_frames'][self.resources['gif_index']])
            self.root.after(int(self.resources['gif_delay'] * 1000), self.update_animation)

    def create_buttons(self):
        button_list = [
            ('sin', 'cos', 'tan', 'ln', '%'),
            ('7', '8', '9', '/', '^'),
            ('4', '5', '6', '*', '√'),
            ('1', '2', '3', '-', '('),
            ('0', '.', '=', '+', ')')
        ]

        row = 4
        for button_row in button_list:
            col = 0
            for button in button_row:
                cmd = lambda x=button: self.click(x)
                bg_color = "#d9d9d9" if button in '0123456789.' else "#ff9500"
                tk.Button(self.main_frame, text=button, width=5, height=2,
                          font=self.resources['custom_font'], bg=bg_color, fg="#000000",
                          activebackground="#bfbfbf" if button in '0123456789.' else "#cc7b00",
                          bd=0, relief="flat", command=cmd,
                          cursor=self.resources['button_cursor']).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        # Нижний ряд кнопок с увеличенными отступами
        tk.Button(self.main_frame, text="C", width=5, height=2,
                  font=self.resources['custom_font'], bg="#ff3b30", fg="#000000",
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.clear,
                  cursor=self.resources['button_cursor']).grid(row=row, column=0, padx=5, pady=10)
        tk.Button(self.main_frame, text="⌫", width=5, height=2,
                  font=self.resources['custom_font'], bg="#ff3b30", fg="#000000",
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.backspace,
                  cursor=self.resources['button_cursor']).grid(row=row, column=1, padx=5, pady=10)
        tk.Button(self.main_frame, text="CH", width=5, height=2,
                  font=self.resources['custom_font'], bg="#ff3b30", fg="#000000",
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.clear_history,
                  cursor=self.resources['button_cursor']).grid(row=row, column=2, padx=5, pady=10)

    def show_about_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("О программе")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="SimpleCalculatorMVVM", font=self.resources['custom_font']).pack(pady=10)
        tk.Label(dialog, text="Версия: 1.0\nАвтор: Карим Атажанов").pack(pady=10)
        tk.Button(dialog, text="Закрыть", command=dialog.destroy,
                  font=self.resources['custom_font']).pack(pady=10)

    def click(self, char):
        # Воспроизведение звука для всех кнопок
        self.load_sound()
        if self.resources['sound']:
            self.resources['sound'].play()

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

    def on_closing(self):
        pygame.mixer.quit()
        self.resources.clear()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()