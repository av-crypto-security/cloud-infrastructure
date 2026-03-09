# ClickHouse Cluster Architecture and Connection

This document describes the architecture of a distributed ClickHouse deployment
and typical connection methods used by engineers when working with a managed
cluster.

## Cluster Architecture

When a ClickHouse cluster is created with two or more nodes, an additional
cluster of three nodes is typically deployed to run Apache ZooKeeper.

Apache ZooKeeper is a distributed coordination service responsible for:

- cluster configuration
- shard synchronization
- replication metadata
- distributed query coordination

Without ZooKeeper a distributed ClickHouse cluster cannot operate.

A typical minimal architecture therefore looks like:

ClickHouse nodes:
- ch-node-1
- ch-node-2

ZooKeeper nodes:
- zk-node-1
- zk-node-2
- zk-node-3

ZooKeeper nodes are usually managed by the platform provider and are not
directly accessible to users.

## ClickHouse Node Model

Unlike traditional relational databases, ClickHouse does not require a single
primary node.

In distributed configurations:

- data can be written to any node
- queries can be executed from any node
- replication is coordinated via ZooKeeper

This model allows horizontal scaling and high query throughput.

## Creating a Cluster

Typical cluster parameters used for analytical workloads:

Node configuration example:

- host type: burstable
- instance class: b3-c1-m4
- storage: network SSD
- storage size: 10 GB

During cluster creation engineers usually define:

- cluster name
- database name
- database user
- password
- public network access

Managed services often provide additional integrations such as:

- analytics dashboards
- monitoring tools
- serverless compute integrations

## Connection Methods

ClickHouse supports several connection protocols:

Native TCP protocol  
Recommended for CLI tools and high-performance clients.

HTTP protocol  
Used by web tools and some database clients.

Common client interfaces include:

- CLI client
- JDBC drivers
- ODBC drivers
- language libraries (Python, Go, Ruby, etc.)

GUI tools such as database workbenches can also connect to ClickHouse.

Typical connection parameters include:

- host
- port
- database
- username
- password
- TLS configuration

When public access is enabled, encrypted connections should always be used.
