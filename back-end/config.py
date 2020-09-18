import connexion
import pika
import time
from kazoo.client import KazooClient


class Config:
    rabbitmq_user = ""
    rabbitmq_pwd = ""
    rabbitmq_address = ""
    rabbitmq_port = 0
    mysql_address = ""
    mysql_user = ""
    mysql_pwd = ""
    mysql_db = ""


    @staticmethod
    def initialize_parameters():
        # connect to Zookeeper
        zk = KazooClient(hosts="172.16.2.36:2181,172.16.2.27:2181,172.16.1.235:2181", read_only=True)
        zk.start()

        data, stat = zk.get("/scooterCloudApp/rabbitmq_user")
        print("Version: %s, rabbitmq_user: %s" % (stat.version, data.decode("utf-8")))
        Config.rabbitmq_user = data.decode("utf-8")

        data, stat = zk.get("/scooterCloudApp/rabbitmq_pwd")
        print("Version: %s, rabbitmq_pwd: %s" % (stat.version, data.decode("utf-8")))
        Config.rabbitmq_pwd = data.decode("utf-8")

        data, stat = zk.get("/scooterCloudApp/rabbitmq_address")
        print("Version: %s, rabbitmq_address: %s" % (stat.version, data.decode("utf-8")))
        Config.rabbitmq_address = data.decode("utf-8")

        data, stat = zk.get("/scooterCloudApp/rabbitmq_port")
        print("Version: %s, rabbitmq_port: %s" % (stat.version, data.decode("utf-8")))
        Config.rabbitmq_port = int(data.decode("utf-8"))

        data, stat = zk.get("/scooterCloudApp/mysql_address")
        print("Version: %s, mysql_address: %s" % (stat.version, data.decode("utf-8")))
        Config.mysql_address = (data.decode("utf-8"))

        data, stat = zk.get("/scooterCloudApp/mysql_user")
        print("Version: %s, mysql_user: %s" % (stat.version, data.decode("utf-8")))
        Config.mysql_user = (data.decode("utf-8"))

        data, stat = zk.get("/scooterCloudApp/mysql_pwd")
        print("Version: %s, mysql_pwd: %s" % (stat.version, data.decode("utf-8")))
        Config.mysql_pwd = (data.decode("utf-8"))

        data, stat = zk.get("/scooterCloudApp/mysql_db")
        print("Version: %s, mysql_db: %s" % (stat.version, data.decode("utf-8")))
        Config.mysql_db = (data.decode("utf-8"))


class Connection:
    connection = 0
    channel = 0

    @staticmethod
    def connect_to_rabbitmq():
        credentials = pika.PlainCredentials(Config.rabbitmq_user, Config.rabbitmq_pwd)
        parameters = pika.ConnectionParameters(Config.rabbitmq_address, Config.rabbitmq_port, '/', credentials)
        Connection.connection = pika.BlockingConnection(parameters)
        Connection.channel = Connection.connection.channel()