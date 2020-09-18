import connexion
import pika
import time 
from kazoo.client import KazooClient
from flask import g


class Config:
    rabbitmq_user = ""
    rabbitmq_pwd = ""
    rabbitmq_address = ""
    rabbitmq_port = 0
    frontendid = ""

    @staticmethod
    def generate_frontend_id():
        Config.frontendid = str(int(round(time.time()*1000)))

    @staticmethod
    def initialize_parameters():
        #connect to Zookeeper
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
