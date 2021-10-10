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
    AutoScalingGroupName = aws_autoscaling_group.web_asg.name 
    LoadBalancer = aws_elb.httplb.name
  }
}


resource "aws_sns_topic" "nlb-failedhosts" {
  name = "nlb-failedhosts"
}


resource "aws_cloudwatch_metric_alarm" "autorecovery" {
  count               =  var.instance_count
  alarm_name          = "Instance state alarm "
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
      AutoScalingGroupName = aws_autoscaling_group.web_asg.name
  }
}
