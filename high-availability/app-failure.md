# Application-Level Failure Recovery

## Scenario

The NGINX process is manually stopped on one instance while the VM remains operational.

---

## Observed Behavior

- HTTP health check fails.
- Load Balancer removes the instance from rotation.
- Instance Group marks instance unhealthy.
- VM is restarted.
- NGINX becomes available again.
- Target returns to HEALTHY state.

---

## Technical Analysis

Health checks operate at application level.

Although the VM remains reachable, failure of the HTTP endpoint results in:

- Traffic isolation
- Automated recovery cycle

This demonstrates health-based infrastructure management.

---

## Outcome

Traffic is redirected to healthy instances.

The failed node is automatically recovered without manual intervention.
