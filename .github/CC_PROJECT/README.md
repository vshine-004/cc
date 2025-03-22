# Event Registration System

A modern event registration system built with Flask and deployed on Azure.

## Features

- User authentication (login/register)
- Event creation and management
- Event registration
- Modern UI with animations
- Responsive design
- Azure SQL Database integration
- Azure Blob Storage for images

## Prerequisites

- Python 3.8 or later
- Azure subscription
- Azure CLI (optional)

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///events.db
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Azure Deployment

### Method 1: Using Azure Portal

1. Create an Azure Web App:
   - Go to Azure Portal
   - Create a new Web App
   - Choose Python 3.8 as runtime stack
   - Select Basic tier for development

2. Create an Azure SQL Database:
   - Create a new SQL Database
   - Choose Basic tier
   - Configure firewall rules
   - Get the connection string

3. Configure Application Settings:
   - Go to your Web App's Configuration
   - Add these settings:
     ```
     SECRET_KEY=your-secret-key
     DATABASE_URL=your-sql-connection-string
     FLASK_ENV=production
     ```

4. Deploy your code:
   - Go to Deployment Center
   - Choose your preferred deployment method (GitHub, Azure Repos, etc.)
   - Configure the deployment

### Method 2: Using Azure CLI

1. Install Azure CLI:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

2. Login to Azure:
```bash
az login
```

3. Run the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Method 3: Using GitHub Actions

1. Create a GitHub repository
2. Push your code to GitHub
3. In Azure Portal:
   - Go to your Web App
   - Select "Deployment Center"
   - Choose "GitHub"
   - Select your repository
   - Configure the branch to deploy

## Database Migration

After deployment, run the database migrations:
```bash
python -c "from app import db; db.create_all()"
```

## Monitoring

1. Enable Application Insights in Azure Portal
2. Monitor application logs
3. Set up alerts for errors
4. Monitor database performance

## Security

1. Enable HTTPS
2. Configure CORS
3. Set up proper authentication
4. Regular security updates
5. Database encryption

## Cost Optimization

1. Use Basic tier for development
2. Configure auto-scaling rules
3. Monitor resource usage
4. Set up cost alerts

## Support

For issues or questions:
1. Check Azure documentation
2. Review application logs
3. Contact Azure support
4. Check GitHub issues

## Updates and Maintenance

Regular maintenance tasks:
1. Update dependencies
2. Backup database
3. Monitor performance
4. Review security settings
5. Update SSL certificates 