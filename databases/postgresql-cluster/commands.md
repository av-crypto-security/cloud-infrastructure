# PostgreSQL Cluster — Operational Commands

---

## 1. Install PostgreSQL Client

sudo apt update
sudo apt install -y postgresql-client

---

## 2. Download Root CA Certificate

mkdir -p ~/.postgresql

wget https://storage.yandexcloud.net/cloud-certs/CA.pem \
     -O ~/.postgresql/root.crt

chmod 0600 ~/.postgresql/root.crt

---

## 3. Connect via SSL (Public Access)

psql "host=<cluster-fqdn> \
      port=6432 \
      sslmode=verify-full \
      dbname=<database-name> \
      user=<db-user> \
      target_session_attrs=read-write"

---

## 4. Create Table (Example)

CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    status TEXT NOT NULL CHECK (status IN ('NEW','PAID','SHIPPED','CANCELLED')),
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

---

## 5. Import CSV Data

\copy orders(order_id,customer_id,status,status,total_amount,created_at) \
FROM '/path/orders.csv' \
DELIMITER ',' \
CSV HEADER;

---

## 6. Check Replication Role

SELECT pg_is_in_recovery();

-- false = primary
-- true  = replica

---

## 7. Check Replication Status (Primary)

SELECT * FROM pg_stat_replication;

---

## 8. Create Database User

CREATE USER app_user WITH PASSWORD 'secure_password';

GRANT CONNECT ON DATABASE app_db TO app_user;

GRANT USAGE ON SCHEMA public TO app_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

---

## 9. Backup (Logical Dump)

pg_dump \
  --host=<cluster-fqdn> \
  --port=6432 \
  --username=<user> \
  --format=custom \
  --file=backup.dump \
  <database-name>

---

## 10. Restore

pg_restore \
  --host=<cluster-fqdn> \
  --port=6432 \
  --username=<user> \
  --dbname=<database-name> \
  backup.dump

---

## 11. Show Active Connections

SELECT * FROM pg_stat_activity;

---

## 12. Check Database Size

SELECT pg_size_pretty(pg_database_size('<database-name>'));
