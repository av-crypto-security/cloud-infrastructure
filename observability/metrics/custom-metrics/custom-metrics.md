# Custom Metrics via API

## Why Custom Metrics?

Managed metrics are often insufficient.

Real systems require:
- Business metrics
- Application-level signals
- Domain-specific indicators

This example demonstrates manual metric ingestion via REST API.

---

## Architecture

Application → JSON payload → REST API → Monitoring Storage → Dashboard

---

## Authentication

We use IAM token for API authentication.

Generate token:

```bash
yc iam create-token
```

Export:
```bash
export IAM_TOKEN=<your_token>
```

IAM tokens expire after 12 hours.
