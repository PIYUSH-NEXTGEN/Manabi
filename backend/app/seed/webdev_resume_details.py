"""Long-form descriptions, role focus, and build guides for the web-dev resume pack."""

DETAILS = {
    "manabi-web-resume-001": {
        "description": (
            "In the complete build, ship a field-ready PWA with a short form "
            "builder, a draft list, a record editor, an outbox screen and a "
            "conflict resolver. The sync service stores each record with a "
            "server version, an idempotency key and a change log, then returns "
            "a structured conflict response instead of overwriting. Add a small "
            "seed command that creates two field workers and a record they can "
            "edit from separate browser profiles.\n\n"
            "The finished repo should include an airplane-mode walkthrough, a "
            "two-profile conflict fixture, retry and duplicate-upload tests, "
            "and a README that explains the sync contract. A reviewer should be "
            "able to create a record offline, reload, reconnect, see it sync, "
            "force a conflict and merge it without losing either person's work."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "Shows you can own state, IndexedDB, service workers and degraded-network UX, not just happy-path screens."},
            {"role": "Full-stack engineer", "how_it_helps": "You designed the sync API, idempotency, versioning and conflict contract across client and server."},
            {"role": "Mobile web / PWA engineer", "how_it_helps": "Offline caching, reconnect behavior and storage limits are the core skills in this role."},
        ],
        "build_guide": [
            {
                "title": "Define the record contract and offline shell",
                "summary": "Start with the data that must survive a dead network, then make the app shell load without one.",
                "steps": [
                    "Write one form schema with text, number, date, photo and GPS fields. Decide what a record version means before writing any sync code.",
                    "Create the React app shell, route table and empty states. Add a service worker that precaches the shell and a visible online/offline indicator.",
                    "Design the local IndexedDB stores: records, drafts, outbox entries, photo blobs and sync errors. Keep the outbox separate from the record table.",
                    "Seed two sample workers and a shared record so you can reproduce concurrent edits from two browser profiles.",
                ],
            },
            {
                "title": "Build the local-first record flow",
                "summary": "Every user action writes locally first. The network is an optional background step.",
                "steps": [
                    "Build the form editor with autosave, validation and a draft list. Persist photo blobs and GPS coordinates without blocking the UI.",
                    "Add an outbox write on every save: record id, base version, changed fields, timestamp and a client-generated idempotency key.",
                    "Implement the sync worker with online/offline listeners, exponential backoff and a manual retry button. Show queued, syncing, failed and conflict states.",
                    "Add a record history view that reads the local change log so the field worker can see what was edited and when.",
                ],
            },
            {
                "title": "Build the sync API and conflict protocol",
                "summary": "The server must reject stale writes explicitly and make repeated requests safe.",
                "steps": [
                    "Create the records and changes tables with a version column and a unique idempotency key per write.",
                    "On write, compare the client base version with the current server version. Return 409 with both field values and the change history when they differ.",
                    "Store the idempotency key with the result so a retried request returns the same response instead of creating a duplicate.",
                    "Add endpoints for pulling updates after a cursor and for submitting a resolved merge with the next version.",
                ],
            },
            {
                "title": "Build the merge and status screens",
                "summary": "The conflict UI is the product. It must keep both versions visible and make the decision understandable.",
                "steps": [
                    "List every conflicting field with mine, theirs, base and a per-field choice. Show who changed it and when beside each value.",
                    "Preview the merged record before saving. Disable submit until every conflict has a choice or an explicit keep-both resolution.",
                    "Build an outbox screen that groups records by queued, syncing, failed and conflict, with a retry action for failed items.",
                    "Add an airplane-mode demo page with clear instructions so a reviewer can reproduce the flow in two minutes.",
                ],
            },
            {
                "title": "Harden, test and document the demo",
                "summary": "Offline apps fail in the seams. Test reconnects, duplicate uploads and partial photo transfers.",
                "steps": [
                    "Add tests for idempotent retries, stale-version conflicts, merge submission and service-worker cache updates.",
                    "Throttle the network in DevTools and verify that a failed photo upload does not block the text record from syncing.",
                    "Write a README with the sync contract, IndexedDB schema, conflict rules, local setup and a short demo script.",
                    "Record a short walkthrough showing offline creation, reload, reconnect and conflict resolution. Link it from the repo.",
                ],
            },
        ],
    },
    "manabi-web-resume-002": {
        "description": (
            "The complete product has a resident submission flow, a public "
            "issue map and list, a staff queue, a duplicate review screen and a "
            "ward-level service report. Each report stores a photo, rough "
            "location, category, status history and SLA deadline. Staff can "
            "merge duplicate reports, split a bad merge, reassign a department "
            "and record why a status changed.\n\n"
            "Finish with a seeded ward dataset, a privacy review of the public "
            "page, tests for duplicate thresholds and SLA edge cases, and a "
            "short operations guide. The strongest demo shows one new report "
            "joining an existing issue, a failed merge being corrected, and a "
            "resolved issue appearing in the public report without exposing the "
            "resident's identity."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built the public intake, staff workflow, duplicate logic and reporting layer end to end."},
            {"role": "Backend engineer", "how_it_helps": "Duplicate matching, SLA state machines, audit records and privacy rules are practical backend design work."},
            {"role": "Product engineer", "how_it_helps": "You can explain the trade-off between false merges and a duplicate backlog, which is the real product problem."},
        ],
        "build_guide": [
            {
                "title": "Model reports, issues and service levels",
                "summary": "Separate a resident report from the issue staff work on. That distinction makes duplicate handling possible.",
                "steps": [
                    "Define report, issue, status event, department, category and SLA policy records. A report can point at one issue; an issue can have many reports.",
                    "Store rough location for public views and precise coordinates for staff, with a clear rule for what leaves the building.",
                    "Write the status transition table: open, triaged, assigned, in progress, paused, resolved and reopened. Record who changed it, when and why.",
                    "Seed three wards, five categories, department routing rules and a small set of duplicate and non-duplicate reports.",
                ],
            },
            {
                "title": "Build intake and duplicate candidates",
                "summary": "Accept reports quickly, then score possible duplicates without silently merging them.",
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
                    "Implement merge and split actions that move reports between issues without deleting either report or its history.",
                    "Compute the SLA deadline from stored status events. Pause on waiting states and escalate when the remaining time crosses a threshold.",
                    "Add a moderation action for abusive or invalid reports, with a reason that appears in the audit log.",
                ],
            },
            {
                "title": "Build the public status experience",
                "summary": "The public page should prove progress without turning residents into a data source for harassment.",
                "steps": [
                    "Publish a map and list that show category, rough area, status and resolution time while hiding names, contacts and exact addresses.",
                    "Show a resolved-this-month summary by ward with average time to resolution and the number of open issues.",
                    "Make the public page read from a projection that contains only public fields, not from the staff table with hidden columns.",
                    "Add a simple report lookup by reference code so a resident can follow their own issue without creating an account.",
                ],
            },
            {
                "title": "Test corrections, privacy and the demo",
                "summary": "The correction path is what makes duplicate detection trustworthy.",
                "steps": [
                    "Test a false merge and a false split, including the audit entries and the public counts after each correction.",
                    "Add SLA tests for pause, resume, breach and overnight/weekend boundaries.",
                    "Review every public API response for leaked personal data and add a test that fails if a private field appears.",
                    "Write an operator guide and a demo script covering intake, duplicate merge, correction, resolution and the public report.",
                ],
            },
        ],
    },
    "manabi-web-resume-003": {
        "description": (
            "Ship a contribution finder with a search page, filter sidebar, "
            "repository cards, a score explanation panel and a personal save "
            "pipeline. The backend wraps GitHub search, stores cached repository "
            "metadata and records the user's saved, opened, commented and "
            "pull-request-opened states.\n\n"
            "The final repo should include a cached results view with refresh "
            "time, rate-limit handling, a small evaluation set of repositories "
            "you inspected by hand, and a README that explains every ranking "
            "signal. A reviewer should be able to find a beginner issue, see why "
            "the repository scored well, save it and advance it through the "
            "pipeline without touching the GitHub API directly."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You combined an external API, caching, ranking and user state in one product."},
            {"role": "Frontend engineer", "how_it_helps": "The filters, score explanations and saved-item pipeline show practical UI work with live third-party data."},
            {"role": "Developer experience engineer", "how_it_helps": "The project is about making contribution paths clearer, which is core developer-experience work."},
        ],
        "build_guide": [
            {
                "title": "Design the search and ranking contract",
                "summary": "Decide what a good first contribution means before calling the API.",
                "steps": [
                    "List the signals you will show: recent commit activity, issue response time, contributing guide, label quality and stars. Give each a clear input and weight.",
                    "Define the result shape: issue, repository, language, labels, last activity, score and the signal breakdown.",
                    "Write down the empty, rate-limited and stale-cache states so the UI does not treat them as success.",
                    "Create a small evaluation sheet with 15-20 repositories you have actually inspected and a note on whether each was welcoming.",
                ],
            },
            {
                "title": "Build the GitHub client and cache",
                "summary": "The wrapper must respect pagination, rate limits and conditional requests.",
                "steps": [
                    "Implement search and repository lookup calls with pagination and a server-side token. Keep the token out of the browser.",
                    "Cache responses with ETags and a fetched-at timestamp. Serve cached data with an age label when the API refuses or rate-limits.",
                    "Batch repository metadata fetches instead of one request per card. Store only the fields the ranking and UI need.",
                    "Add backoff and a clear error object for unauthorized, rate-limited and partial-response cases.",
                ],
            },
            {
                "title": "Implement explainable ranking",
                "summary": "Every score should be reconstructable from visible inputs.",
                "steps": [
                    "Compute each signal separately and normalize it against the current result set or a documented range.",
                    "Combine the signals into one score, then render a breakdown with the raw value and the points contributed.",
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
                "summary": "The ranking is the claim; the evaluation is the evidence.",
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
        "description": (
            "The complete hub has a public needs board, a coordinator map, a "
            "match panel, a fulfilment trail, role management and a daily export. "
            "Needs and offers store category, quantity, rough location, contact "
            "visibility and status. Coordinators can propose a match, accept it, "
            "record delivery and close it with a timestamp and note.\n\n"
            "Finish with an offline queue for weak networks, a compact SMS or "
            "WhatsApp fallback message, seeded response data and a drill script. "
            "The best demo shows a need and an offer being matched on the map, a "
            "second coordinator joining live, the connection dropping, and the "
            "match still completing with a full trail."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built the live board, matching rules, fulfilment model and fallback channel together."},
            {"role": "Frontend engineer", "how_it_helps": "The map, live updates and degraded-network states show real operational UI work."},
            {"role": "Backend engineer", "how_it_helps": "Matching, role checks, delivery tracking and notification fallbacks are practical backend problems."},
        ],
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
                "summary": "The board must update for everyone and every match must leave a trail.",
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
                    "Queue board edits and match updates in the browser when offline and replay them with idempotency keys on reconnect.",
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
        "description": (
            "The finished tool has a product-country selector, a structured "
            "checklist, a source panel for every requirement, a coverage matrix "
            "and a grounded assistant. Each checklist item stores a requirement, "
            "source, source version, last-checked date and plain-language note. "
            "The assistant can only answer from retrieved passages and must cite "
            "them or refuse.\n\n"
            "Ship with three products and three markets, a printable checklist, "
            "an update workflow for a changed regulation and a clear "
            "not-legal-advice notice. The demo should show a user finding a "
            "missing document, opening the official source, asking an unsupported "
            "question and receiving an honest refusal instead of a guess."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built structured domain data, a guided UI, source versioning and a retrieval-backed assistant."},
            {"role": "Backend engineer", "how_it_helps": "Versioned sources, coverage checks, retrieval limits and citation enforcement are practical backend concerns."},
            {"role": "AI application engineer", "how_it_helps": "You can explain retrieval boundaries, citations and refusal behavior, not just model calls."},
        ],
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
                "summary": "The checklist must be a query over structured rules, not a hand-written page.",
                "steps": [
                    "Implement product-country selection and generate a checklist grouped by documents, duties, labeling and market notes.",
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
                "summary": "Traceability is the resume claim, so show the evidence.",
                "steps": [
                    "Test that every checklist item has a valid source and that the assistant cannot answer without a citation.",
                    "Add a regression fixture for one changed regulation and verify the old and new checklist versions.",
                    "Write a README covering the source policy, coverage limits, retrieval design and local setup.",
                    "Record a demo that shows a cited checklist, a source update and a refusal for an unsupported question.",
                ],
            },
        ],
    },
    "manabi-web-resume-006": {
        "description": (
            "The complete planner imports one city's GTFS feed, exposes a trip "
            "API and renders an itinerary with legs, walking transfers and "
            "waiting time on a map. It compares fastest arrival with fewest "
            "transfers in the same query and returns both options. A benchmark "
            "page reports travel time, transfer count and query duration against "
            "a naive baseline.\n\n"
            "Finish with calendar and overnight-trip tests, feed validation, a "
            "small origin-destination benchmark set and a README that explains "
            "why the algorithm is timetable-aware. A reviewer should be able to "
            "enter two stops, see a valid trip, switch objectives and understand "
            "exactly when the next vehicle departs."
        ),
        "target_roles": [
            {"role": "Backend engineer", "how_it_helps": "Timetable modelling, graph algorithms and API design are the core of this project."},
            {"role": "Data engineer", "how_it_helps": "GTFS ingestion, calendar handling, feed validation and benchmark data are practical pipeline work."},
            {"role": "Full-stack engineer", "how_it_helps": "You connected a real algorithm to a map UI and an API without hiding the data model."},
        ],
        "build_guide": [
            {
                "title": "Import and validate GTFS",
                "summary": "The algorithm is only as correct as the feed model underneath it.",
                "steps": [
                    "Download one city feed and load stops, routes, trips, stop_times and calendar records into a staging schema.",
                    "Validate required files, missing stop times, duplicate ids and calendar ranges. Fail loudly with a readable report.",
                    "Normalize dates and time zones. Keep GTFS times as seconds from noon-minus-twelve so after-midnight trips do not wrap.",
                    "Build a queryable timetable index of stop events, route ids and service dates.",
                ],
            },
            {
                "title": "Implement a timetable-aware search",
                "summary": "Use RAPTOR or Connection Scan, not a static Dijkstra graph.",
                "steps": [
                    "Represent a trip as an ordered list of stop events and a route as a sequence of stops.",
                    "Implement round-based RAPTOR or a connection scan that tracks arrival time and transfers for each stop.",
                    "Carry two labels through the search: earliest arrival and fewest transfers. Keep them separate rather than blending them into one score.",
                    "Add walking transfers with a configurable maximum distance and transfer time.",
                ],
            },
            {
                "title": "Expose the planner API",
                "summary": "A thin UI needs a clear, testable contract.",
                "steps": [
                    "Create an endpoint that accepts origin, destination, departure date and time, plus an objective.",
                    "Return both fastest and fewest-transfer itineraries with legs, departure, arrival, waiting time and transfer walk.",
                    "Handle no-service, invalid stop and missing-feed cases with specific errors rather than empty results.",
                    "Add a benchmark endpoint or script that runs stored origin-destination pairs and reports time and transfer counts.",
                ],
            },
            {
                "title": "Build the map itinerary UI",
                "summary": "The map should explain the trip, not decorate it.",
                "steps": [
                    "Build stop search with keyboard selection and a clear origin-destination swap control.",
                    "Render each leg in a different style and separate walking transfers, waiting time and vehicle time in the itinerary list.",
                    "Add an objective toggle for fastest versus fewest transfers and keep both results visible for comparison.",
                    "Show service-date warnings when the selected day has no service or the feed is stale.",
                ],
            },
            {
                "title": "Validate correctness and performance",
                "summary": "Transit demos break on calendars, midnight and transfers. Test those first.",
                "steps": [
                    "Add tests for a normal trip, a weekend trip, an overnight trip and a trip with no service.",
                    "Compare the planner against a brute-force scan on a small extracted feed to prove correctness.",
                    "Run the benchmark against a naive time-expanded graph and record query time and transfer accuracy.",
                    "Document feed setup, algorithm choice and limits in the README, then record a short itinerary demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-007": {
        "description": (
            "The finished app scans a QR code with the camera or accepts pasted "
            "payloads, detects the format, validates the fields and shows the "
            "merchant, amount and currency before routing. It supports UPI, "
            "Bharat QR, EMV-style merchant payloads and ordinary payment links, "
            "then opens an app handoff or a clearly labelled sandbox checkout.\n\n"
            "Ship a merchant QR generator, a local test history, and a fixture "
            "suite covering valid, malformed, ambiguous and unknown payloads. "
            "The best demo shows a bad payload being rejected with a reason, a "
            "valid payload being confirmed field by field, and a generated QR "
            "round-tripping through the same parser without storing sensitive "
            "data."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "The camera flow, confirmation screen, error states and QR generation are practical browser UI work."},
            {"role": "Full-stack engineer", "how_it_helps": "You built parsing, routing, QR generation and history in one small, coherent product."},
            {"role": "Fintech engineer", "how_it_helps": "You can discuss format validation, sandbox boundaries and sensitive-data handling."},
        ],
        "build_guide": [
            {
                "title": "Define formats and safety boundaries",
                "summary": "A payment QR router is a parser with a strict no-real-money boundary.",
                "steps": [
                    "Collect public format documentation for UPI, Bharat QR, EMV merchant payloads and plain payment links.",
                    "Write the supported-fields table and a clear rejection rule for missing, conflicting or unsupported fields.",
                    "Define what is stored: format, masked merchant reference, amount, currency, status and timestamp only.",
                    "State in the README that the app never processes real payments and every checkout is sandbox or app handoff.",
                ],
            },
            {
                "title": "Build the parser pipeline",
                "summary": "Detect, parse, validate and explain as separate stages.",
                "steps": [
                    "Implement a format detector that returns a confidence and a reason, not just a best guess.",
                    "Write one parser per format with typed output and specific validation errors.",
                    "Add fixtures for valid, malformed, ambiguous and unsupported payloads. Make every rejection return a human-readable reason.",
                    "Create a shared parsed-payment shape so the confirmation UI and router do not depend on format-specific details.",
                ],
            },
            {
                "title": "Build scanning, confirmation and routing",
                "summary": "The user must see and confirm the payment details before anything opens.",
                "steps": [
                    "Add camera scanning plus paste and image-upload fallbacks. Handle permission denial cleanly.",
                    "Show merchant, amount, currency, format and warnings on a confirmation screen before routing.",
                    "Route only to an app deep link or sandbox page. Never construct a real payment request from an unconfirmed payload.",
                    "Add a test-mode label and a visible cancel path on every routed screen.",
                ],
            },
            {
                "title": "Add generator, history and test fixtures",
                "summary": "Round-tripping your own QR codes proves the parser is internally consistent.",
                "steps": [
                    "Build a merchant QR generator for at least two supported formats with a preview and download option.",
                    "Parse the generated payload back through the same pipeline and show a round-trip success result.",
                    "Store only test-mode history and mark it clearly. Add a clear-history action.",
                    "Add a fixture viewer so a reviewer can load a bad payload and see the exact rejection path.",
                ],
            },
            {
                "title": "Harden edge cases and document",
                "summary": "Ambiguous input is the normal case, so the UI must ask instead of guessing.",
                "steps": [
                    "Test conflicting amount fields, missing currency, unsupported schemes, oversized input and duplicate payloads.",
                    "Add a manual confirmation step for ambiguous formats and never auto-route when confidence is low.",
                    "Write the format support matrix, privacy rules and local setup in the README.",
                    "Record a demo showing a valid parse, an ambiguous confirmation and a rejected malformed payload.",
                ],
            },
        ],
    },
    "manabi-web-resume-008": {
        "description": (
            "The complete platform has a shopper catalogue with per-store stock, "
            "a reservation hold, a pickup code and a staff phone flow for barcode "
            "updates. Each stock change is an auditable event, and reservations "
            "expire automatically so available units return to the shelf view.\n\n"
            "Finish with a race-condition test for the last unit, a staff "
            "reconciliation report and in-store QR links that open the right "
            "product and store. The strongest demo shows two shoppers racing for "
            "the final unit, one reservation holding it, the other receiving a "
            "clear out-of-stock response, and a pickup reducing stock exactly "
            "once."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built catalogue, inventory, reservations, staff tools and audit history end to end."},
            {"role": "Backend engineer", "how_it_helps": "Transactional stock handling, expiry and race-condition tests are the strongest part of the project."},
            {"role": "E-commerce engineer", "how_it_helps": "Reservation holds, pickup state and stock consistency are core commerce problems."},
        ],
        "build_guide": [
            {
                "title": "Model catalogue, stores and stock events",
                "summary": "Availability is a transaction log, not a number someone edits.",
                "steps": [
                    "Define product, store, stock level, stock event, reservation and pickup records.",
                    "Choose the availability rule: on-hand minus active holds. Store events for reservation, release, pickup and manual adjustment.",
                    "Add store-specific product visibility and in-store QR mappings.",
                    "Seed two stores, a hundred products and a few live reservations so the shopper and staff views have realistic data.",
                ],
            },
            {
                "title": "Build transactional reservations",
                "summary": "The last unit is the whole project. Make the race safe in the database.",
                "steps": [
                    "Reserve stock inside a transaction using a row lock or conditional update that checks available quantity.",
                    "Set an expiry timestamp and a background job that releases expired holds back to available stock.",
                    "Record every reservation and release event with the reservation id so pickups cannot decrement stock twice.",
                    "Add a test that fires two reservations for the last unit at the same time and asserts exactly one succeeds.",
                ],
            },
            {
                "title": "Build the shopper pickup flow",
                "summary": "Shoppers need confidence about what is available at which store.",
                "steps": [
                    "Create catalogue and product pages with per-store availability, pickup window and clear reservation state.",
                    "Show a pickup code and instructions after reservation. Allow cancellation before the hold expires.",
                    "Add store search and a filter for items available nearby.",
                    "Make out-of-stock and expired-hold states explicit rather than silently removing the button.",
                ],
            },
            {
                "title": "Build the staff scan and reconciliation flow",
                "summary": "Staff work on a phone with one hand, so the flow must be fast and forgiving.",
                "steps": [
                    "Build a barcode-scan screen that updates stock or marks a pickup in two taps.",
                    "Show the recent stock events for a product with the source: reservation, pickup or adjustment.",
                    "Add a reconciliation view that lists reservations without pickups and stock levels that disagree with the event sum.",
                    "Protect staff actions with a store-scoped role and log the staff member on every event.",
                ],
            },
            {
                "title": "Test, demo and document the consistency story",
                "summary": "The resume claim is stock correctness, so prove it under load and failure.",
                "steps": [
                    "Add tests for expiry, cancellation, double pickup, manual adjustment and concurrent reservations.",
                    "Run a small load test with parallel reservations and verify available stock never goes negative.",
                    "Create an in-store QR demo that opens a product page for the correct store.",
                    "Write the stock model, transaction rules and setup in the README, then record the last-unit demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-009": {
        "description": (
            "The complete system covers student applications, document upload, "
            "reviewer verification, approver decisions, finance disbursement "
            "records and an admin report. Every state transition has a role, a "
            "reason and an audit entry, and students see a clear status timeline "
            "without emailing the office.\n\n"
            "Finish with rejection and resubmission paths, mock payment records, "
            "permission-boundary tests and an export that reconciles approved "
            "amounts against disbursements. A reviewer should be able to follow "
            "one application from submission through rejection, resubmission, "
            "approval and mock payment without ever seeing a document they are "
            "not allowed to open."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built the student flow, role model, workflow and reporting layer together."},
            {"role": "Backend engineer", "how_it_helps": "Permissions, state transitions, audit logs and reconciliation are real backend concerns."},
            {"role": "Product engineer", "how_it_helps": "You can explain a workflow with rejection, resubmission and finance handoff, not just a single form."},
        ],
        "build_guide": [
            {
                "title": "Model roles, applications and documents",
                "summary": "A workflow is a state machine with permissions, not a status dropdown.",
                "steps": [
                    "Define student, reviewer, approver, finance and admin roles, plus application, document, decision and disbursement records.",
                    "Draw the application state machine: draft, submitted, under review, changes requested, approved, rejected, paid and closed.",
                    "Decide document visibility per role and store the rule with the document type.",
                    "Seed one application in each important state so every role has something to test against.",
                ],
            },
            {
                "title": "Build submission and document handling",
                "summary": "Students need a clear checklist and a safe upload path.",
                "steps": [
                    "Build the application form with required fields, document slots, size limits and file-type validation.",
                    "Store documents with private access and signed, short-lived download links.",
                    "Add draft save, submit confirmation and a status timeline that explains what happens next.",
                    "Implement the rejection path with a reason and a resubmission flow that keeps the previous version.",
                ],
            },
            {
                "title": "Build the review and approval workflow",
                "summary": "Every transition should check the actor, the current state and the reason.",
                "steps": [
                    "Build a reviewer queue with document verification, notes and request-changes actions.",
                    "Build an approver view that only shows verified applications and records a decision with a reason.",
                    "Enforce transitions on the server and log actor, old state, new state, timestamp and reason for every change.",
                    "Add an audit view for admins that filters by application, actor and action.",
                ],
            },
            {
                "title": "Build finance records and reporting",
                "summary": "The report must be derived from the workflow, not typed in separately.",
                "steps": [
                    "Create mock disbursement records tied to an approved application and a signed-off amount.",
                    "Build a finance queue with a clear paid and pending state. Label every payment as mock or test mode.",
                    "Add an export that reconciles approved amounts, recorded disbursements and open items.",
                    "Show a student-facing payment status without exposing internal reviewer notes.",
                ],
            },
            {
                "title": "Test permissions, audit and the full case",
                "summary": "The strongest evidence is a complete case that proves the boundaries held.",
                "steps": [
                    "Add tests that a student cannot read another student's documents and a reviewer cannot approve.",
                    "Test every illegal state transition and assert that no audit entry is created for a rejected action.",
                    "Run one end-to-end case through rejection, resubmission, approval and mock payment.",
                    "Document the role matrix, workflow diagram, setup and data limits in the README.",
                ],
            },
        ],
    },
    "manabi-web-resume-010": {
        "description": (
            "The complete builder lets a shop owner create an account, add "
            "products, upload images, choose a simple theme, preview the store "
            "and publish it at a branded slug. Shoppers browse the public catalogue "
            "and start an order through a WhatsApp link or in-store QR code.\n\n"
            "Finish with draft and published states, tenant-safe ownership checks, "
            "image size limits and an optional test-mode plan page. The strongest "
            "demo creates two shops, proves that one owner cannot read or edit the "
            "other, publishes a storefront and opens the generated WhatsApp order "
            "from a product page on a phone-sized viewport."
        ),
        "target_roles": [
            {"role": "Full-stack engineer", "how_it_helps": "You built tenant-aware data, owner flows and a public storefront in one product."},
            {"role": "Backend engineer", "how_it_helps": "Ownership checks, tenant isolation and slug routing are practical multi-tenant backend work."},
            {"role": "Frontend engineer", "how_it_helps": "The editor, live preview and public storefront show both internal and customer-facing UI."},
        ],
        "build_guide": [
            {
                "title": "Design tenant isolation first",
                "summary": "One database serves every shop, so ownership must be enforced in every query.",
                "steps": [
                    "Define shop, owner, product, theme and order-enquiry records with a shop id on every tenant-owned row.",
                    "Choose the slug rules and reserve names that could collide with app routes.",
                    "Write the ownership check once in a shared access layer instead of repeating it in every handler.",
                    "Create tests that two owners cannot read, update or delete each other's products.",
                ],
            },
            {
                "title": "Build owner onboarding and product editing",
                "summary": "A non-technical owner should publish a credible catalogue without a manual.",
                "steps": [
                    "Build sign-up, shop setup and a dashboard with a clear draft or published state.",
                    "Add product create, edit, reorder, archive and image upload with file-size and dimension limits.",
                    "Build a live preview beside the editor so theme and layout changes are visible immediately.",
                    "Add validation for missing names, prices, images and pickup instructions before publishing.",
                ],
            },
            {
                "title": "Build the public storefront",
                "summary": "The shopper page should load fast and make the next action obvious.",
                "steps": [
                    "Create a public shop page by slug with products, about text, hours and pickup instructions.",
                    "Add product detail pages with images, price, availability and a WhatsApp enquiry button prefilled with the product and shop.",
                    "Generate QR codes for the shop and individual products that resolve to the correct public URL.",
                    "Handle unknown, unpublished and archived shops with clear pages instead of a blank storefront.",
                ],
            },
            {
                "title": "Add plans, limits and safe publishing",
                "summary": "Optional monetisation should not become a fake payment flow.",
                "steps": [
                    "Add an optional test-mode plan page with product and image limits. Label it as a demo and never charge a card.",
                    "Enforce limits on the server and show the remaining allowance in the owner dashboard.",
                    "Log publish, unpublish and plan changes in an owner-visible activity list.",
                    "Add a tenant-safe media cleanup job for deleted or unused images.",
                ],
            },
            {
                "title": "Demo multi-tenancy and document the model",
                "summary": "The resume claim is safe isolation, so show the negative test.",
                "steps": [
                    "Create two seeded shops and demonstrate the ownership block in both the UI and an API test.",
                    "Publish one shop, open its public URL, scan the QR and start a WhatsApp order from a product page.",
                    "Test slug collisions, image limits and unpublished storefront behavior.",
                    "Write the tenant model, access rules and local setup in the README, then record the two-shop demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-011": {
        "description": (
            "For this brief, build and publish one narrow TypeScript package: "
            "a zero-dependency human-duration formatter and parser that handles "
            "inputs such as 90, 1h 30m and 2 days 4 hours. Export a tiny typed "
            "API, document every function and test the edge cases users will hit: "
            "negative values, decimal hours, rounding and invalid input.\n\n"
            "Finish with ESM and CommonJS builds, generated declarations, source "
            "maps, CI tests, bundle-size checks, a changelog and an automated "
            "release. A reviewer should be able to install the package from a "
            "tarball or npm, see the examples in the README and trace one version "
            "from a pull request to a published release note."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You can show typed API design, package consumption and compatibility work that frontend teams rely on."},
            {"role": "Library / platform engineer", "how_it_helps": "Build outputs, types, compatibility policy and releases are the core of library maintenance."},
            {"role": "Developer experience engineer", "how_it_helps": "Docs, examples, bundle-size checks and release automation are direct developer-experience work."},
        ],
        "build_guide": [
            {
                "title": "Define the API and compatibility policy",
                "summary": "A small package needs a sharp promise about what it will and will not do.",
                "steps": [
                    "Write the two or three exported functions and their input and output types before writing implementation code.",
                    "Decide the supported runtimes, module formats, TypeScript versions and the semantic-versioning policy.",
                    "List explicit non-goals such as time zones, localization or calendar math so the scope stays narrow.",
                    "Create a short design note with examples and the error behavior for invalid input.",
                ],
            },
            {
                "title": "Implement and test the utility",
                "summary": "The code is small; the edge cases are the project.",
                "steps": [
                    "Implement the parser and formatter with pure functions and no dependencies.",
                    "Add tests for zero, negative, decimal, overflow, whitespace, mixed units and malformed input.",
                    "Add property-style or table-driven tests to cover round-trip parsing and formatting.",
                    "Check tree-shaking and bundle size, then remove any code that does not earn its place.",
                ],
            },
            {
                "title": "Build the package outputs",
                "summary": "Consumers should not need to know how the package was built.",
                "steps": [
                    "Configure ESM and CommonJS outputs with generated declarations and source maps.",
                    "Set exports, files and sideEffects correctly so bundlers resolve the right entry.",
                    "Add a smoke test that installs the packed tarball into a tiny consumer project and imports it both ways.",
                    "Verify the published file list contains only the build, types, README and license.",
                ],
            },
            {
                "title": "Add CI, releases and documentation",
                "summary": "A package is a maintenance product, not a folder of helpers.",
                "steps": [
                    "Run lint, typecheck, tests and the tarball smoke test in CI on every pull request.",
                    "Set up conventional commits, changelog generation and a release workflow that publishes only after the checks pass.",
                    "Write a README with install, API reference, examples, error behavior and a compatibility table.",
                    "Add a CONTRIBUTING note and a versioned upgrade example so consumers know how to handle breaking changes.",
                ],
            },
            {
                "title": "Publish and prove consumption",
                "summary": "The final proof is another project using the package.",
                "steps": [
                    "Publish a dry-run tarball and inspect the contents before releasing.",
                    "Publish version 1.0.0 and install it into a small demo app that uses the formatter in a real UI.",
                    "Record the bundle-size result and add it to the README.",
                    "Link the release, changelog and demo from the repo description.",
                ],
            },
        ],
    },
    "manabi-web-resume-012": {
        "description": (
            "The complete job system has an enqueue API, a persistent Postgres "
            "queue, a worker pool, scheduled jobs, retry backoff, a dead-letter "
            "queue and an operator dashboard. Jobs store attempts, lease and "
            "heartbeat data, so a crashed worker can be detected and its work "
            "redelivered safely.\n\n"
            "Finish with idempotent example handlers, a failure-injection mode, "
            "a load test and a README that states the delivery guarantee honestly. "
            "The demo should show a worker dying mid-job, the job being reclaimed, "
            "a retry succeeding and a permanently failing job landing in the "
            "dead-letter queue with enough context to debug it."
        ),
        "target_roles": [
            {"role": "Backend engineer", "how_it_helps": "Queue state, retries, timeouts and worker coordination are core backend work."},
            {"role": "Distributed systems engineer", "how_it_helps": "You can discuss delivery guarantees, failure recovery and idempotency from a real test."},
            {"role": "DevOps / SRE", "how_it_helps": "The dashboard, health signals and failure drills map directly to operating a job system."},
        ],
        "build_guide": [
            {
                "title": "Model jobs and worker leases",
                "summary": "The database is the source of truth; the queue is a claim on a row.",
                "steps": [
                    "Define job, attempt, worker, schedule and dead-letter records with status, run time, lease expiry and payload.",
                    "Choose the delivery guarantee: at-least-once, with handlers required to be idempotent.",
                    "Design the claim query so two workers cannot take the same job at the same time.",
                    "Write the state machine: queued, claimed, running, succeeded, retry-wait, dead and cancelled.",
                ],
            },
            {
                "title": "Build the worker loop and retries",
                "summary": "The hard parts are abandonment, backoff and duplicate side effects.",
                "steps": [
                    "Implement claim, heartbeat, complete and fail operations with lease expiry checks.",
                    "Reclaim expired leases and increment attempts without losing the original payload.",
                    "Add exponential backoff with jitter and a maximum-attempts rule that moves the job to dead-letter.",
                    "Add a scheduler path for delayed and recurring jobs using the same claim table.",
                ],
            },
            {
                "title": "Build the operator dashboard",
                "summary": "Operators need to see stuck work before users report it.",
                "steps": [
                    "Show queue depth, oldest queued job, retry counts, dead-letter count and worker heartbeats.",
                    "Add job detail with attempts, errors, payload preview and a safe retry or cancel action.",
                    "Add filters by queue, status, handler and time range.",
                    "Show an alert when no heartbeat has arrived within the expected window.",
                ],
            },
            {
                "title": "Add failure injection and idempotency",
                "summary": "A queue that has never lost a worker is not evidence.",
                "steps": [
                    "Provide example handlers: one idempotent write, one always-fails job and one slow job with a heartbeat.",
                    "Add a fault-injection mode that kills workers, delays completion and drops connections on demand.",
                    "Verify that a repeated job does not duplicate the side effect by using an idempotency key in the handler.",
                    "Run a load test and record throughput, p95 wait time and recovery time after worker loss.",
                ],
            },
            {
                "title": "Document guarantees and the failure demo",
                "summary": "The resume value is reasoning about failure, not a loop with sleep.",
                "steps": [
                    "Write a README section on at-least-once delivery, idempotency and the dead-letter policy.",
                    "Add integration tests for lease expiry, retry, exhaustion and duplicate delivery.",
                    "Record a demo of a worker dying, a job being reclaimed and a final success.",
                    "Include the load-test numbers and the known limits of the implementation.",
                ],
            },
        ],
    },
    "manabi-web-resume-013": {
        "description": (
            "The finished tracker accepts an observer location, loads recent TLE "
            "data for bright satellites, predicts passes and marks only the ones "
            "the observer can actually see. It renders the ground track on a 3D "
            "globe and the pass path on a local sky chart, with rise time, maximum "
            "elevation, direction and duration.\n\n"
            "Finish with cached elements and a visible data age, a separation "
            "between orbital math and rendering, tests against known passes, and "
            "a simple alert for the next good pass. The demo should compare a "
            "predicted ISS pass with a public reference and explain why a "
            "high-elevation pass can still be invisible."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You combined real orbital math with a globe and sky-chart interface in the browser."},
            {"role": "Geospatial / visualization engineer", "how_it_helps": "Coordinate transforms, ground tracks and sky projections are practical visualization work."},
            {"role": "Science software engineer", "how_it_helps": "You can explain the orbital model, its inputs and its validation against known passes."},
        ],
        "build_guide": [
            {
                "title": "Build the orbital data layer",
                "summary": "Predictions start with fresh elements and a clean observer model.",
                "steps": [
                    "Choose a TLE provider and cache the element sets with a fetched-at timestamp.",
                    "Parse TLE lines into a typed satellite record and reject malformed or stale entries.",
                    "Convert observer latitude, longitude and elevation into the coordinate frames used by the propagator.",
                    "Show the element age in the UI and document the provider's usage rules.",
                ],
            },
            {
                "title": "Compute passes and visibility",
                "summary": "Above the horizon is not the same as visible to a person.",
                "steps": [
                    "Use SGP4 to propagate satellite position over a time window and find rise, culmination and set events.",
                    "Compute azimuth and elevation relative to the observer for each sample.",
                    "Compute sun altitude at the observer and whether the satellite is illuminated by the sun.",
                    "Mark a pass visible only when the observer is dark enough and the satellite is sunlit.",
                ],
            },
            {
                "title": "Render the globe and sky chart",
                "summary": "Two views answer different questions: where it is and where to look.",
                "steps": [
                    "Render the observer, satellite position and ground track on a 3D globe with time controls.",
                    "Render the current pass on a sky chart using azimuth and elevation, with labels for the cardinal directions.",
                    "Add a timeline that scrubs the pass and updates both views together.",
                    "Keep the orbital computation in a worker or pure module so rendering never owns the math.",
                ],
            },
            {
                "title": "Add alerts, location and degraded states",
                "summary": "A pass predictor must handle a bad location, stale data and no visible pass.",
                "steps": [
                    "Add location search and a manual coordinate fallback, with clear validation.",
                    "Add an alert for the next visible pass above a chosen elevation threshold.",
                    "Show empty states for no visible passes in the next 24 hours and for stale elements.",
                    "Cache the last good prediction so a temporary provider outage does not blank the page.",
                ],
            },
            {
                "title": "Validate against known passes",
                "summary": "The science claim needs a reference, not a nice animation.",
                "steps": [
                    "Compare rise time, maximum elevation and direction for one pass against a public tracker or published data.",
                    "Add unit tests for coordinate transforms and pass-event detection.",
                    "Document the accuracy limits, TLE freshness and visibility assumptions.",
                    "Record a demo that explains an invisible but high-elevation pass.",
                ],
            },
        ],
    },
    "manabi-web-resume-014": {
        "description": (
            "The complete sandbox lets a user choose a start orbit and target "
            "orbit, compare Hohmann and bi-elliptic transfers, inspect each "
            "delta-v burn and then propagate the chosen trajectory through an "
            "RK4 integrator. The heavy work runs in a Web Worker while the "
            "interface shows step size, simulated time, energy drift and a live "
            "3D trajectory.\n\n"
            "Finish with an analytic transfer check, a JPL Horizons validation "
            "case, a gravity-assist scenario and a README that separates model "
            "assumptions from results. A reviewer should be able to see why one "
            "transfer is cheaper, run it, and understand the cost of a larger "
            "integration step."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You built a responsive simulation UI around real numerical work."},
            {"role": "Scientific software engineer", "how_it_helps": "You can explain integrators, error and validation against an external reference."},
            {"role": "Game / graphics engineer", "how_it_helps": "Trajectory rendering, camera controls and worker-driven updates are practical graphics work."},
        ],
        "build_guide": [
            {
                "title": "Define the orbital model and units",
                "summary": "Most simulation bugs are unit bugs or mismatched frames.",
                "steps": [
                    "Choose the central body, gravitational parameter, distance unit and time unit, and document them in one constants module.",
                    "Represent state as position and velocity and define the coordinate frame used for rendering.",
                    "Implement circular-orbit helpers for radius, speed and period with tests.",
                    "Write the Hohmann and bi-elliptic delta-v formulas with worked examples before building the UI.",
                ],
            },
            {
                "title": "Build transfer comparison",
                "summary": "The user needs to understand the trade before seeing the animation.",
                "steps": [
                    "Create inputs for start radius, target radius and transfer type, with clear ranges and units.",
                    "Compute total delta-v, burn count and transfer time for Hohmann and bi-elliptic transfers.",
                    "Show a side-by-side comparison with the assumptions and the point where one becomes cheaper.",
                    "Add validation for impossible or degenerate orbits instead of returning NaN.",
                ],
            },
            {
                "title": "Implement the RK4 propagator",
                "summary": "The trajectory must come from the integrator, not a scripted path.",
                "steps": [
                    "Implement an RK4 step for point-mass gravity with a configurable time step.",
                    "Track energy and angular momentum so drift can be displayed honestly.",
                    "Move integration into a Web Worker and stream state samples back with a cancel path.",
                    "Add step-size controls and show what happens to energy error when the step grows.",
                ],
            },
            {
                "title": "Render and control the trajectory",
                "summary": "The visual layer should make the physics inspectable.",
                "steps": [
                    "Render the central body, orbit paths, burns and the moving spacecraft on a 3D scene.",
                    "Add camera controls, pause, play, speed and a timeline scrubber.",
                    "Show burn markers with delta-v and time, and highlight the current orbital state.",
                    "Keep rendering decoupled from the worker so the UI stays responsive during a long run.",
                ],
            },
            {
                "title": "Validate, document and demo",
                "summary": "A trajectory that ignores error teaches the wrong lesson.",
                "steps": [
                    "Test the analytic transfer delta-v against hand calculations.",
                    "Validate one simple propagated state against a JPL Horizons reference within a stated tolerance.",
                    "Add one gravity-assist scenario or clearly document it as an extension.",
                    "Write the assumptions, error display and validation results in the README, then record the comparison demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-015": {
        "description": (
            "The finished molecule explorer accepts a SMILES string or a compound "
            "name, resolves structures through PubChem when needed, renders the "
            "molecule in 3D and computes molecular weight, logP, hydrogen-bond "
            "donors and acceptors locally. It explains the Lipinski rule-of-five "
            "item by item instead of returning a bare pass or fail.\n\n"
            "Finish with lazy-loaded chemistry bundles, cached structure lookups, "
            "a two-molecule comparison and substructure search over a small "
            "library. The demo should show a failed lookup degrading cleanly, a "
            "local property calculation with its formula, and a comparison that "
            "explains which rule changed and why."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You integrated a heavy scientific library into a responsive, accessible browser interface."},
            {"role": "Full-stack engineer", "how_it_helps": "PubChem lookup, caching, local compute and the comparison flow form a complete application."},
            {"role": "Science software engineer", "how_it_helps": "You can explain the property calculations, their limits and the educational scope."},
        ],
        "build_guide": [
            {
                "title": "Choose the chemistry stack and scope",
                "summary": "Use a real library and state its limits before building the UI.",
                "steps": [
                    "Pick a browser-compatible chemistry library for parsing, properties and rendering, and verify its bundle size.",
                    "Define the supported inputs: SMILES and compound names, with clear errors for salts, mixtures and invalid strings.",
                    "Write the property list and the exact Lipinski thresholds you will display.",
                    "Add a visible educational disclaimer that this is not a medical or research decision tool.",
                ],
            },
            {
                "title": "Build input and structure resolution",
                "summary": "The same molecule can arrive as a name, a SMILES string or a PubChem record.",
                "steps": [
                    "Build a SMILES input with validation and a small example gallery.",
                    "Add compound-name lookup through PubChem with rate-limit handling and a cached response.",
                    "Normalize the molecule and store the canonical identifier so comparisons and caching are stable.",
                    "Show a clear error panel when lookup fails, including suggestions to try a SMILES string.",
                ],
            },
            {
                "title": "Compute and explain properties",
                "summary": "The educational value is in the explanation, not just the number.",
                "steps": [
                    "Compute molecular weight, logP, donors and acceptors with the chemistry library.",
                    "Render each Lipinski rule with the measured value, threshold, pass state and a plain-language note.",
                    "Add a property table with units and the source of each value.",
                    "Test a few known molecules against published values and document any differences.",
                ],
            },
            {
                "title": "Add 3D rendering and comparison",
                "summary": "Visual and side-by-side views turn a calculator into an explorer.",
                "steps": [
                    "Render the molecule in 3D with rotate, zoom and reset controls.",
                    "Add a two-molecule comparison with aligned property rows and highlighted differences.",
                    "Add substructure search over a small seeded library and show matching molecules.",
                    "Lazy-load the rendering and chemistry bundles so the initial page stays small.",
                ],
            },
            {
                "title": "Test performance and document the limits",
                "summary": "A heavy scientific bundle needs evidence that the app remains usable.",
                "steps": [
                    "Measure initial load, first molecule render and comparison time on a mid-range device.",
                    "Add tests for invalid SMILES, failed PubChem lookup and cache hits.",
                    "Document the property method, known limitations and educational scope in the README.",
                    "Record a demo that shows local computation, a rule explanation and a two-molecule comparison.",
                ],
            },
        ],
    },
    "manabi-web-resume-016": {
        "description": (
            "The complete lab accepts a pasted or fetched DNA or protein sequence, "
            "runs Needleman-Wunsch or Smith-Waterman and animates the scoring "
            "matrix and traceback. It also finds open reading frames, translates "
            "codons and maps restriction sites on the same sequence. Scoring "
            "controls change the alignment visibly.\n\n"
            "Finish with a shared tested algorithm core, rate-limited public "
            "sequence lookup, a cache and an explanation panel for every scoring "
            "choice. A reviewer should be able to paste a short sequence, step "
            "through the matrix, trace the best alignment and see why a gap "
            "penalty changed the result."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "The step-by-step matrix and traceback show advanced state and visualization work."},
            {"role": "Bioinformatics engineer", "how_it_helps": "Alignment, translation and ORF logic are directly relevant domain skills."},
            {"role": "Software engineer / educator", "how_it_helps": "You can explain a dynamic program and make its intermediate state understandable."},
        ],
        "build_guide": [
            {
                "title": "Implement the alignment core",
                "summary": "The algorithm must be testable without the animation.",
                "steps": [
                    "Define a scoring model with match, mismatch, gap-open and gap-extend values.",
                    "Implement global Needleman-Wunsch and local Smith-Waterman with a shared matrix and traceback layer.",
                    "Return the score, aligned sequences and the traceback path as data.",
                    "Add tests for identical, shifted, gapped and empty sequences against hand-checked results.",
                ],
            },
            {
                "title": "Build the step-through visualization",
                "summary": "The matrix is the teaching artifact, so make its state visible.",
                "steps": [
                    "Render the matrix with row and column labels, scores and the current cell highlight.",
                    "Add step, play, pause and reset controls that update from a precomputed trace, not a second implementation.",
                    "Show the recurrence for the current cell with the chosen predecessor highlighted.",
                    "Render the traceback path and the final alignment side by side.",
                ],
            },
            {
                "title": "Add ORF, translation and restriction tools",
                "summary": "One sequence input should power several small teaching tools.",
                "steps": [
                    "Implement six-frame translation with a clear codon table and stop-codon handling.",
                    "Find open reading frames above a configurable minimum length and show their strand and frame.",
                    "Map common restriction sites and show cut positions on the sequence.",
                    "Keep all tools operating on the same normalized sequence and share the input state.",
                ],
            },
            {
                "title": "Fetch public sequences safely",
                "summary": "External sequence data needs caching, validation and clear provenance.",
                "steps": [
                    "Add NCBI or UniProt lookup by accession with a server-side request and rate-limit handling.",
                    "Validate and normalize the returned sequence, and show the accession and source beside it.",
                    "Cache fetched sequences and handle invalid accessions and network failures with clear messages.",
                    "Allow pasted FASTA input and parse headers without losing the sequence.",
                ],
            },
            {
                "title": "Test the teaching path and document it",
                "summary": "The project succeeds when a learner can explain the result.",
                "steps": [
                    "Add tests for scoring changes that flip a gap placement or switch from global to local alignment.",
                    "Verify the ORF and translation tools against a short known sequence.",
                    "Document the scoring model, algorithm choice and public-data limits in the README.",
                    "Record a demo that steps through a matrix and explains one traceback decision.",
                ],
            },
        ],
    },
    "manabi-web-resume-017": {
        "description": (
            "The complete simulator builds a contact network of households, "
            "schools and workplaces, runs infection states over daily steps and "
            "adds vaccination, masking and school-closure interventions. The user "
            "can pause, step and change parameters mid-run while charts show "
            "infections, hospital demand and the reproduction number.\n\n"
            "Finish with a classic SIR comparison, an uncertainty view, a fit to "
            "a small case-count dataset and a visible assumptions panel. The demo "
            "should show two runs with the same starting conditions but different "
            "network structure, then explain why the peak changed."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You built a responsive simulation UI with charts, controls and long-running state."},
            {"role": "Data / scientific software engineer", "how_it_helps": "Network modelling, fitting and uncertainty display are directly relevant."},
            {"role": "Full-stack engineer", "how_it_helps": "The project combines simulation logic, data fitting and a complete interface."},
        ],
        "build_guide": [
            {
                "title": "Define the network and disease model",
                "summary": "The network is the intervention surface; the disease model is the time step.",
                "steps": [
                    "Define person, contact edge, setting, infection state and daily event records.",
                    "Generate a synthetic population with households, schools and workplaces, and document the contact assumptions.",
                    "Choose states such as susceptible, exposed, infectious, hospitalized, recovered and deceased.",
                    "Write the transition rules and parameters in one module with units and defaults.",
                ],
            },
            {
                "title": "Build the simulation loop",
                "summary": "Move the model into a worker before adding any UI complexity.",
                "steps": [
                    "Implement a daily step that updates states from contacts, recovery and intervention effects.",
                    "Add a seeded random generator so runs are reproducible.",
                    "Run the loop in a Web Worker and stream daily summaries to the UI.",
                    "Support pause, step, reset and parameter changes without rebuilding the page.",
                ],
            },
            {
                "title": "Add interventions and comparison",
                "summary": "Interventions should change explicit parameters, not hidden constants.",
                "steps": [
                    "Add vaccination coverage and timing, masking effectiveness and school-closure windows.",
                    "Show every active intervention and its parameter values beside the charts.",
                    "Implement a classic SIR run with the same population size for comparison.",
                    "Let the user clone a run and change one assumption to see the difference.",
                ],
            },
            {
                "title": "Fit a small real dataset",
                "summary": "A model that cannot meet data is only a toy animation.",
                "steps": [
                    "Load a small public case-count series and align its dates with simulation days.",
                    "Fit one or two parameters with a simple grid or least-squares search and show the fit quality.",
                    "Display uncertainty by running several parameter sets and shading the outcome range.",
                    "Label the result as an educational model, not a forecast.",
                ],
            },
            {
                "title": "Validate assumptions and demo the trade-offs",
                "summary": "The resume story is honest modelling, including what the model cannot say.",
                "steps": [
                    "Add tests for deterministic runs with a fixed seed and for intervention parameter changes.",
                    "Check that the SIR comparison and network run use consistent population and time units.",
                    "Document the contact assumptions, fitting limits and uncertainty method in the README.",
                    "Record a demo that compares two networks and explains the peak difference.",
                ],
            },
        ],
    },
    "manabi-web-resume-018": {
        "description": (
            "The complete lab draws a one-dimensional potential barrier or well, "
            "launches a wave packet and solves the time-dependent Schrodinger "
            "equation on a configurable grid. It shows probability density and "
            "the real and imaginary parts of the wave function, then compares "
            "measured transmission with the analytic rectangular-barrier result.\n\n"
            "Finish with a stable numerical scheme, visible grid and time-step "
            "controls, WASM or GPU acceleration and a validation panel that shows "
            "when the approximation leaves tolerance. The demo should show a "
            "wave packet partially tunneling, reflect, and explain the effect of "
            "barrier width and energy."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You built a real-time scientific visualization with performance constraints."},
            {"role": "Web performance engineer", "how_it_helps": "WASM or GPU compute for a numerical solver is a strong performance story."},
            {"role": "Scientific software engineer", "how_it_helps": "You can discuss numerical stability, validation and approximation limits."},
        ],
        "build_guide": [
            {
                "title": "Choose the numerical scheme",
                "summary": "Stability and boundary conditions decide whether the animation means anything.",
                "steps": [
                    "Pick a time-dependent 1D solver approach and document its stability condition.",
                    "Define the grid, time step, spatial domain and absorbing boundaries.",
                    "Implement a Gaussian wave packet initial state and normalize it.",
                    "Write a small command-line or test harness that prints total probability over time.",
                ],
            },
            {
                "title": "Implement the solver core",
                "summary": "Get a correct numerical result before building the visual layer.",
                "steps": [
                    "Implement the update step for the chosen scheme with real and imaginary components kept separate.",
                    "Add a potential barrier and well that can be changed without recompiling the core.",
                    "Track probability conservation and warn when it drifts beyond a threshold.",
                    "Test the free-particle case and a rectangular barrier against known behavior.",
                ],
            },
            {
                "title": "Move compute to WASM or the GPU",
                "summary": "A smooth animation is part of the teaching value.",
                "steps": [
                    "Profile the plain JavaScript solver and identify the update loop as the bottleneck.",
                    "Move the update loop to WebAssembly or a GPU shader and copy only the visible field back to the UI.",
                    "Keep the grid size and time step user-configurable, with a warning for unstable combinations.",
                    "Add a fallback path for browsers without the accelerated backend.",
                ],
            },
            {
                "title": "Build the interactive lab",
                "summary": "The user should change the experiment and understand the response.",
                "steps": [
                    "Render probability density and the real and imaginary parts with a clear legend and axis labels.",
                    "Add controls for barrier height, width, packet energy and initial position.",
                    "Add play, pause, step and reset controls, plus a live time readout.",
                    "Show transmission and reflection measurements from the simulated field.",
                ],
            },
            {
                "title": "Validate against the analytic result",
                "summary": "The tolerance panel is what separates a lab from a demo.",
                "steps": [
                    "Compute analytic transmission for a rectangular barrier and compare it with the measured simulation result.",
                    "Show the difference, the tolerance and a warning when the grid is too coarse.",
                    "Test probability conservation and a few barrier widths, and document the error trend.",
                    "Record a demo that changes barrier width and explains the tunneling change.",
                ],
            },
        ],
    },
    "manabi-web-resume-019": {
        "description": (
            "The complete project is a small React-like library with element "
            "creation, a virtual DOM, keyed reconciliation, function components, "
            "state and effect hooks, a scheduler and a small event system. A demo "
            "app exercises list reordering, conditional rendering, effects and "
            "state updates against the library.\n\n"
            "Finish with focused tests for each layer, a benchmark against React "
            "for mount and keyed-list updates, and a short design note that "
            "explains the differences from React. The strongest demo opens a "
            "debug view showing the work loop, the previous and next trees and "
            "the exact nodes reused during a keyed update."
        ),
        "target_roles": [
            {"role": "Frontend engineer", "how_it_helps": "You can explain rendering, reconciliation and hook semantics from implementation experience."},
            {"role": "UI platform engineer", "how_it_helps": "A small renderer, scheduler and effect system are the core of UI platform work."},
            {"role": "Full-stack engineer", "how_it_helps": "The project shows deep client-side architecture and test discipline."},
        ],
        "build_guide": [
            {
                "title": "Build elements and the first renderer",
                "summary": "Start with a tree that renders once before adding updates.",
                "steps": [
                    "Define the element shape and a createElement helper with props and children.",
                    "Write the DOM renderer for host elements, text nodes, fragments and basic props.",
                    "Add tests for nested children, null children, attributes and event listeners.",
                    "Build a static demo page that renders through the library only.",
                ],
            },
            {
                "title": "Add reconciliation and keys",
                "summary": "The update path is the project; a single render is not enough.",
                "steps": [
                    "Implement a diff that compares previous and next element trees and patches the DOM.",
                    "Add keyed child reconciliation and tests for insert, remove, reorder and replace.",
                    "Handle component boundaries and props changes without remounting every subtree.",
                    "Build a debug panel that shows the previous tree, next tree and reused nodes.",
                ],
            },
            {
                "title": "Add function components, hooks and scheduling",
                "summary": "State and effects need a defined order and a work loop.",
                "steps": [
                    "Implement function components and component instances with stable hook slots.",
                    "Add useState with queued updates and a scheduler that batches work.",
                    "Add useEffect with dependency checks, cleanup and a defined run order.",
                    "Test re-renders, conditional hooks, cleanup and state updates inside effects.",
                ],
            },
            {
                "title": "Add events and the demo app",
                "summary": "A library becomes believable when a real app runs on it.",
                "steps": [
                    "Implement event wiring and cleanup for the supported event types.",
                    "Build a demo with a keyed list, a form, conditional panels and an effect that syncs a document title.",
                    "Add a stress control that inserts, moves and removes many rows.",
                    "Compare the observable behavior with the same demo written in React.",
                ],
            },
            {
                "title": "Benchmark, document and explain",
                "summary": "The resume claim is understanding, not replacing React.",
                "steps": [
                    "Benchmark initial mount and a 1,000-row keyed reorder against React under the same conditions.",
                    "Document where the library differs from React and which guarantees it does not provide.",
                    "Write a design note on the scheduler, reconciliation and hooks.",
                    "Record a demo of the debugger showing a keyed update and one effect cleanup.",
                ],
            },
        ],
    },
    "manabi-web-resume-020": {
        "description": (
            "The finished project implements a real Git subset: content-addressed "
            "blobs, trees and commits with SHA-1 hashes, a staging index, commit, "
            "log, branch and checkout, line diff and a three-way merge with "
            "conflict markers. A small web view reads the object store and draws "
            "the commit graph and the object changes behind each command.\n\n"
            "Finish with compatibility tests that read repositories created by "
            "real Git, a merge-base fixture and a clear explanation of what the "
            "implementation does not support. The demo should create a commit, "
            "switch branches, merge a clean change and then show a conflicting "
            "merge with base, ours and theirs in the web view."
        ),
        "target_roles": [
            {"role": "Backend engineer", "how_it_helps": "Content-addressed storage, object graphs and merge logic are strong systems fundamentals."},
            {"role": "Developer tools engineer", "how_it_helps": "Git internals and command behavior are directly relevant to tooling work."},
            {"role": "Full-stack engineer", "how_it_helps": "You built the core engine and a web view that makes it inspectable."},
        ],
        "build_guide": [
            {
                "title": "Build the object store",
                "summary": "Everything else depends on getting blobs, trees and commits exactly right.",
                "steps": [
                    "Implement blob, tree and commit writing with the real object header, SHA-1 hash and zlib compression.",
                    "Implement object reading and walking, including nested trees and commit parents.",
                    "Add tests that read objects written by real Git and verify the hashes match.",
                    "Expose a small debug command that prints the object type, hash and content ladder.",
                ],
            },
            {
                "title": "Add the index and core commands",
                "summary": "The index is the bridge between the working tree and a commit.",
                "steps": [
                    "Implement index add, remove and status with file mode, path, size and hash entries.",
                    "Implement commit, log and branch creation on top of the object store.",
                    "Add checkout for a branch or commit, including restoring and removing files from the working tree.",
                    "Test add, commit, log, branch and checkout against a simple real repository.",
                ],
            },
            {
                "title": "Add diff and three-way merge",
                "summary": "The merge path is the hardest and most valuable part.",
                "steps": [
                    "Implement line diff between two blobs with a stable output format.",
                    "Find the merge base by walking commit parents and implement three-way file merge for the base, ours and theirs.",
                    "Write conflict markers when both sides change the same region, and keep clean changes automatic.",
                    "Add fixtures for clean merge, conflict, delete-vs-edit and add-vs-add cases.",
                ],
            },
            {
                "title": "Build the web inspection view",
                "summary": "The web page should explain the object graph, not just print logs.",
                "steps": [
                    "Read the repository and expose commits, parents, trees and refs to the web view.",
                    "Draw the commit graph with branch labels and highlight the selected commit.",
                    "For each commit, show the tree diff and the object hashes behind the changed files.",
                    "Add a merge view that shows base, ours, theirs and the resulting conflict markers.",
                ],
            },
            {
                "title": "Prove compatibility and document limits",
                "summary": "Real Git compatibility is the strongest evidence for this project.",
                "steps": [
                    "Clone or create a small repository with real Git and run your reader against it.",
                    "Compare your log, diff and merge output with Git for the same fixture and document intentional differences.",
                    "Write the supported command matrix and unsupported features in the README.",
                    "Record a demo showing a clean merge and a conflicting merge in the web view.",
                ],
            },
        ],
    },
}
