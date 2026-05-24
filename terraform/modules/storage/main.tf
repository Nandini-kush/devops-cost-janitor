resource "aws_s3_bucket" "bucket" {
  bucket = "nimbuskart-dev-bucket"

  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}



resource "aws_ebs_volume" "ebs" {
  availability_zone = "us-east-1a"
  size              = 8

  tags = {
    Name        = "dev-ebs"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}