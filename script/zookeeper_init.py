import sys
from kazoo.client import KazooClient

hosts = "172.16.2.36:2181,172.16.2.27:2181,172.16.1.235:2181"
zk = KazooClient(hosts=hosts, read_only=True)
print('Try to connect to zookeeper at ' + hosts + ' ...')
zk.start()
print("Connected")

#Store the data
zk.delete("/scooterCloudApp", recursive=True)
zk.ensure_path("/scooterCloudApp")
zk.create("/scooterCloudApp/rabbitmq_address", b"172.16.2.27")
zk.create("/scooterCloudApp/rabbitmq_port", b"5672")
zk.create("/scooterCloudApp/rabbitmq_user", b"guest")
zk.create("/scooterCloudApp/rabbitmq_pwd", b"guest")
zk.create("/scooterCloudApp/mysql_address", b"172.16.2.15")
zk.create("/scooterCloudApp/mysql_user", b"root")
zk.create("/scooterCloudApp/mysql_pwd", b"root")
zk.create("/scooterCloudApp/mysql_db", b"scooterdb")

print("Zookeeper initialized")

