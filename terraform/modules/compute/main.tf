resource "aws_security_group" "sg" {
  name   = "dev-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "dev-sg"
    Project     = "NimbusKart"
    Environment = "dev"
    Owner       = "Nandini"
    ManagedBy   = "terraform"
  }
}

# Temporarily disabled due to LocalStack EC2 limitations

 resource "aws_instance" "app" {
   ami           = "ami-12345678"
   instance_type = "t2.micro"

   subnet_id              = var.subnet_id
   vpc_security_group_ids = [aws_security_group.sg.id]

   tags = {
     Name        = "dev-instance"
     Project     = "NimbusKart"
     Environment = "dev"
     Owner       = "Nandini"
     ManagedBy   = "terraform"
   }
 }