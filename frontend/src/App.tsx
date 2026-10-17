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
const IngestPage = lazy(() =>
  import('@/pages/IngestPage').then((m) => ({ default: m.IngestPage })),
);
const KitPage = lazy(() =>
  import('@/pages/KitPage').then((m) => ({ default: m.KitPage })),
);
const MlQuestionPage = lazy(() =>
  import('@/pages/MlQuestionPage').then((m) => ({
    default: m.MlQuestionPage,
  })),
);
const DashboardPage = lazy(() =>
  import('@/pages/DashboardPage').then((m) => ({ default: m.DashboardPage })),
);
const MlQuestionsPage = lazy(() =>
  import('@/pages/MlQuestionsPage').then((m) => ({
    default: m.MlQuestionsPage,
  })),
);
const NotFoundPage = lazy(() =>
  import('@/pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })),
);
const ProblemBoardPage = lazy(() =>
  import('@/pages/ProblemBoardPage').then((m) => ({
    default: m.ProblemBoardPage,
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
                  <Route
                    path="/projects/:id"
                    element={<ProjectDetailPage />}
                  />
                  <Route path="/ingest" element={<IngestPage />} />
                  <Route path="/ml" element={<MlQuestionsPage />} />
                  <Route path="/ml/:id" element={<MlQuestionPage />} />
                  <Route
                    path="/me"
                    element={
                      <RequireAuth>
                        <DashboardPage />
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
