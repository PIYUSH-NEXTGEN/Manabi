import { useQuery } from '@tanstack/react-query';
import { ApiError, getMyAttempt, type AttemptOut } from '@/api/client';
import { useMe } from '@/hooks/useMe';

export function useMlQuestionAttempt(questionId: number) {
  const me = useMe();

  return useQuery<AttemptOut | null, ApiError>({
    queryKey: ['ml', 'attempt', questionId],
    queryFn: async () => {
      try {
        return await getMyAttempt(questionId);
      } catch (error) {
        if (error instanceof ApiError && error.status === 404) {
          return null;
        }
        throw error;
      }
    },
    enabled: Boolean(me.data),
    staleTime: Infinity,
  });
}
