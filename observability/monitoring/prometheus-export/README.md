# Prometheus Metrics Export (Yandex Monitoring → Prometheus → Grafana)

## Overview

This section demonstrates integration of Yandex Cloud Monitoring 
with a self-hosted Prometheus instance.

Prometheus follows the pull model and scrapes metrics from 
the Yandex Monitoring Prometheus-compatible endpoint.

Architecture:
```
Yandex Monitoring (managed) 
        ↓  (Prometheus scrape over HTTPS)
Prometheus 
        ↓
Grafana
```

---

## Why

Managed monitoring is useful.
But Prometheus integration provides:
- Standard PromQL
- Portable monitoring stack
- Vendor-neutral observability
- Advanced alerting capabilities

---

## Prerequisites

- Service Account
- Role: monitoring.viewer
- API key

---

## Security & Secrets Handling

For security reasons, API keys are not hardcoded in `prometheus.yml`.
Prometheus uses:
```
bearer_token_file: /etc/prometheus/secrets/yc_api_key
```
Create a file locally:
```bash
echo "<your_api_key>" > yc_api_key
```
Run container with mounted secret:
```bash
docker run \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/yc_api_key:/etc/prometheus/secrets/yc_api_key \
  prom/prometheus
```
This approach:
- Avoids credential leakage
- Aligns with container security best practices
- Can be easily replaced with Docker/Kubernetes Secrets

---

## Prometheus Configuration

See `prometheus.yml` in this directory.
Replace:
- <folder_id>

---

## Run Prometheus (Docker)

Pull official image:
```bash
docker pull prom/prometheus
```
Create Dockerfile:
```Dockerfile
FROM prom/prometheus
ADD prometheus.yml /etc/prometheus/
```
Build image:
```bash
docker build -t my-prometheus
```
Run container:
```bash
docker run -p 9090:9090 my-prometheus
```

---

## Verify Targets

Open:
```
http://<vm_ip>:9090/targets
```
Expected status:
- prometheus → UP
- yc-monitoring-export → UP

---

## Query Metrics

Open Graph tab.
Example metric:
```
traffic
```
Execute and verify data flow.

## Grafana Integration

1. Add data source → Prometheus
2. URL:
```
http://<vm_ip>:9090
```
3. Save & Test
4. Create dashboard
5. Select metric `traffic`

---

## Result

- Cloud metrics exported to Prometheus
- Visualized in Grafana
- Ready for alerting via PromQL

---

## Production Considerations
- Use TLS between Prometheus and external endpoints
- Restrict inbound access to port 9090
- Use dedicated service account with minimal privileges
- Rotate API keys

---

This setup demonstrates integration of managed cloud monitoring 
with a self-hosted Prometheus stack, enabling portable and 
vendor-neutral observability architecture.
