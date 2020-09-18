  mysql -uroot -p
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
    use mysql;
    UPDATE user SET host='%' WHERE host='localhost' AND user='root';
    FLUSH PRIVILEGES;
    CREATE SCHEMA `scooterdb`;
	USE scooterdb
    DROP TABLE IF EXISTS `scooters`;
    CREATE TABLE `scooters` (
      `licensePlate` varchar(45) NOT NULL,
      `latitude` float(10,8) DEFAULT NULL,
      `longitude` float(10,8) DEFAULT NULL,
      `batteryPercentage` int DEFAULT NULL,
      `status` varchar(45) DEFAULT NULL,
      PRIMARY KEY (`licensePlate`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    LOCK TABLES `scooters` WRITE;
    INSERT INTO `scooters` VALUES ('AAA',99.90000000,99.90000000,41,'BOOKED'),('CCC',55.50000000,55.50000000,13,'FREE'),('X4CNP4',10.30000000,11.30000000,80,'BUSY'),('X4CNPC',10.00000000,11.00000000,80,'BUSY'),('X8CNPC',44.30000000,80.60000000,75,'FREE');
    UNLOCK TABLES;
