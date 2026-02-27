# Rolling Update Strategies in Instance Groups

## Scenario

Demonstrate two rolling update strategies for a Yandex Cloud Instance Group:

1. **Sequential replacement (no expansion allowed)**
2. **Zero-downtime expansion-first strategy**

Initial state:

- Instance Group: 3 VMs
- Multi-zone deployment
- NGINX installed via cloud-init
- Network Load Balancer attached
- Fixed scale: 3

---

# Strategy 1 — Sequential Replacement (No Expansion)

## Goal

Update VM image (Ubuntu 18.04 → Ubuntu 22.04)  
without increasing group size.

---

## Step 1 — Modify Image

Edit `specification.yaml`.

Change:

```yaml
boot_disk_spec:
  disk_spec:
    image_id: <ubuntu_18_image_id>
```

To:

```yaml
boot_disk_spec:
  disk_spec:
    image_id: <ubuntu_22_image_id>
```

---

## Step 2 — Configure Deployment Policy

```yaml
deploy_policy:
  max_unavailable: 1
  max_expansion: 0
```

Meaning:

- No temporary extra instances
- Only 1 VM may be unavailable at a time

---

## Step 3 — Apply Update

```bash
yc compute instance-group update \
  --id <instance_group_id> \
  --file specification.yaml
```

---

## Observed Behavior

### Initial State

Instances show:

```
RUNNING_OUTDATED
```

Meaning they run old image version.

---

### First VM Update Cycle

VM transitions:

```
CLOSING_TRAFFIC
STOPPING_INSTANCE
UPDATING_INSTANCE
STARTING_INSTANCE
OPENING_TRAFFIC
RUNNING_ACTUAL
```

Load Balancer removes VM before update.

Traffic continues on remaining 2 VMs.

---

### Sequential Updates

Same process repeats for remaining VMs.

At no point more than **1 VM** is unavailable.

---

## Capacity During Update
```
| Stage | Active VMs |
|-------|------------|
| Before update | 3 |
| During update | 2 |
| After update | 3 |
```
Temporary capacity reduction occurs.

---

## Technical Characteristics

- Rolling update
- No capacity increase
- Controlled degradation (3 → 2 → 3)
- Safe for moderate traffic loads

---

# Strategy 2 — Expansion-First (Zero Downtime)

## Goal

Update VMs without reducing active capacity.

---

## Step 1 — Modify Image Again

Change `image_id` to new image:

```yaml
boot_disk_spec:
  disk_spec:
    image_id: <new_image_id>
```

---

## Step 2 — Configure Deployment Policy

```yaml
deploy_policy:
  max_unavailable: 0
  max_expansion: 1
```

Meaning:

- No VM can become unavailable
- Group may temporarily expand by +1

---

## Step 3 — Apply Update

```bash
yc compute instance-group update \
  --id <instance_group_id> \
  --file specification.yaml
```

---

## Observed Behavior

### Initial State

```
RUNNING_OUTDATED
```

All VMs running old image.

---

### New VM Creation

Before stopping any VM:

```
CREATING_INSTANCE
STARTING_INSTANCE
OPENING_TRAFFIC
RUNNING_ACTUAL
```

Now group temporarily contains 4 VMs.

---

### Old VM Removal

One outdated VM transitions:

```
CLOSING_TRAFFIC
STOPPING_INSTANCE
DELETING_INSTANCE
```

Group returns to size 3.

---

### Process Repeats

New instance created → old instance removed  
until all VMs run updated image.

---

## Capacity During Update
```
| Stage | Active VMs |
|-------|------------|
| Before update | 3 |
| During update | 4 |
| After update | 3 |
```
No reduction in serving capacity.

---

# Comparison of Strategies
```
| Feature | Sequential | Expansion-First |
|----------|------------|----------------|
| Capacity drop | Yes (3→2) | No |
| Temporary scaling | No | Yes (+1) |
| Resource usage | Lower | Higher |
| Downtime risk | Very low | Minimal |
| Best for | Non-critical systems | High-load production |
```
---

# Traffic Verification

During update:

```bash
curl http://<load_balancer_external_ip>
```

Responses continue without interruption.

To verify OS version after update:

```bash
curl http://<load_balancer_external_ip>
```

Expected output:

```
It is <hostname> on Ubuntu 22.04.x LTS
```

---

# Technical Analysis

Instance Group compares:

- Current instance template
- Desired instance template

When `image_id` changes:

- Existing VMs become `RUNNING_OUTDATED`
- Rolling update is triggered
- Behavior depends on `deploy_policy`

This demonstrates:

- Declarative infrastructure management
- Controlled rolling updates
- Capacity-aware deployment strategies
- Zero-downtime deployment patterns

---

# Outcome

Both strategies:

- Preserve service availability
- Perform automated rolling replacement
- Require no manual VM manipulation

The difference lies in:

- Capacity handling
- Resource consumption
- Risk profile
