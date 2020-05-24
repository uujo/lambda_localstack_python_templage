#!/bin/bash

echo "shutting down localstack"
docker container stop $(docker container ls -aq)
docker-compose -f ./local-test-configs/apigw-dynamo-config/docker-compose.yaml down