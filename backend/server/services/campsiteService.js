import axios from 'axios';

const RIDB_API_KEY = process.env.RIDB_API_KEY || 'f9140866-16e2-4636-a7e2-72e3dbb487b3';
const RIDB_BASE_URL = 'https://ridb.recreation.gov/api/v1';

class CampsiteService {
  /**
   * Fetch all campsites for a given facility/park ID
   * @param {string|number} facilityId - The facility/park ID
   * @returns {Promise<Array>} Array of campsite objects
   */
  async getCampsitesForFacility(facilityId) {
    try {
      const url = `${RIDB_BASE_URL}/facilities/${facilityId}/campsites`;
      const response = await axios.get(url, {
        headers: {
          'accept': 'application/json',
          'apikey': RIDB_API_KEY
        },
        params: {
          limit: 500 // Get up to 500 campsites
        }
      });

      const campsites = response.data.RECDATA || [];
      
      // Transform to a simpler format
      return campsites.map(site => ({
        id: String(site.CampsiteID),
        name: site.CampsiteName || 'Unknown',
        type: site.CampsiteType || 'Unknown',
        loop: site.Loop || 'Unknown',
        accessible: site.CampsiteAccessible || false,
      })).sort((a, b) => {
        // Sort by loop first, then by name
        if (a.loop !== b.loop) {
          return a.loop.localeCompare(b.loop);
        }
        return a.name.localeCompare(b.name);
      });
    } catch (error) {
      console.error(`Error fetching campsites for facility ${facilityId}:`, error.message);
      throw new Error(`Failed to fetch campsites: ${error.message}`);
    }
  }

  /**
   * Fetch facility information
   * @param {string|number} facilityId - The facility/park ID
   * @returns {Promise<Object>} Facility information
   */
  async getFacilityInfo(facilityId) {
    try {
      const url = `${RIDB_BASE_URL}/facilities/${facilityId}`;
      const response = await axios.get(url, {
        headers: {
          'accept': 'application/json',
          'apikey': RIDB_API_KEY
        }
      });

      return {
        id: String(response.data.FacilityID),
        name: response.data.FacilityName || 'Unknown',
        description: response.data.FacilityDescription || '',
      };
    } catch (error) {
      console.error(`Error fetching facility info for ${facilityId}:`, error.message);
      throw new Error(`Failed to fetch facility info: ${error.message}`);
    }
  }

  /**
   * Search for campground facilities by name
   * @param {string} query - Search query (e.g., "Yosemite", "Joshua Tree")
   * @returns {Promise<Array>} Array of matching campground facilities
   */
  async searchFacilities(query) {
    try {
      if (!query || query.trim().length < 2) {
        return [];
      }

      const url = `${RIDB_BASE_URL}/facilities`;
      const response = await axios.get(url, {
        headers: {
          'accept': 'application/json',
          'apikey': RIDB_API_KEY
        },
        params: {
          query: query.trim(),
          limit: 200, // Increased to get more results before filtering
          full: 'true'
        }
      });

      const facilities = response.data.RECDATA || [];
      
      // Filter to only include campgrounds (exclude day use areas, visitor centers, etc.)
      const campgrounds = facilities.filter(facility => {
        const type = (facility.FacilityTypeDescription || '').toLowerCase();
        const name = (facility.FacilityName || '').toLowerCase();
        
        // Include if it's explicitly a campground or has camping in the name
        return type.includes('campground') || 
               type.includes('camping') ||
               name.includes('campground') ||
               name.includes('camp area');
      });

      // Transform to a simpler format
      const results = campgrounds.map(facility => ({
        id: String(facility.FacilityID),
        name: facility.FacilityName || 'Unknown',
        city: facility.FacilityAddrCity || '',
        state: facility.FacilityAddrStateCode || '',
        description: facility.FacilityDescription || '',
        parentName: facility.ParentRecAreaName || '',
        parentRecAreaId: facility.ParentRecAreaID || null,
        type: facility.FacilityTypeDescription || 'Campground',
      }));

      // Sort by relevance to search query
      return this._sortByRelevance(results, query);
    } catch (error) {
      console.error(`Error searching facilities for "${query}":`, error.message);
      throw new Error(`Failed to search facilities: ${error.message}`);
    }
  }

  /**
   * Calculate relevance score for a facility based on search query
   * Higher score = more relevant
   * @param {Object} facility - Facility object with name, city, state, etc.
   * @param {string} query - Search query string
   * @returns {number} Relevance score
   */
  _calculateRelevance(facility, query) {
    const queryLower = query.toLowerCase().trim();
    const nameLower = facility.name.toLowerCase();
    const descLower = (facility.description || '').toLowerCase();
    const words = queryLower.split(/\s+/);
    
    let score = 0;

    // Check if the description explicitly mentions being IN or AT the searched location
    // This is the strongest signal that it's actually in that park/area
    const inLocationPatterns = [
      `in ${queryLower}`,
      `at ${queryLower}`,
      `within ${queryLower}`,
      `${queryLower} national park`,
      `${queryLower} national forest`,
      `${queryLower} state park`,
    ];
    
    for (const pattern of inLocationPatterns) {
      if (descLower.includes(pattern)) {
        // HUGE boost for facilities explicitly described as being IN the location
        score += 10000;
        break;
      }
    }

    // Exact match in name (highest priority for name matching)
    if (nameLower === queryLower) {
      score += 1000;
    }

    // Name starts with query
    if (nameLower.startsWith(queryLower)) {
      score += 500;
    }

    // Name contains query as whole phrase
    if (nameLower.includes(queryLower)) {
      score += 200;
    }

    // Check each word in the query
    for (const word of words) {
      if (word.length < 2) continue; // Skip very short words
      
      // Word appears at start of name
      if (nameLower.startsWith(word)) {
        score += 100;
      }
      
      // Word appears as complete word in name
      const wordBoundaryRegex = new RegExp(`\\b${word}\\b`, 'i');
      if (wordBoundaryRegex.test(nameLower)) {
        score += 50;
      }
      
      // Word appears anywhere in name (partial match)
      if (nameLower.includes(word)) {
        score += 10;
      }
      
      // Check if word appears multiple times in description (indicates relevance)
      const wordMatches = (descLower.match(new RegExp(word, 'g')) || []).length;
      if (wordMatches > 2) {
        score += 50; // Boost if word appears frequently in description
      }
    }

    // Bonus for shorter names (more specific matches)
    if (nameLower.length < 30) {
      score += 5;
    }

    // Bonus for parent area name match
    if (facility.parentName && facility.parentName.toLowerCase().includes(queryLower)) {
      score += 100;
    }

    return score;
  }

  /**
   * Sort facilities by relevance to search query
   * @param {Array} facilities - Array of facility objects
   * @param {string} query - Search query string
   * @returns {Array} Sorted array of facilities
   */
  _sortByRelevance(facilities, query) {
    return facilities.sort((a, b) => {
      const scoreA = this._calculateRelevance(a, query);
      const scoreB = this._calculateRelevance(b, query);
      
      // First sort by relevance score (descending)
      if (scoreB !== scoreA) {
        return scoreB - scoreA;
      }
      
      // If scores are equal, sort alphabetically by name
      return a.name.localeCompare(b.name);
    });
  }
}

export default new CampsiteService();

