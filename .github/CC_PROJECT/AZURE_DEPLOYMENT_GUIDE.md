# Azure Portal Deployment Guide

## Prerequisites
1. Azure account (free tier is sufficient)
2. GitHub account with your code repository
3. Your application code ready in a GitHub repository
4. Python 3.9 or higher installed locally

## Step-by-Step Azure Portal Deployment

### 1. Create Azure Account
1. Go to [Azure Portal](https://portal.azure.com)
2. Sign up for a free account if you don't have one
3. Complete the verification process

### 2. Create Resource Group
1. In Azure Portal, click "Create a resource"
2. Search for "Resource group"
3. Click "Create"
4. Fill in the details:
   - Subscription: Select your subscription
   - Resource group: `event-registration-rg`
   - Region: Choose your preferred region (e.g., East US)
5. Click "Review + create" then "Create"

### 3. Create Azure SQL Database
1. In Azure Portal, click "Create a resource"
2. Search for "SQL Database"
3. Click "Create"
4. Fill in the details:
   - Resource group: Select `event-registration-rg`
   - Database name: `eventdb`
   - Server: Create new
     - Server name: `event-registration-sql`
     - Server admin login: `eventadmin`
     - Password: Create a strong password
     - Location: Same as resource group
5. Click "Review + create" then "Create"

### 4. Configure SQL Server Firewall
1. Go to your SQL Server resource
2. Click "Security" → "Networking"
3. Click "Add client IP"
4. Click "Save"

### 5. Create Web App
1. In Azure Portal, click "Create a resource"
2. Search for "Web App"
3. Click "Create"
4. Fill in the details:
   - Resource group: Select `event-registration-rg`
   - Name: `event-registration-app`
   - Publish: Code
   - Runtime stack: Python 3.9
   - Operating System: Linux
   - Region: Same as resource group
   - App Service Plan: Create new
     - Name: `event-registration-plan`
     - Sku and size: Free F1 (for testing)
5. Click "Review + create" then "Create"

### 6. Configure Web App Settings
1. Go to your Web App resource
2. Click "Configuration" → "Application settings"
3. Add the following settings:
   ```
   SECRET_KEY=<generate-a-random-string>
   DATABASE_URL=<your-sql-connection-string>
   FLASK_ENV=production
   FLASK_APP=app.py
   ```
4. Click "Save"

### 7. Set Up GitHub Deployment
1. In your Web App, go to "Deployment Center"
2. Select "GitHub" as your source
3. Authorize Azure to access your GitHub account
4. Select your repository and branch
5. Click "Save"

### 8. Configure Startup Command
1. In your Web App, go to "Configuration" → "General settings"
2. Set "Startup Command" to:
   ```
   gunicorn --bind=0.0.0.0 --timeout 600 app:app
   ```
3. Click "Save"

### 9. Database Migration
1. Go to your Web App
2. Click "Advanced Tools (Kudu)"
3. Click "Debug console" → "PowerShell"
4. Navigate to your site directory
5. Run the following commands:
   ```powershell
   python -m pip install flask-migrate
   flask db upgrade
   ```

### 10. Verify Deployment
1. Go to your Web App
2. Click the URL (usually `https://event-registration-app.azurewebsites.net`)
3. Test the following:
   - User registration
   - Event creation
   - Event registration

## Backend Setup Guide

### 1. Local Development Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///events.db
   FLASK_ENV=development
   FLASK_APP=app.py
   ```

4. Initialize database:
   ```bash
   python setup_db.py
   ```

### 2. Database Management
1. Create new migration:
   ```bash
   flask db migrate -m "Description of changes"
   ```

2. Apply migration:
   ```bash
   flask db upgrade
   ```

3. Rollback migration:
   ```bash
   flask db downgrade
   ```

### 3. Testing Backend
1. Run the application:
   ```bash
   python app.py
   ```

2. Test API endpoints:
   - GET `/api/events` - List all events
   - GET `/api/events?category=music` - Filter events by category

3. Test database operations:
   - Create a new user
   - Create an event
   - Register for an event
   - View event details

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

### Useful Azure Portal Features

1. Application Insights
   - Go to Web App → "Application Insights"
   - Enable monitoring
   - View application metrics

2. Log Stream
   - Go to Web App → "Log stream"
   - View real-time application logs

3. Backup
   - Go to Web App → "Backup"
   - Configure automated backups

## Cost Management

1. Monitor Usage
   - Go to "Cost Management + Billing"
   - Set up budget alerts
   - Review resource usage

2. Free Tier Limitations
   - 1GB storage
   - 60 minutes/day compute time
   - Shared compute resources

## Support

For additional help:
1. Use Azure Portal's "Help + support"
2. Check Azure documentation
3. Contact Azure support
4. Use Azure community forums 