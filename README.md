# About
Hello world Flask app deployable to AWS API gateway

# Prepare environment
* ```virtualenv --no-download --python=python3.6 env```
* ```source env/bin/activate```
* ```pip3 install -r "requirements.txt"```
* ```pip3 install aws-sam-cli```

# Prepare and upload lambda zip file
```bash
zip -r /tmp/lambda.zip app.py
cd env/lib/python3.6/site-packages
zip -ur /tmp/lambda.zip *
aws --profile sandbox s3 cp /tmp/lambda.zip s3://jakub-aws-sam-lambdas/lambda.zip
```
Don't forget to change the name of zip file or use your own bucket (otherwise you may rewrite lambda which belongs to others).

# Deploy using aws sam
- Replace all **TODO**  lines in ```template.yaml```
- Execute:
```bash
sam deploy --template-file template.yaml --stack-name <your stack name> --region <region> --profile <your profile name> --capabilities CAPABILITY_IAM --force-upload
```

## example
```bash
sam deploy --template-file template-demo.yaml --stack-name pyvo-demo-test --region eu-central-1 --profile sam --capabilities CAPABILITY_IAM --force-upload
```

# AWS doc links
- https://github.com/awslabs/serverless-application-model/blob/develop/versions/2016-10-31.md
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html