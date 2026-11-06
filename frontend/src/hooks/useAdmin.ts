import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  approveSubmission,
  getAdminSubmissions,
  rejectSubmission,
  type AdminSubmissionsOut,
  type ApiError,
  type SubmissionStatusFilter,
} from '@/api/client';

export function useAdminSubmissions(status: SubmissionStatusFilter) {
  return useQuery<AdminSubmissionsOut, ApiError>({
    queryKey: ['admin', 'submissions', status],
    queryFn: () => getAdminSubmissions(status),
    retry: false,
  });
}

function useRefreshAdmin() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: ['admin'] });
  };
}

export function useApproveSubmission() {
  const refresh = useRefreshAdmin();
  return useMutation({
    mutationFn: ({ id, note }: { id: number; note?: string }) =>
      approveSubmission(id, note),
    onSuccess: refresh,
  });
}

export function useRejectSubmission() {
  const refresh = useRefreshAdmin();
  return useMutation({
    mutationFn: ({ id, note }: { id: number; note?: string }) =>
      rejectSubmission(id, note),
    onSuccess: refresh,
  });
}
