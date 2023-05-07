#!/bin/bash

CONTAINER_NAME=tijk-bot
IMAGE_NAME=codeman1o1/tijk-bot

docker stop $CONTAINER_NAME
docker container rm $CONTAINER_NAME
docker image rm $IMAGE_NAME

docker build -t $IMAGE_NAME .
docker run -d --name $CONTAINER_NAME -v /var/run/docker.sock:/var/run/docker.sock --restart unless-stopped $IMAGE_NAME
