import tkinter as tk
from tkinter import filedialog
import os

# Функция для отображения окна выбора файла
def select_video():
    root = tk.Tk()
    root.withdraw() # скрываем окно Tk
    
    # Запрашиваем имя файла у пользователя
    filename = filedialog.askopenfilename(initialdir="/", title="Выберите видеофайл")
    
    if not filename:
        return None
    
    return filename

# Основная функция
if __name__ == '__main__':
    print("Загрузка видео...")
    video_filepath = select_video()
    
    if video_filepath is not None:
        print(f"Видео успешно выбрано: {os.path.basename(video_filepath)}")
    else:
        print("Видео не было выбрано.")
