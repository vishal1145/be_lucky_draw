# Fly.io Deployment Guide

This guide will help you deploy the Lucky Draw Flask application to Fly.io.

## Prerequisites

1. Install Fly.io CLI: https://fly.io/docs/getting-started/installing-flyctl/
2. Sign up for a Fly.io account: https://fly.io/app/sign-up
3. Login to Fly.io: `flyctl auth login`

## Initial Setup

1. **Navigate to the project directory:**
   ```bash
   cd luckydraw
   ```

2. **Create a Fly.io app (if not already created):**
   ```bash
   flyctl launch
   ```
   - This will prompt you to name your app (or use the default)
   - Answer "no" to copying configuration (we already have fly.toml)
   - Answer "no" to deploying now (we'll set secrets first)

3. **Set environment variables/secrets:**
   ```bash
   flyctl secrets set DATABASE_URL="your_database_url"
   flyctl secrets set SECRET_KEY="your_secret_key"
   flyctl secrets set MAIL_SERVER="your_mail_server"
   flyctl secrets set MAIL_PORT="587"
   flyctl secrets set MAIL_USE_TLS="True"
   flyctl secrets set MAIL_USERNAME="your_email"
   flyctl secrets set MAIL_PASSWORD="your_email_password"
   flyctl secrets set MAIL_DEFAULT_SENDER="your_email"
   flyctl secrets set DOMAIN_NAME="your_domain_name"
   flyctl secrets set CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
   
   # Optional: Twilio settings
   flyctl secrets set TWILIO_ACCOUNT_SID="your_twilio_sid"
   flyctl secrets set TWILIO_AUTH_TOKEN="your_twilio_token"
   flyctl secrets set TWILIO_PHONE_NUMBER="your_twilio_number"
   ```

   Or set them all at once:
   ```bash
   flyctl secrets set \
     DATABASE_URL="your_database_url" \
     SECRET_KEY="your_secret_key" \
     MAIL_SERVER="your_mail_server" \
     MAIL_PORT="587" \
     MAIL_USE_TLS="True" \
     MAIL_USERNAME="your_email" \
     MAIL_PASSWORD="your_email_password" \
     MAIL_DEFAULT_SENDER="your_email" \
     DOMAIN_NAME="your_domain_name" \
     CORS_ORIGINS="https://yourdomain.com"
   ```

4. **Deploy the application:**
   ```bash
   flyctl deploy
   ```

## Viewing Logs

```bash
flyctl logs
```

## Scaling

To scale your application:

```bash
# Scale to 2 instances
flyctl scale count 2

# Scale memory
flyctl scale vm shared-cpu-1x --memory 1024
```

## Database Migrations

If you need to run database migrations:

```bash
flyctl ssh console
# Then inside the container:
flask db upgrade
```

## Updating the Application

After making changes:

```bash
flyctl deploy
```

## Monitoring

- View app status: `flyctl status`
- View app info: `flyctl info`
- Open app in browser: `flyctl open`

## Troubleshooting

1. **Check logs:** `flyctl logs`
2. **SSH into the container:** `flyctl ssh console`
3. **View secrets:** `flyctl secrets list` (values are hidden)
4. **Restart the app:** `flyctl restart`

## Notes

- **Build System**: Uses Paketo buildpacks (no Dockerfile needed)
- The app runs on port 8080 internally (configured in fly.toml)
- Gunicorn is used as the WSGI server with 2 workers (configured in Procfile)
- Auto-scaling is enabled (machines start/stop based on traffic)
- HTTPS is forced for all connections
- Python version: 3.10.12 (specified in runtime.txt)

