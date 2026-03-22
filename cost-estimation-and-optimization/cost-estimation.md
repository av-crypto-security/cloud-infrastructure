# Cloud Cost Estimation (Yandex Cloud)

This module demonstrates cost estimation for a typical cloud architecture
using both the official calculator and manual calculations.
This model focuses on relative cost estimation rather than exact pricing.

## Overview

Before deploying any system, it is critical to estimate infrastructure cost.

This example evaluates a system consisting of:

- Compute Cloud (VM)
- Managed PostgreSQL cluster
- Technical support plan

## Architecture Cost Model

### Compute Cloud

Configuration:

- OS: Ubuntu 22.04
- Platform: Intel Ice Lake
- 4 vCPU (100% guaranteed)
- 16 GB RAM
- 100 GB SSD
- Public IP
- 100 GB outbound traffic

### Managed PostgreSQL

- 2 hosts
- class: s3-c4-m16
- storage: 200 GB (network-ssd)
- no public IP

### Support Plan

- Standard plan
- estimated consumption: 35,000 RUB/month

## Cost Estimation Approach

The cost is calculated using:

1. Yandex Cloud Pricing Calculator
2. Manual calculation (for unsupported services)

## Manual Calculation Example (Monitoring)

Given:

- 35 metrics
- 2 values per minute
- 30 days
- Cost per 1M values = 9.8 units

Total values:

```
35 × 2 × (60 × 24 × 30) = 3,024,000 values
```

Cost:

```
3.024 × 9.80 = 29.64 cost units
```

## Key Observations

- Monitoring cost is negligible compared to compute/database
- Compute and DB are dominant cost drivers
- Public IP and traffic contribute additional cost

## Engineering Takeaways

- Always estimate cost before deployment
- Identify high-cost components early
- Use labels and monitoring for cost attribution
- Prefer autoscaling and serverless where possible

## Notes

- Prices may vary depending on region and updates
- Always validate using the official calculator
