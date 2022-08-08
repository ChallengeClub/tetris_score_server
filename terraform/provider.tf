terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    bucket = "tetris-score-server-terraform-state"
    region = "ap-northeast-1"
    key = "terraform.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region  = "ap-northeast-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "tetris-score-server-terraform-state"
}