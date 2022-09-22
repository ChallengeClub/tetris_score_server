resource "aws_vpc" "tetris_score_server_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = var.vpc_tag
  }
}

resource "aws_subnet" "tetris_score_server_subnet" {
  vpc_id            = aws_vpc.tetris_score_server_vpc.id
  cidr_block        = var.subnet_cidr
  availability_zone = "ap-northeast-1c"

  tags = {
    Name = var.vpc_tag
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.tetris_score_server_vpc.id

  tags = {
    Name = var.vpc_tag
  }
}

resource "aws_route_table" "vpc_route_table" {
  vpc_id = aws_vpc.tetris_score_server_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }
  tags = {
    Name = var.vpc_tag
  }
}
