# Commands used

## Create Instance Group
yc compute instance-group create --file specification.yaml

## List instance groups
yc compute instance-group list

## Create Network Load Balancer
yc load-balancer network-load-balancer create \
  --region-id ru-central1 \
  --name my-load-balancer \
  --listener name=http-listener,external-ip-version=ipv4,port=80

## Attach target group
yc load-balancer network-load-balancer attach-target-group my-load-balancer \
  --target-group target-group-id=<TARGET_GROUP_ID>,healthcheck-name=http-check,healthcheck-interval=2s,healthcheck-timeout=1s,healthcheck-unhealthythreshold=2,healthcheck-healthythreshold=2,healthcheck-http-port=80

## Check target health
yc load-balancer network-load-balancer target-states my-load-balancer \
  --target-group-id <TARGET_GROUP_ID>

## Rolling update
yc compute instance-group update \
  --id <INSTANCE_GROUP_ID> \
  --file specification.yaml

## Delete VM (self-healing test)
yc compute instance delete <VM_NAME>

## Delete Instance Group
yc compute instance-group delete <GROUP_NAME>
yc load-balancer network-load-balancer delete <LB_NAME>
