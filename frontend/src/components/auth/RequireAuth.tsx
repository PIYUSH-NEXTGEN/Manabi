import { useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { Skeleton, useToast } from '@/design/primitives';
import { getMyProjects } from '@/api/client';
import { useMe } from '@/hooks/useMe';
import { MY_PROJECTS_QUERY_KEY } from '@/hooks/useMyProjects';

export function RequireAuth({ children }: { children: ReactNode }) {
  const me = useMe();
  const navigate = useNavigate();
  const toast = useToast();
  const queryClient = useQueryClient();

  // Start the dashboard list while the session request is still in flight. The
  // two calls then overlap instead of queuing, and a logged-out visitor just
  // gets the unavoidable 401 a moment before being redirected.
  useEffect(() => {
    if (!me.isPending) return;
    void queryClient.prefetchQuery({
      queryKey: MY_PROJECTS_QUERY_KEY,
      queryFn: getMyProjects,
    });
  }, [me.isPending, queryClient]);

  useEffect(() => {
    if (!me.isPending && !me.data) {
      navigate('/', { replace: true });
      toast('Log in with GitHub to reach your dashboard.');
    }
  }, [me.isPending, me.data, navigate, toast]);

  if (me.isPending) {
    return (
      <main className="border-b border-line">
        <div className="mx-auto w-full max-w-[800px] space-y-3 px-5 py-16 sm:px-6">
          <Skeleton className="h-3 w-40" />
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-24 w-full" />
        </div>
      </main>
    );
  }

  if (!me.data) {
    return null;
  }

  return <>{children}</>;
}
