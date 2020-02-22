#!/bin/bash

while getopts si option ;do
    case ${option} in
        i) INTERACTIVE="SET" ;;
        *) echo "No option is added -i interactive mode for localstack";;
    esac
done

aws_status() {
    echo "check localstack aws status"
    aws dynamodb list-tables --endpoint-url http://localhost:4569
    aws sqs list-queues --endpoint-url=http://localhost:4576
    aws s3api list-buckets --endpoint-url=http://localhost:4572
}

# sam build for the local test
echo "sam build"
sam build -t template-sam.yaml -m requirements-lambda.txt -u -b ./build/ -s projectname/

# start localstat
echo "Start localstack"

if [[ ${INTERACTIVE} = "SET" ]]
    then
        docker-compose up
    else
        docker-compose up -d
        # wait until local stack is set
        sleep 10
        aws_status
fi

