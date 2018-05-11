# About
Hello world Flask app deployable to AWS API gateway

# Prepare environment
* ```virtualenv --no-download --python=python3.6 env```
* ```source env/bin/activate```
* ```pip3 install -r "requirements.txt“```
* ```pip3 install aws-sam-cli```

# Deploy using aws sam
```bash
sam deploy --template-file template.yaml --stack-name <your stack name> --region us-east-1 --profile sandbox --capabilities CAPABILITY_IAM --force-upload
```