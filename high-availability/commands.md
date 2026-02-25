# Deployment and Monitoring Commands

## Create Instance Group
```bash
yc compute instance-group create --file specification.yaml
```

## Create Network Load Balancer
```bash
yc load-balancer network-load-balancer create \
  --region-id ru-central1 \
  --name my-load-balancer \
  --listener name=my-listener,external-ip-version=ipv4,port=80 \
  --target-group target-group-id=<TARGET_GROUP_ID>,\
healthcheck-name=test-health-check,\
healthcheck-interval=2s,\
healthcheck-timeout=1s,\
healthcheck-unhealthythreshold=2,\
healthcheck-healthythreshold=2,\
healthcheck-http-port=80
```

## Monitor System State
```bash
while true; do
  yc compute instance-group \
    --id <INSTANCE_GROUP_ID> list-instances;

  yc load-balancer network-load-balancer \
    --id <LOAD_BALANCER_ID> target-states \
    --target-group-id <TARGET_GROUP_ID>;

  sleep 5;
done
```
