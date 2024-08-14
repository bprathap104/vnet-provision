variable "vnet_name" {
  description = "List of names for the virtual networks"
  type        = string
}

variable "vnet_address_spaces" {
  description = "List of address spaces for the virtual networks"
  type        = list(string)
}

variable "subnet_details" {
  type = list(object({
    cidr = string
    name = string
  }))
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "Central US"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "example-resources"
}