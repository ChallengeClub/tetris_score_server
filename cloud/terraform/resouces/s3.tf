resource "aws_s3_bucket" "tetris-training-bucket" {
  bucket_prefix = "tetris-training"
}

resource "aws_s3_bucket_public_access_block" "tetris-training-bucket-public-access-block" {
  bucket                  = aws_s3_bucket.tetris-training-bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# resource "aws_s3_bucket_acl" "tetris-training_bucket_acl" {
#   bucket = aws_s3_bucket.tetris-training-bucket.id
#   acl    = "private"
# }

resource "aws_s3_bucket_versioning" "tetris-training-bucket-versioning" {
  bucket = aws_s3_bucket.tetris-training-bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

