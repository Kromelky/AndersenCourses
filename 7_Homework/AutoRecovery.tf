resource "aws_cloudwatch_metric_alarm" "nlb_healthyhosts" {
  alarm_name          = "alarmname"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/NetworkELB"
  period              = "60"
  statistic           = "Average"
  threshold           =  var.instance_count
  alarm_description   = "Number of healthy nodes in Target Group"
  actions_enabled     = "true"
  alarm_actions       = [aws_sns_topic.nlb_failedhosts.arn]
  ok_actions          = [aws_sns_topic.nlb_healthyhosts.arn]
  dimensions = {
    TargetGroup  = aws_lb_target_group.httptg.arn_suffix
    LoadBalancer = aws_lb.httplb.arn_suffix
  }
}

resource "aws_lb_target_group" "httptg" {
  name     = "httptg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_sns_topic" "nlb_healthyhosts" {
  name = "user-updates-topic"
}

resource "aws_sns_topic" "nlb_failedhosts" {
  name = "user-updates-topic"
}