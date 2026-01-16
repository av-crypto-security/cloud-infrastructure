resource "yandex_mdb_postgresql_cluster" "this" {
  name        = "postgres-1"
  environment = "PRESTABLE"
  network_id  = var.network_id

  config {
    version = 14

    resources {
      resource_preset_id = "s2.micro"
      disk_type_id       = "network-ssd"
      disk_size          = 16
    }

    postgresql_config = {
      max_connections                   = 395
      enable_parallel_hash              = true
      vacuum_cleanup_index_scale_factor = 0.2
      autovacuum_vacuum_scale_factor    = 0.34
      default_transaction_isolation     = "TRANSACTION_ISOLATION_READ_COMMITTED"
      shared_preload_libraries          = "SHARED_PRELOAD_LIBRARIES_AUTO_EXPLAIN,SHARED_PRELOAD_LIBRARIES_PG_HINT_PLAN"
    }
  }

  database {
    name  = "postgres-1"
    owner = var.postgres_user
  }

  user {
    name     = var.postgres_user
    password = var.postgres_password

    permission {
      database_name = "postgres-1"
    }
  }

  host {
    zone      = var.zone
    subnet_id = var.subnet_id
  }
}