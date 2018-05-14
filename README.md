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
sam deploy --template-file template.yaml --stack-name <your stack name> --region us-east-1 --profile sandbox --capabilities CAPABILITY_IAM --force-upload
```