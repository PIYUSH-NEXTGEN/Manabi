import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  editProblem,
  getAdminReview,
  getCrawlRuns,
  moderateProblem,
  takedownSource,
  type AdminReviewOut,
  type ApiError,
  type CrawlRunOut,
} from '@/api/client';

export function useAdminReview(status = 'pending_review') {
  return useQuery<AdminReviewOut, ApiError>({
    queryKey: ['admin', 'review', status],
    queryFn: () => getAdminReview(status),
    retry: false,
  });
}

export function useCrawlRuns() {
  return useQuery<CrawlRunOut[], ApiError>({
    queryKey: ['admin', 'crawl-runs'],
    queryFn: () => getCrawlRuns(),
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

export function useTakedownSource() {
  const refresh = useRefreshAdmin();
  return useMutation({
    mutationFn: (sourceKey: string) => takedownSource(sourceKey),
    onSuccess: refresh,
  });
}
