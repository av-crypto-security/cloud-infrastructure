# First Application Deployment — NGINX

This document describes the exact sequence of steps required
to deploy a first application (NGINX) into a Managed Kubernetes cluster.

The process consists of:
- Installing kubectl
- Connecting to the cluster
- Creating a Deployment manifest
- Applying the manifest
- Verifying workload state
- Scaling the application

## 1. Install kubectl
kubectl is the command-line client used to communicate with the Kubernetes API.
Installation using APT (recommended for Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg \
  https://packages.cloud.google.com/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] \
https://apt.kubernetes.io/ kubernetes-xenial main" | \
sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update
sudo apt install -y kubectl
```
Verify installation:
```bash
kubectl version --client
```

## 2. Connect to the Managed Kubernetes cluster
Retrieve cluster credentials using the Yandex Cloud CLI:
```bash
yc managed-kubernetes cluster get-credentials \
  --id <cluster_id> \
  --external
```
Verify kubeconfig configuration:
```bash
kubectl config view
```
If configuration is correct, kubectl is now connected to the cluster.

## 3. Create the Deployment manifest
Create a file my-nginx.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: cr.yandex/<registry_id>/ubuntu-nginx:latest
```
Replace <registry_id> with your Container Registry identifier.

A portable, registry-independent demo Deployment manifest is provided in the repository: [my-nginx.yaml](my-nginx.yaml)

## 4. Apply the manifest
Create or update the resource:
```bash
kubectl apply -f my-nginx.yaml
```
Expected output:
```bash
deployment.apps/my-nginx-deployment created
```

## 5. Verify application state
Check Pods:
```bash
kubectl get pods
```
Wait until status becomes: 
```
Running
```
Detailed view:
```bash
kubectl get pods -o wide
```
Full resource description:
```bash
kubectl describe deployment my-nginx-deployment
```

## 6. Scale the Deployment
### Option 1 — Declarative (modify manifest)
Change:
```yaml
replicas: 1
```
to:
```yaml
replicas: 3
```
Then apply again:
```bash
kubectl apply -f my-nginx.yaml
```
### Option 2 — Imperative scaling
```bash
kubectl scale --replicas=3 deployment/my-nginx-deployment
```
Verify:
```bash
kubectl get pods
```
You should now see three running Pods.

## Result
The NGINX application is now:
- managed by a Deployment controller
- running as replicated Pods
- scalable via Kubernetes API
  
This completes the first application deployment workflow.
