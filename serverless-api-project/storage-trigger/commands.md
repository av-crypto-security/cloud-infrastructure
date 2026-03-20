## ===Under construction===
# CLI Commands

This document contains the CLI commands used to deploy
the serverless architecture.

## SA modification
```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
    --role storage.editor \
    --subject serviceAccount:$SERVICE_ACCOUNT_ID

yc iam access-key create --service-account-name service-account-for-cf
```
## OS bucket for trigger using tf
```bash
sudo vi main.tf
terraform init
terraform plan
terraform apply
```
## Function modification
```bash
yc serverless function create --name cloud-function

yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python37 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path cloud-function.zip

echo "export ACCESS_KEY=<ACCESS_KEY>" >> ~/.bashrc && . ~/.bashrc
echo "export SECRET_KEY=<SECRET_KEY>" >> ~/.bashrc && . ~/.bashrc
echo "export BUCKET_NAME=bucket-for-trigger" >> ~/.bashrc && . ~/.bashrc

yc serverless function version list --function-name cloud-function

yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python37 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-version-id <ID> \
  --environment ACCESS_KEY=$ACCESS_KEY \
  --environment SECRET_KEY=$SECRET_KEY \
  --environment BUCKET_NAME=$BUCKET_NAME
```
## Function call
```bash
yc serverless function list
yc serverless function version list --function-name cloud-function

yc serverless function invoke <FUNCTION_ID>

yc serverless function get cloud-function
```
## Trigger function
```bash
yc serverless function create --name trigger-function

yc serverless function version create \
  --function-name trigger-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python37 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path index.py

yc serverless function version list --function-name trigger-function

yc serverless trigger create object-storage \
  --name first-trigger \
  --bucket-id $BUCKET_NAME \
  --events 'create-object' \
  --invoke-function-name trigger-function \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID

yc serverless function list
yc serverless function version list --function-name cloud-function

yc serverless function invoke <FUNCTION_ID>

yc serverless function get cloud-function
```

## Check if the new Object created
```bash
yc serverless function logs trigger-function
```
