# Managed Kubernetes — Load Balancing

This guide demonstrates how to expose an application running inside a Kubernetes cluster
to the public internet using a Service of type `LoadBalancer`.

We deploy an NGINX-based application and expose it via a cloud Network Load Balancer.

## Status

🚧 Work in progress.  
Image registry permissions and production validation are being finalized.


## Why LoadBalancer?

Pods inside a Kubernetes cluster receive internal IP addresses.

Internal IPs:
- are accessible only within the cluster
- may change when pods are recreated
- cannot be used for public access

To expose an application externally, we use:

Service → type: LoadBalancer

This creates a cloud load balancer with a stable public IP address.


## Architecture

User → Public IP → Cloud Load Balancer → Service → Pod


## Prerequisites

- Managed Kubernetes cluster running
- kubectl configured
- Proper IAM roles assigned
- NGINX Deployment already created (with label: app=nginx)


## Step 1 — Create Service Manifest

See: `load-balancer.yaml`


## Step 2 — Apply Manifest

`kubectl apply -f load-balancer.yaml`

Expected output:

`service/my-loadbalancer created`


## Step 3 — Get External IP

`kubectl get svc my-loadbalancer`

Wait until EXTERNAL-IP is assigned.


## Step 4 — Test Access

Open in browser:

`http://<EXTERNAL-IP>`

You should see the NGINX welcome page.


## Troubleshooting

If you receive:

`failed to ensure cloud loadbalancer: Permission denied`

Check IAM roles for your service account:

- load-balancer.admin
- vpc.publicAdmin (if public LB required)


## Result

Application is accessible from the internet via a stable public IP.
