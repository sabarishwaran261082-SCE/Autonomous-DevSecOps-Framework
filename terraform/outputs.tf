output "security_group_id" {
  value = aws_security_group.devsecops_sg.id
}
output "instance_id" {
  value = aws_instance.devsecops_server.id
}

output "public_ip" {
  value = aws_instance.devsecops_server.public_ip
}

output "public_dns" {
  value = aws_instance.devsecops_server.public_dns
}

output "elastic_ip" {
  description = "Elastic IP Address"

  value = aws_eip.devsecops_eip.public_ip
}