import { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card';
import { Input } from './ui/Input';
import { Label } from './ui/Label';
import { Button } from './ui/Button';
import { Select } from './ui/Select';
import type { MonitoringConfig } from '../types/index';
import { format } from 'date-fns';
import { useFacilitySearch } from '../hooks/useFacilitySearch';
import { X } from 'lucide-react';
import { CAMPSITE_TYPES } from '../constants/campsiteTypes';

interface SearchFormProps {
  onSubmit: (config: MonitoringConfig) => void;
  isMonitoring: boolean;
}

interface SelectedFacility {
  id: string;
  name: string;
}

export function SearchForm({ onSubmit, isMonitoring }: SearchFormProps) {
  const [startDate, setStartDate] = useState<string>(
    format(new Date(), 'yyyy-MM-dd')
  );
  const [endDate, setEndDate] = useState<string>(
    format(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd')
  );
  const [nights, setNights] = useState<number>(2);
  const [weekendsOnly, setWeekendsOnly] = useState<boolean>(false);
  const [campsiteType, setCampsiteType] = useState<string>('');
  const [campsiteIds, setCampsiteIds] = useState<string>('');
  const [emailNotifications, setEmailNotifications] = useState<boolean>(false);
  const [browserNotifications, setBrowserNotifications] = useState<boolean>(true);

  // Campground search
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedFacilities, setSelectedFacilities] = useState<SelectedFacility[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Excluded dates
  const [excludedDates, setExcludedDates] = useState<string[]>([]);

  // Track if we've loaded from URL to prevent overwriting
  const [hasLoadedFromUrl, setHasLoadedFromUrl] = useState(false);

  // Use the facility search hook
  const { facilities, loading } = useFacilitySearch(searchQuery);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [showDropdown]);

  // Load state from URL params on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    
    if (params.has('campgrounds')) {
      const ids = params.get('campgrounds')!.split(',');
      const names = params.has('campgroundNames') ? params.get('campgroundNames')!.split(',') : ids;
      const facilities = ids.map((id, idx) => ({
        id: id.trim(),
        name: names[idx]?.trim() || `Campground ${id}`
      }));
      setSelectedFacilities(facilities);
    }
    
    if (params.has('start')) {
      setStartDate(params.get('start')!);
    }
    
    if (params.has('end')) {
      setEndDate(params.get('end')!);
    }
    
    if (params.has('nights')) {
      setNights(parseInt(params.get('nights')!));
    }
    
    if (params.has('weekends')) {
      setWeekendsOnly(params.get('weekends') === 'true');
    }
    
    if (params.has('type')) {
      setCampsiteType(params.get('type')!);
    }
    
    if (params.has('campsiteIds')) {
      setCampsiteIds(params.get('campsiteIds')!);
    }
    
    if (params.has('email')) {
      setEmailNotifications(params.get('email') === 'true');
    }
    
    if (params.has('browser')) {
      setBrowserNotifications(params.get('browser') === 'true');
    }

    if (params.has('excludedDates')) {
      const dates = params.get('excludedDates')!.split(',').map(d => d.trim());
      setExcludedDates(dates);
    }

    // Mark that we've loaded from URL
    setHasLoadedFromUrl(true);
  }, []); // Only run on mount

  // Sync form state to URL params whenever it changes (but skip on initial mount)
  useEffect(() => {
    // Skip URL sync until we've loaded from URL first
    if (!hasLoadedFromUrl) {
      return;
    }
    const params = new URLSearchParams();
    
    if (selectedFacilities.length > 0) {
      params.set('campgrounds', selectedFacilities.map(f => f.id).join(','));
      params.set('campgroundNames', selectedFacilities.map(f => f.name).join(','));
    }
    
    if (startDate) params.set('start', startDate);
    if (endDate) params.set('end', endDate);
    if (nights) params.set('nights', nights.toString());
    if (weekendsOnly) params.set('weekends', 'true');
    if (campsiteType) params.set('type', campsiteType);
    if (campsiteIds) params.set('campsiteIds', campsiteIds);
    if (emailNotifications) params.set('email', 'true');
    if (!browserNotifications) params.set('browser', 'false'); // Only set if false since true is default
    if (excludedDates.length > 0) params.set('excludedDates', excludedDates.join(','));
    
    // Update URL without triggering navigation
    const newUrl = params.toString() ? `${window.location.pathname}?${params.toString()}` : window.location.pathname;
    window.history.replaceState({}, '', newUrl);
  }, [hasLoadedFromUrl, selectedFacilities, startDate, endDate, nights, weekendsOnly, campsiteType, campsiteIds, emailNotifications, browserNotifications, excludedDates]);

  const handleFacilitySelect = (facility: { id: string; name: string }) => {
    // Don't add duplicates
    if (!selectedFacilities.find(f => f.id === facility.id)) {
      setSelectedFacilities([...selectedFacilities, facility]);
    }
    // Keep dropdown open with current search results - don't clear searchQuery
    // User can manually clear or type new search if they want
  };

  const handleRemoveFacility = (facilityId: string) => {
    setSelectedFacilities(selectedFacilities.filter(f => f.id !== facilityId));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Use selected facilities' IDs as park IDs
    const parkIds = selectedFacilities.map(f => parseInt(f.id));

    if (parkIds.length === 0) {
      alert('Please search and select at least one campground');
      return;
    }

    // Parse campsite IDs if provided
    const siteIds = campsiteIds
      ? campsiteIds
          .split(/[\s,]+/)
          .map((id) => parseInt(id.trim()))
          .filter((id) => !isNaN(id))
      : [];

    const config: MonitoringConfig = {
      parks: parkIds,
      startDate,
      endDate,
      nights,
      weekendsOnly,
      campsiteType: campsiteType || undefined,
      campsiteIds: siteIds.length > 0 ? siteIds : undefined,
      excludedDates: excludedDates.length > 0 ? excludedDates : undefined,
      emailNotifications,
      browserNotifications,
    };

    onSubmit(config);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Search Configuration</CardTitle>
        <CardDescription>
          Search for campgrounds and configure your monitoring parameters
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Campground Search */}
          <div className="space-y-3 border-b pb-4">
            <Label htmlFor="campgroundSearch">
              Search Campgrounds <span className="text-red-500">*</span>
            </Label>
            <div className="relative" ref={dropdownRef}>
              <Input
                id="campgroundSearch"
                placeholder="Type to search (e.g., 'Yosemite', 'Joshua Tree')..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setShowDropdown(e.target.value.length > 0);
                }}
                onFocus={() => setShowDropdown(searchQuery.length > 0)}
                disabled={isMonitoring}
              />

              {/* Dropdown with search results */}
              {showDropdown && searchQuery.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-80 overflow-y-auto">
                  {/* Close button */}
                  <div className="sticky top-0 bg-gray-50 border-b border-gray-200 px-3 py-2 flex items-center justify-between">
                    <span className="text-xs text-gray-600 font-medium">
                      Click to select (dropdown stays open)
                    </span>
                    <button
                      type="button"
                      onClick={() => setShowDropdown(false)}
                      className="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-200"
                      title="Close"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                  <div>
                    {loading ? (
                      <div className="px-4 py-3 text-sm text-gray-500">
                        Searching...
                      </div>
                    ) : facilities.length > 0 ? (
                      facilities.map((facility) => {
                        const isSelected = selectedFacilities.some(f => f.id === facility.id);
                        return (
                          <button
                            key={facility.id}
                            type="button"
                            onClick={() => handleFacilitySelect(facility)}
                            disabled={isSelected}
                            className={`w-full px-4 py-3 text-left border-b border-gray-100 last:border-b-0 ${
                              isSelected 
                                ? 'bg-blue-50 opacity-60 cursor-not-allowed' 
                                : 'hover:bg-gray-100 focus:bg-gray-100'
                            } focus:outline-none`}
                          >
                            <div className="font-medium text-sm flex items-center gap-2">
                              {facility.name}
                              {isSelected && (
                                <span className="text-xs text-blue-600 font-normal">✓ Selected</span>
                              )}
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                              {facility.city && facility.state && (
                                <span>{facility.city}, {facility.state}</span>
                              )}
                              {facility.parentName && (
                                <span className="ml-2">• {facility.parentName}</span>
                              )}
                            </div>
                            <div className="text-xs text-gray-400 mt-1">
                              ID: {facility.id}
                            </div>
                          </button>
                        );
                      })
                    ) : (
                      <div className="px-4 py-3 text-sm text-gray-500">
                        No campgrounds found. Try a different search term.
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Selected Facilities Badges */}
            {selectedFacilities.length > 0 && (
              <div className="flex flex-wrap gap-2 pt-2">
                {selectedFacilities.map((facility) => (
                  <div
                    key={facility.id}
                    className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    <span className="font-medium">{facility.name}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveFacility(facility.id)}
                      disabled={isMonitoring}
                      className="hover:bg-blue-200 rounded-full p-0.5 transition-colors disabled:opacity-50"
                      aria-label="Remove campground"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}

            <p className="text-xs text-gray-500">
              {selectedFacilities.length === 0
                ? 'Start typing to search for campgrounds'
                : `${selectedFacilities.length} campground(s) selected`}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="nights">
                Number of Nights <span className="text-red-500">*</span>
              </Label>
              <Input
                id="nights"
                type="number"
                min="1"
                value={nights}
                onChange={(e) => setNights(parseInt(e.target.value))}
                disabled={isMonitoring}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="startDate">
                Start Date <span className="text-red-500">*</span>
              </Label>
              <Input
                id="startDate"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                disabled={isMonitoring}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="endDate">
                End Date <span className="text-red-500">*</span>
              </Label>
              <Input
                id="endDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                disabled={isMonitoring}
                required
              />
            </div>

            {/* Excluded Dates */}
            <div className="space-y-2">
              <Label htmlFor="excludedDate">
                Exclude Specific Dates (Optional)
              </Label>
              <Input
                id="excludedDate"
                type="date"
                min={startDate}
                max={endDate}
                onChange={(e) => {
                  const date = e.target.value;
                  if (date && !excludedDates.includes(date)) {
                    setExcludedDates([...excludedDates, date]);
                  }
                  // Reset the input
                  e.target.value = '';
                }}
                disabled={isMonitoring}
              />
              <p className="text-xs text-gray-500">
                Click to select dates within your range to exclude from the search
              </p>

              {/* Excluded Dates Badges */}
              {excludedDates.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-2">
                  {excludedDates.map((date) => (
                    <div
                      key={date}
                      className="inline-flex items-center gap-2 px-3 py-1.5 bg-red-100 text-red-800 rounded-full text-sm"
                    >
                      <span className="font-medium">{format(new Date(date + 'T00:00:00'), 'MMM d, yyyy')}</span>
                      <button
                        type="button"
                        onClick={() => setExcludedDates(excludedDates.filter(d => d !== date))}
                        disabled={isMonitoring}
                        className="hover:bg-red-200 rounded-full p-0.5 transition-colors disabled:opacity-50"
                        title="Remove"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="campsiteType">Campsite Type (Optional)</Label>
              <Select
                id="campsiteType"
                value={campsiteType}
                onChange={(e) => setCampsiteType(e.target.value)}
                disabled={isMonitoring}
              >
                {CAMPSITE_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </Select>
              <p className="text-xs text-gray-500">
                Filter by specific campsite type (leave as "Any" to see all types)
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="campsiteIds">
                Specific Campsite IDs (Optional)
              </Label>
              <Input
                id="campsiteIds"
                placeholder="18621, 18622"
                value={campsiteIds}
                onChange={(e) => setCampsiteIds(e.target.value)}
                disabled={isMonitoring}
              />
              <p className="text-xs text-gray-500">
                Leave empty for all campsites
              </p>
            </div>
          </div>

          <div className="space-y-3 border-t pt-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="weekendsOnly"
                checked={weekendsOnly}
                onChange={(e) => setWeekendsOnly(e.target.checked)}
                disabled={isMonitoring}
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <Label htmlFor="weekendsOnly" className="cursor-pointer">
                Weekends only (Friday/Saturday starts)
              </Label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="emailNotifications"
                checked={emailNotifications}
                onChange={(e) => setEmailNotifications(e.target.checked)}
                disabled={isMonitoring}
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <Label htmlFor="emailNotifications" className="cursor-pointer">
                Email notifications (requires email setup)
              </Label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="browserNotifications"
                checked={browserNotifications}
                onChange={(e) => setBrowserNotifications(e.target.checked)}
                disabled={isMonitoring}
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <Label htmlFor="browserNotifications" className="cursor-pointer">
                Browser push notifications
              </Label>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={isMonitoring || selectedFacilities.length === 0}
          >
            Start Monitoring
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
