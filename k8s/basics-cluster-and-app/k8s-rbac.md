# Kubernetes RBAC and Cloud Roles (Yandex Cloud)

This document provides a concise reference of typical IAM roles  
used when working with Managed Kubernetes in Yandex Cloud.

Access control is enforced via **Yandex IAM**.  
Roles define what actions a user, team, or service account is allowed to perform.

Roles are assigned at the **cloud**, **folder**, or **resource** level.

---

# 1. Role Categories

There are two main groups of roles:

1. Cloud-level roles (IAM, VPC, Registry, Managed Kubernetes)
2. Cluster-level roles (Kubernetes API access)

This document focuses on practical IAM role usage.

---

# 2. Common Operational Tasks → Required Roles

## Create a Kubernetes cluster

**Role:**  
`k8s.admin`

Allows creating and managing clusters.

> Does NOT allow creating public resources.

---

## Create a public cluster / allow public access

**Role:**  
`vpc.publicAdmin`

Required to create:

- clusters with public API endpoint
- nodes with public IP
- public-facing resources

This role should be granted deliberately.

---

## Install system applications inside cluster

(e.g. Ingress controller, monitoring stack)

**Role:**  
`k8s.cluster-api.cluster-admin`

Provides full administrative access to Kubernetes API.

Use carefully.

---

## Create and manage applications in cluster

(Deployments, Services, ConfigMaps)

**Role:**  
`k8s.cluster-api.editor`

Typical role for developers.

Does NOT allow:

- managing node groups
- modifying cluster infrastructure

---

## Read-only access to cluster

**Role:**  
`k8s.viewer`

Allows observing cluster state without modifying resources.

---

## Push container images to registry

**Role:**  
`container-registry.images.pusher`

Allows:

- uploading images
- pushing new versions

Recommended only for development folders.

---

## Pull container images from registry

**Role:**  
`container-registry.images.puller`

Required for:

- worker nodes
- service accounts
- CI/CD systems

---

## Full registry management

**Role:**  
`container-registry.admin`

Allows:

- push
- delete
- manage repositories

Typically used by DevOps/SRE.

---

## Connect cluster to VPC network

**Role:**  
`vpc.user`

Required for:

- attaching subnets
- working with VPC resources

---

## Manage service accounts

**Role:**  
`iam.serviceAccounts.user`

Allows cluster to use service accounts securely.

---

## 🔹 Allow public load balancers

**Role:**  
`load-balancer.admin`

Required to create public LoadBalancers.

---

# 3. Typical Role Distribution

## Developer

- `k8s.cluster-api.editor`
- `container-registry.images.pusher` (dev only)
- `k8s.viewer`

---

## DevOps / SRE

- `k8s.admin`
- `k8s.cluster-api.cluster-admin`
- `container-registry.admin`
- `vpc.user`
- `iam.serviceAccounts.user`
- `vpc.publicAdmin` (restricted)

---

## CI/CD

- `container-registry.images.pusher`
- `container-registry.images.puller`
- `k8s.cluster-api.editor`

---

## Cluster Nodes

- `container-registry.images.puller`

---

# 4. Security Principles

- Separate production and development environments using folders.
- Grant minimum required roles.
- Avoid giving `cluster-admin` broadly.
- Public access requires explicit additional roles.
- Always distinguish between infrastructure access and application access.

---

# Summary

Kubernetes access in Yandex Cloud is controlled through IAM roles.

- Infrastructure control → `k8s.admin`
- Application management → `k8s.cluster-api.editor`
- Full API control → `k8s.cluster-api.cluster-admin`
- Image operations → `container-registry.*`
- Public exposure → `vpc.publicAdmin`, `load-balancer.admin`

Correct role separation is a key element of cluster reliability and security.
