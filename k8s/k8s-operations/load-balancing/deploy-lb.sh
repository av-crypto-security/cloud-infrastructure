#!/bin/bash

set -e

SERVICE_NAME="my-loadbalancer"
MANIFEST="load-balancer.yaml"
MAX_WAIT=300  # seconds

echo "Applying manifest..."
kubectl apply -f "$MANIFEST"

echo "Waiting for External IP..."

START_TIME=$(date +%s)

while true; do
  EXTERNAL_IP=$(kubectl get svc "$SERVICE_NAME" \
    -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

  if [[ -n "$EXTERNAL_IP" ]]; then
    break
  fi

  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TIME))

  if [[ "$ELAPSED" -gt "$MAX_WAIT" ]]; then
    echo "Timeout waiting for External IP after $MAX_WAIT seconds"
    exit 1
  fi

  echo "Still waiting... ($ELAPSED s elapsed)"
  sleep 5
done

echo "External IP assigned: $EXTERNAL_IP"

echo "Testing connectivity..."
curl --fail --silent --show-error "http://$EXTERNAL_IP"

echo
echo "Deployment successful"
