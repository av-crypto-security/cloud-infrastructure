packer {
  required_plugins {
    yandex = {
      source  = "github.com/hashicorp/yandex"
      version = "~> 1"
    }
  }
}

source "yandex" "ubuntu_nginx" {
  folder_id = var.folder_id
  zone      = var.zone
  subnet_id = var.subnet_id

  source_image_family = "ubuntu-2204-lts"

  image_name        = "ubuntu-nginx"
  image_family      = "ubuntu-nginx"
  image_description = "Ubuntu 22.04 with NGINX installed"

  ssh_username = "ubuntu"
  use_ipv4_nat = true
  disk_type    = "network-ssd"
}

build {
  sources = ["source.yandex.ubuntu_nginx"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y nginx",
      "sudo systemctl enable nginx.service"
    ]
  }
}