# Cluster Access and Authentication

This document explains how authenticated access
to a Managed Kubernetes cluster is established
and controlled.

---

## 1. API access model

All cluster management is performed
through the Kubernetes API server.
Administrative access is provided
via a secured HTTPS endpoint.
This endpoint exposes:
- cluster management interface,
- resource control operations.

It does not expose application traffic.

---

## 2. kubectl as API client

`kubectl` is the standard client
for interacting with the Kubernetes API.
All operations are API-driven:
- create,
- update,
- delete,
- inspect resources.

There is no direct node-level management
required for normal operations.

---

## 3. Credential acquisition flow

Cluster credentials are retrieved
via the cloud provider CLI.
This process:
- authenticates the user via cloud IAM,
- updates local kubeconfig,
- binds user identity to cluster access.

After credentials are configured,
all further operations are performed
directly against the Kubernetes API.

---

## 4. kubeconfig structure

The kubeconfig file stores:
- cluster endpoint information,
- authentication data,
- access contexts.

Multiple clusters may coexist
in a single kubeconfig.
Context isolation is critical to prevent:
- accidental deployment to wrong environments,
- production misconfiguration.

---

## 5. Dual authorization model

Cluster access uses two independent layers:

### Cloud IAM

Controls:
- who can retrieve cluster credentials,
- who can access the API endpoint,
- who can manage cluster infrastructure.

### Kubernetes RBAC

Controls:
- what authenticated identities can do inside the cluster,
- access to namespaces and resources,
- allowed operations (verbs).

Both layers must be configured correctly.
Overprivileged IAM or RBAC
creates significant security risk.

---

## 6. Security risks

Common exposure vectors:
- leaked kubeconfig files,
- excessive IAM roles,
- shared administrative credentials,
- long-lived tokens.

Secure operation requires:
- least-privilege IAM roles,
- restricted RBAC bindings,
- credential protection discipline.

---

## Summary

Cluster access relies on:
- authenticated API communication,
- layered authorization (IAM + RBAC),
- controlled credential distribution.

Understanding this separation
is essential for secure Kubernetes operations.
