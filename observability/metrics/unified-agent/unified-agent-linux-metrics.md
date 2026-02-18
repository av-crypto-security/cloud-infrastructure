# Unified Agent — Linux Metrics Collection

## Why Agent-Based Collection?

Cloud-level metrics are insufficient for:

- Per-process monitoring
- Memory breakdown
- Detailed CPU metrics
- Host-level diagnostics

Unified Agent provides:

- Local metric collection
- Storage buffering
- Routing pipeline
- Namespaced export

---

## Architecture
```
Linux Host
   ↓
Unified Agent
   ↓
Storage (fs)
   ↓
Route
   ↓
YC Monitoring
```
---

## Config Overview

File: `unified-agent-config.yml`

Key sections:

### status
Agent health endpoint.

### storages
Local buffering layer.

### channels
Output routing definition.

### routes
Input plugin → Channel mapping.

---

## Example Config (Core Sections)

```yaml
status:
  port: "16241"

storages:
  - name: main
    plugin: fs
    config:
      directory: /var/lib/yandex/unified_agent/main

channels:
  - name: cloud_monitoring
    channel:
      pipe:
        - storage_ref:
            name: main
      output:
        plugin: yc_metrics
        config:
          folder_id: "<FOLDER_ID>"
          iam:
            cloud_meta: {}

routes:
  - input:
      plugin: linux_metrics
      config:
        namespace: sys
    channel:
      channel_ref:
        name: cloud_monitoring
```

## Important Concept

Namespace sys.* prefixes Linux metrics.
Example metric:
```
sys.memory.MemAvailable
```

Start Agent
```bash
sudo ./unified_agent --config unified-agent-config.yml
```

Expected output:
```
NOTICE agent started
```

## Engineering Insight

Unified Agent implements:
- Edge collection
- Buffered transport
- Pluggable routing
- Metric namespacing
This mirrors production-grade telemetry systems.
