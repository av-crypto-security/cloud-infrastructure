# High Availability Architecture — VM, Zone and Application Failure Handling

This repository demonstrates a multi-zone high availability architecture built in Yandex Cloud using Instance Groups and Network Load Balancer.

The infrastructure is designed to tolerate:

- Virtual machine failures
- Availability zone outages
- Application-level crashes

The system automatically restores desired capacity and maintains traffic availability without manual intervention.

---

## Architecture Overview

The environment consists of:

- Managed Instance Group (3 instances)
- Multi-zone placement:
  - ru-central1-a
  - ru-central1-b
  - ru-central1-d
- Network Load Balancer (L4)
- HTTP health checks
- NGINX deployed via cloud-init
- Fixed scaling policy (3 instances)

Each instance exposes its hostname to visualize traffic distribution.

---

## Architectural Principles Applied

- Declarative desired state
- Self-healing infrastructure
- Multi-zone redundancy
- Health-based traffic routing
- Controlled rolling behavior
- No single point of failure

---

## Failure Scenarios Validated

1. VM-level failure (instance deletion)
2. Zone-level capacity redistribution
3. Application-level health degradation

Each scenario validates automatic reconciliation and resilience mechanisms.
