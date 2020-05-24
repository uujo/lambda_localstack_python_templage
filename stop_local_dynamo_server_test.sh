#!/bin/bash

echo "shutting down local dynamodb"
docker container stop $(docker container ls -aq)
docker system prune