resource "aws_dynamodb_table" "dynamodb-table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Id"

  attribute {
    name = "Id"
    type = "S"
  }

  attribute {
    name = "CreatedAt"
    type = "N"
  }

  attribute {
    name = "Competition"
    type = "S"
  }


  global_secondary_index {
    name            = "CreatedAtIndex"
    hash_key        = "Competition"
    range_key       = "CreatedAt"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "INCLUDE"
    non_key_attributes = [
      "Id",
      "Status",
      "Name",
      "MeanScore",
      "RepositoryURL",
      "Branch",
      "TrialNum",
      "Level",
      "GameMode",
      "GameTime"
    ]
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

resource "aws_dynamodb_table" "dynamodb-news-table" {
  name           = var.dynamodb_news_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Id"

  attribute {
    name = "Id"
    type = "S"
  }

  tags = {
    Name = var.dynamodb_news_table_name
  }
}

resource "aws_dynamodb_table" "dynamodb-training-table" {
  name           = var.dynamodb_training_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "Section-Id"

  attribute {
    name = "Section-Id"
    type = "S"
  }
  attribute {
    name = "Section"
    type = "S"
  }
  attribute {
    name = "Id"
    type = "N"
  }

  global_secondary_index {
    name            = "TrainingSetionIndex"
    hash_key        = "Section"
    range_key       = "Id"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "INCLUDE"
    non_key_attributes = [
      "Section-Id",
      "Title",
      "CreatedAt"
    ]
  }
}