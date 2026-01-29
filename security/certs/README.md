# Certificates and HTTPS in Cloud

This section demonstrates how TLS certificates are issued
and used in a managed cloud environment.

## Why HTTPS matters
TLS protects data in transit and prevents man-in-the-middle attacks.

## Managed certificates vs self-signed
Managed certificates automate issuance, renewal and revocation,
reducing operational risks and operational overhead.

## Domain validation
Certificate issuance requires proving domain ownership,
most commonly via DNS-based challenges.

## Common mistakes
- Expecting HTTPS to work before DNS propagation is complete
- Mixing object storage website endpoints with HTTPS endpoints
- Using self-signed certificates in production environments
