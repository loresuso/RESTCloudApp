 #!/bin/sh
docker pull mysql mysql server
docker run --name mydb -d -p 3306:3306 mysql/mysql-server
docker logs mydb 2>&1 | grep GENERATED
docker exec -it mydb bash