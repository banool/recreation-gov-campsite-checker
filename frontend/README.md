# Frontend - Recreation.gov Campsite Checker

Modern React web interface for monitoring campsite availability on recreation.gov with real-time updates and notifications.

## Prerequisites

- Node.js 20+

## Installation

```bash
npm install
```

## Running Locally

### Development Mode
```bash
npm run dev
```

The app will start on `http://localhost:5173` with hot-reload enabled.

### Production Build
```bash
npm run build
```

Builds the app for production to the `dist/` folder.

### Preview Production Build
```bash
npm run preview
```

Preview the production build locally.

## Available Scripts

- `npm run dev` - Start development server with hot-reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Configuration

The frontend expects the backend server to be running on `http://localhost:3001` by default. This is configured in `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': 'http://localhost:3001',
  },
},
```

To change the backend URL, update this configuration or set an environment variable.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ui/             # Reusable UI components (Button, Card, etc.)
│   │   ├── SearchForm.tsx  # Main search form
│   │   ├── MonitoringStatus.tsx  # Status display
│   │   ├── ResultsPanel.tsx      # Results display
│   │   └── NotificationSettings.tsx
│   ├── hooks/              # Custom React hooks
│   │   ├── useFacilitySearch.ts  # Search logic
│   │   ├── useNotifications.ts   # Notification handling
│   │   └── useSSE.ts            # Server-Sent Events
│   ├── types/              # TypeScript type definitions
│   │   └── index.ts
│   ├── lib/                # Utilities
│   │   └── utils.ts
│   ├── App.tsx             # Main app component
│   ├── App.css             # App styles
│   ├── index.css           # Global styles
│   └── main.tsx            # App entry point
├── public/                 # Static assets
├── index.html             # HTML template
├── package.json
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/ui** - Component library (Button, Card, Input, etc.)
- **Lucide React** - Icon library
- **date-fns** - Date utilities

## Features

### Real-Time Monitoring
- Live updates via Server-Sent Events (SSE)
- Countdown timer showing time until next check
- Check counter and status indicators

### Notifications
- Browser push notifications when campsites are found
- Audio alerts
- Email notifications (configured in backend)

### Search Configuration
- Multiple park IDs (comma or space-separated)
- Date range picker
- Consecutive nights filter
- Weekends-only mode
- Campsite type filter
- Specific campsite IDs

### Results Display
- Expandable park cards
- Available/total site counts
- Visual indicators (✅/❌)
- Individual campsite details with date ranges
- Direct "Book Now" links

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Frontend won't start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Cannot connect to backend

Ensure the backend is running on port 3001:

```bash
curl http://localhost:3001/health
```

Check the browser console for CORS or connection errors.

### Build errors

```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Clear dist folder
rm -rf dist

# Rebuild
npm run build
```

### Browser notifications not working

1. Check browser notification permissions
2. Ensure you're not in incognito/private mode
3. Test notification permission:
   - Open browser console
   - Run: `Notification.requestPermission()`

### Hot reload not working

1. Check that the dev server is running
2. Try refreshing the page
3. Clear browser cache
4. Restart the dev server

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Use TypeScript for type safety
3. Follow existing component patterns
4. Import and use in parent component

Example:

```tsx
// src/components/MyComponent.tsx
interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <div>
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  );
}
```

### Using Custom Hooks

Import hooks from `src/hooks/`:

```tsx
import { useNotifications } from '@/hooks/useNotifications';
import { useSSE } from '@/hooks/useSSE';
```

### Styling

Use Tailwind CSS classes for styling:

```tsx
<div className="flex items-center gap-4 p-4 rounded-lg border">
  <span className="text-sm font-medium">Status</span>
</div>
```

### TypeScript Types

Define types in `src/types/index.ts` or create component-specific type files.

## Testing

### Manual Testing

1. Start both backend and frontend
2. Fill out search form with valid data
3. Click "Start Monitoring"
4. Verify real-time updates appear
5. Check browser notifications when available sites are found

### Browser DevTools

- **Console**: Check for errors and logs
- **Network**: Monitor API calls and SSE connection
- **Application**: Check notification permissions and local storage

## Build for Production

```bash
npm run build
```

The optimized production build will be in the `dist/` folder. You can serve it with any static file server:

```bash
# Using serve (npm install -g serve)
npx serve -s dist

# Using Python
python -m http.server --directory dist 8080
```

## Environment Variables

Create a `.env` file if you need to customize settings:

```bash
# .env
VITE_API_URL=http://localhost:3001
```

Access in code:

```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```

---

For more information, see the main [README.md](../README.md)
