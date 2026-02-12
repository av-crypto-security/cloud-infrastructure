# Node Groups and Compute Layer

Node groups provide the compute capacity
on which Kubernetes workloads run.
This document focuses strictly on
worker node architecture and lifecycle.

---

## 1. Node groups as workload execution layer

All application pods run on worker nodes.
A node group represents a homogeneous pool of virtual machines:
- identical instance type,
- identical Kubernetes version,
- identical networking configuration.

Without node groups, a cluster cannot schedule workloads.

---

## 2. Version alignment

Each node group runs a specific Kubernetes version.
Although Kubernetes allows version skew
between control plane and nodes,
mismatched versions increase operational risk.
Keeping node versions aligned
with the control plane version:
- reduces compatibility issues,
- simplifies troubleshooting,
- improves stability.

---

## 3. Autoscaling behavior

Node groups support automatic scaling.

Scaling is controlled by:
- minimum node count,
- maximum node count.

When scheduling requires more capacity,
new nodes are provisioned.
When load decreases, unused nodes are removed.
Autoscaling effectiveness depends on:
- properly defined resource requests,
- predictable workload behavior.

Improper resource definitions
may prevent scaling from triggering correctly.

---

## 4. Availability considerations

In zonal clusters,
node groups operate within a single availability zone.
This creates:
- lower cost,
- reduced fault tolerance.

Zone-level failures will affect
all workloads in the cluster.
Higher availability requires
multi-zone node distribution.

---

## 5. Public IP exposure

Nodes may receive public IP addresses.
Public IPs allow:
- direct SSH access,
- direct internet egress.

However, public exposure increases:
- attack surface,
- scanning risk,
- misconfiguration impact.

For secure environments,
nodes should operate without public IPs,
using private networking and controlled egress.

---

## 6. SSH access risk model

SSH access is useful for:
- debugging,
- incident response,
- lab environments.

However, SSH:
- bypasses Kubernetes abstraction,
- complicates auditing,
- increases compromise impact.

Best practice:
- avoid routine SSH access,
- restrict it to controlled scenarios,
- prefer Kubernetes-native inspection tools.

---

## Summary

Node groups define:
- workload execution capacity,
- scaling behavior,
- infrastructure exposure level.

Their configuration directly affects
security posture,
cost efficiency,
and operational stability.
