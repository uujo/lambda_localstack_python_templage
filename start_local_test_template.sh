#!/bin/bash

while getopts ui option ;do
    case ${option} in
        i) INTERACTIVE="SET" ;;
        u) SRC_UPDATE="SET" ;;
        *) echo "No option is added -i interactive mode for localstack";;
    esac
done

update_source() {
    echo "Replace build source to original source"

    cp -rf $PWD/src/projectname $PWD/build/LambdaTemplateTest
}

if [[ ${SRC_UPDATE} = "SET" ]]
    then
        update_source
        exit 0
fi

aws_status() {
    echo "check localstack aws status"
    aws dynamodb list-tables --endpoint-url http://localhost:4566
    aws sqs list-queues --endpoint-url=http://localhost:4566
    aws s3api list-buckets --endpoint-url=http://localhost:4566
}

# sam build for the local test
echo "sam build"
sam build -t ./local-test-configs/s3-sqs-dynamo-config/template-sam.yaml -m requirements-lambda.txt -u -b ./build/ -s src/

# start localstat
echo "Start localstack"

if [[ ${INTERACTIVE} = "SET" ]]
    then
        docker-compose -f ./local-test-configs/s3-sqs-dynamo-config/docker-compose.yaml up
    else
        docker-compose -f ./local-test-configs/s3-sqs-dynamo-config/docker-compose.yaml up -d
        # wait until local stack is set
        sleep 18
        aws_status
fi

