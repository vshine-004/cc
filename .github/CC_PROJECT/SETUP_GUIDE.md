# Event Registration Website Setup Guide

## Prerequisites
1. Python 3.9 or higher installed
2. Git installed
3. Azure account (for deployment)
4. Code editor (VS Code recommended)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd event-registration
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy the `.env.example` file to `.env`
2. Update the following variables in `.env`:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///events.db
   FLASK_ENV=development
   FLASK_APP=app.py
   ```

### 5. Initialize Database
```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 6. Run the Application Locally
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Azure Deployment

### 1. Azure CLI Setup
```bash
# Install Azure CLI (if not already installed)
# On Windows (PowerShell as Administrator):
winget install -e --id Microsoft.AzureCLI

# On macOS:
brew install azure-cli

# On Linux:
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### 2. Login to Azure
```bash
az login
```

### 3. Deploy Using Script
```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### 4. Manual Deployment Steps (Alternative)
If you prefer to deploy manually:

1. Create Resource Group:
```bash
az group create --name event-registration-rg --location eastus
```

2. Create Azure SQL Database:
```bash
# Create SQL Server
az sql server create \
    --name event-registration-sql \
    --resource-group event-registration-rg \
    --location eastus \
    --admin-user eventadmin \
    --admin-password <your-password>

# Create Database
az sql db create \
    --resource-group event-registration-rg \
    --server event-registration-sql \
    --name eventdb \
    --service-objective S0
```

3. Create Web App:
```bash
# Create App Service Plan
az appservice plan create \
    --name event-registration-plan \
    --resource-group event-registration-rg \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group event-registration-rg \
    --plan event-registration-plan \
    --name event-registration-app \
    --runtime "PYTHON:3.9" \
    --deployment-source-url <your-github-repo-url>
```

4. Configure Environment Variables:
```bash
az webapp config appsettings set \
    --name event-registration-app \
    --resource-group event-registration-rg \
    --settings \
    SECRET_KEY=<your-secret-key> \
    DATABASE_URL=<your-database-connection-string> \
    FLASK_ENV=production
```

## Post-Deployment Steps

### 1. Database Migration
```bash
# Connect to Azure Web App
az webapp ssh --name event-registration-app --resource-group event-registration-rg

# Run migrations
flask db upgrade
```

### 2. Verify Deployment
1. Visit `https://event-registration-app.azurewebsites.net`
2. Test user registration
3. Test event creation
4. Test event registration

## Troubleshooting

### Common Issues

1. Database Connection Issues
   - Check connection string in Azure Portal
   - Verify firewall rules for SQL Server
   - Ensure database user has correct permissions

2. Application Errors
   - Check application logs in Azure Portal
   - Verify environment variables
   - Check Python version compatibility

3. Deployment Issues
   - Verify GitHub repository access
   - Check deployment logs in Azure Portal
   - Ensure all required files are in repository

### Useful Commands

```bash
# View application logs
az webapp log tail --name event-registration-app --resource-group event-registration-rg

# Restart web app
az webapp restart --name event-registration-app --resource-group event-registration-rg

# View web app settings
az webapp config appsettings list --name event-registration-app --resource-group event-registration-rg
```

## Maintenance

### Regular Tasks

1. Database Backup
   - Set up automated backups in Azure Portal
   - Monitor database size and performance

2. Application Updates
   - Keep dependencies updated
   - Monitor application logs
   - Check for security updates

3. Performance Monitoring
   - Monitor application metrics
   - Check resource usage
   - Optimize as needed

## Support

For additional support:
1. Check Azure documentation
2. Review Flask documentation
3. Contact system administrator
4. Check GitHub issues 