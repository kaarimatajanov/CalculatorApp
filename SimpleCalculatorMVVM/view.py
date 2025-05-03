import tkinter as tk
from tkinter import messagebox, font
from viewmodel import CalculatorViewModel
from PIL import Image, ImageTk
import pygame
import os
import json
import logging

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleCalculatorMVVM")
        self.viewmodel = CalculatorViewModel()
        self.resources = {}
        self.config = self.load_config()
        self.apply_config()
        self.setup_resources()
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """Загрузка конфигурационного файла с обработкой ошибок"""
        default_config = {
            "window": {"width": 500, "height": 750},
            "background_color": "#f0f0f0",
            "font": {"name": "Helvetica", "size": 12},
            "sound_enabled": True,
            "animation": {"width": 100, "height": 50},
            "styles": {
                "default": {
                    "background_color": "#f0f0f0",
                    "button_color": "#d9d9d9",
                    "operator_color": "#ff9500",
                    "special_color": "#ff3b30",
                    "text_color": "#000000",
                    "font_size": 12
                }
            },
            "active_style": "default"
        }
        try:
            with open("SimpleCalculatorMVVM/config.json", "r") as f:
                config = json.load(f)
            # Проверка наличия всех обязательных ключей
            required_keys = ["window", "background_color", "font", "sound_enabled", "animation", "styles", "active_style"]
            for key in required_keys:
                if key not in config:
                    logging.error(f"Отсутствует ключ {key} в config.json. Используется значение по умолчанию.")
                    return default_config
            return config
        except FileNotFoundError:
            logging.error("Файл config.json не найден. Используется конфигурация по умолчанию.")
            messagebox.showwarning("Предупреждение", "Файл config.json не найден. Используется конфигурация по умолчанию.")
            return default_config
        except json.JSONDecodeError:
            logging.error("Неверный формат config.json. Используется конфигурация по умолчанию.")
            messagebox.showerror("Ошибка", "Неверный формат config.json. Используется конфигурация по умолчанию.")
            return default_config
        except Exception as e:
            logging.error(f"Ошибка загрузки config.json: {str(e)}. Используется конфигурация по умолчанию.")
            messagebox.showerror("Ошибка", f"Ошибка загрузки config.json: {str(e)}")
            return default_config

    def apply_config(self):
        """Применение настроек из конфигурации"""
        try:
            window_size = f"{self.config['window']['width']}x{self.config['window']['height']}"
            self.root.geometry(window_size)
            self.root.configure(bg=self.config['background_color'])
            self.active_style = self.config.get("active_style", "default")
            if self.active_style not in self.config["styles"]:
                logging.warning(f"Стиль {self.active_style} не найден. Используется стиль default.")
                self.active_style = "default"
        except Exception as e:
            logging.error(f"Ошибка применения конфигурации: {str(e)}")

    def setup_resources(self):
        # Статическая загрузка
        try:
            # Иконка окна
            self.root.iconbitmap("SimpleCalculatorMVVM/resources/icon.ico")

            # Логотип
            self.resources['logo'] = ImageTk.PhotoImage(
                Image.open("SimpleCalculatorMVVM/resources/logo.png").resize((60, 60), Image.Resampling.LANCZOS)
            )

            # Шрифт из конфигурации
            self.resources['custom_font'] = font.Font(
                family=self.config['font']['name'],
                size=self.config['styles'][self.active_style]['font_size'],
                weight="bold"
            )

            # Курсоры
            self.resources['button_cursor'] = "hand2"
            self.resources['entry_cursor'] = "xterm"

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки ресурсов: {str(e)}")

        # Динамическая загрузка звука
        if self.config['sound_enabled']:
            try:
                pygame.mixer.init()
                self.resources['sound'] = None
                self.load_sound()
            except Exception as e:
                print(f"Ошибка инициализации звука: {str(e)}")

        # Динамическая загрузка анимации
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
                            ImageTk.PhotoImage(gif.copy().resize(
                                (self.config['animation']['width'], self.config['animation']['height']),
                                Image.Resampling.LANCZOS
                            ))
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

        self.main_frame = tk.Frame(self.root, bg=self.config['styles'][self.active_style]['background_color'])
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Логотип
        logo_label = tk.Label(self.main_frame, image=self.resources['logo'],
                              bg=self.config['styles'][self.active_style]['background_color'])
        logo_label.grid(row=0, column=0, columnspan=5, pady=5)

        # Поле ввода
        self.entry = tk.Entry(self.main_frame, width=28, font=("Helvetica", 16),
                              bd=0, bg="#ffffff", fg=self.config['styles'][self.active_style]['text_color'],
                              insertbackground=self.config['styles'][self.active_style]['text_color'],
                              relief="flat", cursor=self.resources['entry_cursor'])
        self.entry.grid(row=1, column=0, columnspan=5, pady=10, ipady=10, sticky="ew")
        self.entry.focus_set()

        # История
        self.history_frame = tk.Frame(self.main_frame, bg=self.config['styles'][self.active_style]['background_color'])
        self.history_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")
        self.history = tk.Text(self.history_frame, height=6, width=28, font=("Helvetica", 12),
                               bg="#ffffff", fg=self.config['styles'][self.active_style]['text_color'],
                               state='disabled', bd=0)
        self.history.pack(side="left", fill="both")
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history['yscrollcommand'] = scrollbar.set

        # Анимация
        if self.resources['gif_frames']:
            self.animation_label = tk.Label(self.main_frame, bg=self.config['styles'][self.active_style]['background_color'])
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

        style = self.config['styles'][self.active_style]
        row = 4
        for button_row in button_list:
            col = 0
            for button in button_row:
                cmd = lambda x=button: self.click(x)
                bg_color = style['button_color'] if button in '0123456789.' else style['operator_color']
                active_bg = "#bfbfbf" if button in '0123456789.' else "#cc7b00"
                tk.Button(self.main_frame, text=button, width=5, height=2,
                          font=self.resources['custom_font'], bg=bg_color, fg=style['text_color'],
                          activebackground=active_bg, bd=0, relief="flat", command=cmd,
                          cursor=self.resources['button_cursor']).grid(row=row, column=col, padx=5, pady=5)
                col += 1
            row += 1

        # Нижний ряд кнопок
        tk.Button(self.main_frame, text="C", width=5, height=2,
                  font=self.resources['custom_font'], bg=style['special_color'], fg=style['text_color'],
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.clear,
                  cursor=self.resources['button_cursor']).grid(row=row, column=0, padx=5, pady=10)
        tk.Button(self.main_frame, text="⌫", width=5, height=2,
                  font=self.resources['custom_font'], bg=style['special_color'], fg=style['text_color'],
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.backspace,
                  cursor=self.resources['button_cursor']).grid(row=row, column=1, padx=5, pady=10)
        tk.Button(self.main_frame, text="CH", width=5, height=2,
                  font=self.resources['custom_font'], bg=style['special_color'], fg=style['text_color'],
                  activebackground="#cc2e26", bd=0, relief="flat", command=self.clear_history,
                  cursor=self.resources['button_cursor']).grid(row=row, column=2, padx=5, pady=10)

    def show_about_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("О программе")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        style = self.config['styles'][self.active_style]
        dialog.configure(bg=style['background_color'])
        tk.Label(dialog, text="SimpleCalculatorMVVM", font=self.resources['custom_font'],
                 fg=style['text_color'], bg=style['background_color']).pack(pady=10)
        tk.Label(dialog, text="Версия: 1.0\nАвтор: Карим Атажанов",
                 fg=style['text_color'], bg=style['background_color']).pack(pady=10)
        tk.Button(dialog, text="Закрыть", command=dialog.destroy,
                  font=self.resources['custom_font'], bg=style['button_color'], fg=style['text_color']).pack(pady=10)

    def click(self, char):
        if self.config['sound_enabled']:
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
    logging.basicConfig(filename="SimpleCalculatorMVVM/calculator.log", level=logging.ERROR)
    root = tk.Tk()
    app = CalculatorView(root)
    root.mainloop()