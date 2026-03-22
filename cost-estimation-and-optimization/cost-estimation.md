# Cloud Cost Estimation

This module demonstrates a structured approach to estimating cloud infrastructure cost.

The goal is not to reproduce calculator output, but to model cost behavior
under different load scenarios and understand key cost drivers.

---

## Overview

Any production system must be evaluated in terms of cost before deployment.

This module models a simple architecture:

* Virtual Machine (Compute)
* Managed Database
* Monitoring

We focus on **cost behavior**, not exact pricing.

---

## Architecture Model

### Compute Layer

* General-purpose VM
* Variable CPU/RAM configurations
* Always-on workload (24/7)

### Database Layer

* Managed PostgreSQL (2 nodes)
* Fixed baseline cost (cluster-based pricing)

### Monitoring

* Pay-per-ingestion model
* Cost depends on metric volume

---

## Monitoring Cost Model

### Formula

Total values:

```
metrics × values_per_minute × minutes_per_month
```

Where:

```
minutes_per_month = 60 × 24 × 30
```

Cost:

```
(total_values / 1_000_000) × price_per_million
```

---

## Scenario Analysis

### Scenario A — Low Load

* 10 metrics
* 1 value/min

### Scenario B — Baseline

* 35 metrics
* 2 values/min

### Scenario C — High Load

* 100 metrics
* 5 values/min

---

## Sensitivity Analysis

Monitoring cost grows linearly with:

* number of metrics
* sampling frequency

Implications:

* doubling metrics → doubles cost
* doubling frequency → doubles cost

This makes monitoring cost predictable and easy to control.

---

## Compute Cost Behavior

Compute cost is different:

* depends on resource allocation (CPU, RAM)
* charged per hour
* not directly tied to actual utilization

Key property:

> Overprovisioned resources generate constant cost even when idle

---

## Database Cost Behavior

Managed databases:

* have baseline cost (cluster nodes)
* scale in discrete steps
* not linear like monitoring

---

## Key Observations

* Monitoring → linear and predictable
* Compute → continuous but usage-insensitive
* Database → step-based pricing

---

## Engineering Takeaways

* Always model multiple load scenarios
* Avoid single-point estimates
* Identify dominant cost drivers early
* Monitoring is rarely the main cost factor
* Compute and DB require the most optimization effort

---

## Notes

* This model is intentionally simplified
* Real pricing depends on region and provider
* Always validate using official pricing tools
