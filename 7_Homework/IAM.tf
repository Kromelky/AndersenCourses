
resource "aws_iam_role" "s3_role" {
  name = "s3_readrole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_policy_attachment" "s3-attach" {
  name       = "s3-attachment"
  roles = [aws_iam_role.s3_role.name] 
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_policy_attachment" "s3-full" {
  name       = "s3-full"
  roles = [aws_iam_role.s3_role.name] 
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
