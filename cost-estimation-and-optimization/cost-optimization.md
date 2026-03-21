# Cost Optimization via Resource Labeling

This module demonstrates how to identify expensive resources
using labels and billing analytics.

## Overview

In real-world systems, cost optimization starts with visibility.

Labels allow grouping and tracking resource consumption.

## Scenario

Multiple virtual machines with different CPU guarantees:

- 5%
- 20%
- 50%
- 100%

Goal: identify the most expensive instance.

## Labeling Strategy

Each VM is assigned a label:

```bash
yc compute instance add-labels <INSTANCE_ID> \
  --labels workload=experiment,load=high
```

Example:

```bash
yc compute instance add-labels fhmg8tipg0j694jgvflq \
  --labels expense=100
```

## Analysis

After labeling:

1. Open Yandex DataLens
2. Navigate to Billing Dashboard
3. Filter by Labels
4. Compare cost per label

## Observations

- Higher CPU guarantee → higher cost
- Idle resources still generate cost
- Labeling enables cost attribution per workload

## Engineering Takeaways

- Always label resources in production
- Use labels for:
  - environments (dev/prod)
  - services
  - teams
- Combine labels with billing dashboards

## Cleanup

Always delete unused resources:

```bash
yc compute instance delete <INSTANCE_ID>
```

## Notes

- Billing data may take time to update
- Labels are critical for FinOps practices
