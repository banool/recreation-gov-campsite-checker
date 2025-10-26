export interface MonitoringConfig {
  parks: number[];
  startDate: string;
  endDate: string;
  nights: number;
  weekendsOnly: boolean;
  campsiteType?: string;
  campsiteIds?: number[];
  excludedDates?: string[];
  emailNotifications: boolean;
  browserNotifications: boolean;
}

export interface ParkAvailability {
  parkId: string;
  parkName: string;
  current: number;
  maximum: number;
  availableSites: {
    [siteId: string]: {
      start: string;
      end: string;
    }[];
  };
}

export interface MonitoringResult {
  success: boolean;
  timestamp: string;
  hasAvailability: boolean;
  parks: ParkAvailability[];
  searchParams: {
    startDate: string;
    endDate: string;
    nights: number;
  };
  error?: string;
  checkNumber?: number;
}

export interface MonitoringStatus {
  isRunning: boolean;
  checkCount: number;
  lastCheckTime: string | null;
  config: MonitoringConfig | null;
  lastResult: MonitoringResult | null;
}

export interface SSEStatusEvent {
  state: 'started' | 'checking' | 'stopped' | 'running';
  checkNumber?: number;
  timestamp: string;
}

export interface SSEResultsEvent extends MonitoringResult {
  checkNumber: number;
}

export interface SSEErrorEvent {
  message: string;
  timestamp: string;
}

