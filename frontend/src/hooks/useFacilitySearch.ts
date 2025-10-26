import { useState, useEffect } from 'react';

export interface Facility {
  id: string;
  name: string;
  city: string;
  state: string;
  description: string;
  parentName: string;
  type: string;
}

interface FacilitySearchResponse {
  success: boolean;
  query: string;
  facilities: Facility[];
  count: number;
}

export function useFacilitySearch(query: string) {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Don't search if query is too short
    if (!query || query.trim().length < 2) {
      setFacilities([]);
      setError(null);
      setLoading(false);
      return;
    }

    // Debounce the search
    const timeoutId = setTimeout(async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `http://localhost:3001/api/search-facilities?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
          throw new Error(`Failed to search facilities: ${response.statusText}`);
        }

        const data: FacilitySearchResponse = await response.json();

        if (data.success) {
          setFacilities(data.facilities);
        } else {
          throw new Error('Failed to search facilities');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setFacilities([]);
      } finally {
        setLoading(false);
      }
    }, 300); // 300ms debounce

    // Cleanup function
    return () => clearTimeout(timeoutId);
  }, [query]);

  return { facilities, loading, error };
}

