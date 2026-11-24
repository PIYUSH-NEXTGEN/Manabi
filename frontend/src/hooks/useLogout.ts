import { useMutation, useQueryClient } from '@tanstack/react-query';
import { logout } from '@/api/client';
import { resetAnalytics } from '@/lib/analytics';

export function useLogout() {
  const queryClient = useQueryClient();

  return useMutation<void, Error>({
    mutationFn: logout,
    onSuccess: () => {
      resetAnalytics();
      queryClient.resetQueries({ queryKey: ['auth', 'me'] });
      // The dashboard list belongs to the signed-out user; never hand it to the
      // next session on a shared browser.
      queryClient.removeQueries({ queryKey: ['me', 'projects'] });
    },
  });
}
