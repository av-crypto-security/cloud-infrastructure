resource "yandex_vpc_network" "this" {
  name = "from-terraform-network"
}

resource "yandex_vpc_subnet" "this" {
  name           = "from-terraform-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.this.id
  v4_cidr_blocks = ["10.2.0.0/16"]
}