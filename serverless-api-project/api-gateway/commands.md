# CLI Commands

Deployment of REST API for monitoring results.

## API Gateway Deployment

```bash
yc serverless api-gateway create \
  --name api-gateway \
  --spec=openapi.yaml \
  --description "Monitoring API Gateway"

yc serverless api-gateway list
yc serverless api-gateway get --name api-gateway
```

## Deploy API Function

```bash
yc serverless function create \
  --name api-function \
  --description "API for monitoring results"

yc serverless function version create \
  --function-name api-function \
  --memory 256m \
  --execution-timeout 10s \
  --runtime python311 \
  --entrypoint index.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --environment CONNECTION_ID=<CONNECTION_ID> \
  --environment DB_USER=<DB_USER> \
  --environment DB_HOST=<DB_HOST> \
  --environment API_TOKEN=<API_TOKEN> \
  --source-path api-function.zip
```

## Update API Gateway

```bash
yc serverless api-gateway update \
  --name api-gateway \
  --spec=openapi.yaml
```

## Test API

```bash
https://<API_ID>.apigw.yandexcloud.net/results
https://<API_ID>.apigw.yandexcloud.net/results?token=<API_TOKEN>
```
