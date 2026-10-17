import { useQuery } from '@tanstack/react-query';
import { ApiError, getMlQuestion, type MlQuestionDetail } from '@/api/client';

export function useMlQuestion(id: number | null) {
  return useQuery<MlQuestionDetail, ApiError>({
    queryKey: ['ml', 'questions', id],
    queryFn: () => getMlQuestion(id as number),
    enabled: id != null,
  });
}
