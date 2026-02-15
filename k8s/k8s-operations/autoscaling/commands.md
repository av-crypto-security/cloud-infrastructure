# Deploy autoscaling stack
kubectl apply -f load-balancer-hpa.yaml

# Check HPA status
kubectl get hpa

# Monitor scaling
watch kubectl get pod,hpa,nodes

# Get service external IP
kubectl get svc my-loadbalancer-hpa

# Generate load
while true; do wget -q -O- http://$LOAD_BALANCER_IP; done
