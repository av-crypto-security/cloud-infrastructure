# CLI Commands

This document describes deployment steps for an event-driven serverless pipeline.

## Service Account Configuration
```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
    --role storage.editor \
    --subject serviceAccount:$SERVICE_ACCOUNT_ID

yc iam access-key create --service-account-name serverless-sa
```
## Object Storage (Terraform)
```bash
terraform init
terraform plan
terraform apply
```
## Upload Function Deployment

```bash
yc serverless function create --name cloud-function

yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 10s \
  --runtime python311 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path cloud-function.zip
```
### Create version with environment variables
```bash
yc serverless function version list --function-name cloud-function

yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 10s \
  --runtime python311 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-version-id <VERSION_ID> \
  --environment ACCESS_KEY=<ACCESS_KEY> \
  --environment SECRET_KEY=<SECRET_KEY> \
  --environment BUCKET_NAME=bucket-for-trigger
```
## Function Invocation
```bash
yc serverless function list
yc serverless function version list --function-name cloud-function
yc serverless function invoke <FUNCTION_ID>
yc serverless function get cloud-function
```
## Trigger Function Deployment
```bash
yc serverless function create --name trigger-function

yc serverless function version create \
  --function-name trigger-function \
  --memory 256m \
  --execution-timeout 10s \
  --runtime python311 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path trigger-index.py
```
## Create Object Storage Trigger
```bash
yc serverless trigger create object-storage \
  --name first-trigger \
  --bucket-id bucket-for-trigger \
  --events 'create-object' \
  --invoke-function-name trigger-function \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID
```
### Trigger Validation
```bash
yc serverless function logs trigger-function
```
