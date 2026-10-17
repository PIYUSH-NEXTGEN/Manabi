import { useQuery } from '@tanstack/react-query';
import {
  ApiError,
  getProblems,
  type ProblemsListOut,
  type ProblemsQuery,
} from '@/api/client';

export function useProblems(query: ProblemsQuery = {}) {
  return useQuery<ProblemsListOut, ApiError>({
    queryKey: ['problems', query],
    queryFn: () => getProblems(query),
  });
}
