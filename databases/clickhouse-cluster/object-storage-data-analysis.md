# Analytical Queries on External Data

ClickHouse can query data directly from object storage without importing it
into a local database.

This capability allows engineers to run analytical queries against datasets
stored in cloud storage systems.

Typical file formats include:

- CSV
- TSV
- Parquet
- JSON

In this example we analyze infrastructure metrics stored as a TSV dataset.

## Dataset Description

The dataset represents telemetry collected from several backend services.

Each record contains:

timestamp  
service name  
deployment region  
CPU utilization  
memory utilization  
request latency  
error rate

This type of dataset is common in observability pipelines.

## Example Analytical Questions

Typical operational questions that can be answered with analytical queries:

Which service has the highest request latency?

Which region shows the highest CPU utilization?

Which service has the highest error rate?

How do latency and CPU usage evolve over time?

## Querying External Data

ClickHouse can read external files using table functions such as:

s3()  
file()  
url()

The schema must be defined explicitly when querying structured text files.

Example schema used for the dataset:

timestamp DateTime  
service String  
region String  
cpu_usage Float32  
memory_usage Float32  
request_latency_ms UInt32  
error_rate Float32

This allows the dataset to be analyzed without creating a table or importing
the data first.

## Benefits of External Queries

This approach is commonly used in data engineering workflows because it allows:

- quick exploration of new datasets
- analysis without ETL pipelines
- temporary analytics workloads
- fast prototyping of queries

For production workloads, datasets are typically ingested into MergeTree
tables for better performance and indexing.
