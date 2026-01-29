# Key Management Service (KMS)

This section demonstrates practical usage of a managed
Key Management Service for data encryption in cloud environments.

## Why KMS matters
KMS allows centralized control over encryption keys,
including rotation, access control and auditability.

## Key vs Key Version
A KMS key is a logical entity that can have multiple versions.
Each encryption operation uses a specific key version.

## Key rotation
Key rotation creates a new primary version of a key
without re-encrypting existing data.

## Scheduled destruction
Key versions can be scheduled for destruction to limit
the lifetime of cryptographic material.

## Eventual consistency
Some KMS operations are eventually consistent,
which means state changes may not be visible immediately.
