# Website Monitoring with Serverless and PostgreSQL

This example demonstrates how serverless functions can be used
for automated monitoring tasks with results stored in a database.

The function periodically checks the availability of a website
and records response metrics in PostgreSQL.

## Architecture

Components involved:

Serverless Function  
Performs HTTP request and measures response time.

Managed PostgreSQL Database  
Stores monitoring results.

Timer Trigger  
Executes the function periodically.

## PostgreSQL Cluster

A managed PostgreSQL cluster is deployed with:

- PostgreSQL version 15
- minimal resource preset
- serverless access enabled

The database contains a simple table used to store monitoring data.

Example schema:
```
measurements(
result INTEGER,
time FLOAT
)
```

## Database Connection

The function connects to PostgreSQL using a managed connection
provided by the serverless platform.

Authentication is performed using a temporary access token
provided by the function execution context.

This approach avoids storing database passwords inside
the function code.

## Monitoring Logic

The function performs an HTTP request to a target website
and measures the response time.

Possible outcomes include:

- HTTP response code
- connection timeout
- read timeout

The result and response time are inserted into the database.

## Timer Trigger

A timer trigger runs the function periodically using
a cron expression.

This allows continuous monitoring without manual execution.
