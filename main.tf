resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_virtual_network" "vnets" {
  name                = var.vnet_name
  address_space       = var.vnet_address_spaces
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "subnets" {
  count                = length(var.subnet_details)
  name                 = var.subnet_details[count.index].name
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.vnets.name
  address_prefixes     = [var.subnet_details[count.index].cidr]
}
