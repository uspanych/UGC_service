#! /bin/bash

docker-compose exec clickhouse-node1 clickhouse-client -n -q "CREATE DATABASE shard;\
CREATE TABLE shard.test (user_id UUID, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_1') ORDER BY viewed_frame;\
CREATE TABLE default.test (user_id UUID, movie_id UUID, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', test, rand());"

docker-compose exec clickhouse-node2 clickhouse-client -n -q "CREATE DATABASE replica;\
CREATE TABLE replica.test (user_id UUID, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_2') ORDER BY viewed_frame;"

docker-compose exec clickhouse-node3 clickhouse-client -n -q "CREATE DATABASE shard;\
CREATE TABLE shard.test (user_id UUID, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_1') ORDER BY viewed_frame;\
CREATE TABLE default.test (user_id UUID, movie_id UUID, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', test, rand());"

docker-compose exec clickhouse-node4 clickhouse-client -n -q "CREATE DATABASE replica;\
CREATE TABLE replica.test (user_id UUID, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_2') ORDER BY viewed_frame;"
