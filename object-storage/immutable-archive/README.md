# Immutable Archive Storage Design

## 1. Objective

Design an object storage architecture for long-term immutable file retention.

Requirements:

- Unstructured data
- Objects must not be modified
- Long-term durable storage
- Rare access pattern
- Controlled temporary external access
- Cost optimization

---

## 2. Architecture Overview

### Storage Layer

- Private S3-compatible bucket
- IAM-restricted access
- Standard storage class → automatic transition to Cold
- Lifecycle policy after 30 days
- Optional bucket size limit

---

### Access Model

- Access via service accounts only
- No public access
- Temporary access via presigned URLs
- HTTPS-only data transfer

---

### Metadata Strategy

Custom object metadata used for classification:

- object_id
- retention_status
- created_at
- classification_tag

Benefits:

- Lightweight object classification
- No external database required for basic filtering
- Metadata retrievable via head-object API

---

## 3. Immutability Model

Objects:

- Are not edited in-place
- Metadata updates performed via object rewrite
- Deletion restricted via IAM policy

Optional hardening:

- Bucket versioning
- Object Lock (WORM)
- Retention policies

---

## 4. Cost Optimization

- Automatic lifecycle transition → Cold storage
- No automatic expiration
- Storage class aligned with rare access workload

---

## 5. Security Controls

- Principle of least privilege
- Dedicated service accounts
- Static access keys stored securely
- Public access block enabled
- No anonymous access

---

## 6. Result

Architecture provides:

- Durable immutable storage
- Controlled external sharing
- Reduced storage cost over time
- Minimal attack surface
- Production-ready design
