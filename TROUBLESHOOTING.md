# 🔧 Troubleshooting Guide

Common issues and their solutions for the Recreation.gov Campsite Checker.

## Table of Contents
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Notification Issues](#notification-issues)
- [Email Issues](#email-issues)
- [Network Issues](#network-issues)

## Backend Issues

### Backend won't start

**Symptom**: Error when running `npm start` in backend directory

**Solutions**:
1. Ensure Python virtual environment is activated:
   ```bash
   source myvenv/bin/activate  # or myvenv\Scripts\activate on Windows
   ```

2. Check Python dependencies:
   ```bash
   cd backend/python
   pip install -r requirements.txt
   ```

3. Verify Node.js dependencies:
   ```bash
   cd backend
   npm install
   ```

4. Check if port 3001 is already in use:
   ```bash
   # macOS/Linux
   lsof -i :3001
   
   # Windows
   netstat -ano | findstr :3001
   ```

### Python script errors

**Symptom**: Backend starts but crashes when monitoring starts

**Solutions**:
1. Check Python version (requires 3.9+):
   ```bash
   python --version
   ```

2. Verify all Python dependencies are installed:
   ```bash
   cd backend/python
   pip list
   ```

3. Check Python script can run standalone:
   ```bash
   cd backend/python
   python camping.py --start-date 2025-06-01 --end-date 2025-06-05 --parks 232448 --nights 2
   ```

### Module import errors

**Symptom**: `ModuleNotFoundError` or import errors

**Solutions**:
1. Ensure you're in the correct directory when running scripts
2. Activate virtual environment
3. Reinstall dependencies:
   ```bash
   pip install -r backend/python/requirements.txt
   ```

## Frontend Issues

### Frontend won't start

**Symptom**: Error when running `npm run dev` in frontend directory

**Solutions**:
1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Clear npm cache:
   ```bash
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

3. Check Node.js version (requires 20+):
   ```bash
   node --version
   ```

### Cannot connect to backend

**Symptom**: "Failed to start monitoring. Is the backend server running?"

**Solutions**:
1. Verify backend is running on port 3001
2. Check backend logs for errors
3. Test backend health endpoint:
   ```bash
   curl http://localhost:3001/health
   ```

4. Check browser console for CORS errors
5. Verify proxy configuration in `frontend/vite.config.ts`

### Build errors

**Symptom**: TypeScript or build errors

**Solutions**:
1. Update dependencies:
   ```bash
   cd frontend
   npm update
   ```

2. Clear Vite cache:
   ```bash
   rm -rf node_modules/.vite
   ```

## Notification Issues

### Browser notifications not working

**Symptom**: No notifications appear when campsites are found

**Solutions**:
1. Grant notification permission when prompted
2. Check browser notification settings:
   - **Chrome**: Settings → Privacy and Security → Site Settings → Notifications
   - **Firefox**: Preferences → Privacy & Security → Permissions → Notifications
   - **Safari**: Preferences → Websites → Notifications

3. Test notifications:
   - Open browser console
   - Run: `new Notification("Test", { body: "Testing notifications" })`

4. Clear site data and try again:
   - Chrome: F12 → Application → Storage → Clear site data

5. Try a different browser

### Notifications blocked

**Symptom**: Permission denied or notifications blocked

**Solutions**:
1. Check if notifications are blocked for the site
2. Clear site permissions and allow when prompted again
3. Make sure you're not in incognito/private mode (some browsers block notifications there)

## Email Issues

### Email notifications not sending

**Symptom**: No emails received when campsites are found

**Solutions**:
1. Verify environment variables are set correctly:
   ```bash
   # In backend directory, create .env file with:
   CAMPSITE_FROM_EMAIL=your-email@gmail.com
   CAMPSITE_EMAIL_PASSWORD=your-app-password
   CAMPSITE_TO_EMAIL=recipient@gmail.com
   CAMPSITE_SMTP_SERVER=smtp.gmail.com
   CAMPSITE_SMTP_PORT=587
   ```

2. For Gmail, ensure you have:
   - 2-factor authentication enabled
   - App password generated (not your regular password)
   - Less secure app access might be disabled (use app password instead)

3. Test email configuration:
   ```bash
   cd backend/python
   python email_notifier.py
   ```

4. Check backend logs for SMTP errors

### Email rate limiting

**Symptom**: Not receiving all email notifications

**Solution**: By design, emails are rate-limited to once per 5 minutes per unique availability set. This prevents spam when the same campsites remain available.

## Network Issues

### Cannot reach recreation.gov

**Symptom**: API errors or "failed to fetch" messages

**Solutions**:
1. Check your internet connection
2. Verify recreation.gov is accessible:
   ```bash
   curl https://www.recreation.gov
   ```

3. Check if you're behind a firewall or proxy
4. Wait a few minutes (recreation.gov might be temporarily down)

### Connection timeout

**Symptom**: Requests timing out

**Solutions**:
1. Check your network speed
2. Increase timeout if needed (modify in `clients/recreation_client.py`)
3. Check if recreation.gov is experiencing issues

### SSE connection dropping

**Symptom**: "Disconnected" status in monitoring UI

**Solutions**:
1. Check if backend is still running
2. Refresh the browser page
3. Check browser console for SSE errors
4. Verify firewall isn't blocking WebSocket/SSE connections

## Performance Issues

### Slow response times

**Solutions**:
1. Reduce number of parks being monitored simultaneously
2. Check CPU/memory usage
3. Close other applications
4. Restart both frontend and backend

### High CPU usage

**Solutions**:
1. Monitoring runs every 20 seconds - this is normal
2. Reduce number of parks if needed
3. Stop monitoring when not needed
4. Check for memory leaks (restart servers)

## Data Issues

### Wrong or missing park data

**Symptom**: Parks showing incorrectly or not at all

**Solutions**:
1. Verify park IDs are correct (check recreation.gov URLs)
2. Some parks may not be available in the current season
3. Check recreation.gov directly to confirm park exists

### Dates not working

**Symptom**: "No campsites available" for dates you know are available

**Solutions**:
1. Verify date format is YYYY-MM-DD
2. Check if dates are too far in the future (recreation.gov typically opens bookings 6 months in advance)
3. Try wider date range
4. Verify campground is open during selected dates

## Still Having Issues?

1. Check the [README.md](README.md) for detailed setup instructions
2. Review [PRD.md](PRD.md) for technical architecture details
3. Check browser and terminal console logs for error messages
4. Restart both frontend and backend servers
5. Try the CLI version to isolate if it's a web UI issue:
   ```bash
   cd backend/python
   python camping.py --start-date 2025-06-01 --end-date 2025-06-05 --parks 232448 --nights 2
   ```

## Getting Help

When reporting issues, please include:
- Operating system and version
- Node.js version (`node --version`)
- Python version (`python --version`)
- Browser and version
- Complete error message from console
- Steps to reproduce the issue

---

**Happy Camping! 🏕️**

