import string

import pymysql.cursors
import pymysql
import json


class DatabaseManager:

    # pip install PyMySql before using
    # main table: scooters
    # table attributes: licensePlate, latitude, longitude, batteryPercentage, status

    # Open new connection
    def __init__(self, host, db, user, password):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)  # results are returned as dictionaries

    # CREATE
    def addScooter(self, licensePlate, latitude, longitude, batteryPercentage, status):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO scooters VALUES (\'{}\', {}, {}, {}, \'{}\');"
                print(sql.format(licensePlate, latitude, longitude, batteryPercentage, status))
                cursor.execute(sql.format(licensePlate, latitude, longitude, batteryPercentage, status))

            self.connection.commit()
            return True
        except:
            print("An exception occurred")
            return False
            # READ

    def getScooters(self, status):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * from scooters WHERE status = \'{}\'"
                cursor.execute(sql.format(status))
                result = cursor.fetchall()

            self.connection.commit()
        except:
            print("An exception occurred")
            return None
        return result

    def getScooter(self, licensePlate):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * from scooters WHERE licensePlate = \'{}\'"
                cursor.execute(sql.format(licensePlate))
                result = cursor.fetchall()

            self.connection.commit()
        except:
            print("An exception occurred")
            return None
        return result

        # UPDATE

    def updateScooter(self, licensePlate, latitude, longitude, batteryPercentage, status):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE scooters SET latitude = \'{}\', longitude = \'{}\', batteryPercentage = \'{}\', status = \'{}\' WHERE licensePlate = \'{}\' "
                print(sql.format(latitude, longitude, batteryPercentage, status, licensePlate))
                cursor.execute(sql.format(latitude, longitude, batteryPercentage, status, licensePlate))

            self.connection.commit()
            return True
        except:
            print("An exception occurred")
            return False

    # DELETE
    def deleteScooter(self, licensePlate):
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM scooters WHERE licensePlate = \'{}\'"
                print(sql.format(licensePlate))
                cursor.execute(sql.format(licensePlate))
                
            self.connection.commit()
            return True
        except:
            print("An exception occurred")
            return False

    # close connection
    def close(self):
        self.connection.close()

    def isConnected(self):
        return self.connection.open


