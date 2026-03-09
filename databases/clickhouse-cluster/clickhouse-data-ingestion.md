# Data Ingestion into ClickHouse

While ClickHouse can query external datasets directly, production systems
typically ingest data into internal tables for performance and indexing.

This document demonstrates how to load structured telemetry data into a
ClickHouse table.

## Example Use Case

Infrastructure metrics are collected periodically from multiple backend
services.

Metrics may include:

- CPU utilization
- memory utilization
- request latency
- error rate

These metrics are written to files by monitoring systems and later ingested
into analytical storage for long-term analysis.

## Creating a Table

Before inserting data, a table must be created.

ClickHouse commonly uses the MergeTree engine for analytical workloads.

MergeTree provides:

- high ingestion throughput
- columnar compression
- partitioning and indexing
- efficient analytical queries

The table schema matches the structure of the telemetry dataset.

Fields include:

timestamp  
service  
region  
cpu_usage  
memory_usage  
request_latency_ms  
error_rate

The primary ordering key is usually the timestamp.

## Loading Data

Data can be inserted using the clickhouse-client command-line tool.

The ingestion pipeline reads the TSV file and pipes it into ClickHouse.

This approach is commonly used in batch ingestion workflows.

## Alternative Ingestion Methods

ClickHouse supports several ingestion approaches:

- CLI ingestion
- HTTP API
- streaming pipelines
- application-level ingestion

In real production systems ingestion often happens through:

- log pipelines
- monitoring systems
- message queues
- streaming platforms

Once data is stored in MergeTree tables it can be queried efficiently for
analytics, monitoring, and reporting.
