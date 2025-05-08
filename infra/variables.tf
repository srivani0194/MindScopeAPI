variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "key_pair_name" {
  description = "SSH key name"
  type        = string
}

variable "public_key_path" {
  description = "Path to your local public SSH key"
  type        = string
}

variable "ami_id" {
  description = "Amazon Linux 2 AMI ID"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "docker_image" {
  description = "Docker image to run"
  type        = string
}
