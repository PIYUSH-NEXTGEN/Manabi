import { useMutation, useQueryClient } from '@tanstack/react-query';
import { logout } from '@/api/client';

export function useLogout() {
  const queryClient = useQueryClient();

  return useMutation<void, Error>({
    mutationFn: logout,
    onSuccess: () => {
      queryClient.resetQueries({ queryKey: ['auth', 'me'] });
    },
  });
}
