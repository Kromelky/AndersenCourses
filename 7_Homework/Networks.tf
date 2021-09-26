resource "aws_vpc" "main" {
  cidr_block       = var.vpc_cidr
  instance_tenancy = var.tenancy
  enable_dns_hostnames = var.enable_dns_support
  enable_dns_support = var.enable_dns_hostnames
  tags = {
    Name = var.vpc_name
  }
}



resource "aws_subnet" "public" {
  cidr_block = var.public_cidr
  vpc_id = aws_vpc.main.id
  tags = {
    Name = var.public_cidr
  }
}

resource "aws_route_table" "rt" {
  
  vpc_id = aws_vpc.main.id
  route {
    cidr_block              = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.main_gw.id
  }

  tags = {
    Name = "main_rt"
  }
}


resource "aws_internet_gateway" "main_gw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "Main_gw"
  }
}

resource "aws_eip" "gw" {
    count = var.instance_count
    instance = aws_instance.webserver[count.index].id
    vpc      = true

    tags     = {
        Name = format("Main Iep %d", count.index + 1 )
    }  
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.rt.id  
}

