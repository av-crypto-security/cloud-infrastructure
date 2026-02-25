# Availability Zone Redistribution

## Scenario

One availability zone is removed from allocation policy.

---

## Observed Behavior

- Instance in removed zone transitions:
  - Closing traffic
  - Deleting instance
- New instance is created in remaining zones.
- Total instance count remains consistent.

---

## Technical Analysis

Instance Group ensures:

- Desired capacity is maintained.
- Zone distribution remains balanced.
- Traffic is only routed to healthy targets.

This simulates a zone-level outage or capacity withdrawal.

---

## Outcome

Service remains operational.

Capacity is rebalanced automatically across remaining zones.
No traffic interruption occurs.
