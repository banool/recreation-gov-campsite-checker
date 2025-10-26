# 🏕️ Recreation.gov Campsite Checker

A powerful tool to monitor campsite availability on recreation.gov with both a modern web interface and command-line support. Get notified instantly when campsites become available!

**This has been updated to work with the new recreation.gov site and API!**

> **Note:** Please don't abuse this tool. Use it responsibly and be mindful that you have an advantage over other campers who don't know how to use scrapers.

## ✨ Features

### Web Interface (NEW!)
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
- **Python 3.9+** (for the backend logic)
- **Node.js 20+** (for the web interface and API server)
- **Python virtual environment** (already set up in `myvenv/`)

### Installation

1. **Install Python Dependencies**
   ```bash
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   cd backend/python
   pip install -r requirements.txt
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   npm install
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Running the Web Application

1. **Start the Backend Server**
   ```bash
   cd backend
   npm start
   # Backend will run on http://localhost:3001
   ```

2. **Start the Frontend (in a new terminal)**
   ```bash
   cd frontend
   npm run dev
   # Frontend will run on http://localhost:5173
   ```

3. **Open Your Browser**
   Navigate to `http://localhost:5173` and start monitoring!

## 📖 Usage Guide

### Web Interface

1. **Configure Search Parameters**
   - Enter park IDs (comma or space-separated)
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

5. **Stop Monitoring**
   - Click "Stop Monitoring" when done

### Command Line Interface

The original CLI is still available in `backend/python/camping.py`:

#### Basic Usage
```bash
cd backend/python
source ../../myvenv/bin/activate

python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 232450 232447 232449 \
  --nights 2
```

#### With Detailed Campsite Info
```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --show-campsite-info \
  --nights 2
```

#### Weekends Only
```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --parks 232448 \
  --nights 2 \
  --weekends-only
```

#### Specific Campsite IDs
```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --parks 232431 \
  --campsite-ids 18621 18622 \
  --nights 2
```

#### With Email Notifications
```bash
# Set up email configuration first (see Email Setup section)
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --nights 2 \
  --email-notifications
```

## 🔍 Finding Park and Campsite IDs

### Park IDs
1. Go to [recreation.gov](https://www.recreation.gov)
2. Search for your desired campground
3. Click on the campground in the search results
4. The URL will look like: `https://www.recreation.gov/camping/campgrounds/232448`
5. The number at the end (232448) is the park ID

### Campsite IDs
1. Navigate to a specific campground on recreation.gov
2. Click on a specific campsite
3. The URL will look like: `https://www.recreation.gov/camping/campsites/18621`
4. The number at the end (18621) is the campsite ID

### Popular Park IDs
- **Yosemite Valley**
  - Upper Pines: 232450
  - Lower Pines: 232447
  - North Pines: 232449
- **Big Sur**
  - Pfeiffer Big Sur: 233116

## 📧 Email Notification Setup

To enable email notifications, set the following environment variables:

```bash
# In backend/.env (create this file)
CAMPSITE_FROM_EMAIL=your-email@gmail.com
CAMPSITE_EMAIL_PASSWORD=your-app-password
CAMPSITE_TO_EMAIL=recipient@gmail.com
CAMPSITE_SMTP_SERVER=smtp.gmail.com
CAMPSITE_SMTP_PORT=587
```

### Gmail Setup
1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the app password as `CAMPSITE_EMAIL_PASSWORD`

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed instructions.

## 🏗️ Project Structure

```
recreation-gov-campsite-checker/
├── backend/
│   ├── python/              # Python campsite checking logic
│   │   ├── camping.py       # Main Python script
│   │   ├── camping_runner.py # Entry point for Node.js
│   │   ├── clients/         # Recreation.gov API client
│   │   ├── utils/           # Utility functions
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
│   │   ├── types/           # TypeScript types
│   │   └── App.tsx
│   └── package.json
├── myvenv/                  # Python virtual environment
├── PRD.md                   # Product Requirements Document
└── README.md
```

## 🔧 Development

### Backend Development
```bash
cd backend
npm run dev  # Uses nodemon for auto-reload
```

### Frontend Development
```bash
cd frontend
npm run dev  # Hot-reload enabled
```

### Python Development
The Python code uses `black` and `isort` for formatting:
```bash
cd backend/python
black -l 80 camping.py
isort camping.py
```

### Running Tests
```bash
cd backend/python
python -m unittest
```

## 🌐 API Endpoints

The Node.js backend provides these REST API endpoints:

- `POST /api/start-monitoring` - Start monitoring with configuration
- `POST /api/stop-monitoring` - Stop active monitoring
- `GET /api/status` - Get current monitoring status
- `GET /api/stream` - Server-Sent Events stream for real-time updates
- `GET /health` - Health check endpoint

See [PRD.md](PRD.md) for detailed API documentation.

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python virtual environment is activated
- Check that all dependencies are installed: `npm install` in `backend/`
- Verify Python 3.9+ is installed and accessible

### Frontend won't connect to backend
- Ensure backend server is running on port 3001
- Check console for CORS errors
- Verify `VITE_API_URL` in frontend (defaults to `http://localhost:3001`)

### Browser notifications not working
- Grant notification permission when prompted
- Check browser notification settings
- Some browsers block notifications in incognito mode

### Email notifications not working
- Verify environment variables are set correctly
- Check email credentials and app password
- Review logs for SMTP errors

## 📝 Command Line Options

```
usage: camping.py [-h] [--debug] --start-date START_DATE --end-date END_DATE
                  [--nights NIGHTS] [--campsite-ids CAMPSITE_IDS [CAMPSITE_IDS ...]]
                  [--show-campsite-info] [--campsite-type CAMPSITE_TYPE]
                  [--json-output] [--weekends-only] [--exclusion-file EXCLUSION_FILE]
                  [--excluded-dates EXCLUDED_DATES [EXCLUDED_DATES ...]]
                  [--email-notifications]
                  (--parks park [park ...] | --stdin)

Options:
  --debug, -d           Debug log level
  --start-date          Start date [YYYY-MM-DD]
  --end-date            End date [YYYY-MM-DD]
  --nights              Number of consecutive nights (default: 1)
  --parks               Park ID(s)
  --campsite-ids        Specific campsite ID(s) (optional)
  --show-campsite-info  Display campsite ID and availability dates
  --campsite-type       Filter by campsite type (e.g., "STANDARD NONELECTRIC")
  --weekends-only       Include only weekends (Friday/Saturday starts)
  --email-notifications Send email when sites are available
```

## 🎯 Future Enhancements

- [ ] SMS notifications via Twilio
- [ ] Multiple saved search profiles
- [ ] Historical availability data and trends
- [ ] User accounts and authentication
- [ ] Scheduled monitoring (cron-like)
- [ ] Mobile app (React Native)

## 📄 License

See [LICENSE.md](LICENSE.md)

## 🙏 Acknowledgments

- Original inspiration: [bri-bri/yosemite-camping](https://github.com/bri-bri/yosemite-camping)
- Thanks to all contributors and the camping community!

## ⚠️ Disclaimer

This tool is for personal use only. Please use it responsibly and in accordance with recreation.gov's terms of service. Be courteous to other campers and don't abuse the system.

---

**Happy Camping! 🏕️**
