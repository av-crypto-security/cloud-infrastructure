# Static Website — CLI Commands

## 1. Create Bucket
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 mb s3://www.example.com
```
---

## 2. Enable Public Read Access
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api put-bucket-policy \
  --bucket www.example.com \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::www.example.com/*"
      }
    ]
  }'
```
---

## 3. Upload Website Files
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3 sync ./site s3://www.example.com/
```
---

## 4. Enable Website Hosting
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api put-bucket-website \
  --bucket www.example.com \
  --website-configuration '{
    "IndexDocument": { "Suffix": "index.html" }
  }'
```
---

## 5. Verify Configuration
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api get-bucket-website \
  --bucket www.example.com
```
---

## 6. Validate Bucket Policy
```bash
aws --endpoint-url=https://storage.yandexcloud.net \
  s3api get-bucket-policy \
  --bucket www.example.com
```
