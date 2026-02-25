# VM Failure Handling

## Scenario

One virtual machine is manually removed from the Instance Group.

---

## Observed Behavior

1. Health check failure is detected by the Load Balancer.
2. Target state transitions:
   - UNHEALTHY
   - DRAINING
3. Traffic is redirected to remaining healthy instances.
4. Instance Group reconciles desired state.
5. New instance is provisioned:
   - CREATING_INSTANCE
   - RUNNING_ACTUAL
6. Target returns to HEALTHY state.

---

## Technical Analysis

Instance Group operates under a declared desired capacity of three instances.

When an instance disappears:

- Health check fails.
- Load Balancer removes the target.
- Reconciliation controller provisions a replacement instance.
- Capacity is restored automatically.

---

## Outcome

Service availability is preserved.

Temporary capacity reduction does not result in downtime.
Full redundancy is restored automatically.
