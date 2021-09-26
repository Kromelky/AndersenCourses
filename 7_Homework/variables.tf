
variable "instance_count" {
    type    = number
    default = 2
    description = "Instances count"
}
variable "ami_key_pair_name" {
    type    = string
    default = "main_key"
    description = "Pem key file name"
}

variable "vpc_cidr" {
  type        = string
  default     = "192.168.1.0/24"
  description = "CIDR for VPC"
}

variable "tenancy" {
  type        = string
  default     = "default"
  description = ""
}

variable "enable_dns_support" {
    default = true
}

variable "enable_dns_hostnames" {
    default = true
}

variable "vpc_name" {
  type        = string
  default     = "mainvpc"
  description = ""
}

variable "public_cidr" {
  type        = string
  default     = "192.168.1.0/24"
  description = "CIDR for VPC"
}