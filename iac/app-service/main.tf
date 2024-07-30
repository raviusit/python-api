## Resource Group
resource "azurerm_resource_group" "default" {
  name     = var.resource_group_name
  location = var.location
}

## Network
resource "azurerm_virtual_network" "default" {
  name                = "${var.resource_group_name}-vnet"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_network_security_group" "default" {
  name                = "${var.resource_group_name}-nsg"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name

  security_rule {
    name                       = "${var.resource_group_name}-nsg"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet" "default" {
  name                 = "${var.resource_group_name}-subnet"
  virtual_network_name = azurerm_virtual_network.default.name
  resource_group_name  = azurerm_resource_group.default.name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.Storage"]

  delegation {
    name = "fs"

    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"

      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_subnet_network_security_group_association" "default" {
  subnet_id                 = azurerm_subnet.default.id
  network_security_group_id = azurerm_network_security_group.default.id
}

resource "azurerm_private_dns_zone" "default" {
  name                = "${var.resource_group_name}-pdz.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.default.name

  depends_on = [azurerm_subnet_network_security_group_association.default]
}

resource "azurerm_private_dns_zone_virtual_network_link" "default" {
  name                  = "${var.resource_group_name}-pdzvnetlink.com"
  private_dns_zone_name = azurerm_private_dns_zone.default.name
  virtual_network_id    = azurerm_virtual_network.default.id
  resource_group_name   = azurerm_resource_group.default.name
}


# DB
resource "random_password" "pass" {
  length = 20
}

resource "azurerm_postgresql_flexible_server" "default" {
  name                   = "${var.db_name}-server"
  resource_group_name    = azurerm_resource_group.default.name
  location               = azurerm_resource_group.default.location
  version                = "15"
  public_network_access_enabled = true
  administrator_login    = "adminTerraform"
  administrator_password = random_password.pass.result
  zone                   = "1"
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"
  backup_retention_days  = 7

  depends_on = [azurerm_private_dns_zone_virtual_network_link.default]
}

# App-Service
resource "azurerm_service_plan" "default" {
  name                = "${var.resource_group_name}-sp"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "default" {
  name                = var.app_name
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  service_plan_id     = azurerm_service_plan.default.id

  identity {
    type = "SystemAssigned"
  }
  site_config {
    always_on                            = false
    default_documents                    = ["Default.asp", "Default.htm", "Default.html", "default.aspx", "hostingstart.html", "iisstart.htm", "index.htm", "index.html", "index.php"]
    ftps_state                           = "FtpsOnly"
    http2_enabled                        = false
    local_mysql_enabled                  = false
    managed_pipeline_mode                = "Integrated"
    remote_debugging_enabled             = false
    remote_debugging_version             = "VS2022"
    vnet_route_all_enabled               = true
    websockets_enabled                   = false
    application_stack {
      python_version = "3.9"
    }
  }

  app_settings = {
    PGDATABASE = azurerm_postgresql_flexible_server_database.default.name
    PGHOST     = "${azurerm_postgresql_flexible_server.default.name}.postgres.database.azure.com"
    PGPASSWORD = azurerm_postgresql_flexible_server.default.administrator_password
    PGPORT     = "5432"
    PGUSER     = "adminTerraform"
  }

  auth_settings {
    enabled                       = "false"
    token_refresh_extension_hours = "0"
    token_store_enabled           = "false"
  }

  client_affinity_enabled         = "false"
  enabled                         = "true"
  https_only                      = "false"

  logs {
    application_logs {
      file_system_level = "Off"
    }
  }
}
