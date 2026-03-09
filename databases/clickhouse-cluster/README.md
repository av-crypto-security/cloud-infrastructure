# ClickHouse Analytics Playground

A small engineering project demonstrating analytical workflows using ClickHouse.

The repository shows how infrastructure metrics can be:

- analyzed directly from external storage
- ingested into analytical tables
- queried using ClickHouse SQL

## Architecture Overview

The project demonstrates a typical analytical workflow used in data platforms.

Telemetry dataset
        │
        ▼
External file (TSV)
        │
        ▼
ClickHouse query (table function)
        │
        ▼
Analytical queries

For production systems the workflow typically evolves into:

Telemetry pipeline
        │
        ▼
Object Storage
        │
        ▼
ClickHouse ingestion
        │
        ▼
MergeTree tables
        │
        ▼
Analytical queries

## Repository Structure

cluster-architecture-and-connection.md  
Description of ClickHouse cluster architecture and connection methods.

object-storage-data-analysis.md  
Querying external datasets without ingestion.

clickhouse-data-ingestion.md  
Batch ingestion of telemetry data into ClickHouse.

commands.md  
CLI commands used during the workflow.

example-metrics.tsv  
Example infrastructure telemetry dataset.

## Example Analytical Queries

Which service has the highest request latency?

Which region shows the highest CPU usage?

Which service produces the most errors?

These questions are common in observability and SRE analytics.

## Technologies

- ClickHouse
- SQL
- TSV datasets
- CLI workflows
