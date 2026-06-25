resource "aws_vpc" "devsecops_vpc" {

  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.project_name}-VPC"
  }
}
# Public Subnet
resource "aws_subnet" "public_subnet" {

  vpc_id                  = aws_vpc.devsecops_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-Public-Subnet"
  }
}
# Internet Gateway
resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.devsecops_vpc.id

  tags = {
    Name = "${var.project_name}-IGW"
  }
}
# Public Route Table
resource "aws_route_table" "public_rt" {

  vpc_id = aws_vpc.devsecops_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.project_name}-Public-RT"
  }
}
# Route Table Association
resource "aws_route_table_association" "public_assoc" {

  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}
