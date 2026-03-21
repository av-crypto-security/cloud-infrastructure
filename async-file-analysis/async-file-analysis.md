# Async File Analysis Pipeline (Serverless + Queue + Object Storage)

This module implements an asynchronous file processing pipeline
based on message queues and serverless functions.

The system demonstrates how to decouple heavy processing workloads
from user-facing APIs using an event-driven architecture.

## Overview

The pipeline simulates a security-oriented file analysis workflow.

Instead of processing files synchronously, tasks are pushed
to a queue and processed asynchronously.

Components:

- API Function (`analysis-api`)  
  Accepts file URLs and creates analysis tasks

- Message Queue (`analysis-queue`)  
  Buffers tasks and ensures reliable delivery

- Worker Function (`analysis-worker`)  
  Processes files asynchronously

- Object Storage (`analysis-storage`)  
  Stores uploaded files and generated results

- YDB (`analysis-db`)  
  Stores task state and results

- Lockbox  
  Stores access credentials securely

## Architecture

1. Client sends request with file URL
2. API function creates a task in DB
3. Task is pushed to message queue
4. Worker function is triggered
5. File is downloaded and analyzed
6. Result is stored in DB and Object Storage
7. Client polls task status

## Why Queue-Based Design

This architecture solves key problems:

- avoids long-lived HTTP connections
- isolates heavy processing from API layer
- improves fault tolerance
- enables horizontal scaling

## Security Context

The pipeline simulates:

- file validation
- content inspection
- controlled file processing

Secrets are never hardcoded and are retrieved
via Lockbox at runtime.

## Task Model

Each task contains:

- task_id (UUID)
- status (pending / done)
- result (analysis output)

## Example Flow

Create task:

```json
{
  "action": "analyze",
  "file_url": "https://example.com/file.txt"
}
```

Check status:

```json
{
  "action": "status",
  "task_id": "uuid"
}
```

## Notes

- Fully asynchronous architecture
- Stateless compute layer
- Queue ensures reliable processing
- Suitable for security pipelines and batch workloads
