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
- OAuth token or service account
- Configured YC CLI (optional)

## Structure
```
terraform/
├── provider.tf # Provider and backend configuration
├── variables.tf # Variable declarations
├── main.tf # Infrastructure resources
├── outputs.tf # Output values
├── terraform.tfvars.example # Example variables file
```

## Usage

1. Clone the repository
2. Create a variables file:
```
cp terraform.tfvars.example terraform.tfvars
```
3. Fill in real values in terraform.tfvars
4. Initialize Terraform:
```
terraform init
```
5. Preview changes:
```
terraform plan
```
6. Apply infrastructure:
```
terraform apply
```

## Notes

terraform.tfvars must not be committed
All sensitive values are marked as sensitive
Configuration is adapted and composed from publicly available
Yandex Cloud Terraform examples


## Disclaimer

This repository is intended for educational and demonstration purposes.
