import { lazy, Suspense } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MotionConfig } from 'motion/react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { RequireAuth } from '@/components/auth/RequireAuth';
import { AppLayout } from '@/components/layout/AppLayout';
import { ToastProvider } from '@/design/primitives';

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
const HomePage = lazy(() =>
  import('@/pages/HomePage').then((m) => ({ default: m.HomePage })),
);
const HowItWorksPage = lazy(() =>
  import('@/pages/HowItWorksPage').then((m) => ({
    default: m.HowItWorksPage,
  })),
);
const KitPage = lazy(() =>
  import('@/pages/KitPage').then((m) => ({ default: m.KitPage })),
);
const DashboardPage = lazy(() =>
  import('@/pages/DashboardPage').then((m) => ({ default: m.DashboardPage })),
);
const NotFoundPage = lazy(() =>
  import('@/pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })),
);
const ProblemBoardPage = lazy(() =>
  import('@/pages/ProblemBoardPage').then((m) => ({
    default: m.ProblemBoardPage,
  })),
);
const RepoAnalyzerPage = lazy(() =>
  import('@/pages/RepoAnalyzerPage').then((m) => ({
    default: m.RepoAnalyzerPage,
  })),
);
const ProblemGuidePage = lazy(() =>
  import('@/pages/ProblemGuidePage').then((m) => ({
    default: m.ProblemGuidePage,
  })),
);
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
const SourcesPage = lazy(() =>
  import('@/pages/SourcesPage').then((m) => ({ default: m.SourcesPage })),
);
const TermsPage = lazy(() =>
  import('@/pages/TermsPage').then((m) => ({ default: m.TermsPage })),
);
const ProjectsOverviewPage = lazy(() =>
  import('@/pages/projects/OverviewPage').then((m) => ({
    default: m.ProjectsOverviewPage,
  })),
);
const WebhooksPage = lazy(() =>
  import('@/pages/projects/WebhooksPage').then((m) => ({
    default: m.WebhooksPage,
  })),
);
const ApiContractsPage = lazy(() =>
  import('@/pages/projects/ApiContractsPage').then((m) => ({
    default: m.ApiContractsPage,
  })),
);
const TenantSecurityPage = lazy(() =>
  import('@/pages/projects/TenantSecurityPage').then((m) => ({
    default: m.TenantSecurityPage,
  })),
);
const IncidentsPage = lazy(() =>
  import('@/pages/projects/IncidentsPage').then((m) => ({
    default: m.IncidentsPage,
  })),
);
const IngestionPage = lazy(() =>
  import('@/pages/projects/IngestionPage').then((m) => ({
    default: m.IngestionPage,
  })),
);
const AnalyticsPage = lazy(() =>
  import('@/pages/projects/AnalyticsPage').then((m) => ({
    default: m.AnalyticsPage,
  })),
);
const AccessibilityPage = lazy(() =>
  import('@/pages/projects/AccessibilityPage').then((m) => ({
    default: m.AccessibilityPage,
  })),
);
const InventoryPage = lazy(() =>
  import('@/pages/projects/InventoryPage').then((m) => ({
    default: m.InventoryPage,
  })),
);
const SyncPage = lazy(() =>
  import('@/pages/projects/SyncPage').then((m) => ({
    default: m.SyncPage,
  })),
);
const WorkflowsPage = lazy(() =>
  import('@/pages/projects/WorkflowsPage').then((m) => ({
    default: m.WorkflowsPage,
  })),
);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

function RouteFallback() {
  return (
    <div className="mx-auto w-[min(1100px,96vw)] animate-pulse space-y-4 py-16" aria-hidden>
      <div className="h-4 w-40 bg-ink/20" />
      <div className="h-16 w-2/3 bg-ink/20" />
      <div className="h-48 w-full bg-ink/20" />
    </div>
  );
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MotionConfig reducedMotion="user">
        <ToastProvider>
          <BrowserRouter>
            <Suspense fallback={<RouteFallback />}>
              <Routes>
                <Route element={<AppLayout />}>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/_kit" element={<KitPage />} />

                  <Route path="/problems" element={<ProblemBoardPage />} />
                  <Route path="/problems/:id" element={<ProblemDetailPage />} />
                  <Route path="/problems/:id/guide"
                    element={<ProblemGuidePage />}
                  />
                  <Route path="/repo-analyzer" element={<RepoAnalyzerPage />} />
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
                  <Route path="/how-it-works" element={<HowItWorksPage />} />
                  <Route path="/sources" element={<SourcesPage />} />
                  <Route path="/faq" element={<FaqPage />} />
                  <Route path="/contribute" element={<ContributePage />} />
                  <Route path="/contact" element={<ContactPage />} />
                  <Route path="/privacy" element={<PrivacyPage />} />
                  <Route path="/terms" element={<TermsPage />} />
                  <Route path="/404" element={<NotFoundPage />} />
                  <Route path="/projects" element={<ProjectsOverviewPage />} />
                  <Route path="/projects/webhooks" element={<WebhooksPage />} />
                  <Route path="/projects/api-contracts" element={<ApiContractsPage />} />
                  <Route path="/projects/tenant-security" element={<TenantSecurityPage />} />
                  <Route path="/projects/incidents" element={<IncidentsPage />} />
                  <Route path="/projects/ingestion" element={<IngestionPage />} />
                  <Route path="/projects/analytics" element={<AnalyticsPage />} />
                  <Route path="/projects/accessibility" element={<AccessibilityPage />} />
                  <Route path="/projects/inventory" element={<InventoryPage />} />
                  <Route path="/projects/sync" element={<SyncPage />} />
                  <Route path="/projects/workflows" element={<WorkflowsPage />} />
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
