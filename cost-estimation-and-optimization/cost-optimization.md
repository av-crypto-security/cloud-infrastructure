# Cost Optimization via Resource Labeling

This module demonstrates how to identify high-cost resources
using labeling and billing analysis.

---

## Overview

Cost optimization starts with visibility.

Without proper attribution, it is impossible to understand
which components generate the highest cost.

Labels provide a mechanism for grouping and analyzing resources.

---

## Scenario

Multiple virtual machines with different CPU guarantees:

* 5%
* 20%
* 50%
* 100%

---

## Hypothesis

Instances with higher CPU guarantee produce higher baseline cost
even under low utilization.

---

## Labeling Strategy

Apply labels to each instance:

```bash
yc compute instance add-labels <INSTANCE_ID> \
  --labels workload=experiment,env=test
```

Example:

```bash
yc compute instance add-labels fhmg8tipg0j694jgvflq \
  --labels expense=high
```

---

## Analysis Workflow

1. Open Yandex DataLens
2. Navigate to Billing Dashboard
3. Filter by Labels
4. Compare cost per group

---

## Observations

* Higher CPU guarantee → higher cost
* Idle resources still incur charges
* Labels enable cost attribution per workload

---

## Conclusion

Cost optimization should focus on:

* reducing overprovisioned CPU
* using lower guarantees where possible
* eliminating idle resources

---

## Production Labeling Strategy

Recommended label structure:

```
env=prod/dev
service=api/worker/db
owner=team-name
```

This enables:

* cost attribution per team
* environment-based filtering
* service-level cost analysis

---

## Cleanup

Always remove unused resources:

```bash
yc compute instance delete <INSTANCE_ID>
```

---

## Notes

* Billing data may be delayed
* Labels are a core FinOps practice
