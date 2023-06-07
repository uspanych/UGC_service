import csv
import random
import time
from uuid import uuid4


def save_to_csv(data, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def gen_data():
    user_id = random.randint(1, 200000)
    movie_id = str(uuid4())
    viewed_frame = random.randint(1000000000, 9000000000)
    return [user_id, movie_id, viewed_frame]


start_time = time.time()

num_records = 10000000  # Количество записей, которое нужно сгенерировать
filename = 'data10m.csv'  # Имя файла, в который сохраняем данные

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['user_id', 'movie_id', 'viewed_frame'])  # Запись заголовков столбцов

for _ in range(num_records):
    data = gen_data()
    save_to_csv(data, filename)

end_time = time.time()
execution_time = end_time - start_time
print("Время выполнения: ", execution_time, " секунд")
