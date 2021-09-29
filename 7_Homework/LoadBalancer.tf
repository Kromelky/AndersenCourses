resource "aws_lb" "httplb" {
  name               = "httplb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sg_allow_web.id]
  subnets            = aws_subnet.public.*.id

  access_logs {
    bucket  = aws_s3_bucket.kromelkylblogsbucket.bucket
    prefix  = "httplb"
    enabled = true
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_lb_target_group" "web_tg" {
  name     = "webserver-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "webattach" {
  count = var.instance_count
  target_group_arn = aws_lb_target_group.web_tg.arn
  target_id        = aws_instance.webserver[count.index].id
  port             = 80
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.httplb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}
