output "fqdn" {
  value = yandex_mdb_postgresql_cluster.this.host[0].fqdn
}

output "database" {
  value = yandex_mdb_postgresql_cluster.this.database[0].name
}