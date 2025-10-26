# Product Requirements Document (PRD)
## Recreation.gov Campsite Checker - Web Application

### 1. Overview
Transform the existing Python CLI campsite checker into a modern web application with real-time monitoring capabilities. Users can configure search parameters through an intuitive UI, start continuous monitoring, and receive instant notifications when campsites become available.

### 2. Goals & Objectives
- Provide a user-friendly web interface for configuring campsite searches
- Enable real-time monitoring with live status updates
- Support multiple notification channels (email, browser push)
- Maintain existing Python logic with minimal changes
- Create a scalable monorepo architecture for future enhancements

### 3. User Stories
- **As a camper**, I want to select multiple parks from a searchable list so I can monitor my preferred campgrounds
- **As a user**, I want to specify date ranges and number of nights so I can find available consecutive bookings
- **As a user**, I want to see live updates of each check cycle so I know the system is working
- **As a user**, I want to start/stop monitoring with a single click so I have control over the process
- **As a user**, I want browser notifications when sites are available so I can book immediately
- **As a user**, I want to see detailed campsite information and direct booking links when availability is found

### 4. Technical Architecture

#### Monorepo Structure
```
recreation-gov-campsite-checker/
├── backend/
│   ├── python/              # Existing Python code
│   │   ├── camping.py
│   │   ├── clients/
│   │   ├── utils/
│   │   ├── enums/
│   │   └── ...
│   ├── server/              # Node.js/Express API
│   │   ├── index.js
│   │   ├── routes/
│   │   └── services/
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── PRD.md
└── README.md
```

#### Tech Stack
- **Frontend**: React 18 + TypeScript + Vite
- **UI Library**: Shadcn/ui + Tailwind CSS (most popular, highly customizable)
- **Backend**: Node.js + Express
- **Real-time Communication**: Server-Sent Events (SSE) for live updates
- **Python Integration**: Child process spawning from Node.js
- **Notifications**: Browser Push API + existing email system

### 5. Features (MVP)

#### 5.1 Search Configuration Form
- Park ID input (multiple, comma-separated or list)
- Date range picker (start date, end date)
- Number of consecutive nights selector
- Optional filters:
  - Weekends only toggle
  - Campsite type dropdown
  - Specific campsite IDs
  - Excluded dates picker
- Email notifications toggle (if configured)
- Browser notifications toggle

#### 5.2 Real-Time Monitoring
- "Start Monitoring" button initiates continuous checking (20-second intervals)
- "Stop Monitoring" button cancels the process
- Live status display:
  - Current check number
  - Last check timestamp
  - Time until next check (countdown)
  - Monitoring state indicator (running/stopped)

#### 5.3 Results Display
- Real-time results panel showing:
  - Park name with availability count
  - Available/total sites ratio
  - Visual indicators (✅/❌)
  - Expandable details per park showing:
    - Individual campsite IDs
    - Available date ranges
    - Direct booking links

#### 5.4 Notifications
- Browser push notifications on availability (with user permission)
- Email notifications (using existing Python email system)
- Audio alert (system sound, as in current implementation)
- Notification history in UI

### 6. Non-Functional Requirements
- **Performance**: UI updates within 100ms of receiving data
- **Reliability**: Automatic recovery from API failures
- **Usability**: Mobile-responsive design
- **Accessibility**: WCAG 2.1 AA compliance with Shadcn/ui

### 7. Future Enhancements (Post-MVP)
- SMS notifications via Twilio
- Multiple search profiles with saved configurations
- Historical availability data and trends
- Multi-user support with authentication
- Scheduled monitoring (cron-like scheduling)

### 8. API Endpoints

#### POST /api/start-monitoring
Starts continuous monitoring with specified parameters.

**Request Body:**
```json
{
  "parks": [232448, 232450],
  "startDate": "2025-06-01",
  "endDate": "2025-06-05",
  "nights": 2,
  "weekendsOnly": false,
  "campsiteType": "STANDARD NONELECTRIC",
  "campsiteIds": [],
  "excludedDates": [],
  "emailNotifications": true,
  "browserNotifications": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Monitoring started",
  "jobId": "uuid"
}
```

#### POST /api/stop-monitoring
Stops the currently running monitoring job.

**Response:**
```json
{
  "success": true,
  "message": "Monitoring stopped"
}
```

#### GET /api/status
Gets the current monitoring status.

**Response:**
```json
{
  "isRunning": true,
  "checkCount": 15,
  "lastCheckTime": "2025-10-25T10:30:00Z",
  "config": { ... }
}
```

#### GET /api/stream
Server-Sent Events endpoint for real-time updates.

**Event Types:**
```
event: status
data: {"state": "checking", "checkNumber": 5, "timestamp": "..."}

event: results
data: {"parks": {...}, "hasAvailability": true, "timestamp": "..."}

event: error
data: {"message": "Error description"}
```

### 9. Data Models

#### MonitoringConfig
```typescript
interface MonitoringConfig {
  parks: number[];
  startDate: string;        // YYYY-MM-DD
  endDate: string;          // YYYY-MM-DD
  nights: number;
  weekendsOnly: boolean;
  campsiteType?: string;
  campsiteIds?: number[];
  excludedDates?: string[];
  emailNotifications: boolean;
  browserNotifications: boolean;
}
```

#### ParkAvailability
```typescript
interface ParkAvailability {
  parkId: string;
  parkName: string;
  current: number;
  maximum: number;
  availableSites: {
    [siteId: string]: {
      start: string;
      end: string;
    }[];
  };
}
```

#### MonitoringResult
```typescript
interface MonitoringResult {
  timestamp: string;
  checkNumber: number;
  parks: ParkAvailability[];
  hasAvailability: boolean;
}
```

### 10. Security Considerations
- No authentication required (single-user system)
- Email credentials stored in environment variables
- No sensitive data persistence
- CORS configuration for local development
- Input validation on all API endpoints

### 11. Deployment
- **Development**: Local development with hot-reload
- **Production**: Can be deployed to any Node.js hosting platform
- **Python Environment**: Requires Python 3.9+ with dependencies installed
- **Environment Variables**: Email configuration via .env file

### 12. Success Metrics
- User can configure and start monitoring in < 30 seconds
- Real-time updates appear within 1 second of completion
- Browser notifications delivered within 2 seconds of availability detection
- Zero missed availability checks during monitoring
- Mobile-responsive UI works on all major browsers

