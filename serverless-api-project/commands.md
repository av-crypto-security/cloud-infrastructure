# CLI Commands

This document contains the CLI commands used to deploy
the serverless architecture.

## Install utilities
```bash
sudo apt install jq
```
## Create service account
```bash
yc iam service-account create \
  --name service-account-for-cf
```
## Assign role
```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role editor
```
## Create cloud function
```bash
yc serverless function create \
  --name cloud-function
```
## Deploy function version
```bash
yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python37 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path index.py
```
## Invoke function
```bash
yc serverless function invoke <FUNCTION_ID>
```
## Allow public invocation
```bash
yc serverless function allow-unauthenticated-invoke \
  cloud-function
```
## Create Object Storage trigger
```bash
yc serverless trigger create object-storage \
  --name my-first-trigger \
  --bucket-id <BUCKET_NAME> \
  --events create-object \
  --invoke-function-name my-trigger-function \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID
```
## Create PostgreSQL cluster
```bash
yc managed-postgresql cluster create \
  --name my-pg-database \
  --postgresql-version 15 \
  --network-name default \
  --disk-type network-hdd \
  --disk-size 10
```
## Create timer trigger
```bash
yc serverless trigger create timer \
  --name trigger-for-postgresql \
  --invoke-function-name function-for-postgresql \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID \
  --cron-expression "* * * * ? *"
```
## Create API Gateway
```bash
yc serverless api-gateway create \
  --name hello-world \
  --spec hello-world.yaml
```
## Update API Gateway
```bash
yc serverless api-gateway update \
  --name hello-world \
  --spec hello-world.yaml
```
