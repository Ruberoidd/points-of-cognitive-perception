import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk
import random
import os


# Функция для генерации случайного названия файла
def generate_random_name():
    adjectives = ["Bright", "Dark", "Mysterious", "Hidden", "Silent", "Shiny"]
    nouns = ["Forest", "Ocean", "Desert", "Mountain", "Sky", "River"]
    return random.choice(adjectives) + "_" + random.choice(nouns)


# Функция для создания изображения с точками
def create_image(preview=False):
    width = int(width_entry.get())
    height = int(height_entry.get())
    dot_size = int(dot_size_entry.get())
    num_dots = int(num_dots_entry.get())
    dot_color = color_button["bg"]

    # Создаем изображение
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Рисуем случайные точки
    for _ in range(num_dots):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse([x, y, x + dot_size, y + dot_size], fill=dot_color)

    if preview:
        # Создаем предварительный просмотр
        show_preview(img)
    else:
        # Сохраняем изображение
        filename = file_name_label.cget("text") + ".png"
        filepath = filedialog.asksaveasfilename(initialfile=filename, defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")])
        if filepath:
            img.save(filepath)
            status_label.config(text=f"Изображение сохранено как: {os.path.basename(filepath)}")


# Функция для показа предварительного просмотра изображения
def show_preview(img):
    # Изменяем размер изображения для предварительного просмотра
    img_preview = img.resize((900, 600))  # Уменьшаем размер для отображения
    img_tk = ImageTk.PhotoImage(img_preview)

    # Обновляем Label с предварительным просмотром
    preview_label.config(image=img_tk)
    preview_label.image = img_tk  # Необходимо сохранить ссылку на объект, чтобы изображение отображалось


# Функция для выбора цвета точек
def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        color_button.config(bg=color)


# Функция для генерации и отображения названия файла
def update_file_name():
    random_name = generate_random_name()
    file_name_label.config(text=random_name)


# Создаем графический интерфейс
root = tk.Tk()
root.title("Генератор случайных точек")

# Поля для ввода ширины и высоты изображения
tk.Label(root, text="Ширина (px):").grid(row=0, column=0)
width_entry = tk.Entry(root)
width_entry.grid(row=0, column=1)
width_entry.insert(0, "1500")

tk.Label(root, text="Высота (px):").grid(row=1, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)
height_entry.insert(0, "1000")

# Поля для ввода размера точек и их количества
tk.Label(root, text="Размер точек (px):").grid(row=2, column=0)
dot_size_entry = tk.Entry(root)
dot_size_entry.grid(row=2, column=1)
dot_size_entry.insert(0, "3")

tk.Label(root, text="Количество точек:").grid(row=3, column=0)
num_dots_entry = tk.Entry(root)
num_dots_entry.grid(row=3, column=1)
num_dots_entry.insert(0, "4000")

# Кнопка для выбора цвета точек
tk.Label(root, text="Цвет точек:").grid(row=4, column=0)
color_button = tk.Button(root, bg="grey", width=10, command=choose_color)
color_button.grid(row=4, column=1)

# Кнопка для генерации имени файла
tk.Label(root, text="Название файла:").grid(row=5, column=0)
file_name_label = tk.Label(root, text=generate_random_name(), width=20)
file_name_label.grid(row=5, column=1)

update_name_button = tk.Button(root, text="Генерировать имя", command=update_file_name)
update_name_button.grid(row=6, column=0, columnspan=2)

# Кнопка для создания изображения
create_button = tk.Button(root, text="Создать изображение", command=create_image)
create_button.grid(row=7, column=0, columnspan=2)

# Кнопка для предварительного просмотра
preview_button = tk.Button(root, text="Предварительный просмотр", command=lambda: create_image(preview=True))
preview_button.grid(row=8, column=0, columnspan=2)

# Поле для предварительного просмотра
preview_label = tk.Label(root)
preview_label.grid(row=9, column=0, columnspan=2)

# Статусная метка
status_label = tk.Label(root, text="")
status_label.grid(row=10, column=0, columnspan=2)

# Запускаем интерфейс
root.mainloop()
