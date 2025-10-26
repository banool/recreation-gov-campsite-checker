import { useEffect, useRef, useState } from 'react';
import type { SSEStatusEvent, SSEResultsEvent, SSEErrorEvent } from '../types/index';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

interface UseSSEResult {
  status: SSEStatusEvent | null;
  results: SSEResultsEvent | null;
  error: SSEErrorEvent | null;
  isConnected: boolean;
}

export function useSSE(): UseSSEResult {
  const [status, setStatus] = useState<SSEStatusEvent | null>(null);
  const [results, setResults] = useState<SSEResultsEvent | null>(null);
  const [error, setError] = useState<SSEErrorEvent | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    // Create EventSource connection
    const eventSource = new EventSource(`${API_URL}/api/stream`);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log('SSE connection opened');
      setIsConnected(true);
    };

    eventSource.addEventListener('status', (event) => {
      try {
        const data = JSON.parse(event.data) as SSEStatusEvent;
        setStatus(data);
      } catch (err) {
        console.error('Failed to parse status event:', err);
      }
    });

    eventSource.addEventListener('results', (event) => {
      try {
        const data = JSON.parse(event.data) as SSEResultsEvent;
        setResults(data);
      } catch (err) {
        console.error('Failed to parse results event:', err);
      }
    });

    eventSource.addEventListener('error', (event) => {
      try {
        const data = JSON.parse(event.data) as SSEErrorEvent;
        setError(data);
      } catch (err) {
        console.error('Failed to parse error event:', err);
      }
    });

    eventSource.onerror = () => {
      console.error('SSE connection error');
      setIsConnected(false);
      // The browser will automatically try to reconnect
    };

    // Cleanup on unmount
    return () => {
      eventSource.close();
      eventSourceRef.current = null;
    };
  }, []);

  return { status, results, error, isConnected };
}

