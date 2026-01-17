# Commands: Service Account KMS Rotation

## Create Service Account
```
yc iam service-account create \
  --name security-labs \
  --description "Service account for KMS key rotation"
```

## Grant Permissions to Manage Service Account
```
yc iam service-account add-access-binding <sa-id> \
  --role editor \
  --subject userAccount:<user-id>
```

## Create Authorized Key
```
yc iam key create \
  --service-account-name security-labs \
  --output key.json
```

## Configure CLI Profile
```
yc config profile create key-rotator
yc config set service-account-key key.json
yc config set folder-id <folder-id>
```

## Grant KMS Permissions
```
yc kms symmetric-key add-access-binding \
  --id <key-id> \
  --role kms.admin \
  --subject serviceAccount:<sa-id>
```

## Rotate Key
```
yc config profile activate key-rotator
yc kms symmetric-key rotate --id <key-id>
```
