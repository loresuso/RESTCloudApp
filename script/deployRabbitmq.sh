#!/bin/sh
cd ../rabbit-mq
docker build -t some-rabbit .
docker run -p 4369:4369 -p 15671:15671 -p 15672:15672 -p 5671:5671 -p 5672:5672 -p 15691:15691 -p 15692:15692 -p 25672:25672 --hostname rabbit --name rabbit -d some-rabbit