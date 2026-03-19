# CLI Commands

This document contains the CLI commands used to deploy
the serverless architecture.

## Install utilities
```bash
sudo apt install jq
```
## Create service account
```bash
export SERVICE_ACCOUNT_ID=$(yc iam service-account create \
  --name serverless-sa \
  --description "service account for cloud functions" \
  --format json | jq -r .id)

yc iam service-account list
```
## Assign role
```bash
echo "export FOLDER_ID=$(yc config get folder-id)" >> ~/.bashrc && . ~/.bashrc 
echo $FOLDER_ID

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
Ensure that the source file `index.py` exists in the working directory before deployment.
```bash
yc serverless function version create \
  --function-name cloud-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python311 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path index.py
```
## Invoke function
```bash
yc serverless function list
yc serverless function version list --function-name cloud-function
yc serverless function invoke <FUNCTION_ID>
```
## Allow public invocation
```bash
yc serverless function allow-unauthenticated-invoke \
  cloud-function
```
