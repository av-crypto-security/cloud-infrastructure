# IPSec Site-to-Site VPN with strongSwan

This lab demonstrates a site-to-site IPSec VPN tunnel
between Yandex Cloud and an external network using strongSwan.

## Why this matters
- Secure connectivity between cloud and on-prem environments
- Encrypted traffic over untrusted networks
- Common enterprise hybrid-cloud scenario

## Architecture
Cloud VPC ↔ IPSec Gateway ↔ Internet ↔ IPSec Gateway ↔ On-prem Network

## What is demonstrated
- IPSec tunnel establishment (IKEv2)
- Pre-shared key authentication
- Static routing via VPC route tables
- Network isolation behind VPN gateways

## Scope and limitations
- This is a minimal functional implementation
- No BGP, no HA, no failover
- Intended for learning and validation, not production use
