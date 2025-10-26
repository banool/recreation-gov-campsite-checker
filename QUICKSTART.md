# 🚀 Quick Start Guide

Get the Recreation.gov Campsite Checker up and running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 20+ installed
- Terminal/Command Prompt

## Step-by-Step Setup

### 1. Activate Python Environment

```bash
# From the project root
source myvenv/bin/activate

# On Windows:
# myvenv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install Python dependencies (if needed)
cd backend/python
pip install -r requirements.txt
cd ../..

# Install backend dependencies
cd backend
npm install
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Start the Backend

```bash
# From the backend directory
cd backend
npm start

# You should see:
# 🚀 Campsite Checker Backend running on http://localhost:3001
```

Keep this terminal open!

### 4. Start the Frontend (New Terminal)

```bash
# From the frontend directory
cd frontend
npm run dev

# You should see:
# ➜  Local:   http://localhost:5173/
```

### 5. Open Your Browser

Navigate to **http://localhost:5173**

## First Search

1. **Enter Park IDs**: Try `232448, 232450` (Yosemite campgrounds)
2. **Set Dates**: Choose dates at least a week out
3. **Set Nights**: Enter `2` for a 2-night stay
4. **Enable Notifications**: Click "Enable Notifications" if prompted
5. **Click "Start Monitoring"**: Watch the magic happen! 🎉

## Stopping

- Press `Ctrl+C` in both terminal windows to stop the servers
- Use the "Stop Monitoring" button in the UI before closing

## Finding Park IDs

1. Go to [recreation.gov](https://www.recreation.gov)
2. Search for a campground (e.g., "Yosemite")
3. Click on a campground
4. Copy the number from the URL: `recreation.gov/camping/campgrounds/[NUMBER]`

## Common Issues

### Backend won't start
- Make sure Python virtual environment is activated
- Check that port 3001 is not in use

### Frontend can't connect
- Verify backend is running on port 3001
- Check browser console for errors

### No notifications
- Click "Enable Notifications" when prompted
- Check browser notification settings

## Need Help?

See the full [README.md](README.md) for detailed documentation, troubleshooting, and advanced usage.

---

**Happy Camping! 🏕️**

