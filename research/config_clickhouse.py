import docker
client = docker.from_env()


NODES = [
    'clickhouse-node1',
    'clickhouse-node2',
    'clickhouse-node3',
    'clickhouse-node4'
]

FUNCS = {
    'clickhouse-node1': [
        "CREATE DATABASE shard;",
        "CREATE TABLE shard.test (user_id Int64, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_1') ORDER BY user_id;",
        "CREATE TABLE default.test (user_id Int64, movie_id UUID, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', test, rand());"
    ],
    'clickhouse-node2': [
        "CREATE DATABASE replica;",
        "CREATE TABLE replica.test (user_id Int64, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_2') ORDER BY user_id;"
    ],
    'clickhouse-node3': [
        "CREATE DATABASE shard;",
        "CREATE TABLE shard.test (user_id Int64, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_1') ORDER BY user_id;",
        "CREATE TABLE default.test (user_id Int64, movie_id UUID, viewed_frame Int64) ENGINE = Distributed('company_cluster', '', test, rand());"
    ],
    'clickhouse-node4': [
        "CREATE DATABASE replica;",
        "CREATE TABLE replica.test (user_id Int64, movie_id UUID, viewed_frame Int64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_2') ORDER BY user_id;"
    ]
}


target_nodes = {k:i for i in client.containers.list() if (k := i.attrs['Config']['Hostname']) in NODES}

for node in NODES:
    target_nodes[node].exec_run('clickhouse-client -n -q "{}"'.format(" ".join(FUNCS[node])))
