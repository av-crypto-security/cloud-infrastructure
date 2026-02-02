# Packer — Golden Image (Ubuntu + NGINX)

This directory contains a Packer template for building a custom
Ubuntu 22.04 image with NGINX installed.

## Purpose

The resulting image is used by Terraform to provision virtual machines,
following immutable infrastructure principles.

## Requirements

- Packer >= 1.9
- Yandex Cloud account
- Service Account credentials exported via environment variables

## Output

- Custom VM image in Yandex Cloud:
  - image_family: ubuntu-nginx
  - image_name: ubuntu-nginx
