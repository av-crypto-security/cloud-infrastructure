# CLI Commands

This document contains the CLI commands used to deploy
the serverless architecture.

## Install utilities

sudo apt install jq

## Create service account

yc iam service-account create \
  --name service-account-for-cf

## Assign role

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role editor

## Create cloud function

yc serverless function create \
  --name my-first-function

## Deploy function version

yc serverless function version create \
  --function-name my-first-function \
  --memory 256m \
  --execution-timeout 5s \
  --runtime python37 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --source-path index.py

## Invoke function

yc serverless function invoke <FUNCTION_ID>

## Allow public invocation

yc serverless function allow-unauthenticated-invoke \
  my-first-function

## Create Object Storage trigger

yc serverless trigger create object-storage \
  --name my-first-trigger \
  --bucket-id <BUCKET_NAME> \
  --events create-object \
  --invoke-function-name my-trigger-function \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID

## Create PostgreSQL cluster

yc managed-postgresql cluster create \
  --name my-pg-database \
  --postgresql-version 15 \
  --network-name default \
  --disk-type network-hdd \
  --disk-size 10

## Create timer trigger

yc serverless trigger create timer \
  --name trigger-for-postgresql \
  --invoke-function-name function-for-postgresql \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID \
  --cron-expression "* * * * ? *"

## Create API Gateway

yc serverless api-gateway create \
  --name hello-world \
  --spec hello-world.yaml

## Update API Gateway

yc serverless api-gateway update \
  --name hello-world \
  --spec hello-world.yaml
