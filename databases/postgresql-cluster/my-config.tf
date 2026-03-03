terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  service_account_key_file = var.sa_key_file
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
}

# -----------------------
# Network
# -----------------------

resource "yandex_vpc_network" "pg_network" {
  name = "pg-network"
}

resource "yandex_vpc_subnet" "pg_subnet_a" {
  name           = "pg-subnet-a"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.pg_network.id
  v4_cidr_blocks = ["10.10.1.0/24"]
}

resource "yandex_vpc_subnet" "pg_subnet_b" {
  name           = "pg-subnet-b"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.pg_network.id
  v4_cidr_blocks = ["10.10.2.0/24"]
}

resource "yandex_vpc_subnet" "pg_subnet_d" {
  name           = "pg-subnet-d"
  zone           = "ru-central1-d"
  network_id     = yandex_vpc_network.pg_network.id
  v4_cidr_blocks = ["10.10.3.0/24"]
}

# -----------------------
# PostgreSQL Cluster
# -----------------------

resource "yandex_mdb_postgresql_cluster" "pg_cluster" {
  name        = "pg-ha-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.pg_network.id
  deletion_protection = true

  config {
    version = "15"

    resources {
      resource_preset_id = "s3-c2-m8"
      disk_type_id       = "network-ssd"
      disk_size          = 50
    }

    backup_window_start {
      hours   = 2
      minutes = 0
    }
  }

  host {
    zone      = "ru-central1-a"
    subnet_id = yandex_vpc_subnet.pg_subnet_a.id
  }

  host {
    zone      = "ru-central1-b"
    subnet_id = yandex_vpc_subnet.pg_subnet_b.id
  }

  host {
    zone      = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.pg_subnet_d.id
  }
}

# -----------------------
# Database
# -----------------------

resource "yandex_mdb_postgresql_database" "app_db" {
  cluster_id = yandex_mdb_postgresql_cluster.pg_cluster.id
  name       = "appdb"
  owner      = yandex_mdb_postgresql_user.app_user.name
}

# -----------------------
# User
# -----------------------

resource "yandex_mdb_postgresql_user" "app_user" {
  cluster_id = yandex_mdb_postgresql_cluster.pg_cluster.id
  name       = "appuser"
  password   = var.postgres_password
}