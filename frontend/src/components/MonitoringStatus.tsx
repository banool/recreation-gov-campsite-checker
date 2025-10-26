import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import type { SSEStatusEvent, SSEErrorEvent } from '../types/index';
import { Activity, CheckCircle, XCircle, Clock, AlertTriangle } from 'lucide-react';
import { format } from 'date-fns';


interface MonitoringStatusProps {
  status: SSEStatusEvent | null;
  error: SSEErrorEvent | null;
  isConnected: boolean;
  onStop: () => void;
}

export function MonitoringStatus({ status, error, isConnected, onStop }: MonitoringStatusProps) {
  const [timeUntilNext, setTimeUntilNext] = useState<number>(20);
  const [lastCheckTime, setLastCheckTime] = useState<Date | null>(null);
  const [lastError, setLastError] = useState<SSEErrorEvent | null>(null);
  const [failedCheckCount, setFailedCheckCount] = useState<number>(0);

  // Track errors
  useEffect(() => {
    if (error) {
      setLastError(error);
      setFailedCheckCount(prev => prev + 1);
      // Clear error message after 30 seconds (but keep the count)
      const timeout = setTimeout(() => setLastError(null), 30000);
      return () => clearTimeout(timeout);
    }
  }, [error]);

  // Update countdown timer
  useEffect(() => {
    if (status?.state === 'checking' || status?.state === 'running') {
      setLastCheckTime(new Date());
      setTimeUntilNext(20);
    }
  }, [status?.checkNumber]);

  useEffect(() => {
    if (!lastCheckTime || status?.state === 'stopped') {
      return;
    }

    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - lastCheckTime.getTime()) / 1000);
      const remaining = Math.max(0, 20 - elapsed);
      setTimeUntilNext(remaining);
    }, 1000);

    return () => clearInterval(interval);
  }, [lastCheckTime, status?.state]);

  // Reset failed check count when monitoring stops
  useEffect(() => {
    if (!status || status.state === 'stopped') {
      setFailedCheckCount(0);
    }
  }, [status?.state]);

  if (!status || status.state === 'stopped') {
    return (
      <Card className="w-full bg-gray-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <XCircle className="h-5 w-5 text-gray-400" />
            Monitoring Stopped
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-500">
            Configure your search parameters and click "Start Monitoring" to begin.
          </p>
        </CardContent>
      </Card>
    );
  }

  const isRunning = status.state === 'checking' || status.state === 'running' || status.state === 'started';

  return (
    <Card className={`w-full ${isRunning ? 'bg-blue-50 border-blue-200' : 'bg-gray-50'}`}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            {isRunning ? (
              <>
                <Activity className="h-5 w-5 text-blue-600 animate-pulse" />
                <span className="text-blue-600">Monitoring Active</span>
              </>
            ) : (
              <>
                <CheckCircle className="h-5 w-5 text-green-600" />
                <span className="text-green-600">Monitoring Complete</span>
              </>
            )}
          </CardTitle>
          <Button
            variant="destructive"
            size="sm"
            onClick={onStop}
          >
            Stop Monitoring
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="flex flex-col">
            <span className="text-xs text-gray-500 uppercase font-semibold mb-1">
              Connection Status
            </span>
            <span className={`flex items-center gap-2 text-sm font-medium ${
              isConnected ? 'text-green-600' : 'text-red-600'
            }`}>
              <div className={`h-2 w-2 rounded-full ${
                isConnected ? 'bg-green-600' : 'bg-red-600'
              }`} />
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          <div className="flex flex-col">
            <span className="text-xs text-gray-500 uppercase font-semibold mb-1">
              Total Checks
            </span>
            <span className="text-lg font-bold text-gray-900">
              {status.checkNumber || 0}
            </span>
          </div>

          <div className="flex flex-col">
            <span className="text-xs text-gray-500 uppercase font-semibold mb-1">
              Failed Checks
            </span>
            <span className={`flex items-center gap-2 text-lg font-bold ${
              failedCheckCount > 0 ? 'text-yellow-600' : 'text-gray-900'
            }`}>
              {failedCheckCount > 0 && <AlertTriangle className="h-4 w-4" />}
              {failedCheckCount}
            </span>
          </div>

          <div className="flex flex-col">
            <span className="text-xs text-gray-500 uppercase font-semibold mb-1">
              Next Check In
            </span>
            <span className="flex items-center gap-2 text-lg font-bold text-gray-900">
              <Clock className="h-4 w-4" />
              {timeUntilNext}s
            </span>
          </div>
        </div>

        {lastCheckTime && (
          <div className="pt-3 border-t border-gray-200">
            <span className="text-xs text-gray-500">
              Last checked at {format(lastCheckTime, 'h:mm:ss a')}
            </span>
          </div>
        )}

        {lastError && (
          <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <div className="flex items-start gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-yellow-800">
                  Check #{lastError.checkNumber} Failed
                </h4>
                <p className="text-xs text-yellow-700 mt-1">
                  {lastError.message}
                </p>
                <p className="text-xs text-yellow-600 mt-1">
                  Monitoring will continue automatically. This may be due to rate limiting or API issues.
                </p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

