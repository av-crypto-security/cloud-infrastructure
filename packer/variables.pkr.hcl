variable "folder_id" {
  type        = string
  description = "Yandex Cloud folder ID"
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID used to build the image"
}

variable "zone" {
  type        = string
  default     = "ru-central1-a"
}