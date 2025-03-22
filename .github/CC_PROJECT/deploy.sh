#!/bin/bash

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Installing Azure CLI..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# Login to Azure
az login

# Create resource group
az group create --name event-registration-rg --location eastus

# Create Azure SQL Database server
az sql server create \
    --name event-registration-sql \
    --resource-group event-registration-rg \
    --location eastus \
    --admin-user eventadmin \
    --admin-password $(openssl rand -base64 32)

# Create database
az sql db create \
    --resource-group event-registration-rg \
    --server event-registration-sql \
    --name eventdb \
    --service-objective S0

# Get connection string
CONNECTION_STRING=$(az sql db show-connection-string \
    --client ado.net \
    --server event-registration-sql \
    --database eventdb \
    --resource-group event-registration-rg \
    --output tsv)

# Create Azure Web App
az webapp create \
    --resource-group event-registration-rg \
    --plan event-registration-plan \
    --name event-registration-app \
    --runtime "PYTHON:3.9" \
    --deployment-source-url https://github.com/yourusername/event-registration.git

# Configure environment variables
az webapp config appsettings set \
    --name event-registration-app \
    --resource-group event-registration-rg \
    --settings \
    SECRET_KEY=$(openssl rand -base64 32) \
    DATABASE_URL="$CONNECTION_STRING" \
    FLASK_ENV=production

echo "Deployment completed! Your app is available at https://event-registration-app.azurewebsites.net" 