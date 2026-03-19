# Creating a Cloud Function via CLI

This document demonstrates how to create and deploy a simple HTTP function using the Yandex Cloud CLI.
The goal is to understand the basic workflow of serverless deployment and version management.

## API-Gateway deployment
```bash
yc serverless api-gateway create \
  --name hello-world \
  --spec=hello-world.yaml \
  --description "hello world"

yc serverless api-gateway list
yc serverless api-gateway get --name hello-world
```

## API-Gateway check
```
https://<API_Gateway_ID>.apigw.yandexcloud.net/hello
https://<API_Gateway_ID>.apigw.yandexcloud.net/hello?user=my_user
```
## Install pipreqs
```bash
pip install pipreqs
pipreqs $PWD --print
pipreqs $PWD --force
```
if not, then: install using flag `--break-system-packages`
in case of wrong encoding: `iconv -f ISO-8859-1 -t utf-8 function-for-user-requests.py -o function-for-user-requests.py`
`pip install --upgrade pipreqs`
## Create a function
```bash
echo "export CONNECTION_ID=<CONNECTION_ID>" >> ~/.bashrc && . ~/.bashrc
echo "export DB_USER=<DB_USER>" >> ~/.bashrc && . ~/.bashrc
echo "export DB_HOST=<DB_HOST>" >> ~/.bashrc && . ~/.bashrc

yc serverless function create \
  --name function-for-user-requests \
  --description "function for response to user"
 
yc serverless function version create \
  --function-name=function-for-user-requests \
  --memory=256m \
  --execution-timeout=5s \
  --runtime=python37 \
  --entrypoint=function-for-user-requests.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --environment VERBOSE_LOG=True \
  --environment CONNECTION_ID=$CONNECTION_ID \
  --environment DB_USER=$DB_USER \
  --environment DB_HOST=$DB_HOST \
  --source-path function-for-user-requests.py
```
## Reload a specification (to make the function available with API Gateway)
```bash
yc serverless api-gateway update \
  --name hello-world \
  --spec=hello-world.yaml
```
## Call the function 
```
https://<API_Gateway_ID>.apigw.yandexcloud.net/results
https://<API_Gateway_ID>.apigw.yandexcloud.net/results?secret=<SECRET_PARAMETER_ADDED_TO_REQUEST_PARAMETERS>
```
