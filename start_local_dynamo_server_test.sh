#!/bin/bash

while getopts u option ;do
    case ${option} in
        u) SRC_UPDATE="SET" ;;
        *) echo "No option is added -i interactive mode for localstack";;
    esac
done

update_source() {
    echo "Replace build source to original source"

    cp -rf $PWD/src/projectname $PWD/build/PostTest
    cp -rf $PWD/src/projectname $PWD/build/GetTest
    cp -rf $PWD/src/projectname $PWD/build/PutTest
    cp -rf $PWD/src/projectname $PWD/build/DeleteTest
}

aws_status() {
    echo "check local dynamodb aws status"
    aws dynamodb list-tables --endpoint-url http://localhost:8000
}

if [[ ${SRC_UPDATE} = "SET" ]]
    then
        update_source
        exit 0
fi

# sam build for the local test
echo "sam build"
sam build -t ./local-test-configs/apigw-dynamo-server-config/api-gw-dynamo-server-sam.yaml -m requirements-lambda.txt -u -b ./build/ -s src/

# start local DynamoDB
echo "Start local DynamoDB"

docker network create lambda-local
docker run -d -v "$PWD":/dynamodb_local_db -p 8000:8000 --network lambda-local --name dynamodb amazon/dynamodb-local

sleep 10

echo "Create a test table"
aws dynamodb create-table --endpoint-url=http://localhost:8000 \
            --table-name TEST_TABLE \
            --attribute-definitions \
                AttributeName=id,AttributeType=S \
            --key-schema \
                AttributeName=id,KeyType=HASH \
            --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws_status

# start sam local
echo "Start sam local with api gateway"

sam local start-api -t build/template.yaml --docker-network lambda-local


