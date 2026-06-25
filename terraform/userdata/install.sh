#!/bin/bash

# Log all output
exec > >(tee /var/log/user-data.log) 2>&1

echo "===== Starting DevSecOps Bootstrap ====="

# Update system
dnf update -y

# Install Git
dnf install -y git

# Install Docker
dnf install -y docker

# Enable Docker
systemctl enable docker
systemctl start docker

# Wait for Docker
sleep 10

# Clone Repository
cd /home/ec2-user

git clone https://github.com/sabarishwaran261082-SCE/Autonomous-DevSecOps-Framework.git

cd Autonomous-DevSecOps-Framework/app

# Build Docker Image
docker build -t autonomous-devsecops .

# Run Container
docker run -d \
  --name autonomous-devsecops \
  -p 5000:5000 \
  --restart unless-stopped \
  autonomous-devsecops

echo "===== Deployment Completed Successfully ====="