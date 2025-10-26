# RIDB API Setup

This project uses the Recreation.gov RIDB (Recreation Information Database) API to fetch campsite information dynamically.

## Getting an API Key

1. Visit https://ridb.recreation.gov/
2. Click "Obtain an API Key"
3. Fill out the form with your information
4. You'll receive your API key immediately

## Setting Up the API Key

### Option 1: Environment Variable (Recommended)

Set the `RIDB_API_KEY` environment variable:

**macOS/Linux:**
```bash
export RIDB_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:RIDB_API_KEY="your-api-key-here"
```

### Option 2: .env File

Create a `.env` file in the `backend` directory:

```bash
cd backend
echo "RIDB_API_KEY=your-api-key-here" > .env
```

**Note:** The `.env` file is gitignored and will not be committed to version control.

## Current API Key

Your current API key: `f9140866-16e2-4636-a7e2-72e3dbb487b3`

**Note:** This key is currently hardcoded in `backend/server/services/campsiteService.js` as a fallback. For production use, please use environment variables instead.

## API Endpoints

### Get Campsites for a Facility

```
GET /api/campsites/:facilityId
```

Example:
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

### Get Facility Information

```
GET /api/facility/:facilityId
```

Example:
```bash
curl http://localhost:3001/api/facility/232448
```

## Rate Limits

The RIDB API has rate limits. Be mindful of the number of requests you make. Consider caching campsite data when possible.

## References

- RIDB API Documentation: https://ridb.recreation.gov/docs
- Recreation.gov: https://www.recreation.gov/

