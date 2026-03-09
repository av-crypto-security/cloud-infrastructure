# Commands

This file contains CLI commands used during the ClickHouse workflow.

## Install certificates
```bash
sudo mkdir --parents /usr/local/share/ca-certificates/cloud && \
sudo wget https://storage.yandexcloud.net/cloud-certs/RootCA.pem \
--output-document /usr/local/share/ca-certificates/cloud/RootCA.crt && \
sudo chmod 655 /usr/local/share/ca-certificates/cloud/RootCA.crt && \
sudo update-ca-certificates
```

## Install ClickHouse client
```bash
sudo apt update
sudo apt install clickhouse-client
```

## Connect to cluster
```bash
clickhouse-client \
--host <host-address> \
--secure \
--user <username> \
--database <database> \
--port 9440 \
--ask-password
```

## Check connection
```SQL
SELECT version();
```

## Create table
```SQL
CREATE TABLE metrics
(
timestamp DateTime,
service String,
region String,
cpu_usage Float32,
memory_usage Float32,
request_latency_ms UInt32,
error_rate Float32
)
ENGINE = MergeTree
ORDER BY timestamp;
```

## Insert data from TSV
```bash
cat example-metrics.tsv | clickhouse-client \
--host <host-address> \
--secure \
--user <username> \
--database <database> \
--port 9440 \
-q "INSERT INTO metrics FORMAT TabSeparated" \
--ask-password
```

## Example analytical queries

Highest latency service
```SQL
SELECT
service,
max(request_latency_ms)
FROM metrics
GROUP BY service
ORDER BY max(request_latency_ms) DESC;
```

Highest error rate
```SQL
SELECT
service,
avg(error_rate)
FROM metrics
GROUP BY service
ORDER BY avg(error_rate) DESC;
```
