# Instance Group and Load Balancer (Yandex Cloud)

This lab demonstrates how to deploy a highly available web application
using Yandex Cloud Instance Groups and a Network Load Balancer.
The infrastructure is described declaratively using a YAML specification,
which represents an early form of Infrastructure as Code (IaC).

This lab demonstrates L4 load balancing using Yandex Cloud Network Load Balancer.
NGINX is used only as a backend web server to verify traffic distribution and health checks.
L7 load balancing is covered separately using managed HTTP load balancers or Kubernetes ingress.

## Architecture

- Instance Group with a fixed size of **3 virtual machines**
- Ubuntu 22.04 virtual machines with NGINX installed via cloud-init
- Network Load Balancer (L4, TCP) distributing traffic on port 80
- Health checks to automatically exclude unhealthy instances
- Rolling updates with no downtime

```
Internet
   |
[ Load Balancer :80 ]
   |
-----------------------------------------
|                   |                   |
VM-1 (NGINX)     VM-2 (NGINX)     VM-3 (NGINX)
```

## Key Concepts

- Instance Groups as a **self-healing** mechanism
- Declarative infrastructure using **YAML specifications**
- Automatic provisioning with **cloud-init**
- Health checks and automatic traffic failover
- **Rolling updates** controlled by deployment policies

## Why YAML instead of Terraform?

This lab intentionally uses native Yandex Cloud instance group
specifications to demonstrate how declarative infrastructure,
self-healing, and rolling updates work at a low level.
Terraform is used in other parts of this repository to manage
similar resources in a more scalable, reusable,
and production-ready way.
