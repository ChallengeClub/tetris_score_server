resource "aws_dynamodb_table" "dynamodb-table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Id"
  range_key      = "CreatedAt"

  attribute {
    name = "Id"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "N"
  }

  attribute {
    name = "RepositoryURL"
    type = "S"
  }

  attribute {
    name = "Level"
    type = "N"
  }

  attribute {
    name = "MeanScore"
    type = "N"
  }

  global_secondary_index {
    name            = "RepositoryIndex"
    hash_key        = "RepositoryURL"
    range_key       = "CreatedAt"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "KEYS_ONLY"
  }

  global_secondary_index {
    name            = "LevelScoreIndex"
    hash_key        = "Level"
    range_key       = "MeanScore"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "KEYS_ONLY"
  }

  tags = {
    Name = var.dynamodb_table_name
  }
}

resource "aws_dynamodb_table" "dynamodb-competition-table" {
  name           = var.dynamodb_competition_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "RepositoryURL"
  range_key      = "Level"

  attribute {
    name = "RepositoryURL"
    type = "S"
  }

  attribute {
    name = "Level"
    type = "N"
  }

  tags = {
    Name = var.dynamodb_competition_table_name
  }
}
