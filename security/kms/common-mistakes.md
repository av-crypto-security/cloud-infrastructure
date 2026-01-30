
# Common KMS Mistakes
Typical mistakes engineers make when working with
Key Management Services for the first time.
---

## Confusing key ID and key version ID
A key is a logical container.
Encryption always uses a **specific key version**.
Mistake:
- assuming the key ID uniquely defines cryptographic material
---

## Expecting rotation to re-encrypt data
Key rotation:
- creates a new version
- does NOT re-encrypt existing ciphertext
Mistake:
- rotating a key and assuming old data is protected by the new version
---

## Treating scheduled destruction as immediate deletion
Scheduled destruction:
- blocks cryptographic operations
- does NOT instantly destroy key material

Mistake:
- assuming data is permanently lost immediately
---

## Ignoring eventual consistency
Some KMS state changes are delayed.
Mistake:
- debugging “broken decryption” while propagation is still in progress
---

## Using KMS as bulk encryption tool
KMS is designed for:
- small payloads
- envelope encryption
Mistake:
- trying to encrypt large files directly with KMS
