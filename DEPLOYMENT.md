# 🚀 Deployment Guide

Guide for deploying the Recreation.gov Campsite Checker to production.

## Deployment Options

### Option 1: Single Server Deployment (Recommended for Personal Use)

Deploy both frontend and backend on a single server (VPS, EC2, etc.)

**Requirements:**
- Ubuntu 20.04+ or similar Linux distro
- Node.js 20+
- Python 3.9+
- Nginx (for reverse proxy)
- PM2 (for process management)

**Steps:**

1. **Install Dependencies**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Node.js 20
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs
   
   # Install Python 3.9+
   sudo apt install -y python3.9 python3.9-venv python3-pip
   
   # Install Nginx
   sudo apt install -y nginx
   
   # Install PM2
   sudo npm install -g pm2
   ```

2. **Clone and Setup**
   ```bash
   cd /var/www
   git clone <your-repo-url> recreation-campsite-checker
   cd recreation-campsite-checker
   
   # Setup Python venv
   python3 -m venv myvenv
   source myvenv/bin/activate
   pip install -r backend/python/requirements.txt
   
   # Install Node dependencies
   cd backend && npm install
   cd ../frontend && npm install && npm run build
   ```

3. **Configure Environment**
   ```bash
   # Create backend/.env
   cat > backend/.env << EOF
   PORT=3001
   CAMPSITE_FROM_EMAIL=your-email@gmail.com
   CAMPSITE_EMAIL_PASSWORD=your-app-password
   CAMPSITE_TO_EMAIL=recipient@gmail.com
   EOF
   ```

4. **Setup PM2**
   ```bash
   # Create PM2 ecosystem file
   cat > ecosystem.config.js << EOF
   module.exports = {
     apps: [{
       name: 'campsite-backend',
       cwd: './backend',
       script: 'server/index.js',
       env: {
         NODE_ENV: 'production',
         PORT: 3001
       }
     }]
   };
   EOF
   
   # Start with PM2
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/campsite-checker
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # Frontend
       location / {
           root /var/www/recreation-campsite-checker/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api {
           proxy_pass http://localhost:3001;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
       
       # SSE endpoint
       location /api/stream {
           proxy_pass http://localhost:3001;
           proxy_http_version 1.1;
           proxy_set_header Connection '';
           proxy_buffering off;
           proxy_cache off;
           chunked_transfer_encoding off;
       }
   }
   ```
   
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/campsite-checker /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Setup SSL (Optional but Recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Option 2: Container Deployment (Docker)

**Create Dockerfile for Backend:**
```dockerfile
# backend/Dockerfile
FROM node:20-slim

# Install Python
RUN apt-get update && apt-get install -y python3.9 python3-pip python3-venv

WORKDIR /app

# Copy Python requirements
COPY python/requirements.txt python/
RUN python3 -m venv /venv
RUN /venv/bin/pip install -r python/requirements.txt

# Copy Node.js dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

ENV PATH="/venv/bin:$PATH"
EXPOSE 3001

CMD ["npm", "start"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3001:3001"
    environment:
      - PORT=3001
      - CAMPSITE_FROM_EMAIL=${CAMPSITE_FROM_EMAIL}
      - CAMPSITE_EMAIL_PASSWORD=${CAMPSITE_EMAIL_PASSWORD}
      - CAMPSITE_TO_EMAIL=${CAMPSITE_TO_EMAIL}
    restart: unless-stopped
    
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
    restart: unless-stopped
```

**Deploy:**
```bash
docker-compose up -d
```

### Option 3: Serverless (Not Recommended)

The continuous monitoring nature of this application doesn't fit well with serverless architectures. Stick with Options 1 or 2.

## Production Considerations

### Security

1. **Environment Variables**
   - Never commit `.env` files
   - Use secure credential storage
   - Rotate email passwords regularly

2. **Rate Limiting**
   - Consider adding rate limits to API
   - Monitor recreation.gov API usage
   - Don't abuse the system

3. **HTTPS**
   - Always use SSL in production
   - Force HTTPS redirect
   - Use strong cipher suites

4. **Updates**
   - Keep dependencies updated
   - Monitor for security vulnerabilities
   - Have a rollback plan

### Monitoring

1. **Application Monitoring**
   ```bash
   # View PM2 logs
   pm2 logs campsite-backend
   
   # Monitor resources
   pm2 monit
   ```

2. **Error Tracking**
   - Consider integrating Sentry or similar
   - Monitor backend logs
   - Set up alerts for failures

3. **Uptime Monitoring**
   - Use uptime monitoring service (UptimeRobot, etc.)
   - Monitor /health endpoint
   - Set up alerts

### Performance

1. **Caching**
   - Cache recreation.gov responses (short TTL)
   - Use Nginx caching for static assets

2. **Scaling**
   - Single instance should handle personal use
   - For multiple users, consider load balancing
   - Database would be needed for multi-user

3. **Resource Limits**
   ```bash
   # PM2 max memory restart
   pm2 start ecosystem.config.js --max-memory-restart 500M
   ```

### Backup

1. **Configuration Backup**
   ```bash
   # Backup env files
   tar -czf backup-$(date +%Y%m%d).tar.gz backend/.env nginx.conf
   ```

2. **Email Timestamp Files**
   - These prevent spam - preserve them
   - `.email_timestamp_*.json` files

## Cost Estimates

### Self-Hosted VPS
- **DigitalOcean Droplet**: $6-12/month
- **AWS EC2 t2.micro**: ~$8/month
- **Linode Nanode**: $5/month

### Domain & SSL
- **Domain**: $10-15/year
- **SSL**: Free (Let's Encrypt)

### Email
- **Gmail**: Free (use app password)
- **SendGrid**: Free tier available

**Total**: ~$5-15/month for personal use

## Maintenance

### Regular Tasks

**Weekly:**
- Check logs for errors
- Monitor disk space
- Review notification accuracy

**Monthly:**
- Update dependencies (test first!)
  ```bash
  cd backend && npm update
  cd ../frontend && npm update
  ```
- Review resource usage
- Check SSL certificate expiry

**Quarterly:**
- Security audit
- Performance review
- Dependency security scan
  ```bash
  npm audit
  ```

### Updating Application

```bash
# Pull latest changes
git pull origin main

# Update backend
cd backend
npm install
pm2 restart campsite-backend

# Update frontend
cd ../frontend
npm install
npm run build

# Reload Nginx
sudo systemctl reload nginx
```

## Rollback Plan

```bash
# Revert to previous git commit
git revert HEAD
# Or
git reset --hard <previous-commit-hash>

# Rebuild and restart
cd backend && npm install
pm2 restart campsite-backend

cd ../frontend && npm install && npm run build
sudo systemctl reload nginx
```

## Troubleshooting Production

### Application won't start
1. Check PM2 logs: `pm2 logs`
2. Verify Python venv is activated
3. Check file permissions
4. Verify environment variables

### Nginx errors
1. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
2. Test configuration: `sudo nginx -t`
3. Check port availability: `sudo netstat -tulpn | grep :80`

### High resource usage
1. Check PM2 monit: `pm2 monit`
2. Reduce concurrent monitoring jobs
3. Consider upgrading server
4. Check for memory leaks

## Advanced: Multi-User Deployment

For serving multiple users (not included in current version):

**Required additions:**
- User authentication system
- Database (PostgreSQL/MongoDB)
- User-specific monitoring jobs
- Rate limiting per user
- Admin dashboard

**Estimated effort**: 40-80 hours of development

## Support

For deployment issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs carefully
3. Test locally first
4. Verify all requirements are met

---

**Good luck with your deployment! 🚀**

