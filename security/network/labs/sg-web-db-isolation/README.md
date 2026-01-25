# Security Groups: Web ↔ Database Isolation

This lab demonstrates how to design and apply **network isolation**
using Security Groups in Yandex Cloud for a typical web application
architecture.

The goal is not to deploy a full production system, but to show
**security-oriented thinking** and **correct use of Security Groups**
as stateful firewalls.

## What this lab shows

* How Security Groups enforce **default deny** behavior
* How to isolate a database from the public network
* How to allow traffic **only where it is explicitly required**
* Why Security Group to Security Group rules are preferred over IP-based rules
* How load balancer health checks affect network security design

## Scope and assumptions

This lab focuses on **network security design**, not availability
or cost optimization.

Out of scope by design:

* Multi-AZ deployment
* Autoscaling
* VPN and IPSec configuration
* Infrastructure as Code (Terraform)

These topics are intentionally excluded to keep the lab focused
and easy to reason about.

## High-level architecture

The system consists of:

* Public Load Balancer
* Web application running on virtual machines
* Managed database cluster
* Dedicated Security Groups for each component

Each component is isolated and communicates only through
explicitly allowed network paths.

A detailed architecture description is provided in `architecture.md`.

## Security principles applied

* Least privilege
* Network segmentation
* No public access to the database
* No administrative access from the Internet
* Explicit handling of health checks

## Optional extensions

This lab can be extended with:

* VPN-based administrative access
* Infrastructure provisioning via Terraform
* TLS termination and certificate management

These extensions are intentionally left out of the base lab.

## Hands-on validation

Security Group behavior was validated using TCP connectivity checks
from different network locations.

Results:

- Direct access to the database from an administrative VM was blocked
- Access from the web VM was explicitly allowed via SG-to-SG rules

This confirms correct network isolation and enforcement of
the principle of least privilege.
