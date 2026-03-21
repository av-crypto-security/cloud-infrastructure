# REST API for Monitoring Data (API Gateway + Serverless)

This module exposes monitoring data through an HTTP API
using API Gateway and a serverless function.

## Overview

The API provides access to monitoring results stored in PostgreSQL.

Components:

- API Gateway (`api-gateway`)  
  HTTP entry point for external clients

- API Function (`api-function`)  
  Handles requests and queries the database

- PostgreSQL (`monitoring-db`)  
  Stores monitoring results

## Architecture

1. Client sends HTTP request
2. API Gateway forwards request to function
3. Function queries PostgreSQL
4. Response is returned as JSON

## Endpoint

GET /results
Returns up to 50 latest monitoring records.

## Query Parameters

- `token` — simple access control parameter

## Security

A simple token-based check is used:

- request must include `?token=<API_TOKEN>`
- otherwise returns HTTP 401

This mechanism is used for demonstration purposes only.

In production systems, proper authentication should be used:

- IAM
- OAuth2
- JWT

## Database Query

The function executes:

```sql
SELECT result, response_time
FROM measurements
ORDER BY time DESC
LIMIT 50;
```

## Response Format

```json
{
  "results": [
    {
      "status": 200,
      "response_time": 0.123
    }
  ]
}
```

## Notes

- Stateless API
- No credentials stored in code
- API Gateway decouples HTTP layer from compute
