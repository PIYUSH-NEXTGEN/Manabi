import { http, HttpResponse } from 'msw';

const stats = {
  problems: 6,
  sources: 3,
  fields: 5,
  projects: 2,
  ml_questions: 2,
};

const problems = [
  {
    id: 1,
    title: 'Crop disease triage for small farms',
    summary:
      'Farmers photograph leaf blight; a phone-first triage flow routes cases to the right extension officer.',
    who_affected: 'Smallholder farmers',
    why_matters: 'Late detection destroys a season of income.',
    field: 'computer-vision',
    domain: 'agriculture',
    difficulty: 'beginner',
    est_hours: 20,
    tech_tags: ['python', 'pytorch', 'mobile'],
    datasets: [],
    approaches: [
      'Fine-tune a small CNN on public leaf datasets',
      'Build an offline-first mobile capture flow',
    ],
    source_name: 'SIH 2026',
    source_id: 'SIH26017',
    source_url: null,
    source_note: null,
    project_count: 1,
    ai_fields: ['approaches'],
  },
  {
    id: 2,
    title: 'Streetlight outage tracker',
    summary:
      'Citizens report dead streetlights; the civic ops desk needs a queue that dedupes by pole and escalates SLAs.',
    who_affected: 'Municipal ward offices',
    why_matters: 'Dark streets cost money and feel unsafe.',
    field: 'web-fullstack',
    domain: 'governance',
    difficulty: 'intermediate',
    est_hours: 40,
    tech_tags: ['typescript', 'react', 'postgres'],
    datasets: [],
    approaches: [
      'Geo-hash reports to dedupe by pole location',
      'SLA escalation states per ward',
    ],
    source_name: 'TCOE',
    source_id: 'TCOE PS12',
    source_url: null,
    source_note: null,
    project_count: 1,
    ai_fields: ['approaches', 'est_hours'],
  },
  {
    id: 3,
    title: 'Fraud pattern walkthrough for UPI micro-transactions',
    summary:
      'A payment ops team samples 40k daily micro-transactions and needs a reproducible drift and rule-tuning notebook.',
    who_affected: 'Payment ops analysts',
    why_matters: 'Rule drift silently lets fraud through.',
    field: 'ml',
    domain: 'fintech',
    difficulty: 'advanced',
    est_hours: 60,
    tech_tags: ['python', 'pandas', 'scikit-learn'],
    datasets: [],
    approaches: [
      'Start with per-merchant z-score baselines',
      'Log rule precision weekly to catch drift',
    ],
    source_name: 'SIH 2026',
    source_id: 'SIH26104',
    source_url: null,
    source_note: null,
    project_count: 0,
    ai_fields: ['approaches'],
  },
  {
    id: 4,
    title: 'Ambulance ETA board for a district control room',
    summary:
      'District control rooms see stale ambulance locations; a live ETA board with honest uncertainty bands.',
    who_affected: 'District emergency controllers',
    why_matters: 'Minutes decide outcomes in emergencies.',
    field: 'geospatial',
    domain: 'disaster-management',
    difficulty: 'intermediate',
    est_hours: 35,
    tech_tags: ['python', 'leaflet', 'gtfs'],
    datasets: [],
    approaches: [
      'Blend last-known GPS with road-network speed priors',
      'Show ETA as a band, not a single number',
    ],
    source_name: 'OpenGov Data Challenge',
    source_id: null,
    source_url: null,
    source_note: 'Submission window closed 5 Oct 2026',
    project_count: 0,
    ai_fields: ['approaches', 'est_hours'],
  },
  {
    id: 5,
    title: 'Attendance pipeline that fails loudly',
    summary:
      'A school network imports biometric attendance CSVs; silent row drops must become alerts with a dry-run mode.',
    who_affected: 'School network administrators',
    why_matters: 'Silent data loss hides absent children.',
    field: 'data-engineering',
    domain: 'education',
    difficulty: 'beginner',
    est_hours: 24,
    tech_tags: ['python', 'airflow', 'pytest'],
    datasets: [],
    approaches: [
      'Row-count reconciliation at every hop',
      'Quarantine bad rows with a human-readable report',
    ],
    source_name: 'TCOE',
    source_id: 'TCOE PS03',
    source_url: null,
    source_note: null,
    project_count: 0,
    ai_fields: ['approaches'],
  },
  {
    id: 6,
    title: 'Pharmacy stock-out early warning',
    summary:
      'Primary health centres report weekly stock cards; predict stock-outs two weeks out with a rules-first baseline.',
    who_affected: 'Primary health centre pharmacists',
    why_matters: 'A stock-out means no treatment that day.',
    field: 'ml',
    domain: 'healthcare',
    difficulty: 'intermediate',
    est_hours: 30,
    tech_tags: ['python', 'timeseries', 'sql'],
    datasets: [],
    approaches: [
      'Two-week rolling consumption rate per item',
      'Only escalate when forecast drops below safety stock',
    ],
    source_name: 'SIH 2026',
    source_id: 'SIH26088',
    source_url: null,
    source_note: null,
    project_count: 0,
    ai_fields: ['approaches', 'who_affected'],
  },
];

const facets = {
  fields: [
    { value: 'ml', count: 2 },
    { value: 'computer-vision', count: 1 },
    { value: 'web-fullstack', count: 1 },
    { value: 'geospatial', count: 1 },
    { value: 'data-engineering', count: 1 },
  ],
  domains: [
    { value: 'agriculture', count: 1 },
    { value: 'governance', count: 1 },
    { value: 'fintech', count: 1 },
    { value: 'disaster-management', count: 1 },
    { value: 'education', count: 1 },
    { value: 'healthcare', count: 1 },
  ],
  difficulties: [
    { value: 'beginner', count: 2 },
    { value: 'intermediate', count: 3 },
    { value: 'advanced', count: 1 },
  ],
  tech_tags: [
    { value: 'python', count: 5 },
    { value: 'react', count: 1 },
    { value: 'pandas', count: 1 },
  ],
  sources: [
    { value: 'SIH 2026', count: 3 },
    { value: 'TCOE', count: 2 },
    { value: 'OpenGov Data Challenge', count: 1 },
  ],
};

const mlQuestions = [
  { id: 1, title: 'Train or test first? Splitting a tiny dataset', difficulty: 'beginner', topic: 'train-test-split', attempted: false },
  { id: 2, title: 'Accuracy says 98% but the model catches nothing', difficulty: 'beginner', topic: 'imbalanced-metrics', attempted: false },
  { id: 3, title: 'The model memorized the training set', difficulty: 'beginner', topic: 'overfitting-basics', attempted: false },
  { id: 4, title: 'Metrics lie after the launch', difficulty: 'beginner', topic: 'bad-eval-split', attempted: false },
  { id: 5, title: 'The model works offline, fails online', difficulty: 'intermediate', topic: 'train-serving-skew', attempted: false },
];

const mlQuestionDetail = {
  id: 1,
  title: 'Train or test first? Splitting a tiny dataset',
  difficulty: 'beginner',
  topic: 'train-test-split',
  attempted: false,
  scenario:
    '## Split first\nYou have 800 labeled customer reviews. One teammate says: train on all 800, check accuracy on the same 800. Another says: split 80/20 first.\n\nList what broke and what you would check first.',
};

const sampleProject = {
  id: 1,
  problem_id: 1,
  problem_title: 'Crop disease triage for small farms',
  repo_url: 'https://github.com/demo-farmer/crop-triage',
  repo_owner: 'demo-farmer',
  repo_name: 'crop-triage',
  open_for_contributors: true,
  owner: { username: 'demo-farmer', avatar_url: null },
  progress: {
    status: 'active',
    commit_count: 14,
    last_commit_at: '2026-10-16T09:24:00Z',
    has_readme: true,
    recent_commits: [
      { sha: 'a1b2c3d', message: 'Add offline capture queue', date: '2026-10-16' },
      { sha: 'e4f5a6b', message: 'Leaf classifier v0', date: '2026-10-14' },
    ],
    open_issues: [
      {
        number: 7,
        title: 'Handle low-light photos',
        url: 'https://github.com/demo-farmer/crop-triage/issues/7',
        labels: ['good first issue'],
      },
    ],
  },
  progress_updated_at: '2026-10-16T10:00:00Z',
};

const secondProject = {
  id: 2,
  problem_id: 2,
  problem_title: 'Streetlight outage tracker',
  repo_url: 'https://github.com/demo-civic/streetlight-ops',
  repo_owner: 'demo-civic',
  repo_name: 'streetlight-ops',
  open_for_contributors: false,
  owner: { username: 'demo-civic', avatar_url: null },
  progress: {
    status: 'stale',
    commit_count: 3,
    last_commit_at: '2026-10-02T18:00:00Z',
    has_readme: true,
    recent_commits: [
      { sha: 'f7g8h9i', message: 'Seed ward data', date: '2026-10-02' },
    ],
    open_issues: [],
  },
  progress_updated_at: '2026-10-02T19:00:00Z',
};

export const handlers = [
  http.get('*/api/health', () => HttpResponse.json({ status: 'ok' })),
  http.get('*/api/auth/me', () =>
    HttpResponse.json({ detail: 'Not authenticated' }, { status: 401 }),
  ),
  http.post('*/api/auth/logout', () => HttpResponse.json({})),
  http.get('*/api/stats', () => HttpResponse.json(stats)),
  http.get('*/api/problems/facets', () => HttpResponse.json(facets)),
  http.get('*/api/problems', ({ request }) => {
    const url = new URL(request.url);
    const limit = Number(url.searchParams.get('limit') ?? '20');
    const offset = Number(url.searchParams.get('offset') ?? '0');
    const q = url.searchParams.get('q');
    const field = url.searchParams.get('field');
    const domain = url.searchParams.get('domain');
    const difficulty = url.searchParams.get('difficulty');
    const source = url.searchParams.get('source');
    const tech = url.searchParams.getAll('tech');

    let filtered = problems;
    if (q) {
      const needle = q.toLowerCase();
      filtered = filtered.filter(
        (p) =>
          p.title.toLowerCase().includes(needle) ||
          p.summary.toLowerCase().includes(needle),
      );
    }
    if (field) filtered = filtered.filter((p) => p.field === field);
    if (domain) filtered = filtered.filter((p) => p.domain === domain);
    if (difficulty) {
      filtered = filtered.filter((p) => p.difficulty === difficulty);
    }
    if (source) filtered = filtered.filter((p) => p.source_name === source);
    if (tech.length > 0) {
      filtered = filtered.filter((p) => tech.every((t) => p.tech_tags.includes(t)));
    }

    return HttpResponse.json({
      items: filtered.slice(offset, offset + limit),
      total: filtered.length,
    });
  }),
  http.get('*/api/problems/:id', ({ params }) => {
    const found = problems.find((p) => p.id === Number(params.id));
    if (!found) {
      return HttpResponse.json({ detail: 'Problem not found' }, { status: 404 });
    }
    const detailProjects =
      found.id === 1 ? [sampleProject] : found.id === 2 ? [secondProject] : [];
    return HttpResponse.json({
      ...found,
      original_text: `${found.title}\n\n${found.summary}`,
      projects: detailProjects,
    });
  }),
  http.post('*/api/problems/:id/projects', async ({ request, params }) => {
    const problem = problems.find((p) => p.id === Number(params.id));
    if (!problem) {
      return HttpResponse.json({ detail: 'Problem not found' }, { status: 404 });
    }

    const body = (await request.json()) as {
      repo_url?: string;
      open_for_contributors?: boolean;
    };
    const repoUrl = body.repo_url ?? '';
    if (!/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(repoUrl)) {
      return HttpResponse.json(
        { detail: 'repo_url must be a GitHub repository URL' },
        { status: 422 },
      );
    }

    const clean = repoUrl.replace(/\.git$/, '');
    const parts = clean.split('/');
    const owner = parts[3];
    const name = parts[4];
    const nextId = Math.max(...problems.map((p) => p.id), 1) + 10;

    return HttpResponse.json({
      id: nextId,
      problem_id: problem.id,
      problem_title: problem.title,
      repo_url: repoUrl,
      repo_owner: owner,
      repo_name: name,
      open_for_contributors: body.open_for_contributors === true,
      owner: { username: owner, avatar_url: null },
      progress: {
        status: 'not_started',
        commit_count: 0,
        last_commit_at: null,
        has_readme: false,
        recent_commits: [],
        open_issues: [],
      },
      progress_updated_at: null,
    });
  }),
  http.get('*/api/ml/questions', () => HttpResponse.json(mlQuestions)),
  http.get('*/api/ml/questions/:id', ({ params }) => {
    if (Number(params.id) !== mlQuestionDetail.id) {
      return HttpResponse.json({ detail: 'Question not found' }, { status: 404 });
    }
    return HttpResponse.json(mlQuestionDetail);
  }),
  http.get('*/api/ml/questions/:id/attempts/me', () =>
    HttpResponse.json({ detail: 'No attempt yet' }, { status: 404 }),
  ),
  http.post('*/api/ml/questions/:id/attempts', async ({ params, request }) => {
    const id = Number(params.id);
    if (Number.isNaN(id) || !mlQuestions.some((q) => q.id === id)) {
      return HttpResponse.json({ detail: 'Question not found' }, { status: 404 });
    }
    const body = (await request.json()) as { answer?: unknown };
    const answer = typeof body.answer === 'string' ? body.answer : '';
    if (answer.trim().length < 20) {
      return HttpResponse.json(
        { detail: 'Answer must be at least 20 characters' },
        { status: 422 },
      );
    }
    return HttpResponse.json({
      id: 1,
      answer,
      created_at: '2026-10-17T09:00:00Z',
      feedback: {
        covered_count: 2,
        total: 4,
        items: [
          {
            point: 'Check the Monday-morning traffic pattern and seasonality split',
            covered: true,
          },
          {
            point: 'Audit the feature table for post-decision (leaked) columns',
            covered: true,
            evidence: 'You named days_since_final_push_notification as a suspect.',
          },
          { point: 'Compare offline AUC vs served AUC on a weekly rollup', covered: false },
          {
            point: 'Set up a monitoring alert on prediction variance',
            covered: false,
          },
        ],
        summary:
          'You caught the core skew points but missed the monitoring angle.',
      },
      explanation:
        '1. Pull the served predictions and bucket by day-of-week before anything else.\n2. Diff the feature snapshot used for training vs at serving time.',
    });
  }),
  http.post('*/api/chat', async ({ request }) => {
    const body = (await request.json()) as {
      messages?: Array<{ role: string; content: string }>;
      page_context?: { problem_id?: number };
    };
    const messages = body.messages ?? [];
    if (
      messages.length === 0 ||
      messages[messages.length - 1].role !== 'user' ||
      messages[messages.length - 1].content.trim().length === 0
    ) {
      return HttpResponse.json(
        { detail: 'messages must end with a non-empty user message' },
        { status: 422 },
      );
    }

    const problemMatches = body.page_context?.problem_id != null
      ? [problems.find((p) => p.id === body.page_context?.problem_id)]
      : [];

    return HttpResponse.json({
      reply:
        'Based on what you told me, the closest problems from the catalog are linked under this reply. Nothing here was invented — both are already in the index.',
      problems: [
        ...problemMatches,
        problems.find((p) => p.id === 5),
        problems.find((p) => p.id === 1),
      ]
        .filter((problem) => problem != null)
        .map((problem) => ({
          id: problem.id,
          title: problem.title,
          field: problem.field,
          difficulty: problem.difficulty,
        })),
    });
  }),
  http.get('*/api/recommendations', () =>
    HttpResponse.json({ detail: 'Not logged in' }, { status: 401 }),
  ),
  http.get('*/api/me/projects', () =>
    HttpResponse.json({ detail: 'Not logged in' }, { status: 401 }),
  ),
  http.post('*/api/ingest', async ({ request }) => {
    const body = (await request.json()) as {
      text?: string;
      url?: string;
    };
    if (!body.text?.trim() && !body.url?.trim()) {
      return HttpResponse.json(
        { detail: 'Either text or url is required' },
        { status: 422 },
      );
    }
    return HttpResponse.json({
      draft: {
        title: 'Crop disease triage for small farms',
        summary:
          'Farmers photograph leaf blight; a phone-first triage flow routes cases to the right extension officer.',
        who_affected: 'Smallholder farmers across three districts',
        why_matters: 'Late detection destroys a season of income.',
        field: 'computer-vision',
        domain: 'agriculture',
        difficulty: 'beginner',
        est_hours: 20,
        tech_tags: ['python', 'pytorch', 'mobile'],
        datasets: [],
        approaches: [
          'Fine-tune a small CNN on public leaf datasets',
          'Build an offline-first mobile capture flow',
        ],
        source_name: 'Pasted statement',
        source_id: null,
        source_url: body.url ?? null,
        source_note: null,
      },
      evidence: {
        who_affected:
          'The statement says "farmers with <2 hectares in district 4/5/8".',
        why_matters: 'The statement says "yield loss up to 40% when spraying misses first signs".',
        approaches: 'The statement lists "photo upload flow" as the planned method.',
      },
      source_url: body.url ?? null,
    });
  }),
  http.post('*/api/problems', async ({ request }) => {
    const body = (await request.json()) as { title?: string };
    const title = typeof body.title === 'string' ? body.title : 'Pasted problem';
    return HttpResponse.json(
      {
        id: 9,
        title,
        summary: 'Pasted.',
        who_affected: 'Someone',
        why_matters: 'It matters',
        field: 'ml',
        domain: 'education',
        difficulty: 'beginner',
        est_hours: 20,
        tech_tags: [],
        datasets: [],
        approaches: [],
        source_name: 'Pasted statement',
        source_id: null,
        source_url: null,
        source_note: null,
        project_count: 0,
        ai_fields: [],
        projects: [],
        original_text: title,
      },
      { status: 201 },
    );
  }),
  http.get('*/api/projects/:id', ({ params }) => {
    const id = Number(params.id);
    if (id === sampleProject.id) {
      return HttpResponse.json(sampleProject);
    }
    if (id === secondProject.id) {
      return HttpResponse.json(secondProject);
    }
    return HttpResponse.json({ detail: 'Project not found' }, { status: 404 });
  }),
  http.get('*/api/projects/:id/progress', ({ params, request }) => {
    const id = Number(params.id);
    const refresh = new URL(request.url).searchParams.get('refresh') === 'true';
    if (id !== sampleProject.id && id !== secondProject.id) {
      return HttpResponse.json({ detail: 'Project not found' }, { status: 404 });
    }
    if (refresh) {
      return HttpResponse.json({
        ...sampleProject.progress,
        commit_count: 15,
      });
    }
    return HttpResponse.json(sampleProject.progress);
  }),
];
