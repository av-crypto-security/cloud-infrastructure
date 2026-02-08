# Instance Group and Load Balancer (Yandex Cloud)

This lab demonstrates how to deploy a highly available web application
using Yandex Cloud Instance Groups and a Network Load Balancer.
The infrastructure is described declaratively using a YAML specification,
which is an introductory form of Infrastructure as Code (IaC).

## Architecture

- Instance Group with a fixed size of 2 virtual machines
- Ubuntu 22.04 virtual machines with NGINX installed via cloud-init
- Network Load Balancer (L4, TCP) distributing traffic on port 80
- Health checks to automatically exclude unhealthy instances
```
Internet
   |
[ Load Balancer :80 ]
   |
---------------------
|                   |
VM-1 (NGINX)     VM-2 (NGINX)
```
## Key Concepts

- Instance Groups as a self-healing mechanism
- Declarative infrastructure with YAML specifications
- Cloud-init for automatic software provisioning
- Health checks and traffic failover
- Rolling updates without downtime

## Why YAML instead of Terraform?

This lab intentionally uses native Yandex Cloud specifications
to demonstrate how instance groups work under the hood.
Terraform is used to manage the same resources
in a more scalable and reusable way.
