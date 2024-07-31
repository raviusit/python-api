# Overview
<br />
<p align="center">
  <img width="50%" alt="Screenshot 2024-07-31 at 2 06 56 AM" src="https://github.com/user-attachments/assets/d372e59f-c39c-483e-b7cb-126029a21cef">
</p>
<br /><br /><br />


This repo contains a data-driven Python web app (running in Flask) deployed as an Azure App Service with the Azure Database for PostgreSQL relational database service. Azure App Service supports Python in a Linux server environment.

This is a basic Python service. Endpoints information for todos API:\
GET /todos → Returns all ToDo\

GET /todos/{id} → Returns a ToDo\
POST /todos → Expects a ToDo (without an id) and returns a ToDo with an id\

URL : https://aa-demo-gufrt.azurewebsites.net/

# Pre-requisite

An Azure account with an active subscription. I am using a free trial subscription here.  
Fundamental knowledge of Python with Flask development, any relational Database, and Terraform for cloud infrastructure resource provisioning.   

# Architecture Diagram 

<img width="60%" alt="Screenshot 2024-07-29 at 7 54 02 PM" src="https://github.com/user-attachments/assets/49c4c57c-e21d-4f4f-9be8-e4ee6fff820b">



# Resources Used
https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app?tabs=flask%2Cwindows&pivots=azure-portal\
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app\
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_flexible_server\
