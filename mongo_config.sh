#!/bin/bash
echo "1. Настройка серверов конфигурации"
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
sleep 3

echo "2. Сборка набора реплик первого шарда"
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
sleep 15

echo "3. Добавление первого шарда в маршрутизатор"
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
sleep 3

echo "4. Сборка набора реплик второго шарда"
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
sleep 6

echo "5. Добавление второго шарда в маршрутизатор"
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
sleep 3

echo "6. Создание базы данных"
docker exec -it mongors1n1 bash -c 'echo "use films" | mongosh'
sleep 3

echo "7. Включение шардирования базы данных"
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"films\")" | mongosh'
sleep 3

echo "8. Создание коллекций"
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.likes\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.reviews\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"films.bookmarks\")" | mongosh'
sleep 3

echo "9. Настройка шардирования по полю"
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.likes\", {\"movie_id\": \"hashed\"})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.reviews\", {\"movie_id\": \"hashed\"})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"films.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'