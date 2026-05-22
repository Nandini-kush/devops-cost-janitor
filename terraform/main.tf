resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_subnet" "public_1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name        = "public-subnet-1"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_subnet" "public_2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"

  tags = {
    Name        = "public-subnet-2"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_instance" "app_server_1" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_1.id

  tags = {
    Name        = "app-server-1"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_instance" "app_server_2" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_2.id

  tags = {
    Name        = "app-server-2"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "nimbuskart-logs-bucket"

  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}

resource "aws_ebs_volume" "orphan_volume" {
  availability_zone = "us-east-1a"
  size              = 8

  tags = {
    Name        = "orphan-ebs"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
  }
}terraform fmt