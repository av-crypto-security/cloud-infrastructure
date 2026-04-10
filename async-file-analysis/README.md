# Async File Analysis Pipeline (Serverless, Yandex Cloud)

## Overview

This project demonstrates a production-style asynchronous processing pipeline for file analysis using serverless components. The system simulates a malware scanning backend where uploaded files are processed asynchronously and results are stored for later retrieval.

The architecture follows real-world backend and cloud security patterns: decoupled services, event-driven processing, and stateless workers.

---

## Architecture

```
Client → API (Cloud Function)
        → YMQ (Message Queue)
        → Worker (Cloud Function)
        → Object Storage (S3)
        → YDB (Task State + Results)
```

### Flow Description

1. Client sends a request to create an analysis task
2. API function:

   * creates a task ID
   * stores metadata in YDB
   * sends a message to YMQ
   * 
Files are expected to be pre-uploaded to Object Storage.
Current API does not handle file uploads.  

3. Worker function:

   * receives message from queue
   * downloads file from Object Storage
   * performs analysis (mocked)
   * writes result back to YDB
4. Client polls task status via API

---

## Components

### 1. API Function

Handles:

* Task creation
* Status retrieval

Key responsibilities:

* Stateless request handling
* Queue publishing
* Database interaction

---

### 2. Worker Function

Handles:

* Message consumption from YMQ
* File retrieval from Object Storage
* File analysis
* Result persistence

Design principles:

* Idempotent processing
* Stateless execution
* Async workload handling

---

### 3. Object Storage

Used for:

* Storing binary files for analysis

---

### 4. Yandex Message Queue (YMQ)

Provides:

* Decoupling between API and processing layer
* Load buffering
* Retry capability

---

### 5. YDB (Document API)

Stores:

* Task metadata
* Processing status
* Analysis results

---

### 6. Lockbox

Used for:

* Secure storage of service account credentials

---

## Data Model

### Task Item (YDB)

```
{
  "task_id": "uuid",
  "ready": false,
  "result": "json string"
}
```

---

## API Contract

### Create Task

Request:

```
{"action": "analyze"}
```

Response:

```
{"task_id": "uuid"}
```

---

### Get Task Status

Request:

```
{"action": "get_task_status", "task_id": "uuid"}
```

Response (processing):

```
{"ready": false}
```

Response (completed):

```
{
  "ready": true,
  "result": "{...}"
}
```

---

## Analysis Logic (Mock)

The system simulates file scanning by:

* Calculating SHA-256 hash
* Assigning a pseudo verdict based on hash
* Returning metadata:

  * hash
  * size
  * verdict (clean/malicious)

This approach allows testing of pipeline behavior without external dependencies.

---

## Security Considerations

* Principle of least privilege (IAM roles minimized)
* Secrets stored in Lockbox
* No hardcoded credentials
* Isolated components via queue

---

## Engineering Highlights

* Event-driven architecture
* Serverless-first design
* Horizontal scalability (queue-based)
* Clear separation of concerns
* Cloud-native storage and messaging

---

## Possible Improvements

* Add task states: pending / processing / done / failed
* Implement retry + Dead Letter Queue (DLQ)
* Add presigned URL upload support
* Introduce real file scanning engine
* Add monitoring and alerting

---

## Use Cases

* Malware scanning pipeline
* File validation services
* Async document processing
* Security analysis backends

---

## Tech Stack

* Python 3
* Yandex Cloud Functions
* Yandex Object Storage (S3-compatible)
* Yandex Message Queue (SQS-compatible)
* YDB (Document API)
* Lockbox

---

## Author Notes

This project is designed as a portfolio-ready implementation of a real backend pattern used in cloud security and distributed systems.

Focus is placed on architecture, reliability, and correctness rather than UI or external integrations.

