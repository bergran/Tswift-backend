#!/usr/bin/env bash

CONTAINER_NAME=postgres_tswift
MACHINE_PORT=5432

docker rm -f ${CONTAINER_NAME}

docker run --name ${CONTAINER_NAME} -p ${MACHINE_PORT}:5432 \
       -e POSTGRES_PASSWORD=postgres -dt postgres