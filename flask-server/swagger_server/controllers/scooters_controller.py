import connexion
import six
import time
import threading
from threading import Thread, Lock
import pika
import json
from swagger_server import pika_dispatcher
from swagger_server.models.array_of_scooter import ArrayOfScooter  # noqa: E501
from swagger_server.models.scooter import Scooter  # noqa: E501
from swagger_server import util
from swagger_server.config import Config
from pika.exceptions import StreamLostError
from flask import g


channels = {}
channels_mutex = Lock()


def connect_to_rabbitmq():
    print("[x] Connecting to RabbitMQ")
    channels_mutex.acquire()
    credentials = pika.PlainCredentials(Config.rabbitmq_user, Config.rabbitmq_pwd)
    parameters = pika.ConnectionParameters(Config.rabbitmq_address, Config.rabbitmq_port, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channels[threading.get_ident()] = channel
    channels_mutex.release()
    print("[x] Connected to RabbitMQ")


def get_channel():
    channels_mutex.acquire()
    channel = channels[threading.get_ident()]
    channels_mutex.release()
    return channel


def has_channel():
    ret = False
    channels_mutex.acquire()
    try:
        if channels[threading.get_ident()] is not None:
            ret = True
    except KeyError:
        ret = False
    channels_mutex.release()
    return ret


def remove_channel():
    channels_mutex.acquire()
    del channels[threading.get_ident()]
    channels_mutex.release()


def add_scooter(body):  # noqa: E501
    """Add a new scooter

     # noqa: E501

    :param body: Scooter data
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        try:
            body = Scooter.from_dict(connexion.request.get_json())  # noqa: E501
            # decide where backend must put the results 
            result_queue = "fe" + Config.frontendid

            # create message containing the task to be executed 
            request_id = generate_request_id()
            task_message = {
                'op': 'add_scooter',
                'licensePlate': body.license_plate,
                'batteryPercentage':  body.battery_percentage,
                'latitude': body.latitude,
                'longitude': body.longitude,
                'status': body.status,
                'resultQueue': result_queue,
                'requestId': request_id
            }
            
            send_to_backend(task_message)
            
            return pika_dispatcher.wait_for_reply(request_id)
        except StreamLostError:
            connect_to_rabbitmq()
            return 'Internal server error', 500

    return 'Bad request', 400


def delete_scooter(licensePlate):  # noqa: E501
    if connexion.request.is_json:
        # decide where backend must put the results
        result_queue = "fe" + Config.frontendid

        # create message containing the task to be executed
        request_id = generate_request_id()
        task_message = {
            'op': 'delete_scooter',
            'licensePlate': licensePlate,
            'resultQueue': result_queue,
            'requestId': request_id
        }

        send_to_backend(task_message)

        return pika_dispatcher.wait_for_reply(request_id)
    return 'Bad request', 400


def get_available_scooters():  # noqa: E501
    try:
        # decide where backend must put the results 
        result_queue = "fe" + Config.frontendid

        # create message containing the task to be executed 
        request_id = generate_request_id()
        task_message = {
            'op': 'get_available_scooters',
            'resultQueue': result_queue,
            'requestId': request_id
        }

        send_to_backend(task_message)

        return pika_dispatcher.wait_for_reply(request_id)
    except StreamLostError:
        connect_to_rabbitmq()
        return 'Internal server error', 500


def get_scooter_by_license_plate(licensePlate):  # noqa: E501
    try:
        # create message containing the task to be executed 
        result_queue = "fe" + Config.frontendid
        
        request_id = generate_request_id()
        task_message = {
            'op': 'get_scooter_by_license_plate',
            'licensePlate': licensePlate,
            'resultQueue': result_queue,
            'requestId': request_id
        }
        
        send_to_backend(task_message)
        return pika_dispatcher.wait_for_reply(request_id)
    except StreamLostError:
        connect_to_rabbitmq()
        return 'Internal server error', 500


def update_scooter(licensePlate):  # noqa: E501
    """Update an existing scooter

     # noqa: E501

    :param licensePlate: License plate of scooter to be updated
    :type licensePlate: str

    :rtype: None
    """
    if connexion.request.is_json:
        try:
            body = Scooter.from_dict(connexion.request.get_json())

            # decide where backend must put the results 
            result_queue = "fe" + Config.frontendid

            # create message containing the task to be executed 
            request_id = generate_request_id()
            task_message = {
                'op': 'update_scooter',
                'licensePlate': licensePlate,
                'batteryPercentage': body.battery_percentage,
                'latitude': body.latitude,
                'longitude': body.longitude,
                'status': body.status,
                'resultQueue': result_queue,
                'requestId': request_id
            }

            send_to_backend(task_message)

            return pika_dispatcher.wait_for_reply(request_id)
        except StreamLostError:
            connect_to_rabbitmq()
            return 'Internal server error', 500
    return 'Bad request', 400


def generate_request_id():
    return str(time.time()) + "-" + str(threading.get_ident())


def send_to_backend(task_message):
    print("[x] send_to_backend() start")

    if not has_channel():
        connect_to_rabbitmq()

    channel = get_channel()

    result_queue = "fe" + Config.frontendid

    # queues declaration
    channel.queue_declare(queue='tasks')
    channel.queue_declare(queue=result_queue)

    # send task message
    channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps(task_message))

    remove_channel()

    print("[x] send_to_backend() completed")


print("[x] scooter_controller.py called. I am fe" + Config.frontendid)