# lambda_localstack_python_templage
Template for lambda  with localstack and sam integration for localtest 

## Prerequesite (on Mac)

* [Python3](https://www.python.org/downloads/)

* [AWS client](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) (pip3 install awscli --upgrade --user)

* [AWS SAM client](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html#serverless-sam-cli-install-mac-pip) (pip3 install --user aws-sam-cli)
  
   * Reference: [Adjust path to use sam cli command](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac-path.html)

* [Docker](https://docs.docker.com/docker-for-mac/install/) - need for the local lambda function testing


## Set up git hooks (pre-commit, pre-push) - This is one time setting. Doesn't have to be repeated every time. (Warning: Hooks are properly triggered only when git command is used on the top level of the repository (nci-vasap-annotation/) currently.

This will copy the _pre-commit_, _pre-push_ files under .git/hooks
```
> git config --local init.templatedir './.git_templates'
> git init
```

**Pre commit:** change the format using Black and Pylint checking (Will fail to commit if pylint score is not 10.

**Pre push:** check the unittest and code coverage (Will fail to push if either unittest fails or code coverage is less than 95%

For special cases, if you still need to commit, push the code use _--no-verify_ option on git commands

```
> git commit --no-verify
> git push origin [branch_name] --no-verify
```

## Local test set up using aws sam and localstack (with python3 venv) - Alternative step by step instrucntion is [here](local-test-setup)

* getting the source code
 
  `git clone https://github.com/BIAD/nci-varsap-annotation.git`
 
* set the virtual environment (optional, you can use other virtual env tools or without it)
  
  `cd nci-varsap-annotation`
  
  `python3 -m venv .venv`
  
  `source .venv/bin/activate`  - activate virtual environment
  
  `pip install -r requirements.txt` - on time setting
 
* To start local test setup

  `bin/start_local_test`   
  
  _-i_ option sets interactive mode on localstack instead of running it background, if you want to monitor localstack log use this option. Without this option, it automatically create the sample data in S3 bucket.


* To check the table, sqs and bucket are created (**Use this setting only if you use _-i_ option, without _-i_, these steps runs automatically**)
  
  `aws dynamodb list-tables --endpoint-url http://localhost:4569`
  
  `aws sqs list-queues --endpoint-url=http://localhost:4576`
  
  `aws s3api list-buckets --endpoint-url=http://localhost:4572`
  
  * put data in S3
  
    `aws s3api put-object --endpoint-url=http://localhost:4572  --bucket VARSAP_BUCKET --key annotation/g-snv-7-7578212-G-A/data.json --body tests/s3_test_data.json`

  * To check S3 object is created

    `aws s3api list-objects --bucket=VARSAP_BUCKET --endpoint-url=http://localhost:4572` 
  
  
* To test annotation lambdas

  * invoke S3 ObjectCreated event
  
    `sam local invoke HandleS3Event -t build/template.yaml --docker-network [repository_name]_local_aws_network -e tests/s3_test_event.json`
  
  * To check whether table has an entry inserted.

    `aws dynamodb scan --table-name TEST_TABLE --endpoint-url http://localhost:4569`
  
  * To check sqs messge is queued
  
    `aws sqs receive-message --queue-url http://localhost:4576/queue/TEST_QUEUE --endpoint-url=http://localhost:4576 --max-number-of-messages=10`
  
  * invoke SQS event
  
    `sam local invoke RequestAnnotation -t build/template.yaml --docker-network [repository_name]_local_aws_network -e tests/sqs_test_event.json`
    
  * check S3 Object is updated: (Might take a while to update annotations) - It will store object in _s3_test_out.json_
   
    `aws s3api get-object --endpoint-url=http://localhost:4572  --bucket TEST_BUCKET --key [path_to_object]/[name_of_object].json s3_test_out.json`
  
* To stop the local test and clean up docker

  `bin/stop_local_test`
    

## Integration Test: To be added

 
## Reference
* [AWS SAM guick start guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-quick-start.html)
* [SAM template](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md)
* [SQS](https://aws.amazon.com/blogs/aws/aws-lambda-adds-amazon-simple-queue-service-to-supported-event-sources/)
* [Lambda function best practice](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
  * Take advantage of Execution Context reuse to improve the performance of your function.
  * Use AWS Lambda Environment Variables to pass operational parameters to your function.
  * Control the dependencies in your function's deployment package.
  * Minimize your deployment package size to its runtime necessities.
  * Reduce the time it takes Lambda to unpack deployment packages.
  * Minimize the complexity of your dependencies.
* [Pros and cons of monorepo](https://serverless-stack.com/chapters/organizing-serverless-projects.html)
* [Directory structure for multiple Lambdas](https://serverless.readme.io/docs/project-structure)
* [Documenting REST API](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-documenting-api.html)
* [Mocking AWS stack locally](https://medium.com/@andyalky/developing-aws-apps-locally-with-localstack-7f3d64663ce4)
* [LocalStack](https://github.com/localstack/localstack)
* [LocalStack with aws sam](http://www.piotrnowicki.com/python/aws/2018/11/16/aws-local-lambda-invocation/)
* [LocalStack with docker](https://itnext.io/docker-compose-aws-localstack-why-not-both-fc8a1db84eca)
* [Lambda debugging](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-debugging-python.html)
* [Scheduling lambda periodically](https://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html)
* [Pyinstrument (python profiling)](https://github.com/joerick/pyinstrument)
* [S3 event message structure](https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html)
* [aws xray python](https://github.com/aws/aws-xray-sdk-python)

