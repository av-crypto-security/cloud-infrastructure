# Kubernetes Cluster Design (Managed Kubernetes)

This document explains the architectural decisions behind creating
a Managed Kubernetes cluster in Yandex Cloud.
The focus is on structural design choices that affect
security, availability, and lifecycle management.

---

## 1. Environment isolation

A Kubernetes cluster is created inside a specific cloud folder.
The folder defines:
- IAM boundaries,
- resource quotas,
- billing scope,
- visibility and administrative access.
  
Placing clusters in dedicated folders is a governance practice
that enables separation between environments
(dev / staging / production).
Isolation at the folder level reduces the blast radius
of configuration mistakes and privilege escalation.

---

## 2. Service accounts and separation of responsibilities

Managed Kubernetes interacts with cloud infrastructure
using service accounts.
Two logical identities are involved:

### Control plane service account
Used by the managed control plane to:
- provision load balancers,
- allocate IP addresses,
- manage disks and other cloud resources.

### Node service account
Used by worker nodes to:
- pull container images,
- access cloud services when required.

Using a single account for both roles is possible
but weakens least-privilege design.
Production clusters should separate these identities
to reduce privilege escalation risk.

---

## 3. Control plane architecture

The control plane:
- schedules workloads,
- maintains cluster state,
- runs core Kubernetes components.

### Zonal vs Regional

Zonal master:
- runs in a single availability zone,
- lower cost,
- single point of failure at zone level.
Regional master:
- distributed across multiple zones,
- higher availability,
- recommended for production.
For learning and non-critical workloads,
a zonal cluster is sufficient.

---

## 4. Kubernetes version and release channel

Release channels determine:
- available Kubernetes versions,
- upgrade behavior,
- lifecycle stability.
Typical characteristics:
- RAPID — frequent automatic updates
- REGULAR — balanced stability and update cadence
- STABLE — conservative update policy
The release channel cannot be changed
after cluster creation.
Version alignment between control plane
and node groups reduces operational risk.

---

## 5. Update strategy

Cluster update policy controls when:
- control plane upgrades occur,
- node groups are updated.
Important characteristics:
- Regional masters remain available during updates.
- Zonal masters may be temporarily unavailable.
- Node upgrades recreate nodes and reschedule pods.
Understanding update behavior is critical
for planning maintenance windows
and workload disruption tolerance.

---

## 6. Encryption integration (KMS)

Managed Kubernetes can integrate
with Key Management Service (KMS)
to encrypt sensitive cluster data,
including Kubernetes secrets stored in etcd.
Enabling KMS provides:
- protection of credentials at rest,
- improved compliance posture,
- reduced impact of storage compromise.
Clusters can function without KMS,
but encryption at rest is recommended
for production workloads.

---

## 7. Network CIDR allocation

Kubernetes assigns internal IP ranges for:
- Pod networks,
- Service networks.
These CIDR ranges must not overlap
with existing VPC address space.
Improper CIDR planning can cause:
- pod startup failures,
- routing conflicts,
- cross-network communication issues.
Automatic allocation is acceptable for labs.
Production environments require deliberate IP planning.

---

## Summary

Cluster design defines:
- isolation boundaries,
- identity model,
- availability level,
- upgrade behavior,
- encryption posture,
- IP addressing strategy.

These decisions determine how secure,
resilient, and maintainable the cluster will be.
