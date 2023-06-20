import time
from threading import Thread
import vertica_python


def Average(lst):
    return sum(lst) / len(lst)


connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': 'vertica',
    'database': 'VMart',
    'autocommit': True,
}

CHUNK_SIZE = 100000
FILE_NAME = "data10m.csv"

sql_create_table = """
    CREATE TABLE views (
    id IDENTITY,
    user_id INTEGER NOT NULL,
    movie_id VARCHAR(256) NOT NULL,
    viewed_frame INTEGER NOT NULL
    );
"""
sql_create_record = """
INSERT INTO views (user_id, movie_id, viewed_frame) VALUES {data};
"""

sql_get_record = """
    SELECT * FROM views;
"""

sql_get_count_record = """
    SELECT COUNT(*) FROM views;
"""

sql_clean_up_table = """
    DELETE FROM views;
"""

sql_get_10_k_record = """
    SELECT * FROM views limit 10000;
"""

sql_get_all_record = """
    SELECT * FROM views;
"""


def get_data_from_csv():
    with open(FILE_NAME, "r") as f:
        _ = f.readline()
        while True:
            try:
                data = [next(f).strip().split(",") for _ in range(CHUNK_SIZE)]
                yield data
            except StopIteration:
                break


def insert_data(log=True):
    total_start_time = time.time()
    items_time = []
    i = 0
    for data in get_data_from_csv():
        with vertica_python.connect(**connection_info) as conn:
            cur = conn.cursor()
            sql = f"""
            {sql_create_record.format(data=", ".join([f"({i}, '{j}', {k})" for i, j, k in data]))}
            """
            start = time.time()
            cur.execute(sql)
            i += 1
            if log:
                item_time = time.time() - start
                items_time.append(item_time)
                print(f"На вставку {i} затрачено: {item_time}")
    if log:
        print("Всего затрачено: ", time.time() - total_start_time)
        print("В среднем на одну итерацию: ", Average(items_time))


def clear_table():
    with vertica_python.connect(**connection_info) as conn:
        cur = conn.cursor()
        cur.execute(sql_clean_up_table)


def create_table():
    with vertica_python.connect(**connection_info) as conn:
        cur = conn.cursor()
        cur.execute(sql_create_table)


def get_table(sql):
    with vertica_python.connect(**connection_info) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        print(cur.fetchall())


insert_data()
# get_table()
# clear_table()

start = time.time()
get_table(sql_get_10_k_record)
print("На селект одной пачки 10000: ", time.time() - start)


start = time.time()
get_table(sql_get_all_record)
print("На селект всех записей: ", time.time() - start)
