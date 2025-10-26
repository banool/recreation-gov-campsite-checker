# Campsite Browser Feature Guide

## Overview

We've added a dynamic campsite browser that fetches campsite information from the Recreation.gov RIDB API. This allows you to search and select specific campsites by name instead of manually entering IDs.

## How It Works

### Backend

1. **API Service** (`backend/server/services/campsiteService.js`):
   - Fetches campsites from the RIDB API for any facility/park
   - Transforms data into a clean format with ID, name, type, loop, and accessibility
   - Uses your RIDB API key: `f9140866-16e2-4636-a7e2-72e3dbb487b3`

2. **New Endpoints** (added to `backend/server/routes/monitoring.js`):
   - `GET /api/campsites/:facilityId` - Fetch all campsites for a park
   - `GET /api/facility/:facilityId` - Fetch facility/park information

### Frontend

1. **Custom Hook** (`frontend/src/hooks/useCampsites.ts`):
   - Automatically fetches campsites when a park ID is entered
   - Handles loading states and errors
   - Caches results per park ID

2. **Enhanced SearchForm** (`frontend/src/components/SearchForm.tsx`):
   - Detects when you enter a park ID
   - Automatically fetches campsites for that park
   - Shows a searchable dropdown with all available campsites
   - Allows searching by name, ID, type, or loop
   - Clicking a campsite adds its ID to the "Specific Campsite IDs" field

## Usage

### 1. Start the Backend

```bash
cd backend
npm start
```

The backend will run on `http://localhost:3001`

### 2. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

### 3. Use the Campsite Browser

1. Enter a park ID (e.g., `232448`) in the "Park IDs" field
2. The system automatically fetches campsites for that park
3. A new section appears: "Browse Campsites for Park 232448"
4. Type in the search box to filter campsites by:
   - Campsite name (e.g., "A005", "B012")
   - Campsite ID (e.g., "1293")
   - Campsite type (e.g., "STANDARD", "TENT ONLY")
   - Loop name (e.g., "A", "B")
5. Click on a campsite to add its ID to your search configuration
6. You can select multiple campsites - they'll be comma-separated

### Example Data

For park 232448, you'll see campsites like:
- **A005** (ID: 1293, Loop: A, Type: STANDARD NONELECTRIC)
- **A006** (ID: 1294, Loop: A, Type: STANDARD NONELECTRIC)
- **B012** (ID: 1175, Loop: Group, Type: GROUP TENT ONLY AREA NONELECTRIC)

## Sample API Responses

### Get Campsites

```bash
curl http://localhost:3001/api/campsites/232448
```

Response:
```json
{
  "success": true,
  "facilityId": "232448",
  "campsites": [
    {
      "id": "1290",
      "name": "A001",
      "type": "MANAGEMENT",
      "loop": "A",
      "accessible": false
    },
    ...
  ],
  "count": 311
}
```

### Get Facility Info

```bash
curl http://localhost:3001/api/facility/232448
```

## Features

✅ **Dynamic Loading** - Campsites are fetched in real-time when you enter a park ID
✅ **Fast Search** - Filter through hundreds of campsites instantly
✅ **Smart Filtering** - Search by name, ID, type, or loop
✅ **Multi-Select** - Add multiple campsites to your search
✅ **Loading States** - Shows loading indicator while fetching
✅ **Error Handling** - Graceful error messages if the API fails
✅ **No Manual IDs** - No more guessing or manually looking up campsite IDs!

## Sample Campsites Data

A static snapshot of campsites for park 232448 has been saved to:
`backend/campsites-232448.json`

This file contains 311 campsites and can be used for reference or offline testing.

## API Key Management

The RIDB API key is currently hardcoded in `campsiteService.js`. For production use:

1. Set the `RIDB_API_KEY` environment variable:
   ```bash
   export RIDB_API_KEY=f9140866-16e2-4636-a7e2-72e3dbb487b3
   ```

2. Or create a `.env` file in the `backend` directory (see `RIDB_API_SETUP.md`)

## Troubleshooting

### Backend not fetching campsites?
- Check that the backend server is running on port 3001
- Verify the API key is correct
- Check the browser console for network errors

### No campsites showing?
- Make sure you've entered a valid park ID
- Check that the park has campsites available
- Look for error messages in the browser console

### CORS errors?
- The backend has CORS enabled for all origins
- Make sure the frontend is making requests to `http://localhost:3001`

## Future Enhancements

Potential improvements:
- Cache campsite data in localStorage to reduce API calls
- Show campsite photos and descriptions
- Add filters for campsite type, accessibility, etc.
- Support searching across multiple parks at once
- Add a "favorites" feature to save commonly used campsites

