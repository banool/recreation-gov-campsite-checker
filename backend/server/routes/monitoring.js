import express from 'express';
import monitoringService from '../services/monitoringService.js';
import campsiteService from '../services/campsiteService.js';

const router = express.Router();

/**
 * POST /api/start-monitoring
 * Start monitoring with the provided configuration
 */
router.post('/start-monitoring', (req, res) => {
  try {
    const config = req.body;

    // Validate required fields
    if (!config.parks || !Array.isArray(config.parks) || config.parks.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Parks array is required and must not be empty',
      });
    }

    if (!config.startDate || !config.endDate) {
      return res.status(400).json({
        success: false,
        error: 'Start date and end date are required',
      });
    }

    const result = monitoringService.startMonitoring(config);
    res.json(result);
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error.message,
    });
  }
});

/**
 * POST /api/stop-monitoring
 * Stop the currently running monitoring job
 */
router.post('/stop-monitoring', (req, res) => {
  const result = monitoringService.stopMonitoring();
  res.json(result);
});

/**
 * GET /api/status
 * Get current monitoring status
 */
router.get('/status', (req, res) => {
  const status = monitoringService.getStatus();
  res.json(status);
});

/**
 * GET /api/stream
 * Server-Sent Events endpoint for real-time updates
 */
router.get('/stream', (req, res) => {
  // Set headers for SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Add client to monitoring service
  monitoringService.addClient(res);

  // Handle client disconnect
  req.on('close', () => {
    monitoringService.removeClient(res);
  });
});

/**
 * GET /api/search-facilities
 * Search for campground facilities by name
 */
router.get('/search-facilities', async (req, res) => {
  try {
    const { query } = req.query;
    
    if (!query) {
      return res.json({
        success: true,
        facilities: [],
        count: 0
      });
    }

    const facilities = await campsiteService.searchFacilities(query);
    
    res.json({
      success: true,
      query,
      facilities,
      count: facilities.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/campsites/:facilityId
 * Fetch all campsites for a given facility/park
 */
router.get('/campsites/:facilityId', async (req, res) => {
  try {
    const { facilityId } = req.params;
    
    if (!facilityId) {
      return res.status(400).json({
        success: false,
        error: 'Facility ID is required'
      });
    }

    const campsites = await campsiteService.getCampsitesForFacility(facilityId);
    
    res.json({
      success: true,
      facilityId,
      campsites,
      count: campsites.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/facility/:facilityId
 * Fetch facility information
 */
router.get('/facility/:facilityId', async (req, res) => {
  try {
    const { facilityId } = req.params;
    
    if (!facilityId) {
      return res.status(400).json({
        success: false,
        error: 'Facility ID is required'
      });
    }

    const facilityInfo = await campsiteService.getFacilityInfo(facilityId);
    
    res.json({
      success: true,
      facility: facilityInfo
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;

