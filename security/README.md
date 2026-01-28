# Security
> ⚠️ This section is under active development and continuously extended.

This section contains a structured set of security-related materials and hands-on labs,
covering core cloud security domains from identity management to network isolation
and secure connectivity.

The goal of this section is **not** to provide a full production reference,
but to demonstrate a solid engineering understanding of security primitives,
their responsibilities, and correct practical usage in cloud environments.

The content is organized by **security domain**, not by tools or services,
to reflect how security is reasoned about in real-world architectures.

---

## Structure overview

### IAM (Identity and Access Management)

`iam/` focuses on identities, permissions, and trust boundaries.

Topics include:
- Service accounts and their lifecycle
- Role assignment and scope (cloud / folder / resource)
- Common misconfigurations and security pitfalls

Hands-on labs demonstrate:
- Creating and using service accounts
- Least-privilege role assignment
- Secure interaction with managed services (e.g., KMS)

---

### KMS (Key Management Service)

`kms/` covers cryptographic key management and data protection.

Topics include:
- Difference between keys and key versions
- Key rotation and destruction semantics
- Practical encryption and decryption workflows

Labs focus on:
- Using managed KMS for application-level encryption
- Understanding operational implications of key rotation

---

### Network Security

`network-security/` addresses traffic isolation and network-level access control.

Topics include:
- Security Groups as stateful firewalls
- Traffic segmentation between application tiers
- Load balancers and health check considerations
- Reference architectures

Hands-on implementations validate:
- Ingress vs egress control
- Security Group to Security Group rules
- Default deny principles

---

### VPN and Secure Connectivity

`vpn/` focuses on secure network connectivity between environments.

Currently covered:
- IPSec VPN using strongSwan
- Site-to-site secure tunnels
- Cryptographic and routing considerations

Labs emphasize:
- Practical tunnel establishment
- Security implications of VPN design choices

---

### Certificates and TLS

`certificates/` covers transport security and certificate management.

Topics include:
- HTTPS termination
- Certificate usage with Object Storage
- Practical TLS configuration scenarios

---

## Labs philosophy

Each lab:
- Is **self-contained**
- Uses a **minimal but realistic setup**
- Includes architecture explanations and command references
- Focuses on validating a specific security principle

Labs are intentionally kept minimal to highlight **security mechanics**
rather than operational overhead.

---

## Intended audience

This section is intended for:
- Junior / mid-level cloud and security engineers
- Interview preparation and portfolio demonstration
- Structured self-study of cloud security fundamentals

---

## Status

This section is actively evolving.

New labs, architecture examples, and deeper threat-model-oriented
materials are added incrementally as part of ongoing practice
and research.
The emphasis is on **understanding why a mechanism exists**
and **how to apply it correctly**, not on blindly following recipes.
