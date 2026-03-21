# Serverless API Project (Yandex Cloud)

This repository demonstrates a production-style serverless architecture built on Yandex Cloud.
The project implements a complete event-driven pipeline, monitoring system, and HTTP API layer using Cloud Functions, Object Storage, Managed PostgreSQL, and API Gateway.

---

## Architecture Overview

The system is composed of four independent but connected modules:

### 1. Cloud Function (Base Module)

A simple serverless function deployed via CLI.

* demonstrates function lifecycle
* uses service account for execution
* supports HTTP invocation

---

### 2. Object Storage Trigger Pipeline

An event-driven pipeline using Object Storage.

Components:

* **Upload Function (`cloud-function`)** — generates and uploads files
* **Object Storage** — stores objects and emits events
* **Trigger Function (`trigger-function`)** — processes events

Flow:

```
Function → Object Storage → Event → Trigger → Function
```

This module demonstrates asynchronous architecture and decoupled services.

---

### 3. Monitoring System (Serverless + PostgreSQL)

A scheduled monitoring pipeline that measures website availability.

Components:

* **Monitoring Function (`monitoring-function`)**
* **PostgreSQL (`monitoring-db`)**
* **Timer Trigger (`monitoring-trigger`)**

Flow:

```
Trigger → Function → HTTP Request → DB Write
```

Key features:

* response time measurement
* fault handling (timeouts, errors)
* secure DB access via IAM token (no static credentials)

---

### 4. REST API (API Gateway + Serverless)

An HTTP API layer exposing monitoring data.

Components:

* **API Gateway (`api-gateway`)**
* **API Function (`api-function`)**
* **PostgreSQL (`monitoring-db`)**

Flow:

```
Client → API Gateway → Function → DB → Response
```

Endpoint:

```
GET /results?token=<API_TOKEN>
```

Returns up to 50 latest monitoring records in JSON format.

---

## Key Concepts Demonstrated

* Serverless function deployment via CLI
* Versioning and configuration of functions
* Event-driven architecture (Object Storage triggers)
* Scheduled execution using cron triggers
* Secure access to Managed PostgreSQL
* IAM-based authentication (no hardcoded secrets)
* API Gateway integration with serverless backend
* Stateless microservice design

---

## Security Considerations

* No credentials stored in source code
* Database access uses temporary IAM tokens:

  ```
  context.token["access_token"]
  ```
* API access protected via token (demo-level security)

> Note: In production systems, token-based query parameters should be replaced with IAM / OAuth / JWT.

---

## Project Structure

```
serverless-api-project/
│
├── create-cloud-function/
│
├── storage-trigger/
│
├── monitoring-function/
│
├── api-gateway/
│
└── README.md
```

---

## Use Cases

This architecture pattern can be applied to:

* monitoring and observability systems
* log processing pipelines
* event-driven data processing
* lightweight backend APIs
* microservice-based systems

---

## Notes

* All components are stateless and independently deployable
* Infrastructure is CLI-driven (Infrastructure-as-Code approach)
* Designed as a portfolio-ready engineering project

---

## **Next Steps**

Planned extensions:

* asynchronous processing patterns
* cost estimation and optimization
* advanced authentication (JWT / IAM)
* metrics and alerting integration
