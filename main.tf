terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("${var.google_cloud_credential_file}")

  project = var.google_cloud_project
  region  = var.default_region
  zone    = var.default_zone
}

### backend configurations
resource "google_compute_address" "static" {
  name   = "ipv4-address-for-backend-endpoint"
  region = var.backend_resource_region
}

resource "google_compute_instance" "default" {
  name         = "backend"
  machine_type = var.backend_machine_type
  zone         = "${var.backend_resource_region}-a"
  tags         = ["http-server"]

  guest_accelerator {
    type  = var.backend_machine_gpu
    count = 1
  }
  scheduling {
    on_host_maintenance = "TERMINATE"
  }

  boot_disk {
    initialize_params {
      image = "deeplearning-platform-release/common-cu113-v20220526-debian-10"
      size  = 50
    }
  }

  network_interface {
    network = "default"

    access_config {
      nat_ip = google_compute_address.static.address
    }
  }

  metadata = {
    install-nvidia-driver = "True"
  }

  metadata_startup_script = file("./service_setup.sh")
}

### frontend configurations
resource "google_cloud_run_service" "default" {
  name     = "frontend"
  location = var.frontend_location

  template {
    spec {
      containers {
        image = var.frontend_gcr_image
        env {
          name  = "BACKEND_URL"
          value = "http://${google_compute_address.static.address}"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.default.location
  project  = google_cloud_run_service.default.project
  service  = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "cloud_run_url" {
  value = google_cloud_run_service.default.status[0].url
}
