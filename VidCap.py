import pandas as pd
import cv2
import numpy as np
import os
def get_current_label(frame_number):
    return f'title_{frame_number}'


data = pd.read_csv("baseline/train_data_categories.csv")
print(data.shape)

for i in range(data.shape[0]):

    video1 = data["video_id"][i]
    print(video1, data["title"][i], data["tags"][i])



    # Путь к видеофайлу
    video_path = 'videos/' + video1 + '.mp4'

    output_dir = 'data/' + str(video1)
    os.makedirs(output_dir, exist_ok=True)

    # Открытие видеофайла
    cap = cv2.VideoCapture(video_path)

    # Инициализация счётчика кадров
    frame_count = 0

    # Перебираем все кадры видео
    while True:
        # Чтение кадра
        ret, frame = cap.read()

        if not ret:
            break

        # Получение текущей метки
        current_label = get_current_label(frame_count)

        # Сохранение кадра в нужную директорию
        output_path = f'{output_dir}/{frame_count}.jpg'
        cv2.imwrite(output_path, frame)

        # Присваивание меток кадрам
        with open('labels.txt', 'a') as labels_file:
            labels_file.write(f'{output_path},{current_label}\n')

        frame_count += 1

    # Закрытие файла
    cap.release()
    cv2.destroyAllWindows()
    # Вывод информации о массиве
    #print(video_as_numpy.shape)
    #print(video_as_numpy)

