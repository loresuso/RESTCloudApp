from threading import Thread, Lock, Condition
from swagger_server.config import Config
import pika
import json


results = {}
results_mutex = Lock()
condition = Condition()
pika_dispatcher_thread = 0


def callback(ch, method, properties, body):
    global results_mutex
    global results
    global condition
    print("[x] Received from back-end: %r" % body)
    # Insert the reply
    body_str = body.decode()
    dict = json.loads(body_str)
    request_id = dict["requestId"]
    result = dict["result"]
    print("[x] result is of type " + str(type(result)))
    results_mutex.acquire()
    results[request_id] = result
    results_mutex.release()
    # Notify all waiting threads
    condition.acquire()
    condition.notify_all()
    condition.release()


def has_reply(request_id):
    global results
    global results_mutex
    ret = False
    results_mutex.acquire()
    try:
        if results[request_id] is not None:
            ret = True
    except KeyError:
        ret = False
    results_mutex.release()
    return ret


def wait_for_reply(request_id):
    global results_mutex
    global results
    global condition
    # Wait until my reply is present in the results dict
    while not has_reply(request_id):
        condition.acquire()
        condition.wait()
        condition.release()
    # Take my reply
    results_mutex.acquire()
    ret = results[request_id]
    del results[request_id]
    results_mutex.release()
    return ret


def start_pika_dispatcher():
    global pika_dispatcher_thread
    pika_dispatcher_thread = PikaDispatcherThread()
    pika_dispatcher_thread.start()


def stop_pika_dispatcher():
    global pika_dispatcher_thread
    pika_dispatcher_thread.stop_consuming()


class PikaDispatcherThread(Thread):

    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.channel = 0
        return

    def connect(self):
        print("[x] PikaDispatcherThread: connecting to RabbitMQ")
        credentials = pika.PlainCredentials(Config.rabbitmq_user, Config.rabbitmq_pwd)
        parameters = pika.ConnectionParameters(Config.rabbitmq_address, Config.rabbitmq_port, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        print("[x] PikaDispatcherThread: connected to RabbitMQ")

    def run(self):
        print("[x] PikaDispatcherThread: started")
        self.connect()
        result_queue = "fe" + Config.frontendid
        self.channel.queue_declare(queue=result_queue)
        self.channel.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        print("[x] PikaDispatcherThread: stopped (consuming)")
        self.channel.stop_consuming()
