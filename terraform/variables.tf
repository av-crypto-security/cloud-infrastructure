variable "sa_key_file" {
  type        = string
  description = "Path to service account key JSON"
  sensitive = true
}

variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "image_id" {
  type = string
}

variable "ssh_public_key_path" {
  type = string
}

variable "postgres_user" {
  type = string
  description = "PostgreSQL database user"
}

variable "postgres_password" {
  type = string
  sensitive = true
}

