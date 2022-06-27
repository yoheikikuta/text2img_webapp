terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("./text2image-353214-4ddcbd70f075.json")

  project = "text2image-353214"
  region  = "asia-northeast1"
  zone    = "asia-northeast1-a"
}

### backend configurations
resource "google_compute_address" "static" {
  name   = "ipv4-address-for-backend-endpoint"
  region = "asia-east1"
}

resource "google_compute_instance" "default" {
  name         = "backend"
  machine_type = "n1-standard-4"
  zone         = "asia-east1-a"
  tags         = ["http-server"]

  guest_accelerator {
    type  = "nvidia-tesla-t4"
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
  location = "asia-northeast1"

  template {
    spec {
      containers {
        image = "asia.gcr.io/text2image-353214/frontend"
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
