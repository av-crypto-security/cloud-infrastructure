module "vpc" {
  source = "./modules/vpc"
  zone   = var.zone
}

module "vm" {
  source              = "./modules/vm"
  zone                = var.zone
  subnet_id           = module.vpc.subnet_id
  image_id            = var.image_id
  ssh_public_key_path = var.ssh_public_key_path
}

module "postgres" {
  source            = "./modules/postgresql"
  zone              = var.zone
  network_id        = module.vpc.network_id
  subnet_id         = module.vpc.subnet_id
  postgres_user     = var.postgres_user
  postgres_password = var.postgres_password
}
