# Prometheus Metrics Export (Yandex Monitoring → Prometheus → Grafana)

This section demonstrates how cloud metrics are exported to Prometheus and visualized in Grafana.
Architecture:
Yandex Monitoring → Prometheus → Grafana

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

## Prometheus Configuration

See `prometheus.yml` in this directory.
Replace:
- <folder_id>
- <api_key>

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
docker build -t my-prometheus .
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

This demonstrates production-grade observability architecture.
