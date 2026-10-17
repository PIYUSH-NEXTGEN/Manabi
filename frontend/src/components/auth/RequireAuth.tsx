import { useEffect, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Skeleton, useToast } from '@/design/primitives';
import { useMe } from '@/hooks/useMe';

export function RequireAuth({ children }: { children: ReactNode }) {
  const me = useMe();
  const navigate = useNavigate();
  const toast = useToast();

  useEffect(() => {
    if (!me.isPending && !me.data) {
      navigate('/', { replace: true });
      toast('Log in with GitHub to reach your dashboard.');
    }
  }, [me.isPending, me.data, navigate, toast]);

  if (me.isPending) {
    return (
      <main className="border-b-[3px] border-ink">
        <div className="mx-auto w-[min(760px,96vw)] space-y-3 py-16">
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
