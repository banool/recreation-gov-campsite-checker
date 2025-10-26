# Campground Search Feature

## ✅ Feature Complete!

Search for campgrounds by name (like "Yosemite" or "Joshua Tree") instead of manually entering facility IDs.

## 🎯 What Was Built

### Backend

1. **`backend/server/services/campsiteService.js`** - Added `searchFacilities()` method
   - Searches RIDB API by query string
   - Filters to only return campgrounds (excludes day-use areas, visitor centers, etc.)
   - Returns clean data with ID, name, city, state, parent area

2. **`backend/server/routes/monitoring.js`** - Added `/api/search-facilities` endpoint
   - GET endpoint with `?query=` parameter
   - Returns array of matching campground facilities
   - Live search - results as you type

### Frontend

1. **`frontend/src/hooks/useFacilitySearch.ts`** (NEW)
   - React hook for facility search
   - Debounced search (300ms) for better UX
   - Handles loading and error states

2. **`frontend/src/components/SearchForm.tsx`** (REWRITTEN)
   - Removed campsite browser (individual sites)
   - Added campground search with live results
   - **Badge UI** - selected campgrounds show as removable badges
   - Selected campground IDs auto-populate the form
   - No manual ID entry needed!

## 🚀 How to Use

1. **Start Backend** (already running with nodemon):
   ```bash
   cd backend
   npm run dev
   ```

2. **Access the App**: http://localhost:5173

3. **Search for Campgrounds**:
   - Type "yosemite" → See 40 matching campgrounds
   - Type "joshua tree" → See Joshua Tree campgrounds
   - Type any location or campground name

4. **Select Campgrounds**:
   - Click on any result to add it
   - Selected campgrounds appear as **blue badges** below the search
   - Click the ✕ on a badge to remove it
   - Select multiple campgrounds

5. **Start Monitoring**:
   - Configure dates, nights, and options
   - Click "Start Monitoring"
   - Selected campground IDs are used automatically

## 🎨 UI Features

### Live Search
- Type at least 2 characters to search
- Results appear in a dropdown as you type
- Shows campground name, location, area, and ID
- Debounced for performance (300ms delay)

### Badge UI
- Selected campgrounds show as blue rounded badges
- Each badge has a remove button (✕)
- Count shows: "X campground(s) selected"
- Badges persist until removed

### Smart Filtering
- Only shows actual campgrounds
- Filters out:
  - Day-use areas
  - Visitor centers
  - Trailheads  
  - Other non-camping facilities

## 📊 Example Searches

### Search: "yosemite"
**Found: 40 campgrounds** including:
- Tuolumne Meadows Campground (ID: 232448)
- North Pines Campground (ID: 232449)
- Porcupine Flat Campground (ID: 10083831)
- Yosemite Creek Campground (ID: 10083840)
- Hodgdon Meadow Campground (ID: 232451)

### Search: "joshua"
Will find Joshua Tree area campgrounds

### Search: "upper pines"
Will find Upper Pines specifically

## 🔧 API Endpoint

```bash
GET /api/search-facilities?query=yosemite
```

**Response:**
```json
{
  "success": true,
  "query": "yosemite",
  "facilities": [
    {
      "id": "232448",
      "name": "Tuolumne Meadows Campground",
      "city": "",
      "state": "",
      "description": "...",
      "parentName": "",
      "type": "Campground"
    },
    ...
  ],
  "count": 40
}
```

## ✨ Benefits

- ✅ **No more manual ID lookup** - just search by name
- ✅ **Discover campgrounds** - see all options in an area
- ✅ **Multi-select** - monitor multiple campgrounds at once
- ✅ **Visual feedback** - badges show what's selected
- ✅ **Fast search** - results appear instantly
- ✅ **Smart filtering** - only real campgrounds, no clutter

## 🗑️ What Was Removed

- **Individual campsite browser** - the feature that showed campsites like "A001", "B012" within a campground
- **useCampsites hook** - no longer needed
- All related UI and code for browsing individual sites

The focus is now on selecting **campgrounds** (facilities), not individual **campsites** within them.

## 📸 User Flow

1. User opens app → sees "Search Campgrounds" field
2. Types "yosemite" → dropdown shows 40 results
3. Clicks "Tuolumne Meadows Campground" → blue badge appears
4. Clicks "North Pines Campground" → second badge appears  
5. Sets dates and options
6. Clicks "Start Monitoring" → monitors both campgrounds

No manual ID entry. No looking up facility codes. Just search and click! 🎉

## 🔑 API Key

Uses your RIDB API key: `f9140866-16e2-4636-a7e2-72e3dbb487b3`

Hardcoded in `campsiteService.js` with fallback to `process.env.RIDB_API_KEY`

## 🎊 Status

**✅ COMPLETE AND TESTED**

- Backend API working
- Frontend live search working  
- Badge UI implemented
- Multi-select working
- No linter errors
- Hot reload enabled (nodemon + Vite HMR)

Ready to use!

