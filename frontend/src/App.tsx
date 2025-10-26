import { useEffect, useState } from 'react';
import { SearchForm } from './components/SearchForm';
import { MonitoringStatus } from './components/MonitoringStatus';
import { ResultsPanel } from './components/ResultsPanel';
import { NotificationSettings } from './components/NotificationSettings';
import { useSSE } from './hooks/useSSE';
import { useNotifications } from './hooks/useNotifications';
import type { MonitoringConfig } from './types/index';
import { Tent } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

function App() {
  const { status, results, error, isConnected } = useSSE();
  const {
    permission,
    isEnabled,
    isSupported,
    requestPermission,
    sendNotification,
  } = useNotifications();

  const [isMonitoring, setIsMonitoring] = useState(false);
  const [currentConfig, setCurrentConfig] = useState<MonitoringConfig | null>(null);

  // Update monitoring state based on SSE status
  useEffect(() => {
    if (status) {
      setIsMonitoring(
        status.state === 'started' ||
          status.state === 'checking' ||
          status.state === 'running'
      );
    }
  }, [status]);

  // Send browser notification when results arrive
  useEffect(() => {
    if (results && results.hasAvailability && currentConfig?.browserNotifications) {
      sendNotification(results);
    }
  }, [results, currentConfig, sendNotification]);

  // Display SSE errors
  useEffect(() => {
    if (error) {
      console.error('SSE Error:', error);
      alert(`Error: ${error.message}`);
    }
  }, [error]);

  const handleStartMonitoring = async (config: MonitoringConfig) => {
    // Request notification permission if needed
    if (config.browserNotifications && permission !== 'granted') {
      await requestPermission();
    }

    try {
      const response = await fetch(`${API_URL}/api/start-monitoring`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      });

      const data = await response.json();

      if (!data.success) {
        alert(`Failed to start monitoring: ${data.error}`);
        return;
      }

      setCurrentConfig(config);
      setIsMonitoring(true);
    } catch (err) {
      console.error('Failed to start monitoring:', err);
      alert('Failed to start monitoring. Is the backend server running?');
    }
  };

  const handleStopMonitoring = async () => {
    try {
      const response = await fetch(`${API_URL}/api/stop-monitoring`, {
        method: 'POST',
      });

      const data = await response.json();

      if (!data.success) {
        alert(`Failed to stop monitoring: ${data.error}`);
        return;
      }

      setIsMonitoring(false);
    } catch (err) {
      console.error('Failed to stop monitoring:', err);
      alert('Failed to stop monitoring. Is the backend server running?');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Tent className="h-10 w-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">
              Recreation.gov Campsite Checker
            </h1>
          </div>
          <p className="text-gray-600 ml-13">
            Monitor campsite availability in real-time and get notified instantly when sites become available
          </p>
        </header>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Notification Settings */}
          {!isMonitoring && (
            <NotificationSettings
              permission={permission}
              isEnabled={isEnabled}
              isSupported={isSupported}
              onRequestPermission={requestPermission}
            />
          )}

          {/* Search Form */}
          {!isMonitoring && (
            <SearchForm
              onSubmit={handleStartMonitoring}
              isMonitoring={isMonitoring}
            />
          )}

          {/* Monitoring Status */}
          {isMonitoring && (
            <MonitoringStatus
              status={status}
              error={error}
              isConnected={isConnected}
              onStop={handleStopMonitoring}
            />
          )}

          {/* Results Panel */}
          {isMonitoring && (
            <ResultsPanel results={results} />
          )}
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500">
          <p>
            Check every 20 seconds · Made with ❤️ for camping enthusiasts
          </p>
          <p className="mt-1">
            Park IDs can be found on{' '}
            <a
              href="https://www.recreation.gov"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              recreation.gov
            </a>
            {' '}in the campground URL
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
