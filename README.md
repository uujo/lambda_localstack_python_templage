# nci-aws-lambda-localstack-template

This provides a templates for aws lambda test in local environment using localstack or local server instances (i.e. dynamoDB). This examples shows only fraction of the services localstack provides. The full list of services are [here](https://github.com/localstack/localstack). This template provides the basic settings for local test which can be used in different projects with minimal configuration changes. Details for the configuration changes is explained `How to use this template` section below.

## Prerequesite (on Mac)

* [Python3](https://www.python.org/downloads/)

* [Docker](https://docs.docker.com/docker-for-mac/install/) - need for the local lambda function testing with sam

* [AWS client](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

* [AWS SAM client](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html)
 

## getting the source code
 
  `git clone https://github.com/BIAD/nci-aws-lambda-localstack-template.git`
  
  `cd lambda-localstack-template`
  

## Set up git hooks (pre-commit, pre-push) - This is one time setting. Doesn't have to be repeated every time. 

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

## set PYTHONPATH for unittest

   `export PYTHONPATH=$PWD/src:$PWD/tests:$PYTHONPATH`
   
   If virtual environment is used below, you can set the above path in __.venv/bin/activate__ file
   
  
## Local test set up using aws sam and localstack (with python3 venv) - virtual environment setting is optional.
 
* set the virtual environment (optional, you can use other virtual env tools or without it) 
  
  `cd lambda-localstack-template`
  
  `python3 -m venv .venv`
  
  `source .venv/bin/activate`  - activate virtual environment
  
  `pip install -r requirements.txt` - one time setting 
     (If install fails with __xcun__ error, run __xcode-select --install__)
   
* Now it is ready to set up the test below.
     
* After all the test is done. get out of virtual environment.

  `deactivate`
  
## Tests Examples

### [Lambda with dynamo, API gateway testing (Localstack)](https://github.com/uujo/lambda-localstack-template/wiki/Lambda-Dynamo-Test)

 
### [Lambda with dynamo, s3, sqs testing (Localstack)](https://github.com/uujo/lambda-localstack-template/wiki/Lambda-S3-SQS-Dynamo-Test)

### [Lambda with dynamo, API gateway testing (local dynamo server)](https://github.com/BIAD/lambda-localstack-template/wiki/Lambda-Local-Dynamo-Server-Test)


## Integration Test: To be added


## [How to use this template](https://github.com/uujo/lambda-localstack-template/wiki/How-to-use-this-template) 

 * goal: With minimal configuation change, testing environment can be set up for different project.
 * There are two main configuration - One for localstack and one for sam. If starting and stop scrip need to be changed as well if you want to reuse the script.

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

