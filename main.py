import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk, ImageFont
import random
import os


# Загрузка слов из файла
def load_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words


# Загружаем слова из файла
words = load_words_from_file('google_words.txt')


# Функция для генерации случайного названия файла (добавлена плотность)
def generate_random_name(width, height, dot_size, num_dots, dot_color, density):
    if len(words) >= 2:
        random_word1 = random.choice(words)
        random_word2 = random.choice(words)
        return f"{random_word1}_{random_word2}_{width}-{height}-{dot_size}-{num_dots}-{dot_color.replace('#', '')}-{density}"
    return "Random_File"


# Функция для создания сводки на изображении (добавлена плотность и перемещено в нижнюю часть изображения)
def add_summary_to_image(img, width, height, dot_size, num_dots, dot_color, density):
    draw = ImageDraw.Draw(img)

    # Подготовка текста для сводки
    summary_text = (f"Width: {width} px\n"
                    f"Height: {height} px\n"
                    f"Dot size: {dot_size} px\n"
                    f"Dot count: {num_dots}\n"
                    f"Dot color: {dot_color}\n"
                    f"Density: {density}%")

    # Шрифт для текста
    font = ImageFont.load_default()

    # Получаем координаты ограничивающего прямоугольника текста
    text_bbox = draw.textbbox((0, 0), summary_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Параметры прямоугольника
    padding = 10
    rectangle_x0 = width - text_width - 2 * padding
    rectangle_y0 = height - text_height - 2 * padding
    rectangle_x1 = width
    rectangle_y1 = height

    # Рисуем желтый прямоугольник
    draw.rectangle([rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1], fill="yellow")

    # Добавляем черный текст поверх желтого фона
    draw.text((rectangle_x0 + padding, rectangle_y0 + padding), summary_text, font=font, fill="black")


# Функция для создания изображения с точками (добавлено использование плотности)
def create_image(preview=False):
    width = int(width_entry.get())
    height = int(height_entry.get())
    dot_size = int(dot_size_entry.get())
    num_dots = int(num_dots_entry.get())
    dot_color = color_button["bg"]
    density = int(density_slider.get())  # Получаем значение плотности слайдера

    # Создаем изображение
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Рисуем случайные точки
    for _ in range(num_dots):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse([x, y, x + dot_size, y + dot_size], fill=dot_color)

    # Добавляем сводку к изображению
    add_summary_to_image(img, width, height, dot_size, num_dots, dot_color, density)

    if preview:
        # Создаем предварительный просмотр
        show_preview(img)
    else:
        # Сохраняем изображение
        filename = generate_random_name(width, height, dot_size, num_dots, dot_color, density) + ".png"
        filepath = filedialog.asksaveasfilename(initialfile=filename, defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")])
        if filepath:
            img.save(filepath)
            status_label.config(text=f"Изображение сохранено как: {os.path.basename(filepath)}")


# Функция для показа предварительного просмотра изображения
def show_preview(img):
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


# Обновляем имя файла при смене параметров
def update_file_name():
    width = int(width_entry.get())
    height = int(height_entry.get())
    dot_size = int(dot_size_entry.get())
    num_dots = int(num_dots_entry.get())
    dot_color = color_button["bg"]
    density = int(density_slider.get())  # Получаем значение плотности слайдера
    random_name = generate_random_name(width, height, dot_size, num_dots, dot_color, density)
    file_name_label.config(text=random_name)


# Создаем графический интерфейс
root = tk.Tk()
root.title("points-of-cognitive-perception")
root.iconbitmap("materials/points-of-cognitive-perception_ico.ico")  # Задаем .ico файл напрямую
root.resizable(False, False)

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

# Добавление слайдера плотности в интерфейс
tk.Label(root, text="Плотность точек:").grid(row=5, column=0)
density_slider = tk.Scale(root, from_=10, to=90, orient=tk.HORIZONTAL)
density_slider.grid(row=5, column=1)
density_slider.set(50)  # Установим начальное значение плотности

# Кнопка для генерации имени файла
tk.Label(root, text="Название файла:").grid(row=6, column=0)
file_name_label = tk.Label(root, text="", width=40)
file_name_label.grid(row=6, column=1)

update_name_button = tk.Button(root, text="Генерировать имя", command=update_file_name)
update_name_button.grid(row=7, column=0, columnspan=2)

# Кнопка для создания изображения
create_button = tk.Button(root, text="Создать изображение", command=create_image)
create_button.grid(row=8, column=0, columnspan=2)

# Кнопка для предварительного просмотра
preview_button = tk.Button(root, text="Предварительный просмотр", command=lambda: create_image(preview=True))
preview_button.grid(row=9, column=0, columnspan=2)

# Поле для предварительного просмотра
preview_label = tk.Label(root)
preview_label.grid(row=10, column=0, columnspan=2)

# Статусная метка
status_label = tk.Label(root, text="")
status_label.grid(row=11, column=0, columnspan=2)

# Обновляем название файла при запуске
update_file_name()

# Запускаем интерфейс
root.mainloop()
