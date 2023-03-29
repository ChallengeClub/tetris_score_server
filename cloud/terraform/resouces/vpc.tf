resource "aws_vpc" "tetris_score_server_vpc" {
  cidr_block = var.score_evaluation_vpc_cidr
  tags = {
    Name = var.score_evaluation_vpc_tag
  }
}

resource "aws_subnet" "tetris_score_server_subnet" {
  vpc_id            = aws_vpc.tetris_score_server_vpc.id
  cidr_block        = var.subnet_cidr
  availability_zone = var.subnet_availability_zone

  tags = {
    Name = var.score_evaluation_vpc_tag
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.tetris_score_server_vpc.id

  tags = {
    Name = var.score_evaluation_vpc_tag
  }
}

resource "aws_route_table" "vpc_route_table" {
  vpc_id = aws_vpc.tetris_score_server_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }
  tags = {
    Name = var.score_evaluation_vpc_tag
  }
}

resource "aws_route_table_association" "ecs_subnet_route_table_association" {
  subnet_id      = aws_subnet.tetris_score_server_subnet.id
  route_table_id = aws_route_table.vpc_route_table.id
}
