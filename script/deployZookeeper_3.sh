#!/bin/sh
docker run -d \
   -p 2181:2181 \
   -p 2888:2888 \
   -p 3888:3888 \
   --name myzk-1 \
   -e ZOO_MY_ID=1 \
   -e ZOO_SERVERS='server.1=172.16.1.235:2888:3888;2181 server.2=172.16.2.27:2888:3888;2181 server.3=0.0.0.0:2888:3888;2181' \
    --restart always \
    zookeeper
