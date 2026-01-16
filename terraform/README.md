# Yandex Cloud Infrastructure (Terraform)

This repository contains Terraform configurations for deploying
basic infrastructure in **Yandex Cloud**.

## Components

The following resources are provisioned:

- Virtual Private Cloud (VPC)
- Subnet
- Compute Instance (VM)
- Managed PostgreSQL cluster (MDB)
- Public SSH access
- NAT for outbound internet access

## Prerequisites

- Terraform >= 1.4
- Yandex Cloud account
- Yandex Cloud service account (recommended) or OAuth token
- Configured YC CLI (optional)

## Structure
```
terraform/
├── provider.tf # Provider configuration
├── variables.tf # Variable declarations
├── main.tf # Infrastructure assembling
├── outputs.tf # Output values
├── terraform.tfvars.example # Example variables file
│
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── vm/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── postgresql/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
```

## Usage

1. Clone the repository
2. Create a variables file:
```
cp terraform.tfvars.example terraform.tfvars
```
3. Place service account key file (sa-key.json) locally (not committed)
4. Fill in real values in terraform.tfvars
5. Initialize Terraform:
```
terraform init
```
6. Preview changes:
```
terraform plan
```
7. Apply infrastructure:
```
terraform apply
```

## Notes

- terraform.tfvars must not be committed
- sa-key.json must not be committed
- All sensitive values are marked as sensitive
- Configuration is adapted from public Yandex Cloud Terraform examples

## Disclaimer

This repository is intended for educational and demonstration purposes.
