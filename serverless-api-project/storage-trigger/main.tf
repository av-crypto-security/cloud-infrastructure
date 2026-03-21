terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = var.oauth_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
}

resource "yandex_storage_bucket" "bucket" {
  bucket     = var.bucket_name
  access_key = var.access_key
  secret_key = var.secret_key
}