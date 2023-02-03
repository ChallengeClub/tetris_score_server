terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.31.0"
    }
  }
  backend "s3" { # s3 bucket for tfstate was created on aws console 
    bucket  = "tetris-score-server-terraform-state-prod"
    region  = "ap-northeast-1"
    key     = "terraform.tfstate"
    encrypt = true
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "resouces" {
  source = "../../resouces"
  api_gateway_allow_origins = [
    var.tetris_frontend_origin,
  ]
  score_evaluation_container_image = var.tetris_ecr_repository
}

variable "tetris_frontend_origin" {
    type = string
    sensitive = true
}

variable "tetris_ecr_repository"{
  type = string
  sensitive = true
}