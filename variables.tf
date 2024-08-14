variable "vnet_name" {
  description = "List of names for the virtual networks"
  type        = string
}

variable "vnet_address_spaces" {
  description = "List of address spaces for the virtual networks"
  type        = list(string)
}

variable "web_subnet_names" {
  description = "List of names for the web subnets"
  type        = list(string)
}

variable "app_subnet_names" {
  description = "List of names for the app subnets"
  type        = list(string)
}

variable "data_subnet_names" {
  description = "List of names for the data subnets"
  type        = list(string)
}

variable "web_cidrs" {
  description = "List of CIDR blocks for the web subnets"
  type        = list(string)
}

variable "app_cidrs" {
  description = "List of CIDR blocks for the app subnets"
  type        = list(string)
}

variable "data_cidrs" {
  description = "List of CIDR blocks for the data subnets"
  type        = list(string)
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "East US"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "example-resources"
}