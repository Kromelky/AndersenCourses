# Build WebServers 
provider "aws" {
    region = var.aws_region
}


resource "aws_instance" "webserver" {
    count = var.instance_count
    ami = "ami-07df274a488ca9195" # Amazon Linux AMI
    instance_type = "t2.micro"
    key_name = aws_key_pair.generated_key.key_name
    subnet_id  = aws_subnet.public[count.index].id
    associate_public_ip_address = true
    iam_instance_profile = aws_iam_instance_profile.ec3_profile.name
    vpc_security_group_ids = [aws_security_group.sg_allow_web.id, aws_security_group.sg_allow_ssh.id]
    user_data = <<EOF
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
EOF
  
  tags = {
      Name = format("Web Server %d", count.index + 1 )
  }
}

resource "aws_iam_instance_profile" "ec3_profile" {
  name = "ec3_profile"
  role = aws_iam_role.s3_role.name
}




