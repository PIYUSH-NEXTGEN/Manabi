import { lazy, Suspense, useEffect, useRef } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MotionConfig } from 'motion/react';
import { BrowserRouter, Route, Routes, useLocation } from 'react-router-dom';
import { RequireAuth } from '@/components/auth/RequireAuth';
import { AppLayout } from '@/components/layout/AppLayout';
import { ScrollToTop } from '@/components/layout/ScrollToTop';
import { ToastProvider } from '@/design/primitives';
import { identifyUser, resetAnalytics, trackPageview } from '@/lib/analytics';
import { useSmoothScroll } from '@/lib/useSmoothScroll';
import { useMe } from '@/hooks/useMe';

const AboutPage = lazy(() =>
  import('@/pages/AboutPage').then((m) => ({ default: m.AboutPage })),
);
const AdminReviewPage = lazy(() =>
  import('@/pages/AdminReviewPage').then((m) => ({
    default: m.AdminReviewPage,
  })),
);
const ContributePage = lazy(() =>
  import('@/pages/ContributePage').then((m) => ({ default: m.ContributePage })),
);
const ContactPage = lazy(() =>
  import('@/pages/ContactPage').then((m) => ({ default: m.ContactPage })),
);
const FaqPage = lazy(() =>
  import('@/pages/FaqPage').then((m) => ({ default: m.FaqPage })),
);
const SponsorsPage = lazy(() =>
  import('@/pages/SponsorsPage').then((m) => ({
    default: m.SponsorsPage,
  })),
);
const HomePage = lazy(() =>
  import('@/pages/HomePage').then((m) => ({ default: m.HomePage })),
);
// The design-system page contains demo controls and is not part of the
// product. It stays available in development and tests only.
const KitPage = import.meta.env.DEV
  ? lazy(() => import('@/pages/KitPage').then((m) => ({ default: m.KitPage })))
  : null;
const DashboardPage = lazy(() =>
  import('@/pages/DashboardPage').then((m) => ({ default: m.DashboardPage })),
);
// After first paint the app preloads every route chunk while the browser is
// idle. Without this, switching pages waits on a network round trip for a
// 1-26 kB chunk and shows the RouteFallback skeleton before the page appears.
const PAGE_PRELOADS = [
  () => import('@/pages/HomePage'),
  () => import('@/pages/ProblemBoardPage'),
  () => import('@/pages/ProblemDetailPage'),
  () => import('@/pages/ProjectDetailPage'),
  () => import('@/pages/DashboardPage'),
  () => import('@/pages/AdminReviewPage'),
  () => import('@/pages/AboutPage'),
  () => import('@/pages/FaqPage'),
  () => import('@/pages/ContributePage'),
  () => import('@/pages/ContactPage'),
  () => import('@/pages/SponsorsPage'),
  () => import('@/pages/PrivacyPage'),
  () => import('@/pages/TermsPage'),
  () => import('@/pages/NotFoundPage'),
  ...(import.meta.env.DEV ? [() => import('@/pages/KitPage')] : []),
];

const NotFoundPage = lazy(() =>
  import('@/pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })),
);
const ProblemBoardPage = lazy(() =>
  import('@/pages/ProblemBoardPage').then((m) => ({
    default: m.ProblemBoardPage,
  })),
);
function prefetchPages() {
  for (const load of PAGE_PRELOADS) void load().catch(() => {});
}

export function schedulePrefetch(): void {
  if (typeof window === 'undefined') return;
  const idle = window.requestIdleCallback;
  if (idle) {
    idle(prefetchPages);
    return;
  }
  setTimeout(prefetchPages, 350);
}

const ProblemDetailPage = lazy(() =>
  import('@/pages/ProblemDetailPage').then((m) => ({
    default: m.ProblemDetailPage,
  })),
);
const ProjectDetailPage = lazy(() =>
  import('@/pages/ProjectDetailPage').then((m) => ({
    default: m.ProjectDetailPage,
  })),
);
const PrivacyPage = lazy(() =>
  import('@/pages/PrivacyPage').then((m) => ({ default: m.PrivacyPage })),
);
const TermsPage = lazy(() =>
  import('@/pages/TermsPage').then((m) => ({ default: m.TermsPage })),
);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
      // Keep fresh results around a little: navigating back to a page that
      // already fetched data renders instantly from cache with a background
      // refresh, instead of re-flashing the loading skeleton.
      staleTime: 30_000,
    },
  },
});

const PAGE_TITLES: Record<string, string> = {
  '/': 'MANABI — Pick a project. Ship it. Prove it.',
  '/problems': 'Projects · MANABI',
  '/me': 'Dashboard · MANABI',
  '/admin/review': 'Submissions · MANABI',
  '/about': 'About · MANABI',
  '/faq': 'FAQ · MANABI',
  '/contribute': 'Contribute · MANABI',
  '/contact': 'Contact · MANABI',
  '/sponsors': 'Sponsors · MANABI',
  '/privacy': 'Privacy · MANABI',
  '/terms': 'Terms · MANABI',
};

function pageTitle(pathname: string): string {
  if (import.meta.env.DEV && pathname === '/_kit') return 'Design kit · MANABI';
  const title = PAGE_TITLES[pathname];
  if (title) return title;
  if (/^\/problems\/\d+$/.test(pathname)) return 'Project brief · MANABI';
  if (/^\/projects\/\d+$/.test(pathname)) return 'Project · MANABI';
  return 'Page not found · MANABI';
}

function RouteTitle() {
  const { pathname } = useLocation();

  useEffect(() => {
    document.title = pageTitle(pathname);
  }, [pathname]);

  return null;
}

function AnalyticsIdentity() {
  const me = useMe();
  const identifiedUserId = useRef<number | null>(null);

  useEffect(() => {
    if (!me.data) {
      identifiedUserId.current = null;
      return;
    }
    if (identifiedUserId.current === me.data.id) return;

    // A changed session without an explicit logout must not retain the prior
    // account's analytics identity.
    if (identifiedUserId.current !== null) resetAnalytics();

    identifyUser(me.data.id, {
      username: me.data.username,
      name: me.data.name ?? undefined,
      is_admin: Boolean(me.data.is_admin),
    });
    identifiedUserId.current = me.data.id;
  }, [me.data]);

  return null;
}

function RoutePageview() {
  const { pathname } = useLocation();

  useEffect(() => {
    trackPageview(pathname);
  }, [pathname]);

  return null;
}

function RouteFallback() {
  return (
    <div className="mx-auto w-full max-w-[1140px] animate-pulse space-y-4 px-5 py-16 sm:px-6" aria-hidden>
      <div className="h-4 w-40 bg-ink/20" />
      <div className="h-16 w-2/3 bg-ink/20" />
      <div className="h-48 w-full bg-ink/20" />
    </div>
  );
}

export function App() {
  useSmoothScroll();

  useEffect(() => {
    schedulePrefetch();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <AnalyticsIdentity />
      <MotionConfig reducedMotion="user">
        <ToastProvider>
          <BrowserRouter>
            <RouteTitle />
            <RoutePageview />
            <ScrollToTop />
            <Suspense fallback={<RouteFallback />}>
              <Routes>
                <Route element={<AppLayout />}>
                  <Route path="/" element={<HomePage />} />
                  {KitPage ? (
                    <Route path="/_kit" element={<KitPage />} />
                  ) : null}

                  <Route path="/problems" element={<ProblemBoardPage />} />
                  <Route path="/problems/:id" element={<ProblemDetailPage />} />
                  <Route
                    path="/projects/:id"
                    element={<ProjectDetailPage />}
                  />
                  <Route
                    path="/me"
                    element={
                      <RequireAuth>
                        <DashboardPage />
                      </RequireAuth>
                    }
                  />

                  <Route
                    path="/admin/review"
                    element={
                      <RequireAuth>
                        <AdminReviewPage />
                      </RequireAuth>
                    }
                  />
                  <Route path="/about" element={<AboutPage />} />
                  <Route path="/faq" element={<FaqPage />} />
                  <Route path="/contribute" element={<ContributePage />} />
                  <Route path="/contact" element={<ContactPage />} />
                  <Route path="/sponsors" element={<SponsorsPage />} />
                  <Route path="/privacy" element={<PrivacyPage />} />
                  <Route path="/terms" element={<TermsPage />} />
                  <Route path="/404" element={<NotFoundPage />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Route>
              </Routes>
            </Suspense>
          </BrowserRouter>
        </ToastProvider>
      </MotionConfig>
    </QueryClientProvider>
  );
}
