terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_address" "master_ip" {
  name   = "cloud-eco-master-ip${var.name_suffix}"
  region = var.region
}

resource "google_compute_address" "worker1_ip" {
  name   = "cloud-eco-worker1-ip${var.name_suffix}"
  region = var.region
}

resource "google_compute_address" "worker2_ip" {
  name   = "cloud-eco-worker2-ip${var.name_suffix}"
  region = var.region
}

resource "google_compute_instance" "master" {
  name         = "cloud-eco-master${var.name_suffix}"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
      size  = 20
    }
  }

  network_interface {
    network = var.network
    access_config {
      nat_ip = google_compute_address.master_ip.address
   }
  }

  tags = ["cloud-eco", "master"]

  metadata_startup_script = file("${path.module}/startup-common.sh")
}

resource "google_compute_instance" "worker1" {
  name         = "cloud-eco-worker1${var.name_suffix}"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
      size  = 20
    }
  }

  network_interface {
    network = var.network
    access_config {
      nat_ip = google_compute_address.worker1_ip.address
    }
  }

  tags = ["cloud-eco", "worker"]

  metadata_startup_script = file("${path.module}/startup-common.sh")
}

resource "google_compute_instance" "worker2" {
  name         = "cloud-eco-worker2${var.name_suffix}"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
      size  = 20
    }
  }

  network_interface {
    network = var.network
    access_config {
      nat_ip = google_compute_address.worker2_ip.address
    }
  }

  tags = ["cloud-eco", "worker"]

  metadata_startup_script = file("${path.module}/startup-common.sh")
}

resource "google_compute_firewall" "allow_k8s_api" {
  name    = "allow-k8s-api${var.name_suffix}"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["6443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["master"]
}

resource "google_compute_firewall" "allow_nodeport_30080" {
  name    = "allow-cloud-eco-nodeport${var.name_suffix}"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["30080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["cloud-eco"]
}

resource "google_compute_firewall" "allow_calico_ipip" {
  name    = "allow-calico-ipip${var.name_suffix}"
  network = var.network

  allow {
    protocol = "4"
  }

  source_ranges = ["10.192.0.0/24"]
  target_tags   = ["cloud-eco"]
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-cloud-eco-ssh${var.name_suffix}"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["cloud-eco"]
}
