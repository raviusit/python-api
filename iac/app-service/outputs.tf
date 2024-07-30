output "resource_group_name" {
  value = azurerm_resource_group.default.name
}

output "azurerm_postgresql_flexible_server" {
  value = azurerm_postgresql_flexible_server.default.name
}

output "postgresql_flexible_server_database_name" {
  value = azurerm_postgresql_flexible_server_database.default.name
}

output "postgresql_flexible_server_admin_password" {
  sensitive = true
  value     = azurerm_postgresql_flexible_server.default.administrator_password
}

output "postgresql_flexible_server_fqdn" {
  sensitive = true
  value     = azurerm_postgresql_flexible_server.default.fqdn
}

output "app_service_name" {
  value = azurerm_linux_web_app.default.name
}
