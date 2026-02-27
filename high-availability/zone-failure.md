# Availability Zone Failure Simulation

## Scenario

Simulate failure of an availability zone by removing it from the Instance Group allocation policy.

Initial setup:

- 3 VMs
- 3 availability zones:
  - ru-central1-a
  - ru-central1-b
  - ru-central1-d
- 1 VM per zone
- Network Load Balancer attached

---

## Step 1 — Adjust Deployment Policy

To allow redistribution, deployment policy must allow expansion and contraction:

```yaml
deploy_policy:
  max_unavailable: 1
  max_expansion: 1
```

This allows:

- +1 temporary instance during redistribution
- -1 instance removal without downtime
```

---

## Step 2 — Remove One Availability Zone

Edit `specification.yaml`:

```yaml
allocation_policy:
  zones:
    - zone_id: ru-central1-a
    - zone_id: ru-central1-b
```

Zone `ru-central1-d` is removed.

Apply changes:

```bash
yc compute instance-group update \
  --id <instance_group_id> \
  --file specification.yaml
```

---

## Observed Behavior

### Traffic Closing

VM located in removed zone transitions to:

```
CLOSING_TRAFFIC
```

Load Balancer stops routing new connections to that instance.

---

### Instance Deletion

Instance transitions to:

```
DELETING_INSTANCE
```

VM is removed from the group.

---

### New Instance Creation

Simultaneously, a new instance is created in remaining zones:

```
CREATING_INSTANCE
```

Then:

```
RUNNING_ACTUAL
```

Target state becomes:

```
HEALTHY
```

---

## Traffic Behavior

During redistribution:

- Service remains available
- No HTTP errors observed
- Load is temporarily balanced across 2 VMs
- After recovery, 3 VMs run across remaining zones

Verification:

```bash
curl http://<load_balancer_external_ip>
```

Responses continue without interruption.

---

## Technical Analysis

Instance Group enforces:

```
scale_policy:
  fixed_scale:
    size: 3
```

When one zone is removed:

- Configuration drift is detected
- Instance in removed zone is gracefully drained
- Replacement is provisioned
- Desired capacity (3) is maintained

This simulates:

- Full zone outage
- Capacity withdrawal
- Regional rebalancing event

---

## Outcome

- No downtime
- No manual traffic switching
- Automatic redistribution across remaining zones
- High availability preserved
