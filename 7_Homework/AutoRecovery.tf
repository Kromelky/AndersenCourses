resource "aws_cloudwatch_metric_alarm" "nlb_healthyhosts" {
  alarm_name          = "HealthyWebServers"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Average"
  threshold           =  var.instance_count
  alarm_description   = "Number of healthy nodes in Target Group"
  actions_enabled     = "true"
  alarm_actions       = [aws_sns_topic.nlb-failedhosts.arn]
  dimensions = {
    TargetGroup  = aws_lb_target_group.web_tg.arn_suffix
    LoadBalancer = aws_lb.httplb.arn_suffix
  }
}

resource "aws_lb_target_group" "httptg" {
  name     = "httptg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_sns_topic" "nlb-failedhosts" {
  name = "nlb-failedhosts"
}


resource "aws_cloudwatch_metric_alarm" "autorecovery" {
  count               =  var.instance_count
  alarm_name          = "Instance state alarm ${aws_instance.webserver[count.index].tags["Name"]}"
  namespace           = "AWS/EC2"
  evaluation_periods  = "2"
  period              = "60"
  alarm_description   = "This metric auto recovers EC2 instances"
  alarm_actions       = ["arn:aws:automate:${var.aws_region}:ec2:recover"]
  statistic           = "Minimum"
  comparison_operator = "GreaterThanThreshold"
  threshold           = "0"
  metric_name         = "StatusCheckFailed_System"
  dimensions = {
      InstanceId = "${aws_instance.webserver[count.index].id}"
  }
}
