# Website Monitoring Pipeline (Serverless + PostgreSQL)

This module implements a serverless monitoring system that measures
website availability and stores results in a PostgreSQL database.

## Overview

The system consists of:

- Monitoring Function (`monitoring-function`)  
  Sends HTTP requests and measures response time.

- Managed PostgreSQL (`monitoring-db`)  
  Stores monitoring results.

- Timer Trigger (`monitoring-trigger`)  
  Executes the function periodically.

## Architecture

The system follows a scheduled execution model:

1. Timer trigger invokes the function
2. Function sends HTTP request to target
3. Response time is measured
4. Result is written to PostgreSQL

## Database

A managed PostgreSQL cluster is used with serverless access enabled.

Example schema:

```sql
CREATE TABLE measurements (
    result INTEGER,
    response_time FLOAT
);
```
## Secure Database Access

Authentication is performed using a temporary IAM token:
```
password=context.token["access_token"]
```
This eliminates the need to store static credentials.

## Monitoring Logic

The function performs an HTTP request with timeouts:
- connection timeout
- read timeout

Failure cases are mapped to custom status codes.

## Scheduling

The function is triggered using a cron expression:
```bash
* * * * ? *
```
This results in execution once per minute.

## Notes
Stateless execution
No hardcoded credentials
Suitable for uptime monitoring and SLA tracking
