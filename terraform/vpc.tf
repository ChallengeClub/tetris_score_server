resource "aws_vpc" "tetris_score_server_vpc" {
  cidr_block = var.vpc_cidr
}

resource "aws_subnet" "tetris_score_server_subnet" {
  vpc_id     = aws_vpc.tetris_score_server_vpc.id
  cidr_block = var.subnet_cidr

  tags = {
    Name = var.subnet_tag
  }
}
