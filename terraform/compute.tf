# Get latest Amazon Linux 2023 AMI
data "aws_ami" "amazon_linux" {

  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
resource "aws_instance" "devsecops_server" {

  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.devsecops_sg.id]
  key_name               = var.key_name

  associate_public_ip_address = true

  root_block_device {
    volume_size = 10
    volume_type = "gp3"
  }

  tags = {
    Name = "${var.project_name}-EC2"
  }
}