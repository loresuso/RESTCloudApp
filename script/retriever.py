from kazoo.client import KazooClient

zk = KazooClient(hosts="172.16.2.36:2181,172.16.2.27:2181,172.16.1.235:2181", read_only=True)
zk.start() #Store the data

data, stat = zk.get("/scooterCloudApp/rabbitmq_user")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
