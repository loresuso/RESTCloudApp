#!/bin/sh
cd ../haproxy
docker build -t myhaproxy .
docker run -d --name myhaproxy1 --network host myhaproxy