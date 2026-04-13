resource "google_storage_bucket" "bronze" {
  name                        = "skillgap-bronze-${var.environment}"
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket" "silver" {
  name                        = "skillgap-silver-${var.environment}"
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "artifacts" {
  name                        = "skillgap-artifacts-${var.environment}"
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
