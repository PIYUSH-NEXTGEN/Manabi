import { useQuery } from '@tanstack/react-query';
import { ApiError, sendHeartbeat, type PresenceOut } from '@/api/client';
import { getDeviceHints, getVisitorId } from '@/lib/visitorId';

/** One heartbeat per visible minute keeps the online window warm. */
export const PRESENCE_HEARTBEAT_MS = 60_000;

export function usePresence() {
  return useQuery<PresenceOut, ApiError>({
    queryKey: ['presence'],
    queryFn: () => sendHeartbeat(getVisitorId(), getDeviceHints()),
    refetchInterval: () =>
      typeof document !== 'undefined' && document.visibilityState === 'visible'
        ? PRESENCE_HEARTBEAT_MS
        : false,
    refetchOnWindowFocus: true,
    staleTime: PRESENCE_HEARTBEAT_MS,
    retry: 1,
  });
}
