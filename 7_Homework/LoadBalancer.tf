resource "aws_lb" "httplb" {
  name               = "httplb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sg_allow_web.id]
  subnets            = aws_subnet.public.*.id

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.kromelkylblogsbucket.bucket
    prefix  = "httplb"
    enabled = true
  }

}

resource "aws_s3_bucket" "kromelkylblogsbucket" {
  bucket  = "kromelkylblogsbucket"
  acl    = "log-delivery-write"

}