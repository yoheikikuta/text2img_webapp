variable "google_cloud_credential_file" {
  type    = string
  default = "./text2image-353214-4ddcbd70f075.json"
}

variable "google_cloud_project" {
  type    = string
  default = "text2image-353214"
}

variable "default_region" {
  type    = string
  default = "asia-northeast1"
}

variable "default_zone" {
  type    = string
  default = "asia-northeast1-a"
}

### For backend configurations
variable "backend_resource_region" {
  type    = string
  default = "asia-east1"
}

variable "backend_machine_type" {
  type    = string
  default = "n1-standard-4"
}

variable "backend_machine_gpu" {
  type    = string
  default = "nvidia-tesla-t4"
}

variable "backend_gcr_image" {
  type    = string
  default = "asia.gcr.io/text2image-353214/backend"
}

### For frontend configurations
variable "frontend_location" {
  type    = string
  default = "asia-northeast1"
}

variable "frontend_gcr_image" {
  type    = string
  default = "asia.gcr.io/text2image-353214/frontend"
}
