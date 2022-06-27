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

  #   service_account {
  #     # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
  #     email  = google_service_account.default.email
  #     scopes = ["cloud-platform"]
  #   }
}
