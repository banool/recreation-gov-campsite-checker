import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { Bell, BellOff, CheckCircle } from 'lucide-react';

interface NotificationSettingsProps {
  permission: NotificationPermission;
  isEnabled: boolean;
  isSupported: boolean;
  onRequestPermission: () => Promise<boolean>;
}

export function NotificationSettings({
  permission,
  isEnabled,
  isSupported,
  onRequestPermission,
}: NotificationSettingsProps) {
  if (!isSupported) {
    return (
      <Card className="w-full bg-yellow-50 border-yellow-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-yellow-800">
            <BellOff className="h-5 w-5" />
            Notifications Not Supported
          </CardTitle>
          <CardDescription>
            Your browser doesn't support notifications
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (permission === 'granted') {
    return (
      <Card className="w-full bg-green-50 border-green-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800">
            <CheckCircle className="h-5 w-5" />
            Notifications Enabled
          </CardTitle>
          <CardDescription>
            You'll receive browser notifications when campsites become available
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (permission === 'denied') {
    return (
      <Card className="w-full bg-red-50 border-red-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-800">
            <BellOff className="h-5 w-5" />
            Notifications Blocked
          </CardTitle>
          <CardDescription>
            You've blocked notifications. Please enable them in your browser settings.
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bell className="h-5 w-5" />
          Enable Browser Notifications
        </CardTitle>
        <CardDescription>
          Get notified instantly when campsites become available
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Button onClick={onRequestPermission} className="w-full">
          Enable Notifications
        </Button>
      </CardContent>
    </Card>
  );
}

