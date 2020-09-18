import string
import json
import time
from distutils.command.install_data import install_data

from pika.exceptions import StreamLostError
from config import Config
from config import Connection
from database_manager import DatabaseManager


# ricordarsi di controllare ritorno json_string


def send_to_frontend(queue_name, response_message, request_id):
    try:
        Connection.channel.queue_declare(queue_name)
        msg_json = {
            'requestId': request_id,
            'result': response_message
        }
        print("\n================================== RESPONSE MESSAGE ==================================\n"
              + json.dumps(msg_json, indent=2) + "\n"
              "======================================================================================\n")
        Connection.channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(msg_json))
        return True
    except StreamLostError:
        Connection.connect_to_rabbitmq()
        return False


def check_type_for_parameter(obj, parameter_name):
    try:
        if parameter_name == "licensePlate":
            str(obj)
        elif parameter_name == "status":
            str(obj)
        elif parameter_name == "resultQueue":
            str(obj)
        elif parameter_name == "op":
            str(obj)
        elif parameter_name == "requestId":
            str(obj)
        else:
            float(obj)
    except ValueError:
        return "Parameter " + parameter_name + " type mismatch"
    return True


def check_parameters(body_decoded, *args):
    for arg in args:
        if arg not in body_decoded:
            return "Parameter " + str(arg) + " is missing"
        else:
            check_type_result = check_type_for_parameter(body_decoded[arg], arg) is not True
            if check_type_result is not True
                return check_type_result
    return True


def callback(ch, method, properties, body):
    print("Task Message received, starting callback computation..")
    global db

    if db is None:
        print("db is None")
        print("================================== Waiting for task message ==================================")
        return

    if not db.isConnected():
        print("Connection with the Database failed")
        print("================================== Waiting for task message ==================================")
        return

    body_decoded = json.loads(body.decode())

    check_result = check_parameters(body_decoded, "resultQueue", "requestId", "op")
    if check_result is not True:
        print(check_result)
        print("================================== Waiting for task message ==================================")
        return
     
    
    queue_name = body_decoded["resultQueue"]
    request_id = body_decoded["requestId"]
    op = body_decoded["op"]

    print("Operation received: " + op)

    if op == "add_scooter":
        print("Starting " + op + " computation...")
        print("Checking parameters...")
        response = check_parameters(body_decoded, "licensePlate", "batteryPercentage", "latitude", "longitude",
                                    "status")
        if response is not True:
            print("check_parameters error: " + response)
            send_to_frontend(queue_name, response, request_id)
            print("================================== Waiting for task message ==================================")
            return

        print("Parameters checking succeeded")
        license_plate = body_decoded["licensePlate"]
        battery_percentage = body_decoded["batteryPercentage"]
        latitude = body_decoded["latitude"]
        longitude = body_decoded["longitude"]
        status = body_decoded["status"]

        result = db.addScooter(license_plate, latitude, longitude, battery_percentage, status)
        send_to_frontend(queue_name, result, request_id)

        if result is True:
            print(op + " succeeded")
        else:
            print(op + " not succeeded")
    elif op == "delete_scooter":
        print("Starting " + op + " computation...")
        print("Checking parameters...")
        response = check_parameters(body_decoded, "licensePlate")
        if response is not True:
            print("check_parameters error:" + response)
            send_to_frontend(queue_name, response, request_id)
            print("================================== Waiting for task message ==================================")
            return
        print("Parameters checking succeeded")
        license_plate = body_decoded["licensePlate"]
        result = db.deleteScooter(license_plate)
        send_to_frontend(queue_name, result, request_id)
        print(op + " succeeded")
    elif op == "get_available_scooters":
        print("Starting " + op + " computation...")
        print("Checking parameters...")
        print("Parameters checking succeeded")
        result = db.getScooters("FREE")
        if result is None:
            send_to_frontend(queue_name, "Error in get_available_scooters", request_id)
            print(op + " not succeeded")
            print("================================== Waiting for task message ==================================")
            return
        send_to_frontend(queue_name, result, request_id)
        print(op + " succeeded")
    elif op == "get_scooter_by_license_plate":
        print("Starting " + op + " computation...")
        print("Checking parameters...")
        response = check_parameters(body_decoded, "licensePlate")
        if response is not True:
            print("check_parameters error:" + response)
            send_to_frontend(queue_name, response, request_id)
            print("================================== Waiting for task message ==================================")
            return
        print("Parameters checking succeeded")
        license_plate = body_decoded["licensePlate"]
        result = db.getScooter(license_plate)
        if result is None:
            send_to_frontend(queue_name, "Error in get_scooter_by_license_plate", request_id)
            print(op + " not succeeded")
        else:
            send_to_frontend(queue_name, result[0], request_id)
            print(op + " succeeded")

    elif op == "update_scooter":
        print("Starting " + op + " computation...")
        print("Checking parameters...")
        response = check_parameters(body_decoded, "licensePlate", "batteryPercentage", "latitude", "longitude",
                                    "status")
        if response is not True:
            print("check_parameters error:" + response)
            send_to_frontend(queue_name, response, request_id)
            print("================================== Waiting for task message ==================================")
            return

        print("Parameters checking succeeded")
        license_plate = body_decoded["licensePlate"]
        battery_percentage = body_decoded["batteryPercentage"]
        latitude = body_decoded["latitude"]
        longitude = body_decoded["longitude"]
        status = body_decoded["status"]

        result = db.updateScooter(license_plate, latitude, longitude, battery_percentage, status)
        send_to_frontend(queue_name, result, request_id)

        if result is True:
            print(op + " succeeded")
        else:
            print(op + " not succeeded")

    else:
        msg = "Error: operation not valid"
        print(msg)
        send_to_frontend(queue_name, msg, request_id)
    print("================================== Waiting for task message ==================================")


print("Initializing parameters...")
Config.initialize_parameters()
print("Parameters initialized")

print("Connecting to RabbitMQ...")
Connection.connect_to_rabbitmq()
print("Connection to RabbitMQ succeeded")

print("Connecting to the Database...")


db = DatabaseManager(Config.mysql_address, Config.mysql_db, Config.mysql_user, Config.mysql_pwd)
if db.isConnected() is False:
    print("Error database connection")
else:
    print("Connection to the Database succeeded")
    Connection.channel.queue_declare('tasks')
    Connection.channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
    print("Start consuming")
    print("================================== Waiting for task message ==================================")
    Connection.channel.start_consuming()

