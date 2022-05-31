# Cloudformation bootstrap for AWS event engine


## deploy the vanilla cloudformation:

``` bash
aws cloudformation deploy --template-file bootstrap.yaml --stack-name devday-bootstrap --capabilities CAPABILITY_NAMED_IAM
```

## Deployment description

This will create a codebuild that will deploy a CDK project with the following steps

- run cdk bootstrap in the given region
- run cdk deploy

## How to clean up

This template also create another codebuild for cleaning purposes.
Just go to codebuild and look for selfdestruct and start the build to delete everything.