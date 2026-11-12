import { cx } from '@/lib/cx';

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return <div aria-hidden className={cx('skeleton h-24 w-full', className)} />;
}
