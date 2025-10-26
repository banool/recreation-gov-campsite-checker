import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import type { MonitoringResult } from '../types/index';
import { CheckCircle, XCircle, ChevronDown, ChevronRight, ExternalLink, Calendar } from 'lucide-react';
import { format } from 'date-fns';

interface ResultsPanelProps {
  results: MonitoringResult | null;
}

export function ResultsPanel({ results }: ResultsPanelProps) {
  const [expandedParks, setExpandedParks] = useState<Set<string>>(new Set());

  if (!results) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Search Results</CardTitle>
          <CardDescription>
            Results will appear here once monitoring starts
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            <Activity className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>Waiting for results...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const togglePark = (parkId: string) => {
    const newExpanded = new Set(expandedParks);
    if (newExpanded.has(parkId)) {
      newExpanded.delete(parkId);
    } else {
      newExpanded.add(parkId);
    }
    setExpandedParks(newExpanded);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              {results.hasAvailability ? (
                <>
                  <CheckCircle className="h-6 w-6 text-green-600" />
                  <span className="text-green-600">Campsites Available!</span>
                </>
              ) : (
                <>
                  <XCircle className="h-6 w-6 text-gray-400" />
                  <span>No Available Campsites</span>
                </>
              )}
            </CardTitle>
            <CardDescription className="mt-1">
              Last updated: {format(new Date(results.timestamp), 'PPpp')}
            </CardDescription>
          </div>
          {results.checkNumber && (
            <div className="text-right">
              <div className="text-sm text-gray-500">Check #{results.checkNumber}</div>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {results.parks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No parks found in search results</p>
          </div>
        ) : (
          results.parks.map((park) => {
            const isExpanded = expandedParks.has(park.parkId);
            const hasAvailability = park.current > 0;

            return (
              <div
                key={park.parkId}
                className={`border rounded-lg overflow-hidden ${
                  hasAvailability ? 'border-green-300 bg-green-50' : 'border-gray-200 bg-white'
                }`}
              >
                <button
                  onClick={() => togglePark(park.parkId)}
                  className="w-full p-4 flex items-center justify-between hover:bg-opacity-80 transition-colors"
                >
                  <div className="flex items-center gap-3 text-left flex-1">
                    {hasAvailability ? (
                      <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                    ) : (
                      <XCircle className="h-5 w-5 text-gray-400 flex-shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">
                        {park.parkName}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Park ID: {park.parkId}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className={`text-lg font-bold ${
                        hasAvailability ? 'text-green-600' : 'text-gray-900'
                      }`}>
                        {park.current} / {park.maximum}
                      </div>
                      <div className="text-xs text-gray-500">
                        available
                      </div>
                    </div>
                  </div>
                  {isExpanded ? (
                    <ChevronDown className="h-5 w-5 text-gray-400 ml-2 flex-shrink-0" />
                  ) : (
                    <ChevronRight className="h-5 w-5 text-gray-400 ml-2 flex-shrink-0" />
                  )}
                </button>

                {isExpanded && hasAvailability && (
                  <div className="border-t border-green-200 bg-white p-4 space-y-4">
                    <h4 className="font-semibold text-sm text-gray-700 mb-3">
                      Available Campsites
                    </h4>
                    {Object.entries(park.availableSites).map(([siteId, dates]) => (
                      <div
                        key={siteId}
                        className="border border-gray-200 rounded-lg p-3 space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <h5 className="font-semibold text-gray-900">
                            Campsite #{siteId}
                          </h5>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              window.open(
                                `https://www.recreation.gov/camping/campsites/${siteId}`,
                                '_blank'
                              )
                            }
                          >
                            <ExternalLink className="h-3 w-3 mr-1" />
                            Book Now
                          </Button>
                        </div>
                        <div className="space-y-1">
                          {dates.map((date, idx) => (
                            <div
                              key={idx}
                              className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded"
                            >
                              <Calendar className="h-4 w-4 text-gray-400" />
                              <span>
                                {date.start} → {date.end}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        )}
      </CardContent>
    </Card>
  );
}

function Activity(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}

