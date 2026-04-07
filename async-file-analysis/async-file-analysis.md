# Async File Analysis Module

This module implements the core asynchronous processing pipeline
used in the project.

It focuses on decoupling request handling from heavy file analysis
using a queue-based event-driven architecture.

---

## Purpose

The module simulates a backend component of a security system,
such as a malware scanning or file inspection service.

It is designed to demonstrate how to:

- process files asynchronously
- scale workloads horizontally
- isolate compute-heavy operations

---

## Architecture Role

This module is responsible for:

- task creation (API layer)
- task delivery (message queue)
- task execution (worker)
- result persistence (database)

---

## Processing Flow

1. API function receives a request to analyze a file
2. A unique task_id is generated
3. Task metadata is stored in YDB
4. A message is sent to YMQ containing:
   - task_id
   - object_name (file in Object Storage)
5. Worker function is triggered by the queue
6. Worker:
   - retrieves file from Object Storage
   - performs analysis
   - stores result in YDB

---

## File Handling Model

Unlike synchronous systems, this pipeline does NOT:

- accept direct file uploads in API
- download files from external URLs

Instead:

- files are pre-stored in Object Storage
- workers operate only on internal storage objects

This approach improves:

- security (no external fetch)
- reliability
- reproducibility

---

## Task Model

Each task contains:

- task_id (UUID)
- ready (boolean)
- result (JSON string)

---

## Analysis Model (Mock)

The system simulates analysis by:

- computing SHA-256 hash
- deriving a pseudo verdict (clean / malicious)
- returning file metadata

This allows testing:

- queue behavior
- async execution
- storage integration

without external dependencies.

---

## Design Principles

### 1. Asynchronous Processing
All heavy operations are executed outside the API layer.

### 2. Stateless Workers
Workers do not store local state and rely on external systems.

### 3. Loose Coupling
Queue separates API and processing logic.

### 4. Fault Isolation
Failures in worker do not affect API availability.

---

## Why This Matters

This module represents a common backend pattern used in:

- antivirus systems
- document processing pipelines
- data ingestion systems
- cloud security services

---

## Relation to Main README

See `README.md` for:

- full system architecture
- API contract
- deployment details

This document focuses only on the internal processing logic.
