import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  submitProject,
  type ProjectCreate,
  type ProjectOut,
} from '@/api/client';

export function useSubmitProject(problemId: number) {
  const queryClient = useQueryClient();

  return useMutation<ProjectOut, Error, ProjectCreate>({
    mutationFn: (body) => submitProject(problemId, body),
    onSuccess: (project) => {
      queryClient.invalidateQueries({ queryKey: ['problem', problemId] });
      queryClient.setQueryData(['project', project.id], project);
    },
  });
}
