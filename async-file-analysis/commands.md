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
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role storage.viewer

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role storage.uploader

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role ymq.reader

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role ymq.writer

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role ydb.admin

yc resource-manager folder add-access-binding $FOLDER_ID \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID \
  --role lockbox.payloadViewer
```

## Lockbox Secret

```bash
yc lockbox secret create \
  --name analysis-secret \
  --payload '[{"key": "ACCESS_KEY_ID", "text_value": "<KEY>"}, {"key": "SECRET_ACCESS_KEY", "text_value": "<SECRET>"}]'
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
yc ydb database create analysis-db --serverless
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
  --runtime python37 \
  --entrypoint index.handle_api \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --package-bucket-name $S3_BUCKET \
  --package-object-name src.zip
```

## Trigger

```bash
yc serverless trigger create message-queue \
  --name analysis-trigger \
  --queue $YMQ_QUEUE_ARN \
  --invoke-function-name analysis-worker \
  --batch-size 1
```
