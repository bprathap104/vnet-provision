# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"  # Specify the version you want to use
    }
  }
  required_version = ">= 1.0"  # Specify the minimum Terraform version
}

provider "azurerm" {
  features {}

  # Uncomment and fill in the following lines if you want to use 
  # service principal authentication instead of Azure CLI or managed identity
  # subscription_id = "YOUR_SUBSCRIPTION_ID"
  # client_id       = "YOUR_CLIENT_ID"
  # client_secret   = "YOUR_CLIENT_SECRET"
  # tenant_id       = "YOUR_TENANT_ID"
}