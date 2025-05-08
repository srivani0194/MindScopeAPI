terraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "mindscope_key" {
  key_name   = var.key_pair_name
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "mindscope_sg" {
  name        = "mindscope-api-sg"
  description = "Allow SSH and FastAPI traffic"

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["24.23.129.20/32"]
  }

  ingress {
    description = "Allow FastAPI HTTP"
    from_port   = 8000
    to_port     = 8000
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
    Name = "mindscope-api-sg"
  }
}

resource "aws_instance" "mindscope_ec2" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.mindscope_key.key_name
  vpc_security_group_ids      = [aws_security_group.mindscope_sg.id]
  associate_public_ip_address = false

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -aG docker ec2-user
              docker pull ${var.docker_image}
              docker run -d -p 8000:8000 ${var.docker_image}
            EOF

  tags = {
    Name = "mindscope-api-server"
  }
}

resource "aws_eip" "mindscope_ip" {
  instance = aws_instance.mindscope_ec2.id
  vpc      = true
  tags = {
    Name = "mindscope-eip"
  }
}
