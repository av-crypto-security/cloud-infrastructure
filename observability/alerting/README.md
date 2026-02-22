# Alerting: High Traffic Detection

This section demonstrates how alerting is implemented for traffic spikes.
The goal: detect abnormal traffic growth and notify operators immediately.

---

## Scenario

We monitor website traffic for the application.
If traffic significantly increases, an alert must trigger and notify via configured channels.

---

## Alert Configuration

The alert is created directly from the existing dashboard widget:

1. Open dashboard
2. Select **Traffic widget**
3. Click **Create Alert**
4. Use:
   - Condition: aggregated query (sum)
   - Threshold: Warning level
5. Configure notification channel:
   - Email / Push / SMS
6. Save alert

Status after creation: `OK`

---

## Trigger Test

Generate traffic load:

```bash
while true; do wget -q -O- <site_url>; done
```
After threshold is exceeded:

- Alert status changes to Warning
- Notification is delivered

## Why This Matters

Alerting provides:

- Early incident detection
- Reduced MTTR
- Automated operator notification
- Production readiness

Monitoring without alerting is just observability.
Alerting makes it operational.
