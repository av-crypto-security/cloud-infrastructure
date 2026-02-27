# Application-Level Failure Recovery

## Scenario

Simulate application failure by stopping NGINX process while the VM remains operational.

Infrastructure:

- 3 VMs
- Network Load Balancer with HTTP health checks
- Instance Group with health monitoring enabled

---

## Step 1 — Enable Instance Health Checks

Ensure health checks are enabled in Instance Group settings:

Management Console → Instance Group → Edit → Enable health checks

---

## Step 2 — Identify Active VM

Check which VM is currently serving traffic:

```bash
curl http://<load_balancer_external_ip>
```

Response example:

```
It is epd4s3k2 on Ubuntu 18.04.6 LTS
```

Obtain external IP of that VM from console.

---

## Step 3 — Connect via SSH

```bash
ssh my-user@<vm_external_ip>
```

Verify NGINX is running:

```bash
ps aux | grep nginx
```

Expected output includes nginx master and worker processes.

---

## Step 4 — Simulate Application Failure

Stop NGINX:

```bash
sudo killall nginx
```

Verify it stopped:

```bash
ps aux | grep nginx
```

No nginx processes should remain.

---

## Observed Behavior

### Health Check Failure

Load Balancer HTTP check fails.

Target state becomes:

```
UNHEALTHY
```

Traffic is redirected to other instances.

Verify:

```bash
curl http://<load_balancer_external_ip>
```

Response now comes from a different VM.

---

### Traffic Draining

Instance transitions to:

```
CLOSING_TRAFFIC
```

Then:

```
STOPPING_INSTANCE
```

---

### Automatic Restart

Instance Group restarts VM.

State transitions:

```
STARTING_INSTANCE
RUNNING_ACTUAL
```

After reboot, cloud-init ensures NGINX is running again.

Target state:

```
HEALTHY
```

---

## Service Verification

After recovery:

```bash
curl http://<load_balancer_external_ip>
```

Traffic is again distributed across all 3 instances.

Direct VM access:

```bash
curl http://<vm_external_ip>
```

Returns NGINX welcome page.

---

## Technical Analysis

Health checks operate at HTTP layer.

Even though:

- VM is reachable
- SSH works

Failure of application endpoint results in:

- Traffic isolation
- Instance restart
- Automatic recovery

This demonstrates:

- Application-level monitoring
- Self-healing infrastructure
- Zero manual intervention

---

## Outcome

- No service downtime
- Automatic traffic rerouting
- Automatic VM restart
- Full recovery without human intervention
