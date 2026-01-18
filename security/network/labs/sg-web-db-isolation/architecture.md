# Architecture Overview

This document describes the logical architecture of the lab
and explains the reasoning behind each security decision.

## Components

### Internet

Represents untrusted external clients accessing the web application.

### Load Balancer

Accepts incoming HTTP/HTTPS traffic from the Internet and forwards
requests to backend web servers.

The load balancer also performs **health checks** against backend
instances.

### Web Servers (VMs)

Virtual machines running the web application.

These instances:

* Accept traffic only from the load balancer
* Do not expose administrative access to the public Internet
* Communicate with the database over a private network

### Managed Database

A managed database cluster (for example, PostgreSQL or MySQL).

The database:

* Has no public IP address
* Accepts traffic only from web servers
* Is protected by its own Security Group

## Security Groups

### sg-web

Attached to web server network interfaces.

Allows:

* Incoming HTTP/HTTPS traffic from the load balancer
* Health check traffic from the load balancer
* Administrative access from a trusted network (optional)

Denies:

* Any other incoming traffic by default

Allows outgoing traffic:

* To the database Security Group on the database port

### sg-db

Attached to the managed database cluster.

Allows:

* Incoming traffic only from sg-web on the database port

Denies:

* Any direct access from the Internet
* Any access from unrelated resources

## Traffic flows

Allowed traffic paths:

* Internet → Load Balancer → Web Servers
* Web Servers → Database
* Load Balancer → Web Servers (health checks)

Blocked traffic paths:

* Internet → Web Servers (direct)
* Internet → Database
* Web Servers → Internet (unless explicitly required)
