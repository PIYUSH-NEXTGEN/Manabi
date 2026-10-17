import { useQuery } from '@tanstack/react-query';
import { ApiError, getMlQuestions, type MlQuestionCard } from '@/api/client';

export function useMlQuestions() {
  return useQuery<MlQuestionCard[], ApiError>({
    queryKey: ['ml', 'questions'],
    queryFn: getMlQuestions,
  });
}
