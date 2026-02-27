# VM Failure Handling

## Scenario

Simulate a virtual machine failure inside a managed Instance Group behind a Network Load Balancer in Yandex Cloud.
The infrastructure consists of:
- Instance Group with 3 VMs
- 3 availability zones:
   - `ru-central1-a`
   - `ru-central1-b`
   - `ru-central1-d`
- Ubuntu 18.04 image
- NGINX installed via cloud-init
- Network Load Balancer with HTTP health checks

---

## Infrastructure Deployment

### Instance Group Specification

Key configuration fragments from specification.yaml:
```yaml
Allocation policy (multi-zone)
allocation_policy:
  zones:
    - zone_id: ru-central1-a
    - zone_id: ru-central1-b
    - zone_id: ru-central1-d
```
Fixed scale
```yaml
scale_policy:
  fixed_scale:
    size: 3
```
Cloud-init configuration
```yaml
metadata:
  user-data: |-
    #cloud-config
      users:
        - name: my-user
          groups: sudo
          lock_passwd: true
          sudo: 'ALL=(ALL) NOPASSWD:ALL'
          ssh-authorized-keys:
            - <public_ssh_key>

      package_update: true
      runcmd:
        - [ apt-get, install, -y, nginx ]
        - >
          bash -c '
          . /etc/os-release;
          sed -i "s/Welcome to nginx/It is $(hostname) on $PRETTY_NAME/"
          /var/www/html/index.nginx-debian.html
          '
```
Each VM serves a page identifying:
- Hostname
- OS version

### Create Instance Group
```bash
yc compute instance-group create --file specification.yaml
```

### Create Network Load Balancer
```bash
yc load-balancer network-load-balancer create \
  --region-id ru-central1 \
  --name my-load-balancer \
  --listener name=my-listener,external-ip-version=ipv4,port=80 \
  --target-group target-group-id=<target_group_id>,healthcheck-name=test-health-check,healthcheck-interval=2s,healthcheck-timeout=1s,healthcheck-unhealthythreshold=2,healthcheck-healthythreshold=2,healthcheck-http-port=80
```
### Verify service
```bash
curl http://<load_balancer_external_ip>
```
Expected result:
```
It is <hostname> on Ubuntu 18.04.x LTS
```
Repeated requests return responses from different VMs.

---

## Monitoring State

Continuous monitoring of:
- Instance Group
- Load Balancer target states
```bash
while true; do
  yc compute instance-group \
    --id <instance_group_id> list-instances;

  yc load-balancer network-load-balancer \
    --id <load_balancer_id> target-states \
    --target-group-id <target_group_id>;

  sleep 5;
done
```

---

## Failure Simulation

One VM was manually deleted via Management Console.

---

## Observed Behavior

### Step 1 — Health Check Failure
Load Balancer detects failure.
Target state:
```
UNHEALTHY
```
Traffic is redirected to remaining two instances.

### Step 2 — Target Removal
Target transitions to:
```
DRAINING
```
Load Balancer stops forwarding traffic to the failed instance.
Service remains available.

### Step 3 — Instance Group Reconciliation
Instance Group detects deviation from desired state:
```
Desired capacity: 3
Actual capacity: 2
```
Reconciliation process starts automatically.
New VM appears with status:
```
CREATING_INSTANCE
```

### Step 4 — VM Initialization
After provisioning:
Instance status:
```
RUNNING_ACTUAL
```
Target state:
```
OPEN_TRAFFIC
```

### Step 5 — Full Recovery
Target becomes:
```
HEALTHY
```
Traffic distribution is restored across all 3 instances.

---

## Technical Analysis

Instance Group operates under:
```yaml
scale_policy:
  fixed_scale:
    size: 3
```
This defines a declared desired state.
When a VM is deleted:
1. Load Balancer health check fails.
2. Target is removed from rotation.
3. Instance Group reconciliation controller detects drift.
4. Replacement instance is provisioned automatically.
5. Capacity returns to declared state.

This demonstrates:
- Self-healing behavior
- Automatic reconciliation
- Zero-downtime architecture
- High availability across availability zones

---

## Outcome

- No service downtime occurred.
- Temporary capacity reduction from 3 → 2 instances.
- Automatic restoration to 3 instances.
- No manual intervention required.

---

## Key Takeaways

- Multi-zone deployment increases fault tolerance.
- Health checks ensure automatic traffic rerouting.
- Instance Group maintains declared capacity.
- Failure of a single VM does not impact availability.
