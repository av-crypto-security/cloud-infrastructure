# Kubernetes Networking — Core Mental Model

This document provides a coherent mental model of how networking works in Kubernetes.
It focuses on the architectural contract, not on specific CNI implementations.

## 1. The Foundational Networking Contract

Kubernetes networking is built on three strict assumptions:
- Every Pod receives its own unique IP address.
- Pods can communicate directly with other Pods without NAT.
- Nodes can reach Pod IPs directly.

If any of these assumptions are violated, the cluster networking model is broken.
This flat network model is fundamental.
All higher-level abstractions rely on it.

## 2. Pod IPs Are Ephemeral

A Pod IP address:
- is assigned when the Pod is created,
- changes if the Pod is recreated,
- must never be treated as a stable interface.

Pods are disposable compute units.
Their identity is not their IP address.
Directly depending on Pod IPs in application logic is a design error.

## 3. Service as a Stable Abstraction

A Service provides:
- a stable virtual IP (ClusterIP),
- load balancing across matching Pods,
- decoupling between clients and Pod lifecycle.

A Service is not a running process.
It is a routing rule programmed into the cluster network layer.
Clients must communicate with Services — not with Pods.

## 4. DNS as a Core Component

Every Service automatically receives a DNS name.
Applications are expected to:
- use DNS names for communication,
- avoid hardcoded IP addresses,
- rely on Kubernetes service discovery.

Cluster DNS is not a convenience feature.
It is a core control plane component that enables dynamic workloads.

## 5. kube-proxy (Conceptually)

kube-proxy implements Service networking by:
- programming iptables or IPVS rules,
- mapping virtual Service IPs to backend Pods,
- routing traffic at Layer 4 (TCP/UDP).

kube-proxy does not perform Layer 7 routing.
It does not inspect HTTP traffic.

## 6. Service vs Ingress

A Service:
- operates inside the cluster,
- provides Layer 4 load balancing,
- abstracts Pod sets.

Ingress:
- manages inbound HTTP(S) traffic,
- requires an Ingress Controller,
- routes external traffic to Services.

Traffic flow for external access typically follows:
```
External Client → Ingress Controller → Service → Pod
```
These components serve different architectural purposes.

## 7. Common Conceptual Failures

Most beginner networking mistakes come from:
- assuming Pod IPs are stable,
- trying to test applications by targeting Pod IPs,
- misunderstanding that LoadBalancer resources expose Services, not Pods,
- assuming networking works like traditional VM-based systems.

Kubernetes networking is designed for:
- dynamic workloads,
- replaceable compute units,
- declarative traffic routing.

Understanding this model prevents most early-stage failures.
