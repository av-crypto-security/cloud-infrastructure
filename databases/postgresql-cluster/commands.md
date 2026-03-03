# PostgreSQL Cluster — Operational Commands

---

## Terraform Deployment
```bash
cd terraform/

terraform init
terraform validate
terraform plan
terraform apply
```
Show created resources
```bash
terraform state list
```
---

## Install PostgreSQL Client
```bash
sudo apt update
sudo apt install -y postgresql-client
```
---

## Download Root CA Certificate
```bash
mkdir -p ~/.postgresql

wget https://storage.yandexcloud.net/cloud-certs/CA.pem \
     -O ~/.postgresql/root.crt

chmod 0600 ~/.postgresql/root.crt
```
---

## Connect to Cluster (SSL Public Access)
```bash
psql "host=<cluster-fqdn> \
      port=6432 \
      sslmode=verify-full \
      dbname=<database-name> \
      user=<db-user> \
      target_session_attrs=read-write"
```
---

## Deploy Schema
```bash
psql "host=<cluster-fqdn> \
      port=6432 \
      dbname=<database-name> \
      user=<db-user> \
      sslmode=verify-full" \
      < schema.sql
```
[`schema.sql`](schema.sql) — Database schema example

---

## Create Table (Example)
```sql
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    status TEXT NOT NULL CHECK (status IN ('NEW','PAID','SHIPPED','CANCELLED')),
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```
---

## Import CSV Sample Data
```sql
\copy app.employee(full_name, position, qualification)
FROM 'employees.csv'
DELIMITER ','
CSV HEADER;
```
---

## Check Replication Role
```sql
SELECT pg_is_in_recovery();
```
```
-- false = primary
-- true  = replica
```
---

## Check Replication Status (Primary)
```sql
SELECT * FROM pg_stat_replication;
```
---

## 8. Create Database User
```sql
CREATE USER app_user WITH PASSWORD 'secure_password';

GRANT CONNECT ON DATABASE app_db TO app_user;

GRANT USAGE ON SCHEMA app TO app_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;
```
---

## 9. Backup (Logical Dump)
```bash
pg_dump \
  --host=<cluster-fqdn> \
  --port=6432 \
  --username=<user> \
  --format=custom \
  --file=backup.dump \
  <database-name>
```
---

## 10. Restore
```bash
pg_restore \
  --host=<cluster-fqdn> \
  --port=6432 \
  --username=<user> \
  --dbname=<database-name> \
  backup.dump
```
---

## 11. Show Active Connections
```sql
SELECT * FROM pg_stat_activity;
```
---

## 12. Check Database Size
```sql
SELECT pg_size_pretty(pg_database_size('<database-name>'));
```
