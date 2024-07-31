# Overview
<br />
<p align="center">
  <img width="50%" alt="Screenshot 2024-07-31 at 2 06 56 AM" src="https://github.com/user-attachments/assets/d372e59f-c39c-483e-b7cb-126029a21cef">
</p>
<br /><br /><br />
<p >This repo contains a data-driven Python web app (running in Flask) deployed as an Azure App Service with the Azure Database for PostgreSQL relational database service. Azure App Service supports Python in a Linux server environment.<br />
This is a basic Python service. Endpoints information for todos API:<br />
GET /todos → Returns all ToDo<br />
GET /todos/{id} → Returns a ToDo<br />
POST /todos → Expects a ToDo (without an id) and returns a ToDo with an id<br />
</p>

<p><b>Public URL <b /> : https://aa-demo-gufrt.azurewebsites.net/</p>

# Pre-requisite
<br>
<p >
* An Azure account with an active subscription. I am using a free trial subscription here.<br>  
* Fundamental knowledge of Python with Flask development, any relational Database, and Terraform for cloud infrastructure resource provisioning.
</p>
<br>   

# Architecture Diagram 
<p align="center">
  <img width="60%" alt="Screenshot 2024-07-29 at 7 54 02 PM" src="https://github.com/user-attachments/assets/49c4c57c-e21d-4f4f-9be8-e4ee6fff820b">
</p>

# Resources Used
<br>
<p >
 - https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app?tabs=flask%2Cwindows&pivots=azure-portal\
 - https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_web_app\
 - https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_flexible_server\
</p >
