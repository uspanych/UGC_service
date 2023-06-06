import time
from clickhouse_driver import Client

client = Client(host='localhost')

SQL_GET_RECORD = """
SELECT * FROM default.test;
"""


SQL_GET_RECORD_LIMIT = """
SELECT * FROM default.test limit 10000;
"""


start = time.time()
print(len(client.execute(SQL_GET_RECORD_LIMIT)))
print("На селект одной пачки 10000: ", time.time() - start)


start = time.time()
print(len(client.execute(SQL_GET_RECORD)))
print("На селект всех записей: ", time.time() - start)
