# Ansible NGINX Configuration Management

A lightweight configuration management scenario demonstrating
how to provision and maintain multiple Ubuntu servers using Ansible over SSH.

## Overview

The playbook configures NGINX on two Ubuntu Server managed nodes
using a single reusable configuration.

The scenario demonstrates:

- Ansible inventory and SSH key-based authentication
- Privilege escalation with `become`
- Package installation using APT
- Jinja2 templates for NGINX configuration and HTML content
- Handler-based NGINX reload
- Service state management (`enabled` and `started`)
- HTTP response validation
- Idempotent execution
- Recovery of a stopped NGINX service

## Architecture

- **Control Node:** Ubuntu Server with Ansible Core
- **Managed Nodes:** Two Ubuntu Server instances
- **Connection:** SSH over a VirtualBox Host-Only network
- **Web server:** NGINX
- **Configuration:** Ansible playbook and Jinja2 templates

## Repository Structure

```text
ansible-nginx-configuration-management/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── playbooks/
│   └── site.yml
├── templates/
│   ├── index.html.j2
│   └── nginx-default.conf.j2
└── screenshots/
```

## Execution

Check inventory and connectivity:

```bash
ansible-inventory --graph
ansible webservers -m ping
```

Validate and execute the playbook:

```bash
ansible-playbook playbooks/site.yml --syntax-check
ansible-playbook playbooks/site.yml --ask-become-pass
```

The playbook installs NGINX, deploys the configuration and custom HTML page,
ensures the service is enabled and running, and checks the HTTP response
from the Control Node.

## Validation

The scenario was validated through:

- Successful Ansible connectivity to both managed nodes
- HTTP 200 responses and rendered HTML content
- NGINX enabled and active state
- A second playbook execution with `changed=0`
- Deliberate NGINX stop followed by successful recovery through Ansible

Screenshots of the execution and validation steps are available in `screenshots/`.

## Scope

This is a local infrastructure automation lab built with VirtualBox.
It demonstrates configuration management fundamentals
and repeatable server configuration;
it is not intended as a production deployment.
