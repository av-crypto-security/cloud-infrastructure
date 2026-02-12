# Kubernetes Storage & Security — Common Pitfalls

This document describes the most frequent storage and security mistakes that occur after deploying the first real workload.
Kubernetes provides primitives.
It does not automatically provide persistence or security guarantees.

## 1. Pods Are Ephemeral Compute Units

A Pod:
- can be terminated at any time,
- can be rescheduled to another node,
- does not guarantee filesystem durability.

Anything written inside the container filesystem is temporary.
If the Pod is recreated, local data is lost.
Applications must treat Pods as disposable execution environments.

## 2. Volume Does Not Automatically Mean Persistence

A Volume:
- is mounted into a Pod,
- exists for the lifetime of that Pod,
- is destroyed when the Pod is removed (for most volume types).

A PersistentVolume (PV):
- exists independently of Pod lifecycle,
- is managed at the cluster level,
- can survive Pod restarts and rescheduling.

Persistence requires:
- a PersistentVolume,
- a PersistentVolumeClaim,
- a suitable storage backend.

Without this separation, data durability is not guaranteed.

## 3. Running Databases in Kubernetes

Common mistakes:
- running a database without a PersistentVolume,
- ignoring backup strategy,
- deploying stateful systems as simple Deployments.
  
Kubernetes does not replace database operational requirements.

Running a database inside Kubernetes still requires:
- persistent storage,
- backup and restore strategy,
- proper lifecycle management.

Containerization does not eliminate state management responsibilities.

## 4. Ignoring SecurityContext

By default, containers may:
- run as root,
- have unnecessary Linux capabilities,
- write to the root filesystem.

SecurityContext allows defining:
- user and group IDs,
- privilege restrictions,
- filesystem policies.

SecurityContext is part of the security model — not an optional hardening layer.
Failing to define it increases risk exposure.

## 5. Secrets Are Not Automatically Encrypted

A Kubernetes Secret:
- is stored in etcd,
- is base64-encoded,
- is not encrypted by default at rest.

Encryption at rest requires:
- enabling an encryption provider,
- or integrating with a Key Management Service (KMS).

## 6. ServiceAccount as Pod Identity

Every Pod runs under a ServiceAccount.
This ServiceAccount:
- provides an identity inside the cluster,
- grants permissions via Kubernetes RBAC,
- exposes a token to the Pod.

Using the default ServiceAccount without restriction:
- increases blast radius,
- violates the principle of least privilege.

ServiceAccount configuration is part of workload security.

## 7. Mental Model Summary

Kubernetes:
- does not guarantee persistence by default,
- does not enforce least privilege automatically,
- does not provide encrypted storage unless configured.

It provides:
- primitives,
- isolation boundaries,
- configurable policies.

Architecture and operational discipline remain the responsibility of the operator.
