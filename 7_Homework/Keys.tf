resource "tls_private_key" "RSA" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = var.ami_key_pair_name
  public_key = tls_private_key.RSA.public_key_openssh
}

resource "local_file" "pem_file" {
  filename = pathexpand("~/.ssh/${aws_key_pair.generated_key.key_name}.pem")
  file_permission = "600"
  directory_permission = "700"
  sensitive_content = tls_private_key.RSA.private_key_pem
}