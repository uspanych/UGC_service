import time
from clickhouse_driver import Client

client = Client(host='localhost')


SQL_CREATE_RECORD = """
INSERT INTO default.test (user_id, movie_id, viewed_frame) VALUES {data};
"""
CHUNK_SIZE = 1_000_000
FILE_NAME = "data10m.csv"


def get_data():
    with open(FILE_NAME, "r") as f:
        _ = f.readline()
        while True:
            try:
                data = [next(f).strip().split(",") for _ in range(CHUNK_SIZE)]
                yield data
            except StopIteration:
                break


def insert_data():
    ch_client = Client(host='localhost')
    for data in get_data():
        start = time.time()
        query = SQL_CREATE_RECORD.format(data=", ".join([f"({i}, '{j}', {k})" for i, j, k in data]))
        ch_client.execute(query)
        print("На вставку одной пачки затрачено: ", time.time() - start)


def main():
    # for data in get_data():
    #     print(data)
    #     time.sleep(1)
    start = time.time()
    insert_data()
    print("Всего затрачено: ", time.time() - start)


if __name__ == '__main__':
    main()
