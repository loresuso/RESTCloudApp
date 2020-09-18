#!/bin/bash
cd ../flask-server
docker build -t myfrontend .
docker run -d -p 8080:8080 --name frontend myfrontend
