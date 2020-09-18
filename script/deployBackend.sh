#!/bin/sh
cd ../back-end
docker build -t mybackend .
docker run -d --name mybackend1 mybackend