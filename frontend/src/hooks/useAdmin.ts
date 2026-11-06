import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  editProblem,
  getAdminReview,
  moderateProblem,
  type AdminReviewOut,
  type ApiError,
} from '@/api/client';

export function useAdminReview(status = 'pending_review') {
  return useQuery<AdminReviewOut, ApiError>({
    queryKey: ['admin', 'review', status],
    queryFn: () => getAdminReview(status),
    retry: false,
  });
}

function useRefreshAdmin() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: ['admin'] });
  };
}

export function useModerateProblem() {
  const refresh = useRefreshAdmin();
  return useMutation({
    mutationFn: ({
      id,
      action,
    }: {
      id: number;
      action: 'approve' | 'reject' | 'unpublish';
    }) => moderateProblem(id, action),
    onSuccess: refresh,
  });
}

export function useEditProblem() {
  const refresh = useRefreshAdmin();
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: { title?: string; summary?: string } }) =>
      editProblem(id, body),
    onSuccess: refresh,
  });
}
