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

## Metric Schema

File: my-metrics.json
Metric type: IGAUGE
IGAUGE = instantaneous gauge value.

Example:
```json
{
  "metrics": [
    {
      "name": "number_of_users",
      "labels": {
        "site": "yoursite"
      },
      "type": "IGAUGE",
      "timeseries": [
        {
          "ts": "2026-02-17T10:00:00Z",
          "value": "22"
        }
      ]
    }
  ]
}
```

## Key Concepts

- name — metric identifier
- labels — dimensional metadata
- type — metric type
- ts — timestamp (RFC3339)
- value — numeric value
- service=custom — required namespace

## Sending Metric

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${IAM_TOKEN}" \
  -d '@my-metrics.json' \
  'https://monitoring.api.cloud.yandex.net/monitoring/v2/data/write?folderId=<FOLDER_ID>&service=custom'
```

Successful response:
```json
{"writtenMetricsCount":1}
```

## Failure Case

Possible error:
```
UNKNOWN_SHARD: Metrics storage is not initialized yet
```

This indicates storage warm-up delay.

## Observability Insight

Custom metrics allow:
- Business monitoring
- SLO calculations
- Alerting on domain metrics
- Engineering-grade telemetry
  
