# Apply load balancer
kubectl apply -f load-balancer.yaml

# Check service status
kubectl get svc my-loadbalancer

# Watch service until EXTERNAL-IP appears
watch kubectl get svc my-loadbalancer

# Test connectivity
curl http://<external_IP>
