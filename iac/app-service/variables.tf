variable "location" {
  description = "The supported Azure location where the resource deployed"
  type    = string
  default = "polandcentral"
}

#    all the other names must be unique within this resource group.
variable "resource_group_name" {
  type    = string
  default = "aa-demo"
}

variable "db_name" {
  type    = string
  default = "aa-db"
}

variable "app_name" {
  type   = string
  default = "aa-demo-gufrt"
}
