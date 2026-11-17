"""Seed 20 web development resume projects."""

from app.seed.runner import seed_problems
from app.seed.webdev_resume_details import DETAILS as RESUME_DETAILS


PROBLEMS = [
    dict(
        source_id="manabi-web-resume-001",
        title="Offline-First Field Data Collection PWA with Conflict-Free Sync",
        summary=(
            "Build a progressive web app for field teams who collect forms, "
            "photos and GPS points where the network is unreliable. Everything "
            "works offline first: the app shell is cached, drafts and photos "
            "live in IndexedDB, and a sync queue sends them when connectivity "
            "returns.\n\n"
            "The hard part is not storing data locally. It is deciding what "
            "happens when two field workers edit the same record before either "
            "one syncs. Give every record a version, keep a per-record change "
            "log, and detect conflicts on the server instead of silently "
            "overwriting. When a conflict happens, show both versions side by "
            "side and let the user merge field by field.\n\n"
            "The demo runs in airplane mode: create records, reload the app, "
            "edit the same record from two browser profiles, reconnect, and "
            "resolve the conflict. Add retries with backoff, idempotency keys "
            "so repeated uploads do not create duplicates, and a small status "
            "screen that shows queued, syncing, failed and conflict states."
        ),
        who_affected="Field survey teams, NGO data collectors, and inspection crews working in low-connectivity areas.",
        why_matters="Lost forms and silent overwrites waste field time and destroy trust in the collected data.",
        field="web-dev",
        domain="social-impact",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["typescript", "react", "pwa", "indexeddb", "service-worker", "sync"],
        datasets=[{"name": "Sample field survey forms", "url": None}],
        approaches=[
            "Cache the app shell with a service worker and store drafts, photos and GPS points in IndexedDB.",
            "Queue writes in an outbox with idempotency keys, retry with backoff, and surface failed uploads.",
            "Version each record and keep a change log so the server can detect conflicting edits.",
            "Provide a field-by-field merge screen instead of resolving conflicts with last-write-wins.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build an offline-first PWA for forms, photos and GPS points with a sync queue and a clear conflict-resolution screen.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "One form schema, offline drafts, queued uploads and a working sync path that survives a page reload.",
                    "checks": [
                        "The app shell and form load with the network disabled.",
                        "Drafts, photos and GPS points persist in IndexedDB after a reload.",
                        "Queued records upload when the connection returns, and retries do not create duplicates.",
                        "A sync status screen shows queued, syncing, failed and completed records.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Two users can edit the same record offline, reconnect and resolve the conflict without losing either version.",
                    "checks": [
                        "Each record carries a version and a change log that the server checks on write.",
                        "Conflicting edits open a merge screen with both values and a per-field choice.",
                        "Idempotency keys make repeated sync requests safe under flaky networks.",
                        "A test demonstrates airplane-mode use, a forced conflict and a successful merge.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "Shows you can handle state, storage, service workers and degraded-network UX, not just happy-path screens."},
                {"role": "Full-stack engineer", "how_it_helps": "You designed the sync API, idempotency and conflict contract across client and server."},
                {"role": "Mobile web / PWA engineer", "how_it_helps": "Offline storage, caching and reconnect behavior are the core skills in this role."},
                {"role": "Backend engineer", "how_it_helps": "The server side is real API work: version checks, retries, duplicate suppression and conflict responses."},
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
                    "example": "Added versioned records and a field-by-field merge UI; two offline edits of the same survey could be reconciled without data loss.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why not just use last-write-wins for conflicts?",
                    "answer": "Last-write-wins is simple but silently discards a real person's work. For field data, one overwritten visit can waste a trip. I version records, detect conflicting edits on the server, and ask the user to merge. I only fall back to a default rule for fields where loss is acceptable.",
                },
                {
                    "question": "How do you stop a retry from creating duplicate records?",
                    "answer": "Each queued write gets a client-generated idempotency key. The server stores the key with the result and returns the same response for a repeat request. The client retries the same key until it receives a success or a conflict.",
                },
                {
                    "question": "What did you store in IndexedDB, and why not localStorage?",
                    "answer": "Forms, drafts, photo blobs, GPS points and the outbox. localStorage is synchronous, string-only and too small for photos. IndexedDB handles blobs, larger records and async access without blocking the UI.",
                },
            ],
            "differentiators": [
                "A real airplane-mode demo, not a screenshot of an offline banner.",
                "An explicit conflict contract across client and server, with a merge screen that keeps both versions.",
                "Idempotent sync, which is usually missing from tutorial-level offline apps.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-002",
        title="Civic Issue Tracker with Duplicate Detection",
        summary=(
            "Build a public issue tracker for local civic problems: potholes, "
            "broken streetlights, garbage collection and similar complaints. "
            "Residents submit a photo and a location. The system groups "
            "duplicates, assigns a category and department, and tracks each "
            "issue against a service-level timer.\n\n"
            "Duplicate detection can start simple. Bucket reports by rounded "
            "location, compare their text with a similarity score, and look at "
            "how close the reports are in time. Tune the threshold with a small "
            "labelled set so nearby but different problems do not get merged. "
            "Keep a public status page that shows open, in-progress and resolved "
            "issues without exposing personal details.\n\n"
            "The work is mostly careful product logic: an audit trail for status "
            "changes, clear assignment rules, an SLA clock that pauses or "
            "escalates correctly, and a moderation path for bad reports. Add a "
            "small admin view where staff can merge false splits and split false "
            "merges."
        ),
        who_affected="Residents reporting local problems, municipal staff handling complaints, and ward offices tracking service levels.",
        why_matters="Duplicate reports hide the real backlog, while missed SLAs turn small civic problems into long-running complaints.",
        field="web-dev",
        domain="governance",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["typescript", "react", "postgres", "geospatial", "rest-api", "moderation"],
        datasets=[{"name": "Sample civic issue reports", "url": None}],
        approaches=[
            "Store reports with location, category, photo and a timestamped status history.",
            "Generate duplicate candidates from nearby location buckets plus text similarity.",
            "Assign departments with configurable category rules and start an SLA timer.",
            "Give staff a merge, split and moderation view so automated grouping can be corrected.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a civic issue tracker that groups duplicate reports, routes them to departments, tracks service-level timers and shows a public status page.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Residents submit reports, staff see a queue, and each report has a category, status and SLA deadline.",
                    "checks": [
                        "A report captures a photo, a location, a category and a short description.",
                        "Staff can move a report through open, in progress and resolved states.",
                        "Each report shows an SLA deadline and whether it is close to breaching.",
                        "A public page lists issues without names, emails or precise addresses.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Nearby reports of the same problem collapse into one issue, and staff can correct the grouping when the automation is wrong.",
                    "checks": [
                        "Location buckets and text similarity propose duplicates with a visible score.",
                        "Staff can merge duplicates and split a bad merge without losing the original reports.",
                        "The audit trail records who changed status, when and why.",
                        "The public page groups resolved issues by ward and shows average resolution time.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You built the data model, public submission flow, staff workflow and status logic end to end."},
                {"role": "Backend engineer", "how_it_helps": "Duplicate matching, SLA timers and audit records are practical backend design work."},
                {"role": "Frontend engineer", "how_it_helps": "The staff queue and moderation screens show form-heavy, state-heavy UI work."},
                {"role": "Product-minded engineer", "how_it_helps": "You can explain the trade-off between false merges and duplicate backlog, which is the real product problem."},
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
                    "example": "Added staff merge and split controls; false duplicate matches could be corrected without deleting either resident's report.",
                },
            ],
            "interview_points": [
                {
                    "question": "How did you tune duplicate detection?",
                    "answer": "I started with a labelled sample, tried location buckets and text similarity, and looked at false merges separately from missed duplicates. A false merge hides a distinct problem, so I chose a conservative threshold and added a staff correction screen.",
                },
                {
                    "question": "How does the SLA clock work?",
                    "answer": "The clock starts when a report is accepted and enters the right category. Status changes are stored with timestamps. Paused states such as waiting on a resident stop the clock, and the deadline is recalculated from the stored history rather than a single mutable field.",
                },
                {
                    "question": "What is public and what is private?",
                    "answer": "The public page shows category, status, rough area and resolution time. It does not show names, contact details, precise coordinates or photos that could identify someone. Staff can see the full report after signing in.",
                },
            ],
            "differentiators": [
                "A correction path for duplicate detection instead of pretending the classifier is always right.",
                "An SLA model based on an auditable status history, not a mutable due date.",
                "A public page designed around privacy, not just a second admin table.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-003",
        title="Open-Source Contribution Finder",
        summary=(
            "Build a search tool for developers who want a useful first "
            "contribution. It queries GitHub issues labelled for beginners, "
            "filters by language and topic, and ranks repositories by signals "
            "that actually predict a good first experience: recent activity, a "
            "contributing guide, issue response time and how often maintainers "
            "close outside pull requests.\n\n"
            "Use the GitHub search API with pagination and conditional requests. "
            "Cache repository and issue data, respect rate limits, and make "
            "stale results visible instead of pretending they are live. Let "
            "users save issues, mark progress and hide repositories they have "
            "already tried.\n\n"
            "The interesting part is the ranking explanation. Every score should "
            "show its inputs so a user can decide whether a repository is "
            "friendly or just popular. Add filters for language, label, recent "
            "activity and minimum stars, then test the ranking against a small "
            "set of repositories you have actually looked at."
        ),
        who_affected="New contributors looking for a first pull request, maintainers who label beginner issues, and bootcamp mentors.",
        why_matters="A welcoming issue list turns curiosity into a merged pull request; a bad pick wastes days and discourages new contributors.",
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=60,
        tech_tags=["typescript", "react", "github-api", "caching", "postgres", "search"],
        datasets=[{"name": "GitHub public issue and repository data", "url": "https://docs.github.com/en/rest"}],
        approaches=[
            "Search GitHub issues by label, language and recency, then fetch repository metadata in batches.",
            "Cache API responses with ETags and show when cached data was last refreshed.",
            "Rank repositories with explainable signals: activity, contributing guide, response time and issue turnover.",
            "Let users save issues and track their own contribution progress.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a GitHub issue finder that ranks beginner-friendly repositories with explainable signals and tracks saved contribution progress.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
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
                        "The ranking shows the exact signals behind each score, not just a number.",
                        "Conditional requests and caching reduce repeated API calls and display cache age.",
                        "Users can filter by recent activity, stars, labels and language.",
                        "A saved issue shows a simple progress state: saved, opened, first comment, pull request opened.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You combined an external API, caching, ranking and user state in one product."},
                {"role": "Frontend engineer", "how_it_helps": "The filters, result explanations and saved-item states show practical UI work with real data."},
                {"role": "Backend engineer", "how_it_helps": "You handled rate limits, pagination, cache invalidation and third-party API failure modes."},
                {"role": "Developer experience engineer", "how_it_helps": "The project is about making contribution paths clearer, which is core developer-experience work."},
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
                    "answer": "I use signals I can explain: recent commits and issue activity, presence of a contributing guide, how quickly maintainers respond on beginner issues, and whether issues get closed rather than left open forever. I show each signal so the user can ignore a score they disagree with.",
                },
                {
                    "question": "How do you handle GitHub rate limits?",
                    "answer": "I cache responses with ETags, batch repository lookups instead of one request per card, page only what the user needs, and back off when the remaining quota is low. The UI shows cached data and its age instead of failing silently.",
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
    ),
    dict(
        source_id="manabi-web-resume-004",
        title="Disaster Response Resource Coordination Hub",
        summary=(
            "Build a coordination board for disaster response where responders "
            "and community members post needs and offers: food, water, shelter, "
            "medical help and transport. Needs and offers appear on a live map, "
            "the system suggests nearby matches, and every match has a "
            "fulfilment trail.\n\n"
            "Design for poor connectivity. The web app should keep the last "
            "known board available, queue updates, and fall back to an SMS or "
            "WhatsApp notification when a device cannot stay online. Make "
            "duplicates visible rather than hiding them: two people may report "
            "the same shelter, and a coordinator needs to see both claims before "
            "marking it fulfilled.\n\n"
            "Add roles for coordinators and field workers, a simple verification "
            "state for offers, and an export for the daily response summary. "
            "Keep personal contact details out of the public map and reveal "
            "them only to signed-in coordinators who need to act."
        ),
        who_affected="Disaster response coordinators, relief volunteers, and affected communities posting urgent needs.",
        why_matters="During a response, duplicate requests and delayed matching leave resources idle while people wait.",
        field="web-dev",
        domain="disaster-management",
        difficulty="intermediate",
        est_hours=90,
        tech_tags=["typescript", "react", "websockets", "geospatial", "pwa", "sms"],
        datasets=[{"name": "Sample need and offer records", "url": None}],
        approaches=[
            "Model needs and offers with location, quantity, contact visibility and fulfilment state.",
            "Match nearby complementary records with distance and category rules.",
            "Keep a live board over WebSockets and queue offline edits in the browser.",
            "Send an SMS or WhatsApp fallback when a coordinator cannot stay online.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build an offline-friendly disaster resource hub with a live map, nearby need-offer matching, fulfilment tracking and an SMS fallback.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
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
                {"role": "Full-stack engineer", "how_it_helps": "You built the live board, matching rules, fulfilment model and fallback channel together."},
                {"role": "Frontend engineer", "how_it_helps": "The map, live updates and degraded-network states show real operational UI work."},
                {"role": "Backend engineer", "how_it_helps": "Matching, role checks, delivery tracking and notification fallbacks are practical backend problems."},
                {"role": "Civic tech engineer", "how_it_helps": "You can discuss privacy, verification and coordination under pressure, not just CRUD."},
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
                    "answer": "I do not hide duplicates. I show them as possible matches and let a coordinator merge or link them. The system can suggest duplicates by location, category and time, but a person confirms because two similar requests may be two real families.",
                },
                {
                    "question": "Why add an SMS fallback instead of only a PWA?",
                    "answer": "A PWA helps when the user can keep the page open, but disaster networks fail and batteries die. SMS or WhatsApp gives a low-bandwidth path to the same coordinator. The app generates a short message with the item ID and status update.",
                },
                {
                    "question": "How did you decide who can see contact details?",
                    "answer": "Public viewers see category, rough location and status only. Signed-in coordinators with an active role can reveal contact details for an open item, and that reveal is logged. This keeps the map useful without turning it into a public contact list.",
                },
            ],
            "differentiators": [
                "A fallback channel for when the live board cannot load.",
                "Duplicate-friendly matching that leaves the final decision with a coordinator.",
                "A fulfilment trail instead of a status field that anyone can overwrite.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-005",
        title="Export Readiness Assistant for Small Businesses",
        summary=(
            "Build a guided tool for small businesses that want to export a "
            "product to a new country. The user picks a product and a target "
            "market and gets a checklist of required documents, relevant "
            "regulations, duties and market notes. Every item links to an "
            "official source and shows the date it was checked.\n\n"
            "Start with three products and three countries. Store the checklist "
            "as structured data, not prose, so a rule can be updated without "
            "rewriting a page. Add a chat assistant that answers only from the "
            "stored sources and refuses when the sources do not cover the "
            "question. Show citations next to every answer.\n\n"
            "Regulations change, so version the source records and display a "
            "last-reviewed date. Add a plain-language summary, a printable "
            "checklist and a clear note that the tool is not legal advice. The "
            "value is traceability: a user can see exactly where each claim "
            "came from."
        ),
        who_affected="Small exporters, trade consultants, and small-business owners checking requirements before their first shipment.",
        why_matters="Missing one document or duty can stop a shipment, and scattered unofficial advice makes the first export expensive and risky.",
        field="web-dev",
        domain="industry",
        difficulty="intermediate",
        est_hours=75,
        tech_tags=["typescript", "react", "postgres", "rag", "citations", "search"],
        datasets=[{"name": "Official export guidance pages for three markets", "url": None}],
        approaches=[
            "Model products, markets, documents and regulations as separate records with source links.",
            "Version each source with a last-checked date and show it beside the claim.",
            "Restrict the chat assistant to retrieved source passages and require citations.",
            "Add a printable checklist and a clear not-legal-advice notice.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build an export readiness assistant that turns official sources into a cited checklist for a product and target country, with a source-grounded chat.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
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
                {"role": "Full-stack engineer", "how_it_helps": "You built structured domain data, a guided UI, source versioning and a retrieval-backed assistant."},
                {"role": "Frontend engineer", "how_it_helps": "The checklist, source citations and printable view show product-focused UI work."},
                {"role": "Backend engineer", "how_it_helps": "Versioned sources, coverage checks and grounded retrieval are practical backend concerns."},
                {"role": "AI application engineer", "how_it_helps": "You can explain retrieval boundaries, citations and refusal behavior, not just model calls."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a cited export-readiness assistant covering {P} products and {C} countries with source dates on every claim.",
                    "example": "Built a cited export-readiness assistant covering 3 products and 3 countries, with an official source and last-checked date on every checklist item.",
                },
                {
                    "bullet": "Restricted the chat assistant to stored sources and required citations, eliminating uncited regulatory answers.",
                    "example": "Restricted the chat assistant to retrieved official passages and required citations; unsupported questions returned a clear refusal instead of a guess.",
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
                    "answer": "A regulation update should change one rule, not a paragraph that mentions five things. Structured items let me show coverage, version changes and a printable checklist from the same source of truth.",
                },
                {
                    "question": "How do you handle outdated sources?",
                    "answer": "Every source has a last-checked date and a version. The UI shows the date, and items older than a threshold are marked for review. A reviewer updates the source and the affected checklist items keep their old version in history.",
                },
            ],
            "differentiators": [
                "Source dates and citations on every claim, including the printable view.",
                "A refusal path for questions the stored sources cannot answer.",
                "Structured rules with version history instead of a static advice page.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-006",
        title="Public Transit Journey Planner (GTFS)",
        summary=(
            "Build a journey planner that reads public transit schedules from "
            "GTFS feeds and returns multi-leg trips. Compare at least two "
            "objectives: fastest arrival and fewest transfers. Show the result "
            "on a map, with each leg, walking transfer and waiting time clearly "
            "separated.\n\n"
            "Start with a correct graph and timetable model. Load stops, routes, "
            "trips and stop times, then implement a real algorithm such as "
            "RAPTOR or Connection Scan instead of a shortest-path shortcut that "
            "ignores departure times. Handle service calendars, time zones and "
            "feeds that cover more than one day.\n\n"
            "Expose the planner through an API and keep the web UI thin. Add a "
            "small benchmark set of origin-destination pairs so changes to the "
            "algorithm can be compared by travel time and transfer count. The "
            "resume signal is that you can explain why the algorithm is correct "
            "on a timetable, not just that it returns a route."
        ),
        who_affected="Commuters, transit agencies, and city planners comparing route quality across a network.",
        why_matters="A planner that ignores transfer time or service calendars sends people on trips that do not exist.",
        field="web-dev",
        domain="transport",
        difficulty="advanced",
        est_hours=150,
        tech_tags=["typescript", "gtfs", "raptor", "postgis", "rest-api", "map-ui"],
        datasets=[{"name": "Public GTFS transit feeds", "url": "https://gtfs.org/"}],
        approaches=[
            "Import GTFS stops, routes, trips, stop times and calendars into a queryable model.",
            "Implement RAPTOR or Connection Scan over timetable events instead of static edge weights.",
            "Compare fastest arrival and fewest transfers as separate objectives.",
            "Render legs and transfers on a map and expose the same planner through an API.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a GTFS journey planner with a timetable-aware algorithm, fastest and fewest-transfer options, a map UI and an API.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "One GTFS feed produces a correct multi-leg trip with walking transfers and a map preview.",
                    "checks": [
                        "GTFS stops, trips and stop times import without losing service-calendar data.",
                        "A query returns a valid itinerary with departure, arrival and transfer times.",
                        "The map shows each transit leg and walking transfer separately.",
                        "A missing or invalid feed produces a clear error instead of a broken route.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The planner compares fastest and fewest-transfer trips and beats a naive graph search on a benchmark set.",
                    "checks": [
                        "RAPTOR or Connection Scan respects departure times and service calendars.",
                        "The API returns both fastest and fewest-transfer options for the same query.",
                        "A benchmark compares travel time and transfer counts against a baseline.",
                        "Time zones, overnight trips and feed validity are handled explicitly.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Backend engineer", "how_it_helps": "Timetable modelling, graph algorithms and API design are the core of this project."},
                {"role": "Full-stack engineer", "how_it_helps": "You connected a real algorithm to a map UI and an API without hiding the data model."},
                {"role": "Data engineer", "how_it_helps": "GTFS ingestion, calendar handling and feed validation are practical data-pipeline work."},
                {"role": "Geospatial engineer", "how_it_helps": "Stops, transfers and map rendering require real geospatial reasoning."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a GTFS journey planner using {ALGO} over timetables, returning fastest and fewest-transfer routes.",
                    "example": "Built a GTFS journey planner using RAPTOR over timetable events, returning fastest and fewest-transfer routes for the same origin-destination query.",
                },
                {
                    "bullet": "Cut average query time to {MS} ms on a benchmark of {N} trips while preserving transfer correctness.",
                    "example": "Cut average query time to 180 ms on a 2,000-trip benchmark by scanning timetable events instead of running a time-expanded graph search.",
                },
                {
                    "bullet": "Handled service calendars, time zones and overnight trips that a naive shortest-path planner breaks on.",
                    "example": "Handled service calendars, time zones and overnight trips, so weekend and after-midnight queries returned valid itineraries instead of phantom routes.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why not use Dijkstra on a static graph?",
                    "answer": "A transit network is time-dependent: an edge is only usable at a specific departure. Dijkstra on a static graph can return a path that cannot be travelled. RAPTOR or Connection Scan works over timetable events and respects waiting and transfer time.",
                },
                {
                    "question": "How do you compare fastest and fewest transfers?",
                    "answer": "They are different objectives, so I keep separate labels during the search rather than collapsing them into one score. The API returns both, and the UI lets the user choose. A single weighted score hides the trade-off.",
                },
                {
                    "question": "What was the hardest part of the GTFS import?",
                    "answer": "Service calendars and time zones. A trip can cross midnight, and the same route can run on different days. I normalize calendar dates before building events and test overnight and weekend cases explicitly.",
                },
            ],
            "differentiators": [
                "A real timetable-aware algorithm instead of a static shortest-path demo.",
                "Two explicit objectives, fastest and fewest transfers, returned side by side.",
                "A benchmark that shows correctness and performance, not just a screenshot.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-007",
        title="Universal QR Payment Router",
        summary=(
            "Build a web app that scans or pastes a payment QR code, identifies "
            "its format, and routes the user to the right payment flow. Support "
            "UPI links, Bharat QR and EMV-style merchant payloads at the parser "
            "level, plus ordinary payment links. Generate merchant QR codes and "
            "keep a local transaction history.\n\n"
            "This is a parsing and safety project, not a payment processor. Build "
            "a format detector, a validated parser per format and a routing layer "
            "that opens the right app or a sandbox checkout. Never store real card "
            "data, and label every sandbox or test-mode result clearly.\n\n"
            "Add tests with valid, malformed and ambiguous payloads. Show the "
            "parsed fields before routing so a user can confirm the merchant, "
            "amount and currency. The resume value comes from the parser design "
            "and the safety boundaries, not from pretending to move real money."
        ),
        who_affected="Shoppers facing mismatched payment apps, small merchants generating QR codes, and fintech developers building payment flows.",
        why_matters="Payment QR formats are fragmented; a clear parser and safe routing layer prevent failed payments and accidental data leakage.",
        field="web-dev",
        domain="fintech",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["typescript", "qr-parsing", "fintech-apis", "sandbox", "security", "rest-api"],
        datasets=[{"name": "Synthetic payment QR payloads", "url": None}],
        approaches=[
            "Detect the payload format before parsing, and reject ambiguous or malformed input.",
            "Build a validated parser per format with tests for edge cases.",
            "Route to a payment app or sandbox checkout without handling real card data.",
            "Generate merchant QR codes and keep a clearly labelled test history.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a payment QR parser and router that identifies formats, validates payloads, routes to sandbox flows and never stores real card data.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A scanned UPI or payment link is parsed, shown for confirmation and routed to the correct app or sandbox page.",
                    "checks": [
                        "The app reads a QR image and extracts the payload text.",
                        "A parser identifies at least two formats and shows merchant, amount and currency.",
                        "Malformed payloads are rejected with a clear reason.",
                        "Routing opens a sandbox or app link without storing card data.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Multiple formats share a tested parser pipeline, and merchant QR generation plus history work end to end.",
                    "checks": [
                        "Format detection and parsing are separate, tested stages with valid and invalid fixtures.",
                        "The app generates merchant QR codes and round-trips them through its own parser.",
                        "Transaction history is clearly marked as test data and stores no sensitive payloads.",
                        "Ambiguous payloads ask for confirmation instead of guessing silently.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You built parsing, routing, QR generation and history in one small product."},
                {"role": "Frontend engineer", "how_it_helps": "The camera flow, confirmation screen and error states are practical browser UI work."},
                {"role": "Fintech engineer", "how_it_helps": "You can discuss format validation, sandbox boundaries and sensitive-data handling."},
                {"role": "Backend engineer", "how_it_helps": "The parser and routing layer need clear contracts, validation and safe error handling."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a payment QR parser that identifies {N} formats and validates payloads before routing.",
                    "example": "Built a payment QR parser that identifies UPI, Bharat QR and payment-link payloads, validating merchant, amount and currency before routing.",
                },
                {
                    "bullet": "Added {N} parser fixtures covering valid, malformed and ambiguous payloads, with zero unhandled inputs.",
                    "example": "Added 40 parser fixtures covering valid, malformed and ambiguous payloads; every rejected case returned a specific reason.",
                },
                {
                    "bullet": "Kept the app inside sandbox boundaries with no real card storage and explicit test-mode labels.",
                    "example": "Kept all routing inside sandbox or app-handoff flows, stored no card data and labelled every test transaction in the UI.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you avoid misrouting a payment?",
                    "answer": "I detect the format first, validate the fields, and show the parsed merchant, amount and currency before routing. Ambiguous payloads ask the user to confirm. I do not guess when a field is missing or inconsistent.",
                },
                {
                    "question": "Why not process real payments?",
                    "answer": "Payment processing needs licensed partners, compliance and real settlement. This project is a parser and router with sandbox or app handoff. Keeping that boundary clear is part of the design, not a missing feature.",
                },
                {
                    "question": "What do you store in transaction history?",
                    "answer": "Only test-mode metadata: format, masked merchant reference, amount, status and timestamp. I do not store full QR payloads, card data or anything that would be sensitive in a real payment.",
                },
            ],
            "differentiators": [
                "A tested parser pipeline with explicit rejection reasons.",
                "Sandbox boundaries and test-mode labels that match the project scope.",
                "Merchant QR generation that round-trips through the same parser.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-008",
        title="Click-and-Collect Shopping Platform with Live In-Store Inventory",
        summary=(
            "Build an online catalogue where shoppers can see stock per store, "
            "reserve an item and pick it up in person. Store staff update stock "
            "by scanning barcodes, and QR codes in the shop open the matching "
            "product page.\n\n"
            "The central problem is inventory consistency. A reservation must "
            "hold stock for a short window, a completed pickup must reduce it, "
            "and an expired reservation must release it. Keep these operations "
            "in one transactional path and test race conditions when two users "
            "reserve the last unit.\n\n"
            "Build separate views for shoppers and staff. Shoppers need clear "
            "availability and pickup instructions; staff need a fast barcode "
            "scan flow that works on a phone. Add an audit trail for stock "
            "changes so a mismatch can be traced to a reservation, pickup or "
            "manual adjustment."
        ),
        who_affected="Local retailers, shoppers who want reliable pickup, and store staff managing stock across shelves and online orders.",
        why_matters="Stale stock data causes cancelled pickups and wasted trips; a single reservation path keeps online promises and shelf reality aligned.",
        field="web-dev",
        domain="industry",
        difficulty="intermediate",
        est_hours=90,
        tech_tags=["typescript", "react", "postgres", "barcode", "transactions", "ecommerce"],
        datasets=[{"name": "Sample product catalogue and store stock", "url": None}],
        approaches=[
            "Model stock per store and keep reservations, pickups and adjustments in one transaction log.",
            "Expire unpaid reservations automatically and return held stock.",
            "Give staff a phone-friendly barcode scan flow for stock updates.",
            "Use in-store QR codes that deep-link to the product page and store availability.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a click-and-collect storefront with per-store live stock, reservation holds, staff barcode updates and in-store QR product links.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Shoppers see per-store stock, reserve an item and get a pickup code; staff can adjust stock.",
                    "checks": [
                        "Product pages show stock for a selected store.",
                        "A reservation holds one unit for a short window and shows a pickup code.",
                        "Staff can change stock and the shopper view reflects it.",
                        "An expired reservation releases the held unit automatically.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Concurrent reservations cannot oversell the last unit, and every stock change is traceable.",
                    "checks": [
                        "Reservation, pickup and adjustment operations use a consistent transactional path.",
                        "A concurrency test proves two shoppers cannot both reserve the last unit.",
                        "The stock audit trail identifies whether a change came from a reservation, pickup or manual adjustment.",
                        "A staff barcode-scan flow updates stock from a phone and handles unknown barcodes cleanly.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You built catalogue, inventory, reservations, staff tools and audit history end to end."},
                {"role": "Backend engineer", "how_it_helps": "Transactional stock handling and race-condition tests are the strongest part of the project."},
                {"role": "Frontend engineer", "how_it_helps": "The shopper and staff flows show mobile-friendly, task-focused UI work."},
                {"role": "E-commerce engineer", "how_it_helps": "Reservation holds, pickup state and stock consistency are core commerce problems."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a click-and-collect flow that held stock per store and prevented overselling across {N} concurrent reservations.",
                    "example": "Built a click-and-collect flow that held stock per store and prevented overselling in a 50-user concurrency test for the last unit.",
                },
                {
                    "bullet": "Cut stock mismatches by adding a single reservation, pickup and adjustment ledger with an audit trail.",
                    "example": "Cut stock mismatches by recording every reservation, pickup and manual adjustment in one ledger, making each change traceable to its source.",
                },
                {
                    "bullet": "Added a phone barcode-scan flow that let staff update shelf stock without a desktop terminal.",
                    "example": "Added a phone-friendly barcode flow that let staff update shelf stock during a shift without returning to a desktop terminal.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you prevent two shoppers from reserving the last unit?",
                    "answer": "I perform the availability check and the reservation write in one transaction with a row lock or a conditional update on available stock. The second request sees the held stock and fails cleanly instead of creating an oversold reservation.",
                },
                {
                    "question": "Why hold stock instead of only checking it at pickup?",
                    "answer": "A pickup promise without a hold lets the shop sell the item before the shopper arrives. A short hold protects the shopper while an expiry releases abandoned reservations so stock does not stay frozen.",
                },
                {
                    "question": "How do you debug an inventory mismatch?",
                    "answer": "Every change is an immutable ledger entry with a reason and reference: reservation, pickup, expiry or manual adjustment. I can sum the entries for a product and store and compare that to the shelf count.",
                },
            ],
            "differentiators": [
                "A concurrency test for the last-unit reservation, not just a happy-path checkout.",
                "One inventory ledger for reservations, pickups and manual edits.",
                "A staff barcode flow designed for a phone on the shop floor.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-009",
        title="Paperless Scholarship Disbursement System",
        summary=(
            "Build a platform for scholarship applications: students submit "
            "documents, reviewers verify them, approvers move applications "
            "through a workflow, and finance records disbursements. Every action "
            "lands in an audit trail, and students can see their own status "
            "without emailing the office.\n\n"
            "The core is role-based workflow, not file upload. Define reviewer "
            "and approver permissions, document-verification states, rejection "
            "reasons and a clear resubmission path. Use mock payments and label "
            "them as such. Tie each disbursement to an approved application and "
            "a signed-off amount so the report cannot drift from the workflow.\n\n"
            "Add an admin dashboard with exportable disbursement reports, plus "
            "tests for permission boundaries. The resume signal is that you can "
            "model a real approval process with an audit trail and keep sensitive "
            "student documents out of the wrong hands."
        ),
        who_affected="Students applying for scholarships, scholarship reviewers, finance staff and program administrators.",
        why_matters="Paper applications get lost and status questions consume staff time; a permissioned workflow makes decisions and payments traceable.",
        field="web-dev",
        domain="education",
        difficulty="intermediate",
        est_hours=95,
        tech_tags=["typescript", "react", "postgres", "rbac", "workflow", "audit-log"],
        datasets=[{"name": "Synthetic scholarship applications", "url": None}],
        approaches=[
            "Model applications, documents, verification states and approval steps as explicit records.",
            "Enforce reviewer and approver permissions on every workflow transition.",
            "Record an audit entry for each view of sensitive documents, decision and payment.",
            "Use mock disbursements tied to approved applications and exportable reports.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a role-based scholarship platform for applications, document verification, approval workflows, mock disbursements and audited reports.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Students apply with documents, reviewers verify them, and approved applications proceed to a mock disbursement.",
                    "checks": [
                        "A student can submit an application and upload required documents.",
                        "A reviewer can approve or reject a document with a reason.",
                        "An approved application can be marked for mock disbursement.",
                        "Each student sees only their own application status.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The full role-based workflow enforces boundaries, records every action and exports a reconciliation report.",
                    "checks": [
                        "Reviewer and approver permissions are enforced on API routes and UI actions.",
                        "Every decision, document view and disbursement writes an audit entry.",
                        "A rejected student can resubmit only the affected document without restarting the application.",
                        "The finance export reconciles approved amounts against mock disbursement records.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You built the application flow, role model, workflow and reporting layer together."},
                {"role": "Backend engineer", "how_it_helps": "Permissions, state transitions, audit logs and reconciliation are real backend concerns."},
                {"role": "Frontend engineer", "how_it_helps": "The student status page and reviewer queue show careful multi-role UI work."},
                {"role": "Product engineer", "how_it_helps": "You can explain a workflow with rejection, resubmission and finance handoff, not just a single form."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a role-based scholarship workflow covering {N} applications, document verification and mock disbursements.",
                    "example": "Built a role-based scholarship workflow covering 500 sample applications, document verification, approvals and mock disbursements.",
                },
                {
                    "bullet": "Enforced reviewer and approver permissions with an audit trail for every sensitive document view and decision.",
                    "example": "Enforced reviewer and approver permissions on all API routes, with an audit trail for every document view, decision and disbursement.",
                },
                {
                    "bullet": "Cut resubmission work by letting students replace only the rejected document instead of the whole application.",
                    "example": "Cut resubmission work by letting students replace only the rejected document; the rest of the application stayed intact and reviewable.",
                },
            ],
            "interview_points": [
                {
                    "question": "How do you stop a reviewer from approving their own application?",
                    "answer": "Permissions are checked on the server for each transition, and the actor is stored with the decision. A reviewer cannot act on an application tied to their own account. The UI hides the action, but the API enforces it.",
                },
                {
                    "question": "Why keep an audit trail for document views?",
                    "answer": "Scholarship documents are sensitive. Knowing who opened a document and when makes misuse detectable and supports a real review process. The audit entry is separate from the workflow state, so it cannot be edited by a normal update.",
                },
                {
                    "question": "How do you keep disbursement reports consistent?",
                    "answer": "A disbursement references an approved application and a fixed amount. Finance records are append-only in the mock flow, and the export reconciles approved applications against recorded disbursements instead of recalculating from mutable fields.",
                },
            ],
            "differentiators": [
                "Server-enforced role boundaries, with a test for self-approval.",
                "A resubmission path that preserves the rest of the application.",
                "An append-only audit trail around sensitive documents and payments.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-010",
        title="Storefront Builder for Local Shops",
        summary=(
            "Build a multi-tenant storefront builder for small local shops. A "
            "shop owner signs up, adds products, picks a simple theme and shares "
            "a branded link. Shoppers browse the catalogue and start an order "
            "through a WhatsApp enquiry or a QR code placed in the shop.\n\n"
            "Multi-tenancy is the core engineering problem. Every shop has its "
            "own slug, products and settings, but one codebase and one database "
            "serve all of them. Enforce tenant boundaries in every query and "
            "test that one owner cannot read or edit another shop's data.\n\n"
            "Add image uploads with size limits, draft and published states, and "
            "an optional test-mode subscription plan. Do not take real payments "
            "without proper setup. The resume signal is a clean tenant model, "
            "safe ownership checks and a shareable storefront that a real shop "
            "could use."
        ),
        who_affected="Small shop owners without a website, local customers, and freelancers building low-cost commerce tools.",
        why_matters="A local shop needs a credible online catalogue and a simple order path, not a full marketplace with a heavy setup.",
        field="web-dev",
        domain="industry",
        difficulty="intermediate",
        est_hours=85,
        tech_tags=["typescript", "react", "postgres", "multi-tenant", "whatsapp", "qr"],
        datasets=[{"name": "Synthetic shop catalogue data", "url": None}],
        approaches=[
            "Give each shop a slug, settings and isolated product records behind an ownership check.",
            "Support draft and published storefronts with image uploads and size limits.",
            "Generate WhatsApp order links and QR codes that point at the shop or product.",
            "Add an optional test-mode subscription plan without real payment processing.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a multi-tenant storefront builder for local shops with branded links, product pages, WhatsApp enquiries, QR codes and tenant-safe ownership checks.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "One owner can create a shop, add products and share a published storefront link.",
                    "checks": [
                        "A shop owner signs up, creates a shop and adds products with images.",
                        "A published storefront is reachable at a clean shop slug.",
                        "A shopper can start a WhatsApp enquiry from a product.",
                        "Draft shops are not publicly reachable.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Many shops share the same app with enforced tenant boundaries, QR links and a test-mode plan.",
                    "checks": [
                        "Every query and mutation checks tenant ownership on the server.",
                        "A test proves one owner cannot read or edit another shop's products.",
                        "Shop and product QR codes resolve to the right public page.",
                        "A test-mode subscription state can be changed without touching real payment data.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Full-stack engineer", "how_it_helps": "You built tenant-aware data, owner flows and a public storefront in one product."},
                {"role": "Backend engineer", "how_it_helps": "Ownership checks, isolation and slug routing are practical multi-tenant backend work."},
                {"role": "Frontend engineer", "how_it_helps": "The editor, preview and public storefront show both internal and customer-facing UI."},
                {"role": "Product engineer", "how_it_helps": "You turned a vague local-business need into a narrow, usable product with a clear order handoff."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a multi-tenant storefront builder serving {N} shops from one codebase with server-enforced ownership checks.",
                    "example": "Built a multi-tenant storefront builder serving 25 sample shops from one codebase, with server-enforced ownership checks on every product query.",
                },
                {
                    "bullet": "Added branded links, WhatsApp enquiries and QR codes that turned a shop catalogue into a shareable order path.",
                    "example": "Added branded shop links, WhatsApp enquiry links and printable QR codes, giving each shop a shareable catalogue without a full checkout.",
                },
                {
                    "bullet": "Tested tenant isolation so no owner could read or edit another shop's catalogue.",
                    "example": "Added tests proving a shop owner could not read or edit another tenant's products, including direct ID-based requests.",
                },
            ],
            "interview_points": [
                {
                    "question": "What does multi-tenant mean in this project?",
                    "answer": "Many shops share one application and database, but each shop's data is isolated by a tenant ID. Every query includes the tenant, and every mutation checks ownership on the server. A shop slug identifies the public storefront, not a trusted permission.",
                },
                {
                    "question": "Why use WhatsApp instead of a cart and checkout?",
                    "answer": "Small shops often close orders in WhatsApp already. A lightweight enquiry link avoids payment and delivery complexity while still giving the shop an online catalogue. A full checkout would be a later step, not the first version.",
                },
                {
                    "question": "How do you test tenant isolation?",
                    "answer": "I sign in as one owner and request another shop's product by ID through the API, not just by clicking the UI. The request must fail. I repeat that for edits, image uploads and settings.",
                },
            ],
            "differentiators": [
                "A real tenant model with isolation tests, not just a shop ID in the URL.",
                "A shareable WhatsApp and QR order path that fits how small shops already work.",
                "A narrow first version with billing explicitly optional and test-mode only.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-011",
        title="Typed NPM Utility Library",
        summary=(
            "Design, build and publish a small TypeScript utility package that "
            "solves one real problem, such as date handling, validation or "
            "accessible UI helpers. Keep the API narrow, document every exported "
            "function and test the behavior users depend on.\n\n"
            "The package work is as important as the utility. Ship ESM and "
            "CommonJS builds, generate type declarations, run tests in CI, and "
            "automate versioning and release notes. Use a real changelog and "
            "semantic versioning so consumers can trust upgrades.\n\n"
            "Pick a problem you have actually hit, not another wrapper around an "
            "existing library. Add benchmarks or bundle-size checks if the "
            "package claims to be small. Publish a demo page or README examples "
            "that a new user can copy. The resume signal is that you can ship a "
            "maintained package, not just write a helper file."
        ),
        who_affected="Frontend and Node developers who need a small, typed utility, and maintainers who depend on predictable releases.",
        why_matters="Small utilities spread through teams; tests, types and release automation decide whether they save time or become a maintenance burden.",
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=55,
        tech_tags=["typescript", "npm", "vitest", "esm", "ci-cd", "documentation"],
        datasets=[{"name": "Public package usage examples", "url": None}],
        approaches=[
            "Choose one narrow problem and define a small typed API with clear error behavior.",
            "Build ESM and CommonJS outputs with generated declarations and source maps.",
            "Test edge cases in CI and check bundle size or benchmarks.",
            "Automate semantic releases, changelog entries and package publishing.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Publish a narrow TypeScript utility package with tests, ESM and CommonJS builds, generated docs, CI and automated versioned releases.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A typed utility with tests, a README and a working package build that another project can install.",
                    "checks": [
                        "The package exposes a small API with generated type declarations.",
                        "Unit tests cover normal, boundary and invalid inputs.",
                        "A local consumer can install the built package and use it.",
                        "The README shows install, usage and one limitation.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The package ships both module formats, releases automatically and has a documented compatibility policy.",
                    "checks": [
                        "ESM and CommonJS builds both work in a smoke-test consumer.",
                        "CI runs tests, type checks and a build on every pull request.",
                        "Semantic release automation creates version tags and changelog entries.",
                        "The README documents browser and Node support, bundle size or benchmark results.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You can show typed API design, package consumption and browser compatibility work."},
                {"role": "Library / platform engineer", "how_it_helps": "Build formats, types, releases and compatibility policy are the core of library maintenance."},
                {"role": "Full-stack engineer", "how_it_helps": "A published package proves you can ship code other developers install and upgrade."},
                {"role": "Developer experience engineer", "how_it_helps": "Docs, examples and release automation are direct developer-experience work."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Published a typed utility package with {N} tests, ESM and CommonJS builds and automated releases.",
                    "example": "Published a typed date-range utility with 45 tests, ESM and CommonJS builds, generated declarations and automated semantic releases.",
                },
                {
                    "bullet": "Cut consumer setup to one install by shipping both module formats and clear type declarations.",
                    "example": "Shipped both module formats and generated declarations, so browser and Node consumers could install and import the package without a bundler workaround.",
                },
                {
                    "bullet": "Added CI checks for tests, types and build output, catching release-breaking changes before publish.",
                    "example": "Added CI checks for tests, type declarations and both builds, catching a broken CommonJS export before the next release.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why publish both ESM and CommonJS?",
                    "answer": "Different consumers use different module systems. A dual build avoids forcing a bundler workaround. I test both in a small consumer project because a build that compiles is not the same as a package that imports correctly.",
                },
                {
                    "question": "How do you decide the API surface?",
                    "answer": "I start from one real use case and expose the smallest set of functions that solves it. I avoid options until a second real case needs them. A narrow API is easier to test, document and keep stable.",
                },
                {
                    "question": "How do you handle breaking changes?",
                    "answer": "Semantic versioning, a changelog and a clear compatibility note. Breaking changes get a major version and a migration example. Automation creates the release, but I review the changelog before publishing.",
                },
            ],
            "differentiators": [
                "A real installable package with both module formats, not a local helper file.",
                "Automated releases and a compatibility policy, not just a version number.",
                "Tests and docs for edge cases consumers actually hit.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-012",
        title="Distributed Task Queue",
        summary=(
            "Build a background job system with a persistent queue, a worker "
            "pool and a dashboard. Jobs should retry with backoff, support "
            "scheduled runs, move to a dead-letter queue after repeated failure "
            "and expose enough state to debug a stuck worker.\n\n"
            "The important guarantees are at-least-once delivery and idempotent "
            "job handlers. A worker can crash after taking a job and before "
            "recording success, so the queue must be able to redeliver without "
            "duplicating side effects. Add visibility timeouts, heartbeats and a "
            "clear rule for when a job is considered abandoned.\n\n"
            "Load-test the system while workers fail on purpose. Show queue "
            "depth, retry counts and worker health in a monitoring view. The "
            "resume signal is that you can reason about failure and recovery, "
            "not just run a job in a loop."
        ),
        who_affected="Backend teams running email, report, media or sync jobs, and on-call engineers who debug stuck work.",
        why_matters="Background jobs fail in partial ways; retries, timeouts and dead-letter handling decide whether a failure is recoverable or silent.",
        field="web-dev",
        domain="distributed-systems",
        difficulty="advanced",
        est_hours=150,
        tech_tags=["typescript", "nodejs", "postgres", "workers", "retries", "observability"],
        datasets=[{"name": "Synthetic job payloads", "url": None}],
        approaches=[
            "Persist jobs with state, attempts, visibility timeout and scheduled run time.",
            "Run a worker pool with heartbeats and reclaim abandoned jobs.",
            "Retry with exponential backoff and move exhausted jobs to a dead-letter queue.",
            "Expose queue depth, retry counts and worker health in a dashboard.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a distributed task queue with persistent jobs, worker heartbeats, retries with backoff, a dead-letter queue and a monitoring dashboard.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Workers pull persisted jobs, retry failures and show queue depth in a dashboard.",
                    "checks": [
                        "Jobs are stored before a worker picks them up.",
                        "A failed job retries with backoff and eventually stops.",
                        "Exhausted jobs move to a dead-letter state instead of disappearing.",
                        "The dashboard shows queued, running, failed and completed counts.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Abandoned jobs are reclaimed, side effects stay idempotent, and a failure test shows the system recovering.",
                    "checks": [
                        "Visibility timeouts and worker heartbeats reclaim jobs from crashed workers.",
                        "Job handlers use idempotency keys so redelivery does not duplicate side effects.",
                        "Scheduled jobs run once at the intended time under multiple workers.",
                        "A load test kills workers mid-job and the queue returns to a healthy state without losing work.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Backend engineer", "how_it_helps": "Queue state, retries, timeouts and worker coordination are core backend work."},
                {"role": "Distributed systems engineer", "how_it_helps": "You can discuss delivery guarantees, failure recovery and idempotency from a real test."},
                {"role": "DevOps / SRE", "how_it_helps": "The dashboard, health signals and failure tests map directly to operating a job system."},
                {"role": "Full-stack engineer", "how_it_helps": "You built both the worker infrastructure and the operator-facing monitoring UI."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a distributed task queue that processed {N} jobs with retries, visibility timeouts and a dead-letter path.",
                    "example": "Built a distributed task queue that processed 100,000 sample jobs with exponential retries, visibility timeouts and a dead-letter queue.",
                },
                {
                    "bullet": "Kept job side effects idempotent under at-least-once delivery and worker crashes.",
                    "example": "Kept email-style job side effects idempotent under at-least-once delivery, so a worker crash and redelivery did not send duplicates.",
                },
                {
                    "bullet": "Load-tested worker failure and recovered abandoned jobs without losing queued work.",
                    "example": "Load-tested with workers killed mid-job; heartbeat-based reclamation returned abandoned jobs to the queue without losing work.",
                },
            ],
            "interview_points": [
                {
                    "question": "What delivery guarantee does your queue provide?",
                    "answer": "At-least-once. A worker can crash after doing the work but before acknowledging it, so redelivery is possible. That is why handlers use idempotency keys. Exactly-once delivery is much harder and usually the wrong promise.",
                },
                {
                    "question": "How do you know a worker is stuck rather than slow?",
                    "answer": "Workers send heartbeats while processing. A visibility timeout extends while heartbeats arrive. If the timeout expires, the job is considered abandoned and can be reclaimed. The dashboard shows both heartbeat age and attempts.",
                },
                {
                    "question": "Why keep a dead-letter queue?",
                    "answer": "A job that fails repeatedly should stop consuming worker time and become visible to an operator. The dead-letter queue keeps the payload, attempts and last error so the failure can be inspected and replayed after a fix.",
                },
            ],
            "differentiators": [
                "Heartbeat-based recovery for crashed workers, tested under load.",
                "Idempotent side effects under at-least-once delivery.",
                "An operator dashboard with queue depth, retries and worker health.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-013",
        title="Satellite Pass Predictor & Live Sky Tracker",
        summary=(
            "Build a browser tool that tells a user when the ISS and other "
            "bright satellites will pass overhead. Show whether the pass is "
            "actually visible by checking the observer's darkness and the "
            "satellite's illumination, then draw the path on a 3D globe and a "
            "sky chart.\n\n"
            "Use public orbital elements and a real SGP4 implementation in the "
            "browser. Cache the element sets, respect the provider's usage "
            "guidance, and show the age of the data. Compute the observer's "
            "position from coordinates, compare sun altitude for darkness, and "
            "check whether the satellite is in sunlight rather than only above "
            "the horizon.\n\n"
            "Add pass times, maximum elevation, direction and a simple alert "
            "before a good pass. Keep the orbital math separate from the "
            "rendering so the predictions can be tested against known passes."
        ),
        who_affected="Astronomy hobbyists, educators and anyone planning to watch the ISS or a bright satellite pass.",
        why_matters="Most trackers list every overhead pass, including ones the observer cannot see; visibility logic makes the result actually useful.",
        field="web-dev",
        domain="other",
        difficulty="intermediate",
        est_hours=90,
        tech_tags=["typescript", "satellite-js", "threejs", "sgp4", "astronomy", "caching"],
        datasets=[{"name": "Public satellite orbital element sets", "url": "https://celestrak.org/"}],
        approaches=[
            "Load and cache public TLE data, and show how old the elements are.",
            "Propagate orbits in the browser with SGP4 and compute observer-relative passes.",
            "Check observer darkness and satellite illumination before calling a pass visible.",
            "Render the ground track on a 3D globe and the pass on a sky chart.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a browser satellite pass predictor with SGP4, visibility checks, a 3D globe and a sky chart.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "For a location and satellite, show upcoming passes with time, elevation and a sky path.",
                    "checks": [
                        "The app loads a TLE set and computes passes for the next 24 hours.",
                        "Each pass shows start time, maximum elevation and duration.",
                        "A sky chart draws the pass path for the selected observer.",
                        "Invalid coordinates or stale TLE data produce a clear warning.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Visibility is computed from observer darkness and satellite illumination, and predictions are tested against known passes.",
                    "checks": [
                        "Sun altitude determines whether the observer is dark enough to see the pass.",
                        "The satellite is checked for sunlight, not just line of sight.",
                        "A 3D globe shows the ground track and the observer's location.",
                        "A small test set compares predicted pass times with published results within a tolerance.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You combined real orbital math with a globe and sky-chart interface in the browser."},
                {"role": "Full-stack engineer", "how_it_helps": "TLE caching, API handling and client-side prediction form a complete data-to-UI pipeline."},
                {"role": "Geospatial / visualization engineer", "how_it_helps": "Coordinate transforms, ground tracks and sky projections are practical visualization work."},
                {"role": "Science software engineer", "how_it_helps": "You can explain the model, its inputs and its validation against known passes."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a browser satellite tracker using SGP4 that predicted {N} passes with visibility checks for observer darkness.",
                    "example": "Built a browser satellite tracker using SGP4 that predicted 40 ISS passes and filtered out passes the observer could not see because of daylight or Earth shadow.",
                },
                {
                    "bullet": "Cut unnecessary API calls by caching TLE sets and showing element age in the UI.",
                    "example": "Cut TLE API calls by caching element sets locally and showing their age, so users saw when predictions were based on older orbital data.",
                },
                {
                    "bullet": "Rendered ground tracks on a 3D globe and pass paths on a sky chart from the same prediction model.",
                    "example": "Rendered ground tracks on a 3D globe and pass paths on a sky chart from one prediction model, keeping the two views consistent.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why is a pass above the horizon not always visible?",
                    "answer": "The observer needs darkness and the satellite needs sunlight for a bright pass. A satellite can be overhead in daylight, or in Earth's shadow, so the user would see nothing. I check sun altitude at the observer and illumination at the satellite.",
                },
                {
                    "question": "Why run SGP4 in the browser?",
                    "answer": "It keeps the interaction local and avoids a server round trip for every location change. The model is small enough to run client-side, and the TLE data is cached. The cost is showing element age clearly rather than pretending the orbit is current.",
                },
                {
                    "question": "How did you validate the predictions?",
                    "answer": "I compared a small set of passes against published predictions and checked that differences stayed inside a reasonable tolerance. I also tested coordinate edge cases and stale TLE handling. The model is not perfect, so the UI shows the data age.",
                },
            ],
            "differentiators": [
                "Real visibility logic, not just a list of overhead passes.",
                "A 3D globe and a sky chart driven by the same prediction code.",
                "Element-age awareness built into the UI.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-014",
        title="Mission Trajectory Playground",
        summary=(
            "Build a physics sandbox for planning spacecraft transfers between "
            "orbits. A user chooses a start and target orbit, compares Hohmann "
            "and bi-elliptic transfers, and sees the delta-v required for each "
            "burn. Then watch the trajectory run through a numerical integrator "
            "instead of a canned animation.\n\n"
            "Keep the orbital mechanics and the simulation separate. Compute "
            "transfer burns analytically, then propagate the resulting state "
            "with RK4 under point-mass gravity. Run the heavy integration in a "
            "Web Worker so the interface stays responsive, and show step size, "
            "energy error and elapsed simulated time.\n\n"
            "Validate against real positions from JPL Horizons for a simple "
            "case, and let the user try one gravity assist. The resume signal is "
            "that you can connect numerical methods, performance and validation "
            "in a browser app."
        ),
        who_affected="Students, space enthusiasts and educators exploring orbital mechanics and mission design.",
        why_matters="A visible trajectory that ignores integration error teaches the wrong lesson; validation and error display make the sandbox trustworthy.",
        field="web-dev",
        domain="other",
        difficulty="advanced",
        est_hours=150,
        tech_tags=["typescript", "physics", "rk4", "web-workers", "threejs", "validation"],
        datasets=[{"name": "JPL Horizons reference positions", "url": "https://ssd.jpl.nasa.gov/horizons/"}],
        approaches=[
            "Compute Hohmann and bi-elliptic transfer delta-v analytically.",
            "Propagate the state with RK4 under point-mass gravity in a Web Worker.",
            "Show step size, energy drift and simulated time next to the trajectory.",
            "Validate a simple case against JPL Horizons and add one gravity-assist scenario.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a browser mission trajectory sandbox that compares transfer burns, integrates the trajectory with RK4 and validates results against JPL Horizons.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A user compares Hohmann and bi-elliptic delta-v for two circular orbits and sees the simulated transfer.",
                    "checks": [
                        "The app computes delta-v for both transfer types from the chosen orbits.",
                        "The transfer trajectory animates from the integrated state, not a fixed path.",
                        "The user can change the start and target orbit radii and see the result update.",
                        "A clear label explains units and assumptions.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The simulation runs smoothly in a worker, shows integration error and matches a JPL Horizons reference case.",
                    "checks": [
                        "RK4 runs in a Web Worker with a visible step size and simulated time.",
                        "Energy error or another integration diagnostic is shown to the user.",
                        "A validation case compares positions with JPL Horizons within a stated tolerance.",
                        "One gravity-assist scenario changes the trajectory in a way the user can inspect.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You built a responsive simulation UI around real numerical work."},
                {"role": "Full-stack engineer", "how_it_helps": "The project combines client-side computation, data validation and a complete interface."},
                {"role": "Scientific software engineer", "how_it_helps": "You can explain integrators, error and validation against an external reference."},
                {"role": "Game / graphics engineer", "how_it_helps": "Trajectory rendering, camera controls and worker-driven updates are practical graphics work."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a mission trajectory sandbox that compared Hohmann and bi-elliptic delta-v and integrated transfers with RK4 in a Web Worker.",
                    "example": "Built a mission trajectory sandbox that compared Hohmann and bi-elliptic delta-v and integrated each transfer with RK4 in a Web Worker without blocking the UI.",
                },
                {
                    "bullet": "Validated simulated positions against JPL Horizons and surfaced integration error instead of hiding it.",
                    "example": "Validated a reference trajectory against JPL Horizons within a stated tolerance and displayed energy drift so users could judge the simulation.",
                },
                {
                    "bullet": "Added an inspectable gravity-assist scenario on top of the transfer planner.",
                    "example": "Added a gravity-assist scenario that changed the trajectory and let users inspect the pre- and post-assist orbital elements.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why use RK4 instead of a simple Euler step?",
                    "answer": "Euler accumulates error quickly in orbital motion, which shows up as drift in energy and position. RK4 gives much better accuracy for the same rough step size. I still display error because numerical integration is an approximation, not truth.",
                },
                {
                    "question": "Why run the simulation in a Web Worker?",
                    "answer": "Integration and rendering compete for the main thread. A worker keeps the interface responsive while the state propagates. The worker sends position samples or state updates, and the UI renders them.",
                },
                {
                    "question": "How did you validate the physics?",
                    "answer": "I used a simple case with known inputs, compared positions against JPL Horizons over a fixed interval, and stated the tolerance. I also checked energy behavior and made the assumptions visible in the UI.",
                },
            ],
            "differentiators": [
                "A real integrator with visible error, not a canned animation.",
                "Validation against an external reference source.",
                "Worker-based simulation that keeps the UI responsive.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-015",
        title="Molecule Explorer & Drug-Likeness Checker",
        summary=(
            "Build a browser tool where a user types or draws a molecule, sees it "
            "in 3D, and gets properties computed locally: molecular weight, logP, "
            "hydrogen-bond donors and acceptors, and a Lipinski rule-of-five "
            "verdict explained in plain language.\n\n"
            "Use a real cheminformatics library in the browser rather than a "
            "hand-written property table. Accept SMILES and compound names, fetch "
            "structures from PubChem when needed, and respect its rate limits. "
            "Load the large chemistry bundle lazily so the first page stays fast.\n\n"
            "Add substructure search over a small library and a side-by-side "
            "comparison of two molecules. Keep the educational disclaimer visible "
            "and explain each rule instead of only showing pass or fail. The "
            "resume signal is that you integrated a heavy scientific library into "
            "a usable web interface."
        ),
        who_affected="Chemistry students, educators and early-stage researchers checking basic drug-likeness properties.",
        why_matters="Property calculations are easy to get subtly wrong; a transparent, library-backed explorer teaches the rules and shows its assumptions.",
        field="web-dev",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["typescript", "rdkit-js", "3dmol", "cheminformatics", "pubchem", "lazy-loading"],
        datasets=[{"name": "PubChem compound structures", "url": "https://pubchem.ncbi.nlm.nih.gov/"}],
        approaches=[
            "Parse SMILES or resolve a compound name through PubChem, then render the molecule in 3D.",
            "Compute weight, logP, donors, acceptors and Lipinski checks with a real chemistry library.",
            "Load the heavy chemistry bundle lazily and cache resolved structures.",
            "Add substructure search and a two-molecule comparison with plain-language explanations.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a browser molecule explorer with local drug-likeness calculations, 3D rendering, PubChem lookup, substructure search and comparison.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A SMILES string renders in 3D and shows the five Lipinski properties with a clear verdict.",
                    "checks": [
                        "The app parses a valid SMILES string and renders a 3D structure.",
                        "Molecular weight, logP, donors and acceptors are computed locally.",
                        "The Lipinski verdict explains which rule passed or failed.",
                        "Invalid input produces a useful error instead of an empty viewer.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Name lookup, lazy loading, substructure search and comparison all work without blocking the first page.",
                    "checks": [
                        "Compound names resolve through PubChem with caching and rate-limit handling.",
                        "The chemistry bundle loads only when the explorer is used.",
                        "Substructure search works over a small local library.",
                        "Two molecules can be compared side by side with property differences highlighted.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You integrated a heavy scientific library into a responsive browser interface."},
                {"role": "Full-stack engineer", "how_it_helps": "PubChem lookup, caching and the local compute path form a complete application."},
                {"role": "Science software engineer", "how_it_helps": "You can explain the property calculations, their limits and the educational scope."},
                {"role": "Web performance engineer", "how_it_helps": "Lazy loading a large chemistry bundle is a concrete performance case study."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a browser molecule explorer with local Lipinski calculations and 3D rendering, cutting first-load JS by {X}% with lazy loading.",
                    "example": "Built a browser molecule explorer with local Lipinski calculations and 3D rendering, cutting initial JavaScript by 40% by loading the chemistry bundle only on demand.",
                },
                {
                    "bullet": "Added PubChem name lookup with caching and rate-limit handling for {N} compounds.",
                    "example": "Added PubChem name lookup with caching and rate-limit handling, covering 500 compound lookups without exceeding the public API limits.",
                },
                {
                    "bullet": "Explained each drug-likeness rule in plain language instead of showing a bare pass or fail.",
                    "example": "Explained each Lipinski rule in plain language, so users could see which property failed and why it matters.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why use a chemistry library instead of calculating properties yourself?",
                    "answer": "Lipinski properties have edge cases around aromaticity, protonation and descriptor definitions. A maintained library is more correct than a quick formula. I keep the educational explanation custom, but the numbers come from a tested implementation.",
                },
                {
                    "question": "How did you keep the page fast with a large chemistry bundle?",
                    "answer": "The explorer loads the chemistry and 3D bundles only when the user opens it. The landing page does not import them. I also cache resolved structures so repeat lookups do not refetch or recompute.",
                },
                {
                    "question": "What does the tool not tell the user?",
                    "answer": "It does not predict safety, efficacy or clinical suitability. Lipinski rules are a rough drug-likeness filter, not a medical verdict. The UI says this clearly and keeps the language educational.",
                },
            ],
            "differentiators": [
                "Real cheminformatics in the browser with lazy loading.",
                "Plain-language explanations next to each rule.",
                "PubChem lookup with caching and visible rate-limit handling.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-016",
        title="Sequence Alignment & Gene Finder Lab",
        summary=(
            "Build a teaching lab for DNA and protein sequences. A user pastes a "
            "sequence, runs Needleman-Wunsch or Smith-Waterman, and watches the "
            "scoring matrix fill step by step. Then trace back the best alignment "
            "and change gap or substitution scores to see the result shift.\n\n"
            "Implement the algorithms yourself; the visualization is the point. "
            "Keep the matrix and traceback separate from the UI so both global and "
            "local alignment share the same tested core. Add an open-reading-frame "
            "finder, codon translation and a restriction-site map on the same "
            "sequence input.\n\n"
            "Fetch real sequences from NCBI or UniProt with rate-limit handling, "
            "and cache them. The resume signal is that you can make a dynamic "
            "programming algorithm understandable without hiding the computation "
            "behind a library call."
        ),
        who_affected="Biology students, educators and developers learning sequence algorithms.",
        why_matters="Alignment is central to bioinformatics; an interactive traceback makes the scoring choices and their consequences visible.",
        field="web-dev",
        domain="education",
        difficulty="intermediate",
        est_hours=90,
        tech_tags=["typescript", "bioinformatics", "dynamic-programming", "ncbi-api", "visualization", "caching"],
        datasets=[{"name": "NCBI and UniProt public sequences", "url": "https://www.ncbi.nlm.nih.gov/"}],
        approaches=[
            "Implement global and local alignment with a shared matrix and traceback core.",
            "Animate matrix filling and traceback without blocking the interface.",
            "Add ORF finding, codon translation and restriction-site mapping.",
            "Fetch and cache sequences from public sources with rate-limit handling.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build an interactive sequence alignment lab with step-by-step matrix filling, traceback, ORF finding, translation and public sequence lookup.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Two sequences run global alignment, show the score and render the aligned result with matches highlighted.",
                    "checks": [
                        "Needleman-Wunsch returns the correct score for a small test pair.",
                        "The traceback produces an alignment with gaps and matches.",
                        "The user can change gap and mismatch scores and rerun.",
                        "Invalid nucleotides or proteins produce a clear error.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The matrix fills step by step, local alignment shares the core, and the lab adds ORF, translation and restriction views.",
                    "checks": [
                        "Matrix filling animates without freezing the page.",
                        "Smith-Waterman and Needleman-Wunsch share one tested alignment core.",
                        "ORF finding, translation and restriction-site mapping work on the same input.",
                        "A fetched NCBI or UniProt sequence is cached and displayed with its source.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "The step-by-step matrix and traceback show advanced state and visualization work."},
                {"role": "Full-stack engineer", "how_it_helps": "You built the algorithm core, public data lookup and the teaching interface."},
                {"role": "Bioinformatics engineer", "how_it_helps": "Alignment, translation and ORF logic are directly relevant domain skills."},
                {"role": "Software engineer / educator", "how_it_helps": "You can explain a dynamic program and make its intermediate state visible."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built an interactive sequence alignment lab covering global and local alignment with step-by-step matrix traceback.",
                    "example": "Built an interactive sequence alignment lab covering Needleman-Wunsch and Smith-Waterman, with step-by-step matrix filling and traceback for both.",
                },
                {
                    "bullet": "Shared one tested alignment core across two algorithms and added ORF, translation and restriction-site views.",
                    "example": "Shared one tested alignment core across global and local modes, then added ORF finding, codon translation and restriction-site mapping on the same sequence input.",
                },
                {
                    "bullet": "Added cached NCBI and UniProt lookup so real sequences load without repeated API calls.",
                    "example": "Added cached NCBI and UniProt lookup, so a demo sequence loaded once and could be reused without hitting public API limits.",
                },
            ],
            "interview_points": [
                {
                    "question": "What is the difference between global and local alignment?",
                    "answer": "Global alignment forces the full sequences to align end to end. Local alignment finds the best-scoring substring pair and resets negative scores to zero. They share the matrix and traceback structure but differ in initialization and where traceback starts.",
                },
                {
                    "question": "How did you keep the matrix animation responsive?",
                    "answer": "I compute the matrix in small batches and render updates between batches instead of blocking on the full computation. For larger inputs, I use a worker or a step control so the user can advance the fill deliberately.",
                },
                {
                    "question": "How did you test the alignment code?",
                    "answer": "I used small hand-checked pairs, known textbook cases and edge cases such as empty input, all mismatches and repeated bases. I compared scores and traceback output, not only whether an alignment was returned.",
                },
            ],
            "differentiators": [
                "A visible dynamic-programming traceback, not a black-box alignment result.",
                "One shared core for global and local alignment.",
                "Public sequence lookup with caching and source display.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-017",
        title="Epidemic Spread Simulator on Contact Networks",
        summary=(
            "Build an educational simulator that spreads a disease through a "
            "contact network of households, schools and workplaces. Add "
            "interventions such as vaccination, masking and school closure, and "
            "compare the outcome with a classic SIR curve.\n\n"
            "Model the population as a network, not a single mixed pool, so "
            "contacts change the shape of the outbreak. Run the simulation in a "
            "Web Worker, keep the assumptions visible, and let the user pause, "
            "step and change parameters mid-run. Add chart views for infections, "
            "hospital demand and the reproduction number over time.\n\n"
            "Fit the model to a small real case-count dataset and show how the "
            "estimate changes with assumptions. Label it as an educational model, "
            "not a forecast. The resume signal is that you can combine simulation, "
            "network structure and honest uncertainty in one interface."
        ),
        who_affected="Public-health students, educators and policy teams exploring intervention trade-offs.",
        why_matters="Network structure and timing change outbreak outcomes; an interactive model makes assumptions and uncertainty easier to discuss.",
        field="web-dev",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=95,
        tech_tags=["typescript", "simulation", "network-model", "web-workers", "charts", "epidemiology"],
        datasets=[{"name": "Synthetic contact networks and sample case counts", "url": None}],
        approaches=[
            "Generate a contact network from households, schools and workplaces.",
            "Simulate infection states over daily steps in a Web Worker.",
            "Add vaccination, masking and closure interventions with visible parameters.",
            "Fit a simple model to sample case counts and display uncertainty and assumptions.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a network-based epidemic simulator with interventions, SIR comparison, real-case fitting and visible assumptions.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A contact network spreads an infection over time and the user can compare one intervention with no intervention.",
                    "checks": [
                        "The simulation runs on a generated household, school and workplace network.",
                        "Infection states update over daily steps and produce an epidemic curve.",
                        "The user can turn one intervention on and rerun the simulation.",
                        "The UI states the model assumptions and that it is not a forecast.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The simulator runs smoothly in a worker, compares several interventions and fits sample case counts with uncertainty.",
                    "checks": [
                        "The simulation runs in a Web Worker and the UI stays responsive during long runs.",
                        "Vaccination, masking and school closure can be combined and compared against a baseline.",
                        "A fit view shows observed case counts, model output and a stated uncertainty band.",
                        "The reproduction number is plotted over time and responds to interventions.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You built a responsive simulation UI with charts, controls and long-running state."},
                {"role": "Full-stack engineer", "how_it_helps": "The project combines simulation logic, data fitting and a complete interface."},
                {"role": "Data / scientific software engineer", "how_it_helps": "Network modelling, fitting and uncertainty display are directly relevant."},
                {"role": "Product engineer", "how_it_helps": "You can explain assumptions and intervention trade-offs to non-specialists."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a network epidemic simulator that compared {N} interventions and kept the UI responsive with a Web Worker.",
                    "example": "Built a network epidemic simulator that compared vaccination, masking and school closure against a baseline while running the model in a Web Worker.",
                },
                {
                    "bullet": "Fitted the model to sample case counts and displayed uncertainty instead of a single forecast line.",
                    "example": "Fitted the model to sample case counts and displayed an uncertainty band, keeping the educational scope visible next to the chart.",
                },
                {
                    "bullet": "Made assumptions and parameters visible so users could change them mid-run and see the effect.",
                    "example": "Made contact assumptions and intervention parameters visible, so users could pause, change a value and compare the new curve without restarting the page.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why model contacts as a network?",
                    "answer": "A single mixed population hides who meets whom. Households and schools create clusters that change the outbreak shape and the effect of school closure. A network model lets those structures matter.",
                },
                {
                    "question": "Why is this not a forecast?",
                    "answer": "The model is simplified and fitted to limited sample data. It teaches mechanisms and trade-offs, but it does not include all real-world behavior. The UI states the assumptions and shows uncertainty instead of presenting one exact future.",
                },
                {
                    "question": "How does vaccination change the result?",
                    "answer": "Vaccination removes or reduces susceptibility for selected network nodes, which can break transmission chains. The effect depends on coverage and who is vaccinated, so the simulator lets the user change both rather than assuming one fixed number.",
                },
            ],
            "differentiators": [
                "A contact-network model rather than a single pooled SIR curve.",
                "Visible assumptions and uncertainty alongside the simulation.",
                "Worker-based runs that stay responsive during long simulations.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-018",
        title="Quantum Tunneling Lab",
        summary=(
            "Build an interactive solver for the one-dimensional time-dependent "
            "Schrodinger equation. A user draws a potential barrier or well, "
            "launches a wave packet and watches it tunnel, reflect and interfere. "
            "Compare the measured transmission with the analytic result for a "
            "rectangular barrier.\n\n"
            "The numerical solver is the product. Use a stable scheme, keep the "
            "grid and time step visible, and run the heavy computation in "
            "WebAssembly or on the GPU so the animation stays smooth. Show the "
            "probability density and the real and imaginary parts of the wave "
            "function rather than only a decorative line.\n\n"
            "Add a validation panel with the analytic transmission for a simple "
            "barrier and a note when the numerical result falls outside tolerance. "
            "The resume signal is that you can combine numerical PDE work, "
            "performance and a teaching interface."
        ),
        who_affected="Physics students, educators and anyone learning quantum tunneling through visual experiments.",
        why_matters="Tunneling is hard to build intuition for; an interactive solver with a known-answer check makes the approximation and its limits visible.",
        field="web-dev",
        domain="other",
        difficulty="advanced",
        est_hours=160,
        tech_tags=["typescript", "wasm", "numerical-pde", "webgl", "physics", "visualization"],
        datasets=[{"name": "Analytic rectangular-barrier reference values", "url": None}],
        approaches=[
            "Implement a stable 1D time-dependent Schrodinger solver on a configurable grid.",
            "Render probability density and wave-function components in real time.",
            "Run the compute-heavy solver in WebAssembly or on the GPU.",
            "Compare transmission with the analytic rectangular-barrier result and show tolerance.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build an interactive 1D quantum tunneling lab with a numerical Schrodinger solver, live wave-packet visualization and analytic validation.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A wave packet hits a rectangular barrier, and the user sees reflection and transmission on screen.",
                    "checks": [
                        "The solver evolves a Gaussian wave packet on a fixed grid.",
                        "The UI draws probability density and the barrier over time.",
                        "The user can change barrier height or width and rerun.",
                        "The simulation does not blow up for the supported parameter range.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The solver stays smooth under real-time compute, and measured transmission is checked against the analytic result.",
                    "checks": [
                        "WebAssembly or GPU compute keeps the animation responsive at the chosen grid size.",
                        "The UI shows grid spacing, time step and total probability as diagnostics.",
                        "Measured transmission is compared with the analytic rectangular-barrier value.",
                        "A warning appears when the numerical result falls outside the stated tolerance.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You built a real-time scientific visualization with performance constraints."},
                {"role": "Web performance engineer", "how_it_helps": "WASM or GPU compute for a numerical solver is a strong performance story."},
                {"role": "Scientific software engineer", "how_it_helps": "You can discuss numerical stability, validation and approximation limits."},
                {"role": "Graphics engineer", "how_it_helps": "Rendering a live wave field requires practical GPU and animation work."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built an interactive 1D Schrodinger solver that kept a {N}x{N} grid running smoothly with WebAssembly compute.",
                    "example": "Built an interactive 1D Schrodinger solver that kept a 2,048-point grid running smoothly by moving the time step into WebAssembly.",
                },
                {
                    "bullet": "Validated simulated transmission against the analytic barrier result and warned when error exceeded tolerance.",
                    "example": "Validated simulated transmission against the analytic rectangular-barrier result and warned users when error exceeded the stated tolerance.",
                },
                {
                    "bullet": "Visualized probability density and wave-function components in real time instead of a canned animation.",
                    "example": "Visualized probability density plus the real and imaginary components in real time, so users could see interference and reflection as they happened.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why is numerical stability the main challenge?",
                    "answer": "A bad time step or spatial discretization makes the wave function grow without bound. I chose a stable scheme for the supported parameter range and show grid spacing, time step and total probability so users can see when the simulation is no longer trustworthy.",
                },
                {
                    "question": "Why move the solver to WebAssembly or the GPU?",
                    "answer": "The time loop updates every grid point on every step, which is too slow in plain JavaScript for smooth animation. WASM or GPU compute keeps the frame rate usable while preserving the same numerical model.",
                },
                {
                    "question": "How do you know the simulation is correct?",
                    "answer": "For a rectangular barrier, I compare measured transmission with the analytic result. I also check total probability stays near one and test a free-particle case. The validation panel states the tolerance instead of implying exact agreement.",
                },
            ],
            "differentiators": [
                "A real numerical PDE solver, not a scripted animation.",
                "Analytic validation and visible error tolerance.",
                "WASM or GPU compute for smooth real-time output.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-019",
        title="Build Your Own React",
        summary=(
            "Write a small React-like library from scratch: element creation, a "
            "virtual DOM, diffing, a reconciler, function components, state and "
            "effect hooks, an event system and keyed list updates. Then build a "
            "demo app with your library and benchmark it against real React.\n\n"
            "Keep the API intentionally small and document the differences from "
            "React. The learning is in the update path: how a state change "
            "schedules work, how the reconciler matches old and new trees, why "
            "keys matter, and how effects are cleaned up. Write tests for each "
            "piece before composing them.\n\n"
            "Add a short write-up or visual debugger that shows the work loop and "
            "the diff for a list update. The resume signal is deep understanding "
            "of UI libraries, not a claim that your version replaces React."
        ),
        who_affected="Frontend engineers preparing for interviews and developers who want to understand how UI libraries work.",
        why_matters="Most frontend bugs come from state, reconciliation and effect timing; rebuilding the core makes those concepts concrete.",
        field="web-dev",
        domain="developer-tools",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["typescript", "virtual-dom", "reconciliation", "hooks", "benchmarking", "testing"],
        datasets=[{"name": "Synthetic render and list-update benchmarks", "url": None}],
        approaches=[
            "Implement element creation, virtual nodes and a reconciler with keyed children.",
            "Add function components plus state and effect hooks with a small scheduler.",
            "Build a demo app and test each layer independently.",
            "Benchmark render and list updates against React and document the differences.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Build a small React-like library with virtual DOM diffing, a reconciler, function components, hooks and keyed updates, then test and benchmark it.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A demo app renders components, updates state and handles a keyed list without breaking.",
                    "checks": [
                        "Element creation and rendering produce the expected DOM.",
                        "A state update rerenders only the affected component subtree.",
                        "Keyed list reordering preserves component state.",
                        "The library has tests for rendering and updates.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Hooks, effects and a scheduler work together, and a benchmark plus write-up explain the trade-offs.",
                    "checks": [
                        "State and effect hooks run in a defined order with cleanup between renders.",
                        "The reconciler handles insertions, removals, moves and keyed updates.",
                        "A demo app exercises forms, effects and list updates end to end.",
                        "A benchmark compares render and update time with React, and a write-up explains the differences.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Frontend engineer", "how_it_helps": "You can explain rendering, reconciliation and hook semantics from implementation experience."},
                {"role": "UI platform engineer", "how_it_helps": "A small renderer and scheduler are the core of UI platform work."},
                {"role": "Full-stack engineer", "how_it_helps": "The project shows deep client-side architecture and test discipline."},
                {"role": "Interview candidate", "how_it_helps": "It gives you a concrete story for virtual DOM, keys and effect timing questions."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a React-like library with virtual DOM diffing, a reconciler, hooks and keyed updates, plus a demo app.",
                    "example": "Built a React-like library with virtual DOM diffing, a reconciler, state and effect hooks and keyed list updates, then used it to build a small demo app.",
                },
                {
                    "bullet": "Benchmarked render and list-update performance against React and documented where the small implementation diverges.",
                    "example": "Benchmarked render and list-update performance against React and documented where the simpler reconciler diverged on large keyed lists.",
                },
                {
                    "bullet": "Added tests for each layer, including keyed moves and effect cleanup, before composing the library.",
                    "example": "Added tests for rendering, keyed moves and effect cleanup before composing the library, so regressions were caught at the layer that caused them.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why do keys matter in a list?",
                    "answer": "Keys tell the reconciler which old node matches which new node. Without stable keys, a reorder can look like a series of content updates and lose component state. I test insertions, removals and moves explicitly.",
                },
                {
                    "question": "How do effects run after a render?",
                    "answer": "The render phase builds the new tree. After commit, the scheduler runs pending effects and cleans up previous effects first. Dependencies decide whether an effect reruns. The order is defined, and cleanup is not optional.",
                },
                {
                    "question": "What did you learn by rebuilding React?",
                    "answer": "Most of the complexity is in scheduling and reconciliation, not JSX. Keys, batching and effect cleanup are not details; they decide whether updates preserve state and whether components behave predictably.",
                },
            ],
            "differentiators": [
                "A working reconciler with keyed updates, not just a render function.",
                "Hook and effect semantics covered by tests.",
                "A benchmark and honest write-up instead of a claim of React parity.",
            ],
        },
    ),
    dict(
        source_id="manabi-web-resume-020",
        title="Build Your Own Git",
        summary=(
            "Implement the core of Git: content-addressed object storage for "
            "blobs, trees and commits with SHA-1 hashing, a staging index, "
            "commit, log, branch and checkout, diff, and a three-way merge with "
            "conflict markers. Then add a web page that draws the commit graph "
            "and shows what each command changes inside the repository.\n\n"
            "The important parts are the object model and the index. A commit "
            "points at a tree; a tree points at blobs and other trees; a branch "
            "is a movable reference to a commit. Keep those invariants clear and "
            "test them by reading repositories created by real Git.\n\n"
            "The merge path should show base, ours and theirs, and write conflict "
            "markers when it cannot merge cleanly. The web view is not decoration: "
            "it makes the graph and object changes inspectable. The resume signal "
            "is that you can explain content-addressable storage and a real "
            "three-way merge."
        ),
        who_affected="Developers learning version-control internals and interviewers who want to see systems reasoning.",
        why_matters="Git is used every day but its object model and merge behavior are often opaque; rebuilding the core makes both concrete.",
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=95,
        tech_tags=["typescript", "git-internals", "sha1", "graph-visualization", "nodejs", "testing"],
        datasets=[{"name": "Repositories created by real Git", "url": None}],
        approaches=[
            "Store blobs, trees and commits as content-addressed objects with SHA-1 hashes.",
            "Implement a staging index plus commit, log, branch and checkout.",
            "Add diff and a three-way merge with explicit conflict markers.",
            "Render the commit graph and object changes in a small web view.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development resume project idea.",
        original_text="Implement Git object storage, the index, commits, branches, checkout, diff and a three-way merge, with a web view of the commit graph.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A repository can stage files, create a commit, show log output and check out a branch.",
                    "checks": [
                        "Blobs, trees and commits are stored with content-derived hashes.",
                        "The index stages additions and changes correctly.",
                        "Commit and log match the expected parent and tree structure.",
                        "Branch checkout restores the working tree for a simple case.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Diff, branch operations and a three-way merge work, and the repository can read real Git objects.",
                    "checks": [
                        "Diff shows added, removed and changed lines between commits.",
                        "A three-way merge writes conflict markers when changes overlap.",
                        "The implementation reads a repository created by real Git.",
                        "A web page draws the commit graph and shows the object changes behind each command.",
                    ],
                },
            ],
            "target_roles": [
                {"role": "Backend engineer", "how_it_helps": "Content-addressed storage, object graphs and merge logic are strong systems fundamentals."},
                {"role": "Full-stack engineer", "how_it_helps": "You built the core engine and a web view that makes it inspectable."},
                {"role": "Developer tools engineer", "how_it_helps": "Git internals and command behavior are directly relevant to tooling work."},
                {"role": "Interview candidate", "how_it_helps": "You can explain hashing, trees, commits and three-way merges with a working example."},
            ],
            "resume_bullets": [
                {
                    "bullet": "Implemented Git-style content-addressed storage, index, commits, branches, checkout and three-way merge.",
                    "example": "Implemented Git-style blob, tree and commit storage with SHA-1 hashing, plus the index, commit, log, branch, checkout and a three-way merge.",
                },
                {
                    "bullet": "Verified compatibility by reading and walking repositories created by real Git.",
                    "example": "Verified the object model by reading and walking real Git repositories, including nested trees and merge commits.",
                },
                {
                    "bullet": "Built a web commit-graph view that showed how each command changed the object store.",
                    "example": "Built a web commit-graph view that showed the object changes behind commit, branch and merge commands instead of only the final log.",
                },
            ],
            "interview_points": [
                {
                    "question": "What makes Git storage content-addressed?",
                    "answer": "Every object is named by a hash of its content. A blob hash identifies file content, a tree hash identifies a directory listing, and a commit hash identifies a snapshot plus metadata. If the content changes, the hash changes, which makes integrity checks natural.",
                },
                {
                    "question": "How does a three-way merge work?",
                    "answer": "It finds a merge base, compares base-to-ours and base-to-theirs, and applies non-overlapping changes. When both sides change the same region differently, it writes conflict markers. A clean merge is not just a diff between the two branch tips.",
                },
                {
                    "question": "Why add a web view to a Git implementation?",
                    "answer": "The object graph is the hard concept. A visual view of commits, parents, trees and branch references makes the implementation inspectable. It also forces the command layer to expose what it actually changed, not just print a log line.",
                },
            ],
            "differentiators": [
                "Compatibility checked against repositories created by real Git.",
                "A real three-way merge with conflict markers.",
                "A web view of the object graph, not only a command-line demo.",
            ],
        },
    ),
]


for _problem in PROBLEMS:
    _detail = RESUME_DETAILS.get(_problem["source_id"])
    if _detail is None:
        continue
    _problem["summary"] = (
        f"{_problem['summary'].rstrip()}\n\n{_detail['description']}"
    )
    _problem["resume_kit"]["target_roles"] = _detail["target_roles"]
    _problem["build_guide"] = _detail["build_guide"]


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
