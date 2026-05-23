resource "aws_s3_bucket" "bucket" {
  bucket = "nimbuskart-dev-bucket"
}

resource "aws_ebs_volume" "ebs" {
  availability_zone = "us-east-1a"
  size              = 8

  tags = {
    Name        = "dev-ebs"
    Project     = "NimbusKart"
    Environment = "dev"
    Owner       = "Nandini"
    ManagedBy   = "terraform"
  }
}