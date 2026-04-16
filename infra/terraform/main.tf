terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  # local backend for the moment, switching to gcp later
  backend "local" {}
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("~/.gcp/skillgap-493211-191f7f049595.json")
}

resource "google_project_service" "artifact_registry" {
  service = "artifactregistry.googleapis.com"
}
