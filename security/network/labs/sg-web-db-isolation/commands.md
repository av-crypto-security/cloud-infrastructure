# Commands Reference — Security Groups Hands-on (Yandex Cloud)

This document contains the exact sequence of commands used to implement
and validate Security Groups behavior in Yandex Cloud.

All actions were performed from a dedicated administrative VM
using a Service Account and the Yandex Cloud CLI.

---

## 0. Service Account (pre-created)

A Service Account was created once via Web Console and granted the following roles on the folder:

- vpc.admin
- compute.admin
- iam.serviceAccounts.user

This permission set is sufficient for managing VPC, Security Groups,
and Compute Instances in a lab environment without excessive privileges.

---

## 1. Administrative VM (jump host)

The administrative VM is used as a controlled execution environment
for all infrastructure operations.

**Parameters:**
- OS: Ubuntu 22.04 LTS
- Public IP: enabled
- Service Account: attached
- Security Group: default

## 2. Yandex Cloud CLI installation

```
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
source ~/.bashrc

yc version
```

## 3. CLI initialization (Service Account context)

```
yc config profile create sg-lab
yc config profile activate sg-lab
yc config set folder-id <FOLDER_ID>
yc config list
yc resource-manager folder list
```

## 4. Network and subnet

```
yc vpc network create --name sg-net
yc vpc subnet create \
  --name sg-subnet \
  --network-name sg-net \
  --zone ru-central1-a \
  --range 10.10.0.0/24
```

## 5. Security Groups: Web tier (sg-web) and Database tier (sg-db)

```
yc vpc security-group create \
  --name sg-web \
  --network-name sg-net \
  --description "SG for web VM"
yc vpc security-group list

yc vpc security-group update-rules <sg-web-id> \
  --add-rule "direction=ingress,protocol=tcp,port=80,v4-cidrs=[0.0.0.0/0]"

yc vpc security-group update-rules <sg-web-id> \
  --add-rule "direction=ingress,protocol=tcp,port=22,v4-cidrs=[<your-ip>/32]"

yc vpc security-group create \
  --name sg-db \
  --network-name sg-net \
  --description "SG for DB"

yc vpc security-group update-rules <sg-web-id> \
  --add-rule "direction=egress,protocol=tcp,port=3306,security-group-id=<sg-db-id>"

yc vpc security-group update-rules <sg-db-id> \
  --add-rule "direction=ingress,protocol=tcp,port=3306,security-group-id=<sg-web-id>"


yc vpc security-group get sg-web
yc vpc security-group get sg-db
```

## 6. Web VM and DB creation examples

```
yc compute instance create \
  --name web-vm \
  --zone ru-central1-a \
  --network-interface subnet-name=sg-subnet,security-group-ids=<sg-web-id>,nat-ip-version=ipv4 \
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts \
  --ssh-key ~/.ssh/id_rsa.pub

yc managed-mysql cluster create \
  --name="my-mysql" \
  --mysql-version 8.0 \
  --environment=production \
  --network-name= sg-net\
  --security-group-ids enp6saqnq4ie******** \
  --host zone-id=ru-central1-a,subnet-id=b0rcctk2rvtr******** \
  --resource-preset s2.micro \
  --disk-type network-ssd \
  --disk-size 20 \
  --user name=<username>,password="<userpassword>" \
  --database name=<dbname> \
  --deletion-protection
```

## 7. Connectivity validation (Security Groups)

```
sudo apt install -y netcat-openbsd
```
### Test from admin VM (should be blocked), test from web VM (should succeed)
```bash
nc -zv <db-fqdn-or-ip> 3306
```
