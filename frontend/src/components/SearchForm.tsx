import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card';
import { Input } from './ui/Input';
import { Label } from './ui/Label';
import { Button } from './ui/Button';
import type { MonitoringConfig } from '../types/index';
import { format } from 'date-fns';
import { useFacilitySearch } from '../hooks/useFacilitySearch';

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

  // Use the facility search hook
  const { facilities, loading } = useFacilitySearch(searchQuery);

  const handleFacilitySelect = (facility: { id: string; name: string }) => {
    // Don't add duplicates
    if (!selectedFacilities.find(f => f.id === facility.id)) {
      setSelectedFacilities([...selectedFacilities, facility]);
    }
    setSearchQuery('');
    setShowDropdown(false);
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
            <div className="relative">
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
                  {loading ? (
                    <div className="px-4 py-3 text-sm text-gray-500">
                      Searching...
                    </div>
                  ) : facilities.length > 0 ? (
                    facilities.map((facility) => (
                      <button
                        key={facility.id}
                        type="button"
                        onClick={() => handleFacilitySelect(facility)}
                        className="w-full px-4 py-3 text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none border-b border-gray-100 last:border-b-0"
                      >
                        <div className="font-medium text-sm">{facility.name}</div>
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
                    ))
                  ) : (
                    <div className="px-4 py-3 text-sm text-gray-500">
                      No campgrounds found. Try a different search term.
                    </div>
                  )}
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

            <div className="space-y-2">
              <Label htmlFor="campsiteType">Campsite Type (Optional)</Label>
              <Input
                id="campsiteType"
                placeholder="STANDARD NONELECTRIC"
                value={campsiteType}
                onChange={(e) => setCampsiteType(e.target.value)}
                disabled={isMonitoring}
              />
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
