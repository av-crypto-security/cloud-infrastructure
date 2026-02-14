# Managed Kubernetes — Horizontal Pod Autoscaling (HPA)

This guide demonstrates how to configure automatic scaling
based on CPU utilization.

We will:

1. Deploy a test workload
2. Expose it via LoadBalancer
3. Configure Horizontal Pod Autoscaler
4. Generate artificial load
5. Observe scaling behavior


## Architecture

User → Load Balancer → Service → Deployment → Pods
                                    ↑
                                    |
                                  HPA


## Why HPA?

HPA automatically adjusts the number of pods based on metrics:

- CPU utilization
- Memory (if configured)
- Custom metrics


## Step 1 — Deploy Application + Service + HPA

See: `load-balancer-hpa.yaml`


## Step 2 — Apply Manifest

`kubectl apply -f load-balancer-hpa.yaml`

Expected output:

```
deployment.apps/my-nginx-deployment-hpa created
service/my-loadbalancer-hpa created
horizontalpodautoscaler.autoscaling/my-hpa created
```


## Step 3 — Get External IP

`kubectl get svc my-loadbalancer-hpa`

Export it:

`export LOAD_BALANCER_IP=<EXTERNAL-IP>`


## Step 4 — Monitor Cluster

```sh
while true; do
kubectl get pod,svc,hpa,nodes -o wide
sleep 5
done
```


## Step 5 — Generate Load

```sh
while true; do
wget -q -O- http://$LOAD_BALANCER_IP
done
```

You will observe:

- Pods increasing (HPA)
- Nodes increasing (Cluster Autoscaler)


## Step 6 — Stop Load

`Ctrl + C`

Cluster will scale down automatically.


## Result

- Application scales horizontally
- Infrastructure scales automatically
- No manual intervention required
