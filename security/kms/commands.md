# KMS Commands (Essential)
Minimal set of CLI commands required to work with
symmetric keys, key versions and rotation in Yandex Cloud KMS.

---
## Prerequisites
- Yandex Cloud CLI (`yc`) is installed and configured
- A symmetric KMS key has been created
- The key ID is known (`<KEY_ID>`)
---

## Encrypt data
```bash
yc kms symmetric-crypto encrypt \
  --id <KEY_ID> \
  --plaintext-file plain.txt \
  --ciphertext-file encrypted.txt
```

## Decrypt data
```bash
yc kms symmetric-crypto decrypt \
  --id <KEY_ID> \
  --ciphertext-file encrypted.txt \
  --plaintext-file decrypted.txt
```

## Rotate key
```bash
yc kms symmetric-key rotate <KEY_ID>
```

## Encrypt after rotation
```bash
yc kms symmetric-crypto encrypt \
  --id <KEY_ID> \
  --plaintext-file plain.txt \
  --ciphertext-file encrypted_with_new_key.txt
```
