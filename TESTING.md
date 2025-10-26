# 🧪 Testing Guide

How to test the Recreation.gov Campsite Checker to ensure everything is working correctly.

## Quick Test Checklist

Use this checklist to verify the application is working properly:

- [ ] Backend server starts without errors
- [ ] Frontend starts and loads in browser
- [ ] Connection status shows "Connected"
- [ ] Can submit search form
- [ ] Monitoring starts successfully
- [ ] Status updates every 20 seconds
- [ ] Results appear in real-time
- [ ] Browser notifications work (if enabled)
- [ ] Can stop monitoring
- [ ] No console errors

## Manual Testing

### 1. Backend Server Test

```bash
# Terminal 1: Start backend
cd backend
npm start

# Expected output:
# 🚀 Campsite Checker Backend running on http://localhost:3001
# 📡 SSE endpoint: http://localhost:3001/api/stream
```

**Test health endpoint:**
```bash
curl http://localhost:3001/health
# Expected: {"status":"ok","timestamp":"..."}
```

### 2. Frontend Test

```bash
# Terminal 2: Start frontend
cd frontend
npm run dev

# Expected output:
# ➜  Local:   http://localhost:5173/
```

**Open browser and verify:**
- Page loads without errors
- UI renders correctly
- No console errors in browser DevTools

### 3. Connection Test

**Check connection status:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter by "EventStream" or look for `/api/stream`
4. Should see active connection with status 200

**Verify in UI:**
- Connection indicator should show "Connected" (green dot)

### 4. Search Form Test

**Test with valid data:**
1. Enter parks: `232448, 232450`
2. Start date: Tomorrow's date
3. End date: 7 days from start date
4. Nights: `2`
5. Click "Start Monitoring"

**Expected behavior:**
- Form submits without errors
- Monitoring status appears
- First check starts immediately
- Check counter increments

**Test validation:**
1. Try submitting with no park IDs
   - Should show error: "Please enter at least one park ID"
2. Try invalid park IDs (letters)
   - Should be filtered out
3. Try past dates
   - Should work (might not find availability)

### 5. Real-Time Updates Test

**Monitor the status display:**
- Check number should increment every ~20 seconds
- Countdown timer should count down from 20 to 0
- Timestamp should update with each check
- "Checking" state should flash during each check

**Console verification:**
```javascript
// Open browser console and watch for SSE events:
// You should see:
// SSE connection opened
// Status events every 20 seconds
// Results events after each check
```

### 6. Results Display Test

**Test with unavailable sites:**
- Use dates far in the future or fully booked dates
- Should show "No Available Campsites" for each park
- Should display ❌ icons
- Parks should be collapsible but no details to show

**Test with available sites:**
- Use a campground that typically has availability
- Or use the excluded campsites feature to filter
- Should show "Campsites Available!" banner
- Should display ✅ icons
- Should show campsite details when expanded
- Should have "Book Now" links

### 7. Notifications Test

**Browser notifications:**
1. Click "Enable Notifications" if prompted
2. Grant permission when browser asks
3. Wait for or trigger an availability result
4. Should see browser notification popup
5. Click notification to focus window

**Test notification blocking:**
1. Block notifications in browser settings
2. UI should show "Notifications Blocked" message
3. Instructions to re-enable should appear

### 8. Stop Monitoring Test

**During active monitoring:**
1. Click "Stop Monitoring" button
2. Monitoring should stop immediately
3. Status should change to "Monitoring Stopped"
4. Check counter should stop incrementing
5. Search form should become editable again

### 9. Email Notifications Test (Optional)

**Setup email:**
```bash
# Create backend/.env file with:
CAMPSITE_FROM_EMAIL=your-email@gmail.com
CAMPSITE_EMAIL_PASSWORD=your-app-password
CAMPSITE_TO_EMAIL=recipient@gmail.com
```

**Test email:**
```bash
cd backend/python
source ../../myvenv/bin/activate
python email_notifier.py
```

**In application:**
1. Enable email notifications in search form
2. Start monitoring
3. Wait for availability
4. Check email inbox
5. Verify email received with campsite details

### 10. Error Handling Test

**Test backend disconnection:**
1. Start monitoring
2. Stop backend server (Ctrl+C)
3. Frontend should show "Disconnected"
4. Restart backend
5. Browser should reconnect automatically

**Test network errors:**
1. Disconnect from internet
2. Try starting monitoring
3. Should show error: "Failed to start monitoring"
4. Reconnect internet
5. Try again - should work

**Test invalid park IDs:**
1. Enter park ID: `999999999`
2. Start monitoring
3. Should handle gracefully (might show 0/0 sites)

## Automated Testing

### Backend Tests

```bash
cd backend/python
python -m unittest discover tests
```

### Component Testing (Future)

```bash
cd frontend
npm run test
```

## Load Testing

**Test multiple simultaneous parks:**
1. Enter 10+ park IDs
2. Start monitoring
3. Monitor system resources
4. Should handle gracefully

**Test long-running monitoring:**
1. Start monitoring
2. Leave running for 1+ hours
3. Check for memory leaks
4. Verify SSE connection stays alive

## Integration Testing Scenarios

### Scenario 1: Basic Yosemite Search
```
Parks: 232448, 232450, 232447, 232449
Dates: Next month, 5 days range
Nights: 2
Expected: All parks checked, results displayed
```

### Scenario 2: Specific Campsite
```
Parks: 232448
Campsite IDs: Enter a known campsite ID
Dates: Wide range
Expected: Only specific campsite checked
```

### Scenario 3: Weekends Only
```
Parks: 232448
Dates: Entire month
Nights: 2
Weekends Only: Enabled
Expected: Only Friday/Saturday starts shown
```

### Scenario 4: Email + Browser Notifications
```
Parks: Any with likely availability
Email: Enabled
Browser: Enabled
Expected: Both notification types received
```

## Performance Benchmarks

**Expected performance:**
- Initial page load: < 2 seconds
- Form submission: < 500ms
- SSE connection: < 1 second
- Check completion: 5-10 seconds (depends on # of parks)
- UI update after result: < 100ms

**Resource usage:**
- Backend memory: < 200MB
- Frontend memory: < 100MB
- CPU: < 10% between checks, < 50% during checks

## Common Test Issues

### False Positives
- Some parks may show availability that disappears quickly
- This is normal - recreation.gov data updates frequently

### False Negatives
- Sometimes recreation.gov API is slow or returns incomplete data
- Try refreshing or checking directly on website

### Timing Issues
- First check might take longer (30-40 seconds)
- Subsequent checks should be 20 seconds apart

## Test Data

**Known working park IDs:**
- 232448 (Yosemite - Upper Pines)
- 232450 (Yosemite - Lower Pines)
- 234038 (Big Bend - Chisos Basin)
- 233116 (Pfeiffer Big Sur)

**Test dates:**
- Use dates 1-6 months in the future for best results
- Avoid current date (usually unavailable)
- Try both peak and off-peak seasons

## Reporting Bugs

When filing a bug report, include:

1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Screenshots** (if applicable)
5. **Console logs** (both browser and terminal)
6. **Environment details:**
   - OS version
   - Browser version
   - Node.js version
   - Python version

## Continuous Testing

**During development:**
1. Test after every significant change
2. Run linters: `npm run lint` (if configured)
3. Check console for warnings
4. Test in multiple browsers

**Before releasing:**
1. Run full test suite
2. Test on different OS (Mac, Windows, Linux)
3. Test in different browsers (Chrome, Firefox, Safari)
4. Verify documentation is up to date

---

**Happy Testing! 🧪**

