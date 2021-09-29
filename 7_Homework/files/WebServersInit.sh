#!/bin/bash
sudo yum -y update
sudo yum -y install mc
sudo amazon-linux-extras install nginx1.12
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-backup
sudo mkdir /usr/share/nginx/test
sudo aws s3 cp s3://kromelkyandersen/index.html /usr/share/nginx/test/index.html
sudo aws s3 cp s3://kromelkyandersen/nginx.conf /etc/nginx/nginx.conf 
sudo systemctl start nginx
sudo systemctl enable nginx
sudo chkconfig http on