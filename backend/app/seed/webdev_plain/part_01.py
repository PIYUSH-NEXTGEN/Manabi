"""Plain-language overrides for the MANABI web development resume briefs."""

OVERRIDES = {
    "manabi-web-resume-001": {
        "summary": (
            "Build a progressive web app for field teams who collect forms, photos and GPS "
            "points where the network is unreliable. The app loads offline, keeps drafts and "
            "photos in IndexedDB, and sends queued work when the connection returns. It helps "
            "survey teams, NGOs and inspection crews.\n\n"
            "The tricky case is two field workers editing the same record before either one "
            "syncs. Each record carries a version and a change log. The server detects the "
            "conflict instead of overwriting. When it happens, the app shows both versions and "
            "lets the user merge them field by field."
        ),
        "who_affected": (
            "Field survey teams, NGO data collectors and inspection crews who work where the "
            "connection is weak."
        ),
        "why_matters": (
            "Lost forms and silent overwrites waste field time and make people distrust the "
            "collected data."
        ),
        "approaches": [
            "Cache the app shell with a service worker and keep drafts, photos and GPS points in IndexedDB.",
            "Queue writes in an outbox with idempotency keys, retry with backoff and show failed uploads to the user.",
            "Version each record and keep a change log so the server can spot conflicting edits.",
            "Give users a field-by-field merge screen instead of settling conflicts with last-write-wins.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "One form schema, offline drafts, queued uploads and a sync path that survives a page reload.",
                    "checks": [
                        "The app shell and form load with the network disabled.",
                        "Drafts, photos and GPS points stay in IndexedDB after a reload.",
                        "Queued records upload when the connection returns, and retries do not create duplicates.",
                        "A sync status screen shows queued, syncing, failed and completed records.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Two users edit the same record offline, reconnect and resolve the conflict without losing either version.",
                    "checks": [
                        "Each record carries a version and a change log that the server checks on write.",
                        "Conflicting edits open a merge screen with both values and a per-field choice.",
                        "Idempotency keys make repeated sync requests safe on flaky networks.",
                        "A test shows airplane-mode use, a forced conflict and a successful merge.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "You can own state, IndexedDB, service workers and the degraded-network experience, awkward states included.",
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "You designed the sync API, idempotency, versioning and the conflict contract across client and server.",
                },
                {
                    "role": "Mobile web / PWA engineer",
                    "how_it_helps": "Offline caching, reconnect behavior and storage limits are the core skills in this role.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built an offline-first PWA that queued {N} field records and synced them without duplicates after reconnects.",
                    "example": "Built an offline-first PWA that queued 1,200 field records and synced them without duplicates across flaky mobile connections.",
                },
                {
                    "bullet": "Cut lost field submissions to {X}% by adding IndexedDB drafts, idempotent retries and visible sync states.",
                    "example": "Cut lost field submissions from 8% to under 1% with IndexedDB drafts, idempotent retries and a sync status screen.",
                },
                {
                    "bullet": "Added versioned records and a merge UI so concurrent offline edits no longer overwrote each other.",
                    "example": "Added versioned records and a field-by-field merge UI. Two offline edits of the same survey could be reconciled without data loss.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why not use last-write-wins for conflicts?",
                    "answer": "Last-write-wins is simple, but it silently throws away a real person's work. In field data, one overwritten visit can waste a trip. I version records, detect conflicting edits on the server and ask the user to merge. I only fall back to a default rule for fields where losing data is acceptable.",
                },
                {
                    "question": "How do you stop a retry from creating duplicate records?",
                    "answer": "Each queued write gets a client-generated idempotency key. The server stores the key with the result and returns the same response for a repeat request. The client retries the same key until it gets a success or a conflict.",
                },
                {
                    "question": "What did you store in IndexedDB, and why not localStorage?",
                    "answer": "Forms, drafts, photo blobs, GPS points and the outbox. localStorage is synchronous, string-only and too small for photos. IndexedDB handles blobs, larger records and async access without blocking the UI.",
                },
            ],
            "differentiators": [
                "A real airplane-mode demo, not a screenshot of an offline banner.",
                "A clear conflict contract across client and server, with a merge screen that keeps both versions.",
                "Idempotent sync, which most tutorial-level offline apps leave out.",
            ],
        },
        "build_guide": [
            {
                "title": "Agree on the record shape and load the shell offline",
                "summary": "Start with the data that has to survive a dead network. Then make the app shell load without one.",
                "steps": [
                    "Write one form schema with text, number, date, photo and GPS fields. Decide what a record version means before you write sync code.",
                    "Create the React app shell, route table and empty states. Add a service worker that precaches the shell and a visible online/offline indicator.",
                    "Design the local IndexedDB stores: records, drafts, outbox entries, photo blobs and sync errors. Keep the outbox separate from the record table.",
                    "Seed two sample workers and a shared record so you can reproduce concurrent edits from two browser profiles.",
                ],
            },
            {
                "title": "Make every action write locally first",
                "summary": "Every user action writes to the device first. The network is an optional background step.",
                "steps": [
                    "Build the form editor with autosave, validation and a draft list. Save photo blobs and GPS coordinates without blocking the UI.",
                    "Add an outbox write on every save: record id, base version, changed fields, timestamp and a client-generated idempotency key.",
                    "Build the sync worker with online/offline listeners, exponential backoff and a manual retry button. Show queued, syncing, failed and conflict states.",
                    "Add a record history view that reads the local change log so the field worker can see what changed and when.",
                ],
            },
            {
                "title": "Build the sync API and the conflict rules",
                "summary": "The server has to reject stale writes and make repeated requests safe.",
                "steps": [
                    "Create the records and changes tables with a version column and a unique idempotency key for each write.",
                    "On write, compare the client base version with the current server version. Return 409 with both field values and the change history when they differ.",
                    "Store the idempotency key with the result so a retried request returns the same response instead of a duplicate.",
                    "Add endpoints for pulling updates after a cursor and for submitting a resolved merge with the next version.",
                ],
            },
            {
                "title": "Build the merge screen and the status screen",
                "summary": "The conflict screen is the product. It has to keep both versions visible and make the choice clear.",
                "steps": [
                    "List every conflicting field with mine, theirs, base and a per-field choice. Show who changed it and when beside each value.",
                    "Preview the merged record before saving. Disable submit until every conflict has a choice or an explicit keep-both resolution.",
                    "Build an outbox screen that groups records by queued, syncing, failed and conflict, with a retry action for failed items.",
                    "Add an airplane-mode demo page with clear instructions so someone can reproduce the flow in two minutes.",
                ],
            },
            {
                "title": "Harden, test and document the demo",
                "summary": "Offline apps break in the seams. Test reconnects, duplicate uploads and partial photo transfers.",
                "steps": [
                    "Add tests for idempotent retries, stale-version conflicts, merge submission and service-worker cache updates.",
                    "Throttle the network in DevTools. Check that a failed photo upload does not block the text record from syncing.",
                    "Write a README with the sync contract, IndexedDB schema, conflict rules, local setup and a short demo script.",
                    "Record a short walkthrough of offline creation, reload, reconnect and conflict resolution. Link it from the repo.",
                ],
            },
        ],
    },
    "manabi-web-resume-002": {
        "summary": (
            "Build a public issue tracker for local civic problems such as potholes, broken "
            "streetlights and missed garbage collection. Residents send a photo and a location. "
            "The system groups duplicates, assigns a category and department, and tracks each "
            "issue against a service-level timer. Residents, municipal staff and ward offices "
            "all use it.\n\n"
            "Duplicate detection can start simple. Bucket reports by rounded location, compare "
            "their text with a similarity score and check how close they are in time. Tune the "
            "threshold on a small labelled set so nearby but different problems stay apart. The "
            "rest is careful product logic: an audit trail, clear assignment rules, an SLA clock "
            "that pauses and escalates correctly, and a moderation path for bad reports."
        ),
        "who_affected": (
            "Residents who report local problems, municipal staff who handle complaints and ward "
            "offices that track service levels."
        ),
        "why_matters": (
            "Duplicate reports hide the real backlog, and a missed SLA turns a small civic "
            "problem into a long complaint."
        ),
        "approaches": [
            "Store reports with location, category, photo and a timestamped status history.",
            "Build duplicate candidates from nearby location buckets plus text similarity.",
            "Assign departments with configurable category rules and start an SLA timer.",
            "Give staff a merge, split and moderation view so they can correct automated grouping.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Residents submit reports, staff see a queue and each report has a category, status and SLA deadline.",
                    "checks": [
                        "A report captures a photo, a location, a category and a short description.",
                        "Staff can move a report through open, in progress and resolved states.",
                        "Each report shows an SLA deadline and whether it is close to breaching.",
                        "A public page lists issues without names, emails or precise addresses.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Nearby reports of the same problem collapse into one issue, and staff can fix the grouping when automation is wrong.",
                    "checks": [
                        "Location buckets and text similarity suggest duplicates with a visible score.",
                        "Staff can merge duplicates and split a bad merge without losing the original reports.",
                        "The audit trail records who changed status, when and why.",
                        "The public page groups resolved issues by ward and shows average resolution time.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "You built the public intake, staff workflow, duplicate logic and reporting layer end to end.",
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": "Duplicate matching, SLA state machines, audit records and privacy rules are practical backend design work.",
                },
                {
                    "role": "Product engineer",
                    "how_it_helps": "You can explain the trade-off between false merges and a duplicate backlog, which is the central product problem.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a civic issue tracker that grouped duplicate reports and cut the staff queue by {X}%.",
                    "example": "Built a civic issue tracker that grouped duplicate reports by location and text similarity, cutting the ward staff queue by 35% in a pilot dataset.",
                },
                {
                    "bullet": "Tracked {N} issues against SLA timers with an audit trail and a public status page.",
                    "example": "Tracked 4,000 sample issues against service-level timers, with an audit trail for every status change and a public status page.",
                },
                {
                    "bullet": "Added staff merge and split controls so automated duplicate detection could be corrected without losing reports.",
                    "example": "Added staff merge and split controls. False duplicate matches could be corrected without deleting either resident's report.",
                },
            ],
            "interview_points": [
                {
                    "question": "How did you tune duplicate detection?",
                    "answer": "I started with a labelled sample and tried location buckets plus text similarity. I looked at false merges separately from missed duplicates. A false merge hides a distinct problem, so I chose a conservative threshold and added a staff correction screen.",
                },
                {
                    "question": "How does the SLA clock work?",
                    "answer": "The clock starts when a report is accepted and lands in the right category. Status changes are stored with timestamps. Paused states such as waiting on a resident stop the clock. The deadline is recalculated from the stored history instead of a single mutable field.",
                },
                {
                    "question": "What is public and what is private?",
                    "answer": "The public page shows category, status, rough area and resolution time. It hides names, contact details, precise coordinates and photos that could identify someone. Staff see the full report after signing in.",
                },
            ],
            "differentiators": [
                "A correction path for duplicate detection instead of pretending the classifier is always right.",
                "An SLA model built on an auditable status history, not a mutable due date.",
                "A public page designed around privacy, not a second admin table.",
            ],
        },
        "build_guide": [
            {
                "title": "Model reports, issues and service levels",
                "summary": "Keep a resident report separate from the issue staff work on. That split makes duplicate handling possible.",
                "steps": [
                    "Define report, issue, status event, department, category and SLA policy records. A report can point at one issue. An issue can have many reports.",
                    "Store rough location for public views and precise coordinates for staff. Write down the rule for what leaves the building.",
                    "Write the status transition table: open, triaged, assigned, in progress, paused, resolved and reopened. Record who changed it, when and why.",
                    "Seed three wards, five categories, department routing rules and a small set of duplicate and non-duplicate reports.",
                ],
            },
            {
                "title": "Build intake and duplicate candidates",
                "summary": "Accept reports quickly, then score possible duplicates without merging them silently.",
                "steps": [
                    "Build the resident form with photo upload, category hints and browser geolocation. Allow a rough location when GPS is denied.",
                    "Bucket nearby reports by rounded coordinates and compare descriptions with a simple text similarity score.",
                    "Show the top candidates to staff with distance, time gap and score. Never auto-merge without a visible confirmation step.",
                    "Add a labelled evaluation file so threshold changes can be checked against known duplicate and distinct pairs.",
                ],
            },
            {
                "title": "Build the staff workflow and SLA clock",
                "summary": "Staff need a fast queue, an audit trail and a deadline that recalculates from real events.",
                "steps": [
                    "Create the staff queue with filters for ward, category, department, status and SLA risk.",
                    "Add merge and split actions that move reports between issues without deleting either report or its history.",
                    "Compute the SLA deadline from stored status events. Pause on waiting states and escalate when the remaining time crosses a threshold.",
                    "Add a moderation action for abusive or invalid reports, with a reason that appears in the audit log.",
                ],
            },
            {
                "title": "Build the public status experience",
                "summary": "The public page should show progress without turning residents into a data source for harassment.",
                "steps": [
                    "Publish a map and list that show category, rough area, status and resolution time while hiding names, contacts and exact addresses.",
                    "Show a resolved-this-month summary by ward with average time to resolution and the number of open issues.",
                    "Make the public page read from a projection with only public fields, not from the staff table with hidden columns.",
                    "Add a simple report lookup by reference code so a resident can follow their issue without an account.",
                ],
            },
            {
                "title": "Test corrections, privacy and the demo",
                "summary": "The correction path is what makes duplicate detection trustworthy.",
                "steps": [
                    "Test a false merge and a false split, including the audit entries and the public counts after each correction.",
                    "Add SLA tests for pause, resume, breach and overnight and weekend boundaries.",
                    "Review every public API response for leaked personal data. Add a test that fails if a private field appears.",
                    "Write an operator guide and a demo script covering intake, duplicate merge, correction, resolution and the public report.",
                ],
            },
        ],
    },
    "manabi-web-resume-003": {
        "summary": (
            "Build a search tool for developers who want a useful first contribution. It queries "
            "GitHub issues labelled for beginners, filters by language and topic, and ranks "
            "repositories by signs that predict a good first experience: recent activity, a "
            "contributing guide, issue response time and how often maintainers close outside "
            "pull requests. New contributors, maintainers and bootcamp mentors use it.\n\n"
            "The ranking explanation is the interesting part. Every score shows its inputs so a "
            "user can tell whether a repository is friendly or simply popular. Add filters for "
            "language, label, recent activity and minimum stars. Test the ranking against a "
            "small set of repositories you have actually read."
        ),
        "who_affected": (
            "New contributors looking for a first pull request, maintainers who label beginner "
            "issues and bootcamp mentors."
        ),
        "why_matters": (
            "A welcoming issue list turns curiosity into a merged pull request. A bad pick "
            "wastes days and discourages new contributors."
        ),
        "approaches": [
            "Search GitHub issues by label, language and recency, then fetch repository metadata in batches.",
            "Cache API responses with ETags and show when cached data was last refreshed.",
            "Rank repositories with signals you can explain: activity, contributing guide, response time and issue turnover.",
            "Let users save issues and track their own contribution progress.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Search beginner-labelled issues by language, open a result and save it for later.",
                    "checks": [
                        "The app calls the GitHub search API and shows issue title, repository, labels and language.",
                        "Results paginate and handle an empty result set cleanly.",
                        "A user can save and unsave an issue, and saved items persist.",
                        "API errors and rate-limit responses produce a useful message instead of a blank screen.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Each repository gets a transparent welcome score, and the app stays useful when GitHub rate-limits the client.",
                    "checks": [
                        "The ranking shows the exact signals behind each score, with more than a bare number.",
                        "Conditional requests and caching reduce repeated API calls and display cache age.",
                        "Users can filter by recent activity, stars, labels and language.",
                        "A saved issue shows a simple progress state: saved, opened, first comment, pull request opened.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "You combined an external API, caching, ranking and user state in one product.",
                },
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "The filters, score explanations and saved-item pipeline show practical UI work with live third-party data.",
                },
                {
                    "role": "Developer experience engineer",
                    "how_it_helps": "The project makes contribution paths clearer, which is core developer-experience work.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a contribution finder that ranked {N} repositories with explainable welcome signals and cached API responses.",
                    "example": "Built a contribution finder that ranked 800 repositories by activity, response time and contributing guidance, with cached responses that cut API calls by 60%.",
                },
                {
                    "bullet": "Cut GitHub API usage by {X}% using ETags, batched requests and a visible cache for stale issue data.",
                    "example": "Cut GitHub API usage by 55% with ETags and batched repository fetches, and labelled cached results with their last refresh time.",
                },
                {
                    "bullet": "Let users track saved issues from bookmark to first pull request in one place.",
                    "example": "Added a saved-issue pipeline with saved, opened, commented and pull-request-opened states for first-time contributors.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you rank a welcoming repository?",
                    "answer": "I use signals I can explain: recent commits and issue activity, a contributing guide, how fast maintainers answer beginner issues and whether issues get closed. I show each signal so the user can ignore a score they disagree with.",
                },
                {
                    "question": "How do you handle GitHub rate limits?",
                    "answer": "I cache responses with ETags and batch repository lookups instead of one request per card. I page only what the user needs and back off when the remaining quota is low. The UI shows cached data and its age instead of failing silently.",
                },
                {
                    "question": "What makes a good first issue?",
                    "answer": "A clear scope, a reproducible problem, acceptance criteria and a maintainer who responds. Labels help, but activity and response behavior matter more. The project surfaces those signals because a beginner label alone is not enough.",
                },
            ],
            "differentiators": [
                "Ranking with visible inputs, not a mystery score.",
                "Cache-age labels that keep the product honest under API limits.",
                "A saved-issue pipeline that follows the contribution from bookmark to pull request.",
            ],
        },
        "build_guide": [
            {
                "title": "Design the search and ranking contract",
                "summary": "Decide what a good first contribution means before you call the API.",
                "steps": [
                    "List the signals you will show: recent commit activity, issue response time, contributing guide, label quality and stars. Give each one a clear input and weight.",
                    "Define the result shape: issue, repository, language, labels, last activity, score and the signal breakdown.",
                    "Write down the empty, rate-limited and stale-cache states so the UI does not treat them as success.",
                    "Create a small evaluation sheet with 15-20 repositories you have inspected and a note on whether each was welcoming.",
                ],
            },
            {
                "title": "Build the GitHub client and cache",
                "summary": "The wrapper has to respect pagination, rate limits and conditional requests.",
                "steps": [
                    "Build the search and repository lookup calls with pagination and a server-side token. Keep the token out of the browser.",
                    "Cache responses with ETags and a fetched-at timestamp. Serve cached data with an age label when the API refuses or rate-limits.",
                    "Batch repository metadata fetches instead of one request per card. Store only the fields the ranking and UI need.",
                    "Add backoff and a clear error object for unauthorized, rate-limited and partial-response cases.",
                ],
            },
            {
                "title": "Implement explainable ranking",
                "summary": "Every score should be rebuildable from inputs the user can see.",
                "steps": [
                    "Compute each signal on its own and normalize it against the current result set or a documented range.",
                    "Combine the signals into one score, then show a breakdown with the raw value and the points each one added.",
                    "Add filters for language, label, minimum stars, recent activity and repository age.",
                    "Run the ranking against your evaluation sheet, adjust weights and write down what changed.",
                ],
            },
            {
                "title": "Build search, saved issues and progress",
                "summary": "The user needs a path from curiosity to a first pull request.",
                "steps": [
                    "Build the search page with URL-synced filters, result pagination and a cache-age banner.",
                    "Add a repository detail panel with score inputs, contributing-guide status and direct links to the issue and repository.",
                    "Implement save, hide and progress states. Persist them per user and show a simple saved-issues board.",
                    "Add an empty state that suggests removing a narrow filter instead of showing a blank page.",
                ],
            },
            {
                "title": "Evaluate, document and demo",
                "summary": "The ranking is the claim. The evaluation is the evidence.",
                "steps": [
                    "Add tests for cache hits, rate-limit fallback, filter combinations and pipeline transitions.",
                    "Write a short evaluation note with the repositories inspected, the false positives and the final thresholds.",
                    "Document the API limits, caching policy and how to run the app with a personal token locally.",
                    "Record a demo that searches, explains a score, saves an issue and moves it to pull-request-opened.",
                ],
            },
        ],
    },
    "manabi-web-resume-004": {
        "summary": (
            "Build a coordination board for disaster response where responders and community "
            "members post needs and offers. That covers food, water, shelter, medical help and "
            "transport. Needs and offers appear on a live map, the system suggests nearby "
            "matches, and every match has a fulfilment trail.\n\n"
            "Design for poor connectivity. The web app keeps the last known board available, "
            "queues updates and falls back to an SMS or WhatsApp notification when a device "
            "cannot stay online. Duplicates stay visible on purpose. Two people may report the "
            "same shelter, and a coordinator needs to see both claims before marking it fulfilled."
        ),
        "who_affected": (
            "Disaster response coordinators, relief volunteers and affected communities posting "
            "urgent needs."
        ),
        "why_matters": (
            "During a response, duplicate requests and slow matching leave resources idle while "
            "people wait."
        ),
        "approaches": [
            "Model needs and offers with location, quantity, contact visibility and fulfilment state.",
            "Match nearby complementary records with distance and category rules.",
            "Keep a live board over WebSockets and queue offline edits in the browser.",
            "Send an SMS or WhatsApp fallback when a coordinator cannot stay online.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Coordinators can post, view and fulfil needs and offers on a map that updates for everyone.",
                    "checks": [
                        "Needs and offers have a category, location, quantity and contact visibility setting.",
                        "The board updates live when another coordinator adds or fulfils an item.",
                        "A simple distance rule suggests nearby complementary offers and needs.",
                        "Contact details stay hidden from the public view.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The hub keeps working on a weak connection and gives coordinators a clear fulfilment trail for every match.",
                    "checks": [
                        "Offline edits are queued and replayed when the connection returns.",
                        "SMS or WhatsApp fallback sends a compact update when the live board cannot be reached.",
                        "Every match records who proposed it, who accepted it and when it was fulfilled.",
                        "The daily export summarizes open needs, unmatched offers and completed deliveries.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "You built the live board, matching rules, fulfilment model and fallback channel together.",
                },
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "The map, live updates and degraded-network states show real operational UI work.",
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": "Matching, role checks, delivery tracking and notification fallbacks are practical backend problems.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a live disaster resource board that matched {N} needs and offers by location and category.",
                    "example": "Built a live disaster resource board that matched 600 sample needs and offers by location and category, with a fulfilment trail for each match.",
                },
                {
                    "bullet": "Kept coordination usable on weak networks with offline queues and an SMS fallback.",
                    "example": "Kept coordination usable on weak networks by queueing offline board edits and sending SMS fallback updates when the live app was unreachable.",
                },
                {
                    "bullet": "Separated public map data from coordinator-only contact details without slowing the response workflow.",
                    "example": "Separated public map data from coordinator-only contact details, so residents could see needs without exposing phone numbers.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you handle duplicate needs during a response?",
                    "answer": "I do not hide duplicates. I show them as possible matches and let a coordinator merge or link them. Location, category and time can suggest duplicates, but a person confirms because two similar requests may be two real families.",
                },
                {
                    "question": "Why add an SMS fallback instead of a PWA alone?",
                    "answer": "A PWA helps while the user can keep the page open, but disaster networks fail and batteries die. SMS or WhatsApp gives a low-bandwidth path to the same coordinator. The app generates a short message with the item ID and status update.",
                },
                {
                    "question": "How did you decide who can see contact details?",
                    "answer": "Public viewers see category, rough location and status only. Signed-in coordinators with an active role can reveal contact details for an open item, and that reveal is logged. The map stays useful without turning into a public contact list.",
                },
            ],
            "differentiators": [
                "A fallback channel for when the live board cannot load.",
                "Duplicate-friendly matching that leaves the final decision with a coordinator.",
                "A fulfilment trail instead of a status field that anyone can overwrite.",
            ],
        },
        "build_guide": [
            {
                "title": "Model needs, offers and response roles",
                "summary": "A disaster board is a coordination record, not a social feed.",
                "steps": [
                    "Define need, offer, match, delivery event and contact-reveal records with category, quantity, location and status.",
                    "Choose the role model: public viewer, field worker and coordinator. Write down which role can create, match, reveal contact details and close an item.",
                    "Separate public fields from coordinator-only fields at the query layer, not with a hidden field in the UI.",
                    "Seed a realistic response scenario with food, water, shelter, medical and transport records across a few neighbourhoods.",
                ],
            },
            {
                "title": "Build the live board and match flow",
                "summary": "The board has to update for everyone, and every match must leave a trail.",
                "steps": [
                    "Build the map and list views with category filters, status badges and a clear stale-data indicator.",
                    "Add WebSocket updates for create, update, match and fulfil events. Fall back to polling when the socket cannot connect.",
                    "Implement proximity and category matching that suggests complementary needs and offers, with distance and quantity shown.",
                    "Record proposed, accepted, picked up and delivered events with actor, timestamp and note. Never reduce the trail to one status field.",
                ],
            },
            {
                "title": "Add offline queue and fallback messaging",
                "summary": "Connectivity is a feature state, not an error page.",
                "steps": [
                    "Queue board edits and match updates in the browser when offline. Replay them with idempotency keys on reconnect.",
                    "Keep the last known board snapshot available and label its age so coordinators do not treat old data as live.",
                    "Generate a compact SMS or WhatsApp message for a match or urgent need, with an item reference and a short status line.",
                    "Test on a throttled connection: drop the socket, make an edit, reconnect and confirm the board reconciles.",
                ],
            },
            {
                "title": "Build privacy, verification and exports",
                "summary": "Contact data and offer quality need explicit controls.",
                "steps": [
                    "Log every contact-detail reveal with the coordinator, item and time. Show the log to admins.",
                    "Add a simple offer verification state and a note field. Keep unverified offers visible but clearly marked.",
                    "Build a daily export with open needs, unmatched offers, active matches and completed deliveries.",
                    "Add an admin view for duplicate clusters so coordinators can link two reports without deleting either one.",
                ],
            },
            {
                "title": "Run a drill, test failures and document it",
                "summary": "The project is credible only if it works under a realistic failure.",
                "steps": [
                    "Write tests for role permissions, contact visibility, match transitions and offline replay.",
                    "Run a two-browser drill: create a need, match an offer, disconnect one browser, complete delivery, then reconnect.",
                    "Check the daily export against the board after the drill and reconcile any mismatch.",
                    "Document setup, the fallback message format, the drill script and the privacy model in the README.",
                ],
            },
        ],
    },
    "manabi-web-resume-005": {
        "summary": (
            "Build a guided tool for small businesses that want to export a product to a new "
            "country. The user picks a product and a target market. The tool returns a checklist "
            "of required documents, regulations, duties and market notes. Every item links to an "
            "official source and shows the date it was checked.\n\n"
            "Regulations change, so the source records carry versions and a last-reviewed date. "
            "The chat assistant answers only from stored sources and refuses when they do not "
            "cover the question. Citations sit next to every answer. A user can always see where "
            "each claim came from."
        ),
        "who_affected": (
            "Small exporters, trade consultants and small-business owners checking requirements "
            "before a first shipment."
        ),
        "why_matters": (
            "One missing document or duty can stop a shipment. Scattered unofficial advice makes "
            "a first export expensive and risky."
        ),
        "approaches": [
            "Model products, markets, documents and regulations as separate records with source links.",
            "Version each source with a last-checked date and show it beside the claim.",
            "Restrict the chat assistant to retrieved source passages and require citations.",
            "Add a printable checklist and a clear not-legal-advice notice.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "One product and one country produce a cited checklist with documents, duties and official links.",
                    "checks": [
                        "The user selects a product and country from a small curated set.",
                        "Each checklist item shows a requirement, source link and last-checked date.",
                        "The page clearly states that it is not legal advice.",
                        "A printable view keeps the citations intact.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Three products and three countries work, and the chat answers only with cited passages from the stored sources.",
                    "checks": [
                        "Source records are versioned and updates do not silently rewrite old claims.",
                        "The chat retrieves passages, answers with citations and refuses unsupported questions.",
                        "A coverage view shows which product-country pairs have complete source data.",
                        "A reviewer can update a rule and see exactly which checklist items changed.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "You built structured domain data, a guided UI, source versioning and a retrieval-backed assistant.",
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": "Versioned sources, coverage checks, retrieval limits and citation enforcement are practical backend concerns.",
                },
                {
                    "role": "AI application engineer",
                    "how_it_helps": "You can explain retrieval boundaries, citations and refusal behavior, with model calls as only one part.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a cited export-readiness assistant covering {P} products and {C} countries with source dates on every claim.",
                    "example": "Built a cited export-readiness assistant covering 3 products and 3 countries, with an official source and last-checked date on every checklist item.",
                },
                {
                    "bullet": "Restricted the chat assistant to stored sources and required citations, eliminating uncited regulatory answers.",
                    "example": "Restricted the chat assistant to retrieved official passages and required citations. Unsupported questions returned a clear refusal instead of a guess.",
                },
                {
                    "bullet": "Versioned source records so a regulation update could be reviewed without losing the previous claim.",
                    "example": "Versioned source records and displayed review dates, so a tariff update could be reviewed against the previous checklist without losing history.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you keep the assistant from inventing regulations?",
                    "answer": "The model only sees retrieved source passages and must answer from them with citations. If retrieval returns nothing relevant, the app refuses. I also keep regulatory claims as structured records so the checklist does not depend on free-form generation.",
                },
                {
                    "question": "Why store checklist items as structured data?",
                    "answer": "A regulation update should change one rule, not a paragraph that mentions five things. Structured items let me show coverage, version changes and a printable checklist from one source of truth.",
                },
                {
                    "question": "How do you handle outdated sources?",
                    "answer": "Every source has a last-checked date and a version. The UI shows the date, and items older than a threshold are marked for review. A reviewer updates the source, and the affected checklist items keep their old version in history.",
                },
            ],
            "differentiators": [
                "Source dates and citations on every claim, including the printable view.",
                "A refusal path for questions the stored sources cannot answer.",
                "Structured rules with version history instead of a static advice page.",
            ],
        },
        "build_guide": [
            {
                "title": "Curate the source corpus and checklist model",
                "summary": "Three markets done properly beat thirty markets with unverifiable claims.",
                "steps": [
                    "Pick three products and three destination markets. Collect official documents, forms and tariff pages for each pair.",
                    "Define requirement, source, source-version, product, market and coverage records. Keep the checklist derived from those records.",
                    "Write a plain-language note for each requirement and mark the exact source passage that supports it.",
                    "Define the source review date and a rule for what happens when an item is past its review window.",
                ],
            },
            {
                "title": "Build the checklist engine and coverage view",
                "summary": "The checklist has to be a query over structured rules, not a hand-written page.",
                "steps": [
                    "Build product-country selection and generate a checklist grouped by documents, duties, labeling and market notes.",
                    "Show the source link, source date and plain-language note for every item. Add a printable view that keeps citations.",
                    "Build a coverage matrix that shows incomplete product-country pairs instead of hiding gaps.",
                    "Add a reviewer workflow to update a rule and see which checklist items changed.",
                ],
            },
            {
                "title": "Build grounded retrieval and citations",
                "summary": "The assistant is useful only when it can prove where an answer came from.",
                "steps": [
                    "Chunk the curated sources with stable ids and embed or index them for retrieval.",
                    "Retrieve passages for the question, pass only those passages to the model and require a citation id for each claim.",
                    "Return a refusal when retrieval is weak or the passages do not answer the question. Show the retrieved passages beside the answer.",
                    "Log the question, retrieved ids and refusal reason so failures can be reviewed.",
                ],
            },
            {
                "title": "Build the user-facing workflow",
                "summary": "The interface should guide a first exporter without pretending to be a lawyer.",
                "steps": [
                    "Create a short intake flow for product, destination and shipment context, then land on the generated checklist.",
                    "Add progress checkboxes, notes and a summary the user can share with a trade consultant.",
                    "Show the not-legal-advice notice beside the checklist and in the printable view, not buried in the footer.",
                    "Add source freshness warnings when any supporting item is past its review date.",
                ],
            },
            {
                "title": "Validate, document and demo",
                "summary": "Traceability is the point of the project, so show the evidence.",
                "steps": [
                    "Test that every checklist item has a valid source and that the assistant cannot answer without a citation.",
                    "Add a regression fixture for one changed regulation and verify the old and new checklist versions.",
                    "Write a README covering the source policy, coverage limits, retrieval design and local setup.",
                    "Record a demo that shows a cited checklist, a source update and a refusal for an unsupported question.",
                ],
            },
        ],
    },
}
