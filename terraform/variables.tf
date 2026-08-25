variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "australia-southeast2"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "australia-southeast2-a"
}

variable "network" {
  description = "VPC network name"
  type        = string
  default     = "default"
}

variable "machine_type" {
  description = "VM machine type"
  type        = string
  default     = "e2-custom-4-8192"
}

variable "image" {
  description = "Boot image"
  type        = string
  default     = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
}

variable "ssh_user" {
  description = "SSH username"
  type        = string
  default     = "ubuntu"
}

variable "name_suffix" {
  description = "Suffix added to Terraform-created resource names to avoid clashes"
  type        = string
  default     = "-tf"
}

