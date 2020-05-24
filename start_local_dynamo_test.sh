#!/bin/bash

while getopts iu option ;do
    case ${option} in
        i) INTERACTIVE="SET" ;;
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
    echo "check localstack aws status"
    aws dynamodb list-tables --endpoint-url http://localhost:4566
}

if [[ ${SRC_UPDATE} = "SET" ]]
    then
        update_source
        exit 0
fi

# sam build for the local test
echo "sam build"
sam build -t ./local-test-configs/apigw-dynamo-config/api-gw-template-sam.yaml -m requirements-lambda.txt -u -b ./build/ -s src/

# start localstat
echo "Start localstack"

if [[ ${INTERACTIVE} = "SET" ]]
    then
        docker-compose -f ./local-test-configs/apigw-dynamo-config/docker-compose.yaml up
    else
        docker-compose -f ./local-test-configs/apigw-dynamo-config/docker-compose.yaml up -d
        # wait until local stack is set
        sleep 15
        aws_status
        echo "Start aws sam local api gateway"
        sam local start-api -t build/template.yaml --docker-network apigw-dynamo-config_local_aws_network
fi

