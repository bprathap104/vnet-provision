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

resource "azurerm_subnet" "web_subnets" {
  count                = length(var.web_subnet_names)
  name                 = var.web_subnet_names[count.index]
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.vnets.name
  address_prefixes     = [var.web_cidrs[count.index]]
}

resource "azurerm_subnet" "app_subnets" {
  count                = length(var.app_subnet_names)
  name                 = var.app_subnet_names[count.index]
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.vnets.name
  address_prefixes     = [var.app_cidrs[count.index]]
}

resource "azurerm_subnet" "data_subnets" {
  count                = length(var.data_subnet_names)
  name                 = var.data_subnet_names[count.index]
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.vnets.name
  address_prefixes     = [var.data_cidrs[count.index]]
}