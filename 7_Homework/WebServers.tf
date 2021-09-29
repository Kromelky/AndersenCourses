# Build WebServers 

resource "aws_instance" "webserver" {
    count = var.instance_count
    ami = "ami-07df274a488ca9195" # Amazon Linux AMI
    instance_type = "t2.micro"
    key_name = aws_key_pair.generated_key.key_name
    subnet_id  = aws_subnet.public[count.index].id
    associate_public_ip_address = true
    iam_instance_profile = aws_iam_instance_profile.ec3_profile.name
    vpc_security_group_ids = [aws_security_group.sg_allow_web.id, aws_security_group.sg_allow_ssh.id]
    user_data = file("/files/WebServersInit.sh")
  
  tags = {
      Name = "Web Server ${ count.index + 1}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_instance_profile" "ec3_profile" {
  name = "ec3_profile"
  role = aws_iam_role.s3_role.name
}




