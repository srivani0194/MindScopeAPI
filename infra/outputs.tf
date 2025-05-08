output "ec2_public_ip" {
  description = "Elastic Public IP of the EC2 instance"
  value       = aws_eip.mindscope_ip.public_ip
}
