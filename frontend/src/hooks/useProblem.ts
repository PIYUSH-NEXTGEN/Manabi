import { useQuery } from '@tanstack/react-query';
import { ApiError, getProblem, type ProblemDetail } from '@/api/client';

export function useProblem(id: number) {
  return useQuery<ProblemDetail, ApiError>({
    queryKey: ['problem', id],
    queryFn: () => getProblem(id),
    enabled: Number.isInteger(id) && id > 0,
  });
}
