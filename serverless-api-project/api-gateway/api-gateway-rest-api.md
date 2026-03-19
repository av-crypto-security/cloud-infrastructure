# REST API using API Gateway and Serverless Functions

This document describes how to expose a serverless function
through an HTTP REST API using API Gateway.

The API retrieves monitoring results from PostgreSQL
and returns them to clients.

## API Gateway

API Gateway acts as an HTTP frontend for serverless functions.

The gateway configuration is defined using an OpenAPI specification.

Example endpoint:

/results

The endpoint forwards incoming HTTP requests directly
to the serverless function.

## Request Authorization

The API uses a simple query parameter called `secret`
to restrict access.

Requests without the correct parameter return an
HTTP 401 response.

This mechanism is intended only for demonstration
purposes. In production systems authentication would
typically use:

- IAM
- JWT tokens
- OAuth

## Database Query

The function retrieves up to 50 monitoring records
from the PostgreSQL database.

The query executed by the function:
```sql
SELECT * FROM measurements LIMIT 50
```
Results are returned in JSON format.

## API Workflow

1. client sends HTTP request to API Gateway
2. gateway invokes the serverless function
3. function queries PostgreSQL
4. results are returned to the client
