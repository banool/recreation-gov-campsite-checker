# 🏕️ Recreation.gov Campsite Checker

A powerful tool to monitor campsite availability on recreation.gov with both a modern web interface and command-line support. Get notified instantly when campsites become available!

**This has been updated to work with the new recreation.gov site and API!**

> **Note:** Please don't abuse this tool. Use it responsibly and be mindful that you have an advantage over other campers who don't know how to use scrapers.

## ✨ Features

### Web Interface
- 🖥️ **Modern React UI** - Clean, intuitive interface built with React + TypeScript
- 🔄 **Real-time Monitoring** - Live updates every 20 seconds via Server-Sent Events
- 🔔 **Browser Notifications** - Instant push notifications when sites become available
- 📧 **Email Alerts** - Optional email notifications
- 📊 **Live Status Dashboard** - See check progress, countdown timers, and connection status
- 📱 **Mobile Responsive** - Works great on all devices
- 🎯 **Detailed Results** - Expandable park details with direct booking links

### Command Line Interface
- 🔍 Flexible search across multiple parks simultaneously
- 📅 Date range and consecutive night filtering
- 🎪 Specific campsite ID targeting
- 📧 Email notifications
- 🔄 Continuous monitoring mode

## 🚀 Quick Start

### Prerequisites
- **Node.js 20+** (for the web interface and API server)
- **Python 3.9+** (for the backend logic)

### 1. Install Dependencies

```bash
# Install backend dependencies (includes Python dependencies setup)
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Configure Email Notifications (Optional)

Create a `backend/.env` file with your email settings:

```bash
# backend/.env
CAMPSITE_FROM_EMAIL=your-email@gmail.com
CAMPSITE_EMAIL_PASSWORD=your-app-password
CAMPSITE_TO_EMAIL=recipient@gmail.com
CAMPSITE_SMTP_SERVER=smtp.gmail.com
CAMPSITE_SMTP_PORT=587
```

**Gmail Setup:**
1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the app password as `CAMPSITE_EMAIL_PASSWORD`

> **💡 Pro Tip:** Use a Gmail alias for the sender to get phone notifications! For example, use `youremail+campsites@gmail.com` as the sender and `youremail@gmail.com` as the recipient.

### 3. Run the Application

**Start the Backend:**
```bash
cd backend
npm start
# Backend will run on http://localhost:3001
```

**Start the Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
# Frontend will run on http://localhost:5173
```

**Open Your Browser:**
Navigate to `http://localhost:5173` and start monitoring!

## 📖 Using the Web Interface

1. **Configure Search Parameters**
   - Search for campsite (I suggest starting with parkname then campsite name like "Yosemite pines")
   - Select start and end dates
   - Specify number of consecutive nights needed
   - Optionally filter by campsite type or specific campsite IDs
   - Toggle weekends-only mode if needed

2. **Enable Notifications**
   - Click "Enable Notifications" to allow browser notifications
   - Optionally enable email notifications (requires email setup)

3. **Start Monitoring**
   - Click "Start Monitoring" to begin checking every 20 seconds
   - Watch live status updates and countdown timer
   - View results in real-time as they arrive

4. **Receive Alerts**
   - Get instant browser notifications when sites are available
   - See detailed availability with expandable park cards
   - Click "Book Now" links to go directly to reservation page

## 🔍 Finding Park IDs

1. Go to [recreation.gov](https://www.recreation.gov)
2. Search for your desired campground
3. Click on the campground in the search results
4. The URL will look like: `https://www.recreation.gov/camping/campgrounds/232448`
5. The number at the end (232448) is the park ID

**Popular Park IDs:**
- **Yosemite Valley**
  - Upper Pines: 232450
  - Lower Pines: 232447
  - North Pines: 232449
- **Big Sur**
  - Pfeiffer Big Sur: 233116

## 💻 Command Line Interface

The original CLI is still available in `backend/python/camping.py`:

```bash
cd backend/python
source ../../myvenv/bin/activate  # On Windows: ..\..\myvenv\Scripts\activate

# Basic usage
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 232450 \
  --nights 2

# With email notifications
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --nights 2 \
  --email-notifications

# Weekends only
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --parks 232448 \
  --nights 2 \
  --weekends-only
```

## 🏗️ Project Structure

```
recreation-gov-campsite-checker/
├── backend/
│   ├── python/              # Python campsite checking logic
│   │   ├── camping.py       # Main Python script
│   │   ├── camping_runner.py # Entry point for Node.js
│   │   ├── clients/         # Recreation.gov API client
│   │   └── ...
│   ├── server/              # Node.js Express API
│   │   ├── index.js         # Express server
│   │   ├── routes/          # API routes
│   │   └── services/        # Business logic
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom React hooks
│   │   └── App.tsx
│   └── package.json
├── myvenv/                  # Python virtual environment
└── README.md
```

## 🔧 Development

**Backend Development:**
```bash
cd backend
npm run dev  # Uses nodemon for auto-reload
```

**Frontend Development:**
```bash
cd frontend
npm run dev  # Hot-reload enabled
```

**Python Development:**
```bash
cd backend/python
source ../../myvenv/bin/activate
python camping.py --help
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python virtual environment is activated
- Check that all dependencies are installed: `npm install` in `backend/`
- Verify Python 3.9+ is installed and accessible
- Check if port 3001 is already in use

### Frontend won't connect to backend
- Ensure backend server is running on port 3001
- Check console for CORS errors
- Verify backend is accessible at `http://localhost:3001/health`

### Browser notifications not working
- Grant notification permission when prompted
- Check browser notification settings
- Some browsers block notifications in incognito mode

### Email notifications not working
- Verify environment variables are set correctly in `backend/.env`
- Check email credentials and app password
- For Gmail, ensure 2FA is enabled and you're using an app password
- Test with: `cd backend/python && python email_notifier.py`

## 📚 Additional Documentation

- **[TESTING.md](TESTING.md)** - Testing guide and checklist
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Detailed troubleshooting guide
- **[PRD.md](PRD.md)** - Product requirements and technical architecture

## 📄 License

See [LICENSE.md](LICENSE.md)

## 🙏 Acknowledgments

- Original inspiration: [bri-bri/yosemite-camping](https://github.com/bri-bri/yosemite-camping)
- Thanks to all contributors and the camping community!

## ⚠️ Disclaimer

This tool is for personal use only. Please use it responsibly and in accordance with recreation.gov's terms of service. Be courteous to other campers and don't abuse the system.

---

**Happy Camping! 🏕️**
