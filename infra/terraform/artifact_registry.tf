resource "google_artifact_registry_repository" "skillgap" {
  provider = google
  location = var.region
  repository_id = "skillgap"
  format = "DOCKER"
}
