resource "aws_launch_configuration" "web_config" {
  name          = "WebServer"
  image_id      = data.aws_ami.latest_amazon_linux.id
  instance_type = "t3.micro"
  key_name = aws_key_pair.generated_key.key_name
  associate_public_ip_address = true
  iam_instance_profile = aws_iam_instance_profile.ec3_profile.name
  security_groups = [aws_security_group.sg_allow_web.id, aws_security_group.sg_allow_ssh.id]
  user_data = file("/files/WebServersInit.sh")

  lifecycle {
    create_before_destroy = true
  }

}