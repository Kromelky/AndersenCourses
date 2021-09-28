
resource "aws_s3_bucket" "kromelkylblogsbucket" {
  bucket  = "kromelkylblogsbucket"
  acl    = "private"
}

resource "aws_s3_bucket_policy" "kromelkylblogsbucketpolicy" {
  bucket = aws_s3_bucket.kromelkylblogsbucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "S3Admin"
    Statement = [
      {
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::054676820928:root"
        },
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::kromelkylblogsbucket/*"
     },
     {
      "Effect": "Allow",
      "Principal": {
        "Service": "delivery.logs.amazonaws.com"
      },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::kromelkylblogsbucket"
    }
    ]
  })
}