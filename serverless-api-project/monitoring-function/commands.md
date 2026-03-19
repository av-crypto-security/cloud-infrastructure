# CLI Commands

This document contains the CLI commands used to deploy
the serverless architecture.

## Additional role for the SA
```bash
yc resource-manager folder add-access-binding $FOLDER_ID \
  --role serverless.mdbProxies.user \
  --subject serviceAccount:$SERVICE_ACCOUNT_ID
```
## Create PostgreSQL cluster
```bash
yc vpc subnet list

yc managed-postgresql cluster create \
  --name pg-database \
  --description 'For Serverless' \
  --postgresql-version 15 \
  --environment production \
  --network-name default \
  --resource-preset c3-c2-m4 \
  --host zone-id=<HOST_ZONE_ID>,subnet-id=<SUBNET_ID> \
  --disk-type network-hdd \
  --disk-size 10 \
  --user name=<USER_NAME>,password=<STRONG_PASSWORD> \
  --database name=<DB_NAME>,owner=<USER_NAME> \
  --websql-access \
  --serverless-access

yc managed-postgresql cluster list
yc managed-postgresql cluster get <NAME_OR_CLUSTER_ID>
```
## Create table
```sql
CREATE TABLE measurements (
    result integer,
    time float
);
```
## Create a function
```bash
echo "export CONNECTION_ID=<CONNECTION_ID>" >> ~/.bashrc && . ~/.bashrc
echo "export DB_USER=<DB_USER>" >> ~/.bashrc && . ~/.bashrc
echo "export DB_HOST=<DB_HOST>" >> ~/.bashrc && . ~/.bashrc

yc serverless function create \
  --name  function-for-postgresql \
  --description "function for postgresql"

yc serverless function version create \
  --function-name=function-for-postgresql \
  --memory=256m \
  --execution-timeout=5s \
  --runtime=python37 \
  --entrypoint=function-for-postgresql.entry \
  --service-account-id $SERVICE_ACCOUNT_ID \
  --environment VERBOSE_LOG=True \
  --environment CONNECTION_ID=$CONNECTION_ID \
  --environment DB_USER=$DB_USER \
  --environment DB_HOST=$DB_HOST \
  --source-path function-for-postgresql.py

yc serverless function version list --function-name function-for-postgresql
yc serverless function invoke --name function-for-postgresql
```
## Create a trigger-timer
```bash
yc serverless trigger create timer \
  --name trigger-for-postgresql \
  --invoke-function-name function-for-postgresql \
  --invoke-function-service-account-id $SERVICE_ACCOUNT_ID \
  --cron-expression '* * * * ? *'
```
