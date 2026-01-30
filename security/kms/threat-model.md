# Threat Model: Scheduled Key Version Destruction

This document explains what security guarantees
scheduled destruction of KMS key versions actually provides.

---

## Threats it mitigates

### Compromised service account
If a service account is compromised:
- scheduling destruction disables decryption
- attacker cannot access historical data

---

### Accidental key misuse
Scheduled destruction limits:
- lifetime of cryptographic material
- blast radius of leaked ciphertext

---

### Delayed incident response
Allows time to:
- investigate incidents
- cancel destruction if it was triggered by mistake

---

## Threats it does NOT mitigate

- Exposure of plaintext before encryption
- Data leaked while key version was active
- Weak IAM policies granting decrypt permissions

---

## Why destruction is delayed

Delayed deletion:
- prevents irreversible mistakes
- supports incident recovery
- ensures auditability

This is a **security feature**, not a limitation.

---

## Key takeaway

Scheduled destruction:
- is an access control mechanism
- reduces long-term risk
- complements IAM, not replaces it
