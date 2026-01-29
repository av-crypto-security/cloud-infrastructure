# HTTPS for Object Storage using Certificate Manager

This lab demonstrates how to expose a static website
hosted in Object Storage over HTTPS using a managed TLS certificate.

## Architecture overview
User → DNS → Object Storage (HTTPS endpoint)
                ↘
          Certificate Manager → Let's Encrypt

## What is demonstrated
- Domain ownership validation via DNS
- Automated certificate issuance (ACME)
- HTTPS configuration for Object Storage

## Key steps (high-level)
1. Register a domain and configure DNS records
2. Create a public Object Storage bucket configured for static website hosting
3. Request a managed TLS certificate via Certificate Manager
4. Complete DNS-based domain ownership validation
5. Attach the issued certificate to the Object Storage HTTPS endpoint

## Result
After DNS propagation and certificate issuance,
the static website is accessible over HTTPS
with a valid trusted certificate.
