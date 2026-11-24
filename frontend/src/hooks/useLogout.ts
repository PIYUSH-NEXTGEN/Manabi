import { useMutation, useQueryClient } from '@tanstack/react-query';
import { logout } from '@/api/client';
import { isPostHogConfigured, posthog } from '@/lib/posthog';

export function useLogout() {
  const queryClient = useQueryClient();

  return useMutation<void, Error>({
    mutationFn: logout,
    onSuccess: () => {
      if (isPostHogConfigured) posthog.reset();
      queryClient.resetQueries({ queryKey: ['auth', 'me'] });
      // The dashboard list belongs to the signed-out user; never hand it to the
      // next session on a shared browser.
      queryClient.removeQueries({ queryKey: ['me', 'projects'] });
    },
  });
}
