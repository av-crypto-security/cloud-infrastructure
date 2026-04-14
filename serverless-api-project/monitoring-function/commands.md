# CLI Commands
Deployment steps for serverless monitoring with PostgreSQL.

## Service Account Role
```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
  --role serverless.mdbProxies.user \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID
```

## Create PostgreSQL Cluster
```bash
yc vpc subnet list

yc managed-postgresql cluster create \
  --name monitoring-db \
  --description 'Serverless monitoring database' \
  --postgresql-version 15 \
  --environment production \
  --network-name default \
  --resource-preset c3-c2-m4 \
  --host zone-id=<ZONE_ID>,subnet-id=<SUBNET_ID> \
  --disk-type network-hdd \
  --disk-size 10 \
  --user name=<DB_USER>,password=<STRONG_PASSWORD> \
  --database name=<DB_NAME>,owner=<DB_USER> \
  --websql-access \
  --serverless-access
```

## Create Table
```sql
CREATE TABLE measurements (
    result INTEGER,
    response_time FLOAT
);
```

## Deploy Monitoring Function
```bash
yc serverless function create \
  --name monitoring-function \
  --description "Website monitoring function"

yc serverless function version create \
  --function-name monitoring-function \
  --memory 256m \
  --execution-timeout 10s \
  --runtime python311 \
  --entrypoint monitoring-function.handler \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --environment VERBOSE_LOG=True \
  --environment CONNECTION_ID=<CONNECTION_ID> \
  --environment DB_USER=<DB_USER> \
  --environment DB_HOST=<DB_HOST> \
  --source-path monitoring-function.zip
```

## Test Function
```bash
yc serverless function invoke --name monitoring-function
```

## Create Timer Trigger
```bash
yc serverless trigger create timer \
  --name monitoring-trigger \
  --invoke-function-name monitoring-function \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID \
  --cron-expression '* * * * ? *'
```
