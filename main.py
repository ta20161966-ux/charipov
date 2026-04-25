import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json

# --- Конфигурация ---
HISTORY_FILE = "history.json"
MIN_LENGTH = 8
MAX_LENGTH = 32

# --- Функции логики ---
def generate_password(length, use_digits, use_letters, use_upper, use_special):
    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_lowercase
        if use_upper:
            chars += string.ascii_uppercase
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Не выбран ни один тип символов!")
    return ''.join(random.choices(chars, k=length))

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f)

def load_history():
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- Основная логика приложения ---
def on_generate():
    try:
        length = int(scale_length.get())
        if length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError(f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}.")

        password = generate_password(
            length,
            var_digits.get(),
            var_letters.get(),
            var_upper.get(),
            var_special.get()
        )

        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

        # Добавляем в историю
        history.append(password)
        save_history(history)

        # Обновляем таблицу истории
        for i in tree_history.get_children():
            tree_history.delete(i)
        for pwd in history:
            tree_history.insert('', 'end', values=(pwd,))

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

# --- Инициализация данных ---
history = load_history()

# --- Создание окна ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x400")

# --- Виджеты ---
frame_settings = tk.LabelFrame(root, text="Настройки")
frame_settings.pack(pady=10, fill=tk.X, padx=10)

tk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky='e')
scale_length = tk.Scale(frame_settings, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL)
scale_length.set(12)
scale_length.grid(row=0, column=1, sticky='we')

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky='w')
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=2, column=0, sticky='w')
tk.Checkbutton(frame_settings, text="Верхний регистр", variable=var_upper).grid(row=1, column=1, sticky='w')
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special).grid(row=2, column=1, sticky='w')

btn_generate = tk.Button(root, text="Сгенерировать", command=on_generate)
btn_generate.pack(pady=5)

frame_password = tk.Frame(root)
frame_password.pack(pady=10, fill=tk.X, padx=10)
tk.Label(frame_password, text="Пароль:").pack(side=tk.LEFT)
entry_password = tk.Entry(frame_password)
entry_password.pack(side=tk.LEFT, expand=True, fill=tk.X)

frame_history = tk.LabelFrame(root, text="История")
frame_history.pack(pady=10, fill='both', expand=True, padx=10)

tree_history = ttk.Treeview(frame_history, columns=("password",), show="headings")
tree_history.heading("password", text="Пароль")
tree_history.column("password", width=450)
tree_history.pack(fill='both', expand=True)

# Заполняем историю при запуске
for pwd in history:
    tree_history.insert('', 'end', values=(pwd,))

# --- Запуск ---
root.mainloop()
