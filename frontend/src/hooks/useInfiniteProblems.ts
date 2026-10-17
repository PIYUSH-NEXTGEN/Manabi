import {
  useInfiniteQuery,
  type InfiniteData,
} from '@tanstack/react-query';
import {
  getProblems,
  type ProblemsListOut,
  type ProblemsQuery,
} from '@/api/client';

const PAGE_SIZE = 12;

type BoardQuery = Omit<ProblemsQuery, 'limit' | 'offset'>;

export function useInfiniteProblems(query: BoardQuery) {
  return useInfiniteQuery<
    ProblemsListOut,
    Error,
    InfiniteData<ProblemsListOut>,
    [string, string, BoardQuery],
    number
  >({
    queryKey: ['problems', 'board', query],
    queryFn: ({ pageParam }) =>
      getProblems({ ...query, limit: PAGE_SIZE, offset: pageParam }),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      const loaded = allPages.reduce((acc, page) => acc + page.items.length, 0);
      return loaded < lastPage.total ? loaded : undefined;
    },
  });
}
