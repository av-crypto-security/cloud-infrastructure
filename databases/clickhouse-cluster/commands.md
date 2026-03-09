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

## Install ClickHouse Client

Add the official ClickHouse repository and install the client.

```bash
sudo apt update && sudo apt install --yes apt-transport-https ca-certificates dirmngr && \

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754 && \

echo "deb https://packages.clickhouse.com/deb stable main" | \
sudo tee /etc/apt/sources.list.d/clickhouse.list

sudo apt update && sudo apt install --yes clickhouse-client
```

## Download client configuration
```bash
mkdir --parents ~/.clickhouse-client

wget "https://storage.yandexcloud.net/doc-files/clickhouse-client.conf.example" \
--output-document ~/.clickhouse-client/config.xml
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

Service with maximum latency spike
```SQL
SELECT
service,
max(request_latency_ms)
FROM metrics
GROUP BY service
ORDER BY max(request_latency_ms) DESC
LIMIT 1;
```

Average CPU usage by region
```SQL
SELECT
region,
avg(cpu_usage) AS avg_cpu
FROM metrics
GROUP BY region
ORDER BY avg_cpu DESC;
```

Request latency over time
```SQL
SELECT
toStartOfFiveMinute(timestamp) AS time_bucket,
avg(request_latency_ms) AS avg_latency
FROM metrics
GROUP BY time_bucket
ORDER BY time_bucket;
```

Top CPU usage spikes
```SQL
SELECT
timestamp,
service,
cpu_usage
FROM metrics
ORDER BY cpu_usage DESC
LIMIT 5;
```

CPU vs latency correlation by service
```SQL
SELECT
service,
avg(cpu_usage) AS avg_cpu,
avg(request_latency_ms) AS avg_latency
FROM metrics
GROUP BY service
ORDER BY avg_latency DESC;
```

## Querying external data from S3

ClickHouse can query external datasets directly from object storage without loading them into tables.

Services with highest latency spike (S3)
```SQL
SELECT
    timestamp,
    service,
    region,
    request_latency_ms
FROM s3(
    'https://storage.yandexcloud.net/<your-bucket>/example-metrics.tsv',
    'TSVWithNames',
    'timestamp DateTime, service String, region String, cpu_usage Float32, memory_usage Float32, request_latency_ms UInt32, error_rate Float32'
)
ORDER BY request_latency_ms DESC
LIMIT 10;
```

Average CPU usage by region (S3)
```SQL
SELECT
    region,
    avg(cpu_usage) AS avg_cpu
FROM s3(
    'https://storage.yandexcloud.net/<your-bucket>/example-metrics.tsv',
    'TSVWithNames',
    'timestamp DateTime, service String, region String, cpu_usage Float32, memory_usage Float32, request_latency_ms UInt32, error_rate Float32'
)
GROUP BY region
ORDER BY avg_cpu DESC;
```

Request latency trend over time (S3)
```SQL
SELECT
    toStartOfFiveMinute(timestamp) AS time_bucket,
    avg(request_latency_ms) AS avg_latency
FROM s3(
    'https://storage.yandexcloud.net/<your-bucket>/example-metrics.tsv',
    'TSVWithNames',
    'timestamp DateTime, service String, region String, cpu_usage Float32, memory_usage Float32, request_latency_ms UInt32, error_rate Float32'
)
GROUP BY time_bucket
ORDER BY time_bucket;
```
