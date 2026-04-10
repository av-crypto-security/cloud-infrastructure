# Deployment Commands

## Service Account

```bash
yc iam service-account create \
  --name analysis-sa \
  --description "service account for async pipeline"
```

### Assign roles:

```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role storage.viewer

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role storage.uploader

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role ymq.reader

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role ymq.writer

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role ydb.admin

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role lockbox.payloadViewer

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$ANALYSIS_SERVICE_ACCOUNT_ID \
  --role serverless.functions.invoker
```

## Lockbox Secret

```bash
yc iam access-key create --service-account-name analysis-sa

yc lockbox secret create --name analysis-secret \
  --folder-id $FOLDER_ID \
  --description "keys for serverless" \
  --payload '[{"key": "ACCESS_KEY_ID", "text_value": "<ACCESS_KEY_ID>"}, {"key": "SECRET_ACCESS_KEY", "text_value": "<SECRET_ACCESS_KEY_VALUE>"}]'

```

## Message Queue

```bash
aws sqs create-queue \
  --queue-name analysis-queue \
  --endpoint https://message-queue.api.cloud.yandex.net/
```

### Get ARN
```bash
aws sqs get-queue-attributes \
  --endpoint https://message-queue.api.cloud.yandex.net \
  --queue-url $YMQ_QUEUE_URL \
  --attribute-names QueueArn
```

## YDB

```bash
yc ydb database create analysis-db \
  --serverless \
  --folder-id $FOLDER_ID

aws dynamodb create-table \
  --cli-input-json file://tasks.json \
  --endpoint-url $DOCAPI_ENDPOINT \
  --region ru-central1
```

## Functions

```bash
yc serverless function create --name analysis-api
yc serverless function create --name analysis-worker
```

### Deploy:

```bash
yc serverless function version create \
  --function-name analysis-api \
  --memory=256m \
  --execution-timeout=10s \
  --runtime=python311 \
  --entrypoint=index.handle_api \
  --service-account-id $ANALYSIS_SERVICE_ACCOUNT_ID \
  --environment SECRET_ID=$SECRET_ID \
  --environment YMQ_QUEUE_URL=$YMQ_QUEUE_URL \
  --environment DOCAPI_ENDPOINT=$DOCAPI_ENDPOINT \
  --environment S3_BUCKET=$S3_BUCKET \
  --package-bucket-name $S3_BUCKET \
  --package-object-name src.zip

yc serverless function version create \
  --function-name analysis-worker \
  --memory=512m \
  --execution-timeout=60s \
  --runtime=python311 \
  --entrypoint=index.handle_process_event \
  --service-account-id $ANALYSIS_SERVICE_ACCOUNT_ID \
  --environment SECRET_ID=$SECRET_ID \
  --environment YMQ_QUEUE_URL=$YMQ_QUEUE_URL \
  --environment DOCAPI_ENDPOINT=$DOCAPI_ENDPOINT \
  --environment S3_BUCKET=$S3_BUCKET \
  --package-bucket-name $S3_BUCKET \
  --package-object-name src.zip
```

## Trigger

```bash
yc serverless trigger create message-queue \
  --name analysis-trigger \
  --queue $YMQ_QUEUE_ARN \
  --queue-service-account-id $ANALYSIS_SERVICE_ACCOUNT_ID \
  --invoke-function-name analysis-worker  \
  --invoke-function-service-account-id $ANALYSIS_SERVICE_ACCOUNT_ID \
  --batch-size 1 \
  --batch-cutoff 10s
```
