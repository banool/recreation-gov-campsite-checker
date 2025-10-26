# Backend - Recreation.gov Campsite Checker

Node.js Express server that coordinates the Python campsite checking logic and provides a REST API and Server-Sent Events (SSE) for the frontend.

## Prerequisites

- Node.js 20+
- Python 3.9+

## Installation

```bash
# Install Node.js dependencies
npm install

# This will automatically set up the Python virtual environment
# and install Python dependencies during the postinstall script
```

## Configuration

Create a `.env` file in the `backend/` directory for email notifications (optional):

```bash
# backend/.env
CAMPSITE_FROM_EMAIL=your-email@gmail.com
CAMPSITE_EMAIL_PASSWORD=your-app-password
CAMPSITE_TO_EMAIL=recipient@gmail.com
CAMPSITE_SMTP_SERVER=smtp.gmail.com
CAMPSITE_SMTP_PORT=587
```

## Running Locally

### Production Mode
```bash
npm start
```

The server will start on `http://localhost:3001`

### Development Mode (with auto-reload)
```bash
npm run dev
```

Uses nodemon to automatically restart when files change.

## Available Scripts

- `npm start` - Start the production server
- `npm run dev` - Start the development server with auto-reload
- `npm test` - Run tests (if configured)

## API Endpoints

### Health Check
```
GET /health
```

Returns server status.

### Start Monitoring
```
POST /api/start-monitoring
Content-Type: application/json

{
  "parks": [232448, 232450],
  "startDate": "2025-06-01",
  "endDate": "2025-06-05",
  "nights": 2,
  "weekendsOnly": false,
  "campsiteType": "",
  "campsiteIds": [],
  "emailNotifications": true
}
```

### Stop Monitoring
```
POST /api/stop-monitoring
```

### Get Status
```
GET /api/status
```

### Server-Sent Events Stream
```
GET /api/stream
```

Real-time updates for monitoring status and results.

## Project Structure

```
backend/
├── server/
│   ├── index.js                 # Express server entry point
│   ├── routes/
│   │   └── monitoring.js        # API routes
│   └── services/
│       ├── campsiteService.js   # Python process management
│       └── monitoringService.js # Monitoring logic
├── python/
│   ├── camping.py               # Main Python script
│   ├── camping_runner.py        # Node.js entry point
│   ├── clients/                 # Recreation.gov API client
│   ├── utils/                   # Utility functions
│   └── requirements.txt         # Python dependencies
├── package.json
└── .env                         # Environment variables (create this)
```

## Python Integration

The Node.js server spawns Python processes to perform the actual campsite checking. The Python virtual environment is located at `../../myvenv/` relative to the backend directory.

### Manual Python Setup (if needed)

```bash
# Activate virtual environment
source ../myvenv/bin/activate  # On Windows: ..\myvenv\Scripts\activate

# Install Python dependencies
cd python
pip install -r requirements.txt
```

### Running Python Script Directly

```bash
cd python
source ../../myvenv/bin/activate

python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --nights 2
```

## Troubleshooting

### Port Already in Use

If port 3001 is already in use:

```bash
# macOS/Linux
lsof -i :3001
kill -9 <PID>

# Windows
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

### Python Virtual Environment Not Found

```bash
# Create virtual environment
cd ..
python3 -m venv myvenv
source myvenv/bin/activate
cd backend/python
pip install -r requirements.txt
```

### Python Script Errors

Ensure Python 3.9+ is installed and accessible:

```bash
python --version
# or
python3 --version
```

### Module Import Errors

Ensure the virtual environment is activated and dependencies are installed:

```bash
source ../myvenv/bin/activate
cd python
pip install -r requirements.txt
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 3001 |
| `CAMPSITE_FROM_EMAIL` | Sender email address | - |
| `CAMPSITE_EMAIL_PASSWORD` | Email app password | - |
| `CAMPSITE_TO_EMAIL` | Recipient email address | - |
| `CAMPSITE_SMTP_SERVER` | SMTP server | smtp.gmail.com |
| `CAMPSITE_SMTP_PORT` | SMTP port | 587 |

## Development

### Adding New API Endpoints

1. Add route handler in `server/routes/monitoring.js`
2. Implement business logic in `server/services/`
3. Update frontend to call new endpoint

### Modifying Python Integration

- Python entry point: `python/camping_runner.py`
- Service handling Python processes: `server/services/campsiteService.js`

## Testing

```bash
# Test health endpoint
curl http://localhost:3001/health

# Test monitoring (with server running)
curl -X POST http://localhost:3001/api/start-monitoring \
  -H "Content-Type: application/json" \
  -d '{
    "parks": [232448],
    "startDate": "2025-06-01",
    "endDate": "2025-06-05",
    "nights": 2
  }'
```

## Logs

The server logs to stdout. In production, consider using a logging service or redirecting to a file:

```bash
npm start > backend.log 2>&1
```

---

For more information, see the main [README.md](../README.md)

