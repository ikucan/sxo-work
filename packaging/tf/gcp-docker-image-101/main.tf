
provider "google" {
  credentials = file(var.credentials_file)
  project = var.project
  region  = var.region
  zone    = var.zone
}

locals {
  instance_name = format("%s-%s", var.instance_name, substr(md5(module.gce-container.container.image), 0, 8))
}


module "gce-container" {
  // source = "/workstem/gcp/terraform-google-container-vm/"
  source = "terraform-google-modules/container-vm/google"
  version = "~> 2.0"
  
  container = {
    image = "iztokkucan/pybuild:0.0.1"

    env = [
      {
        name  = "TEST_VAR"
        value = "********************* Hello World! *********************"
      },
    ]

    command = [
      "/bin/bash",
      "-c",
      "echo $TEST_VAR"
    ]

    args = [
    ]

    volumeMounts = [
      {
        mountPath = "/cache"
        name      = "tempfs-0"
        readOnly  = false
      },
    ]
  }

  volumes = [
    {
      name = "tempfs-0"

      emptyDir = {
        medium = "Memory"
      }
    },
  ]

  restart_policy = "Always"
}

//        value = "$$$$$$$$$$$$$$$$$$$$$ Hello World! $$$$$$$$$$$$$$$$$$$$$"


resource "google_compute_instance" "vm" {
  project      = var.project_id
  name         = local.instance_name
  machine_type = "n1-standard-1"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  network_interface {
    subnetwork_project = var.subnetwork_project
    subnetwork         = var.subnetwork
    access_config {}
  }

  tags = ["container-vm-example"]

  metadata = {
    gce-container-declaration = module.gce-container.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }
  
  labels = {
    container-vm = module.gce-container.vm_container_label
  }

  service_account {
    email = var.client_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}