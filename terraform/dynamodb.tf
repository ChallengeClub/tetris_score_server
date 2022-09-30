resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Id"
  range_key      = "RegisteredAt"

  attribute {
    name = "Id"
    type = "S"
  }

  attribute {
    name = "RegisteredAt"
    type = "N"
  }

  attribute {
    name = "UserName"
    type = "S"
  }

  attribute {
    name = "Level"
    type = "S"
  }

  attribute {
    name = "AverageScore"
    type = "N"
  }

  global_secondary_index {
    name            = "UserNameIndex"
    hash_key        = "UserName"
    range_key       = "RegisteredAt"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "KEYS_ONLY"
  }

  global_secondary_index {
    name            = "LevelScoreIndex"
    hash_key        = "Level"
    range_key       = "AverageScore"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "KEYS_ONLY"
  }

  tags = {
    Name = var.dynamodb_table_name
  }
}
