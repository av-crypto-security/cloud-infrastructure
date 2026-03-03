# Immutable Archive — CLI Commands

## 1. Create Service Account
```bash
yc iam service-account create --name archive-sa

yc resource-manager folder add-access-binding <folder-id> \
  --role storage.admin \
  --subject serviceAccount:<service-account-id>

yc iam access-key create --service-account-name archive-sa
```
---

## 2. Create Private Bucket
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 mb s3://immutable-archive-prod
```
---

## 3. Upload Object
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 cp file01.bin s3://immutable-archive-prod/
```
---

## 4. List Objects
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 ls s3://immutable-archive-prod/
```
---

## 5. Add or Replace Metadata
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api copy-object \
  --bucket immutable-archive-prod \
  --copy-source immutable-archive-prod/file01.bin \
  --key file01.bin \
  --metadata-directive REPLACE \
  --metadata object_id=001,retention_status=active
```
---

## 6. Inspect Object Metadata
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api head-object \
  --bucket immutable-archive-prod \
  --key file01.bin
```
---

## 7. Enable Versioning (Recommended)
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api put-bucket-versioning \
  --bucket immutable-archive-prod \
  --versioning-configuration Status=Enabled
```
---

## 8. Apply Lifecycle Policy (30 Days → Cold)

Create `lifecycle.json`:
```json
{
  "Rules": [
    {
      "ID": "transition-to-cold",
      "Filter": { "Prefix": "" },
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "COLD"
        }
      ]
    }
  ]
}
```
Apply:
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api put-bucket-lifecycle-configuration \
  --bucket immutable-archive-prod \
  --lifecycle-configuration file://lifecycle.json
```
---

## 9. Generate Presigned URL (Temporary Access)
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 presign s3://immutable-archive-prod/file01.bin \
  --expires-in 3600
```
---

## 10. Block Public Access (Best Practice)
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api put-public-access-block \
  --bucket immutable-archive-prod \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
