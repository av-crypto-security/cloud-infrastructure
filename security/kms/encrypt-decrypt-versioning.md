# Encrypting and Decrypting Data with KMS Key Versions

This lab demonstrates how symmetric encryption works in a managed
KMS service, including key versioning, rotation and scheduled destruction.

## What is demonstrated
- Creating a symmetric encryption key
- Encrypting and decrypting data using KMS
- Difference between key ID and key version ID
- Key rotation and primary version change
- Scheduled destruction of a key version
- Eventual consistency behavior

## High-level flow
1. A symmetric KMS key is created with automatic rotation enabled
2. Data is encrypted using the current primary key version
3. The data is successfully decrypted
4. The key is rotated, creating a new primary version
5. An old key version is scheduled for destruction
6. Data encrypted with the scheduled-for-destruction version
   cannot be decrypted while the version is inactive
7. Data encrypted with the new primary version remains accessible
8. The scheduled destruction is canceled
9. The old key version becomes active again
10. Data encrypted with the old version can be decrypted successfully

## Encryption and decryption
Data encryption and decryption are performed using the `yc` CLI.
During encryption, KMS returns metadata indicating
which key and key version were used.

## Key rotation
Rotating a key creates a new key version and promotes it
to primary without re-encrypting existing data.

## Scheduled destruction and access loss
When a key version is scheduled for destruction,
it becomes unavailable for decryption.
If the scheduled destruction is canceled,
the key version becomes active again
and previously encrypted data can be decrypted.

## Eventual consistency
Changes to key version state may not be reflected immediately.
This behavior is expected and documented for KMS operations.
