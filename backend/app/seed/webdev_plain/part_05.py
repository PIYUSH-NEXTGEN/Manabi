"""Plain-language overrides for web-dev hackathon briefs 001 to 006."""

OVERRIDES = {
    "manabi-web-hackathon-001": {
        "summary": (
            "Build a mobile web app for field teams who work without internet. "
            "They can fill forms, add photos and mark GPS points offline, then "
            "sync when the connection returns.\n\n"
            "Two people may edit the same record. The app keeps both versions, "
            "flags the conflict and asks the user to merge field by field. "
            "Nothing gets silently overwritten."
        ),
        "who_affected": (
            "Field survey teams, NGO data collectors and inspection crews who "
            "work in places with poor connectivity."
        ),
        "why_matters": (
            "Lost forms and quiet overwrites waste field time and make people "
            "stop trusting the data."
        ),
        "approaches": [
            "Cache the app shell with a service worker and keep drafts, photos and GPS points in IndexedDB.",
            "Put writes in an outbox with idempotency keys, retry with backoff and show failed uploads.",
            "Version each record and keep a change log so the server can spot conflicting edits.",
            "Give users a field-by-field merge screen instead of resolving conflicts with last write wins.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Field data stops disappearing when the network does, and "
                "conflicting edits become a decision instead of a silent overwrite."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "Ask the judges how many forms their last field survey lost "
                        "to bad connectivity. This app is the answer to that question."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Field teams work where Wi-Fi dies. Paper gets lost, photos "
                        "sit in camera rolls, and last-write-wins sync quietly throws "
                        "away someone's visit."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "An offline-first PWA keeps drafts, photos and GPS in "
                        "IndexedDB. A versioned record and a queued outbox sync when "
                        "the network returns. If two workers edit the same record, "
                        "the app shows both versions and asks for a merge."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Put the laptop in airplane mode, create a record, reload, "
                        "edit from a second profile, reconnect and resolve the "
                        "conflict. Then show the queue status and a safe retry."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Background sync, photo compression, a map review screen and "
                        "per-field conflict rules so low-risk data needs less human "
                        "attention."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Why not use localStorage?",
                    "answer": (
                        "Photos, GPS points and a queued outbox need blobs and bigger "
                        "records. localStorage is synchronous, string-only and too "
                        "small. IndexedDB handles async access without blocking the UI."
                    ),
                },
                {
                    "question": "Why not let the last write win?",
                    "answer": (
                        "For field data, an overwritten visit can waste a trip and "
                        "break trust. We detect concurrent versions and ask the user "
                        "to merge. We only default on fields where losing data is "
                        "acceptable."
                    ),
                },
                {
                    "question": "How do you stop retries from duplicating records?",
                    "answer": (
                        "Every queued write carries a client-generated idempotency "
                        "key. The server stores the key with the result and returns "
                        "the same response for a repeat attempt."
                    ),
                },
                {
                    "question": "What happens if the server rejects a sync hours later?",
                    "answer": (
                        "The record moves to a failed state with the server's reason "
                        "and stays in the outbox. The user can fix it, retry, or "
                        "export it instead of losing the work."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Define the record contract and offline shell",
                "summary": (
                    "Start with the data that must survive a dead network, then make "
                    "the app shell load without one."
                ),
                "steps": [
                    "Write one form schema with text, number, date, photo and GPS fields. Decide what a record version means before writing sync code.",
                    "Create the React app shell, routes and empty states. Add a service worker that precaches the shell and a visible online/offline indicator.",
                    "Design the IndexedDB stores: records, drafts, outbox entries, photo blobs and sync errors. Keep the outbox separate from the record table.",
                    "Seed two sample workers and a shared record so you can reproduce concurrent edits from two browser profiles.",
                ],
            },
            {
                "title": "Build the local-first record flow",
                "summary": (
                    "Every user action writes locally first. The network is an "
                    "optional background step."
                ),
                "steps": [
                    "Build the form editor with autosave, validation and a draft list. Save photo blobs and GPS coordinates without blocking the UI.",
                    "Add an outbox write on every save: record id, base version, changed fields, timestamp and a client-generated idempotency key.",
                    "Build the sync worker with online/offline listeners, exponential backoff and a manual retry button. Show queued, syncing, failed and conflict states.",
                    "Add a record history view that reads the local change log so the field worker can see what changed and when.",
                ],
            },
            {
                "title": "Build the sync API and conflict protocol",
                "summary": (
                    "The server must reject stale writes on purpose and make "
                    "repeated requests safe."
                ),
                "steps": [
                    "Create the records and changes tables with a version column and a unique idempotency key per write.",
                    "On write, compare the client base version with the current server version. Return 409 with both field values and the change history when they differ.",
                    "Store the idempotency key with the result so a retried request returns the same response instead of creating a duplicate.",
                    "Add endpoints for pulling updates after a cursor and for submitting a resolved merge with the next version.",
                ],
            },
            {
                "title": "Build the merge and status screens",
                "summary": (
                    "The conflict screen is the product. It must keep both versions "
                    "visible and make the choice easy to follow."
                ),
                "steps": [
                    "List every conflicting field with mine, theirs, base and a per-field choice. Show who changed it and when beside each value.",
                    "Preview the merged record before saving. Disable submit until every conflict has a choice or an explicit keep-both resolution.",
                    "Build an outbox screen that groups records by queued, syncing, failed and conflict, with a retry action for failed items.",
                    "Add an airplane-mode demo page with clear instructions so a reviewer can reproduce the flow in two minutes.",
                ],
            },
            {
                "title": "Harden, test and document the demo",
                "summary": (
                    "Offline apps fail in the seams. Test reconnects, duplicate "
                    "uploads and partial photo transfers."
                ),
                "steps": [
                    "Add tests for idempotent retries, stale-version conflicts, merge submission and service-worker cache updates.",
                    "Throttle the network in DevTools and check that a failed photo upload does not block the text record from syncing.",
                    "Write a README with the sync contract, IndexedDB schema, conflict rules, local setup and a short demo script.",
                    "Record a short walkthrough that shows offline creation, reload, reconnect and conflict resolution. Link it from the repo.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-002": {
        "summary": (
            "Build a public site where residents report local problems like "
            "potholes, broken streetlights or missed garbage pickup. Each report "
            "has a photo and a location, and similar reports are grouped so staff "
            "see one real issue instead of many duplicates.\n\n"
            "Staff can assign the issue, track a service deadline and update its "
            "status. The interesting part is grouping reports without hiding "
            "mistakes, since staff can merge and split at any time."
        ),
        "who_affected": (
            "Residents who report local problems, municipal staff who handle "
            "complaints and ward offices that track service levels."
        ),
        "why_matters": (
            "Duplicate reports hide the real backlog, and missed deadlines turn "
            "small civic problems into long-running complaints."
        ),
        "approaches": [
            "Store reports with location, category, photo and a status history.",
            "Propose duplicate candidates from nearby location buckets plus text similarity.",
            "Assign departments with configurable category rules and start an SLA timer.",
            "Give staff a merge, split and moderation view so they can fix bad grouping.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Every civic complaint becomes one tracked issue, so residents can "
                "see progress and staff can see the real backlog."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A pothole gets reported three times, fixed once, and closes "
                        "as three separate tickets. The reporting system is failing "
                        "both sides."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Residents call or email and never hear back. Staff retype "
                        "the same complaint and cannot tell whether two reports are "
                        "the same problem."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "A resident submits a photo and pin. We bucket by location, "
                        "compare text similarity and show likely duplicates before "
                        "another ticket is created. Staff get one queue, categories, "
                        "owners and an SLA clock. Residents get a public status page."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "File a streetlight report, file a near-duplicate and show "
                        "the merge prompt. Then switch to staff view, move the issue "
                        "to in progress and resolved, and refresh the resident page "
                        "to show the timeline."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Ward-based assignment, escalation for overdue SLAs, "
                        "learning from duplicate feedback and an open export of "
                        "resolved issues."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How accurate is duplicate detection?",
                    "answer": (
                        "It starts as a candidate system, not an automatic merge. "
                        "Location plus text similarity gives high recall, and staff "
                        "make the final call. We tune the threshold with a small "
                        "labelled set."
                    ),
                },
                {
                    "question": "How do you avoid merging two different problems nearby?",
                    "answer": (
                        "We show a confidence score, category, photo and distance "
                        "before merging. A false merge is reversible with a split "
                        "action, and the audit trail keeps both original reports."
                    ),
                },
                {
                    "question": "What does the public page hide?",
                    "answer": (
                        "Reporter contact details are never public. The public sees "
                        "the category, status, timestamps and location at a level "
                        "coarse enough to avoid exposing a home address."
                    ),
                },
                {
                    "question": "Why would a municipal office adopt it?",
                    "answer": (
                        "It replaces a phone-and-paper log with a queue staff can "
                        "actually run. The first version needs only a browser and a "
                        "small set of categories."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Model reports, issues and service levels",
                "summary": (
                    "Keep a resident report separate from the issue staff work on. "
                    "That split makes duplicate handling possible."
                ),
                "steps": [
                    "Define report, issue, status event, department, category and SLA policy records. A report can point at one issue and an issue can have many reports.",
                    "Store a rough location for public views and precise coordinates for staff. Write down what leaves the building.",
                    "Write the status transition table: open, triaged, assigned, in progress, paused, resolved and reopened. Record who changed it, when and why.",
                    "Seed three wards, five categories, department routing rules and a small set of duplicate and non-duplicate reports.",
                ],
            },
            {
                "title": "Build intake and duplicate candidates",
                "summary": (
                    "Take reports quickly, then score possible duplicates without "
                    "merging them behind the user's back."
                ),
                "steps": [
                    "Build the resident form with photo upload, category hints and browser geolocation. Allow a rough location when GPS is denied.",
                    "Bucket nearby reports by rounded coordinates and compare descriptions with a simple text similarity score.",
                    "Show the top candidates to staff with distance, time gap and score. Never auto-merge without a visible confirmation step.",
                    "Add a labelled evaluation file so threshold changes can be checked against known duplicate and distinct pairs.",
                ],
            },
            {
                "title": "Build the staff workflow and SLA clock",
                "summary": (
                    "Staff need a fast queue, an audit trail and a deadline that "
                    "recalculates from real events."
                ),
                "steps": [
                    "Create the staff queue with filters for ward, category, department, status and SLA risk.",
                    "Implement merge and split actions that move reports between issues without deleting either report or its history.",
                    "Compute the SLA deadline from stored status events. Pause on waiting states and escalate when remaining time crosses a threshold.",
                    "Add a moderation action for abusive or invalid reports, with a reason that appears in the audit log.",
                ],
            },
            {
                "title": "Build the public status experience",
                "summary": (
                    "The public page should prove progress without turning "
                    "residents into a target for harassment."
                ),
                "steps": [
                    "Publish a map and list that show category, rough area, status and resolution time while hiding names, contacts and exact addresses.",
                    "Show a resolved-this-month summary by ward with average time to resolution and the number of open issues.",
                    "Make the public page read from a projection that holds only public fields, not from the staff table with hidden columns.",
                    "Add a simple report lookup by reference code so a resident can follow their own issue without an account.",
                ],
            },
            {
                "title": "Test corrections, privacy and the demo",
                "summary": (
                    "The correction path is what makes duplicate detection "
                    "trustworthy."
                ),
                "steps": [
                    "Test a false merge and a false split, including the audit entries and the public counts after each correction.",
                    "Add SLA tests for pause, resume, breach and overnight or weekend boundaries.",
                    "Review every public API response for leaked personal data and add a test that fails if a private field appears.",
                    "Write an operator guide and a demo script covering intake, duplicate merge, correction, resolution and the public report.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-003": {
        "summary": (
            "Build a platform where people swap skills instead of money. Each "
            "person lists what they can teach and what they want to learn, and the "
            "app finds a fair match, schedules a session and collects feedback "
            "afterwards.\n\n"
            "Direct two-way swaps come first. A small three-way swap search "
            "handles cases where no pair exists. Every match must explain who "
            "teaches what to whom."
        ),
        "who_affected": (
            "Students, hobbyists, freelancers and community groups who want to "
            "learn a practical skill without paying for a course."
        ),
        "why_matters": (
            "Useful knowledge is spread unevenly, and money or formal courses "
            "block many learners. A trusted exchange turns idle teaching time into "
            "real learning."
        ),
        "approaches": [
            "Model each person as a set of offered and wanted skills with a level and availability.",
            "Find two-way swaps first, then run a bounded search for three-way cycles.",
            "Explain every match with the exact skills exchanged and why both people fit.",
            "Add request, accept, decline, scheduling, completion, rating, report and block flows, with request limits and duplicate suppression.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Skill exchange turns unused knowledge into a structured swap, "
                "with a clear match explanation instead of a group-chat maybe."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "Everyone knows something someone nearby wants to learn. "
                        "The problem is finding that person without paying for a "
                        "course or spamming a group chat."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Informal skill barter runs on memory and luck. Direct swaps "
                        "are hard enough, and a three-person cycle is almost "
                        "impossible to coordinate by hand."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "People list skills they can teach and want to learn. We "
                        "find reciprocal pairs first, then search a bounded graph "
                        "for three-way cycles. Every match explains who teaches "
                        "what to whom. Request, schedule, rating and report flows "
                        "keep it safe."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Show two seeded profiles with an obvious pair, open the "
                        "explanation, accept the request and schedule a session. "
                        "Then switch to the three-way cycle and show why no pair "
                        "existed."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Skill verification, group exchanges, calendar integrations "
                        "and a reputation system that is harder to game."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Why find three-way cycles at all?",
                    "answer": (
                        "Many communities have useful knowledge but no direct "
                        "two-way overlap. A bounded cycle search turns three people "
                        "who each have something the next wants into one viable "
                        "exchange."
                    ),
                },
                {
                    "question": "How do you stop the matching graph from becoming spam?",
                    "answer": (
                        "Outgoing requests are rate-limited, duplicate matches are "
                        "hidden, blocking removes future candidates, and a declined "
                        "request cannot be retried right away."
                    ),
                },
                {
                    "question": "What stops someone from claiming a skill they do not have?",
                    "answer": (
                        "The MVP uses ratings, completion confirmations and reports. "
                        "Verification comes later, and we say plainly that "
                        "reputation is earned through completed exchanges."
                    ),
                },
                {
                    "question": "How do you solve the cold-start problem?",
                    "answer": (
                        "The graph needs density, so we would launch with a class, "
                        "campus or community rather than a whole city. We would "
                        "seed it through existing groups."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Model the exchange before writing UI",
                "summary": (
                    "The match is the product. Get the skills graph and the request "
                    "lifecycle right first."
                ),
                "steps": [
                    "Define profile, offered skill, wanted skill, availability and request states on paper.",
                    "Decide how proficiency and preferred format, online or in person, affect a match.",
                    "Write the allowed request transitions: pending, accepted, declined, completed and cancelled.",
                    "List the safety rules: report, block, contact limits and what is shown publicly.",
                ],
            },
            {
                "title": "Build the skill graph",
                "summary": (
                    "A small realistic graph is enough to prove the matching idea."
                ),
                "steps": [
                    "Create profile and skill tables with a normalized skill name and a free-text note.",
                    "Build profile editing and a searchable list of offered skills.",
                    "Seed 20-30 profiles containing a deliberate two-way pair and one three-way cycle.",
                    "Write queries that list candidates for a person, with the direction of each skill edge.",
                ],
            },
            {
                "title": "Match, rank and explain",
                "summary": (
                    "A match without an explanation looks like random luck and will "
                    "not be trusted."
                ),
                "steps": [
                    "Implement direct pair matching by intersecting wanted and offered skills.",
                    "Add a depth-limited cycle search for three-person exchanges.",
                    "Score matches with skill overlap, availability overlap and a reciprocity signal.",
                    "Show a match card that spells out who teaches what to whom and why it qualified.",
                ],
            },
            {
                "title": "Requests, sessions and trust",
                "summary": (
                    "The exchange has to survive acceptance, scheduling and a bad "
                    "experience."
                ),
                "steps": [
                    "Implement request accept or decline, with duplicate and spam suppression.",
                    "Add session scheduling with time zones, reminders and a completion confirmation.",
                    "Add ratings and a private report flow. Make blocking remove future matches.",
                    "Rate-limit outgoing requests and test that declining does not create a loop.",
                ],
            },
            {
                "title": "Make the demo obvious",
                "summary": "Show a pair and a cycle, not a profile page.",
                "steps": [
                    "Seed one obvious two-way match and one three-way cycle with readable names.",
                    "Rehearse the path from editing skills to an explained match and an accepted session.",
                    "Test the empty and no-match states so the demo never shows a blank screen.",
                    "Capture screenshots of the match explanations for the pitch deck.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-004": {
        "summary": (
            "Build a search tool that helps new developers find a good first "
            "open-source issue. It filters GitHub issues by language and topic, "
            "then explains why a repository is beginner-friendly.\n\n"
            "Rankings use signals like recent activity, a contribution guide and "
            "how quickly maintainers respond. Every score shows the reason behind "
            "it, and users can save issues and track their own progress."
        ),
        "who_affected": (
            "New contributors looking for a first pull request, maintainers who "
            "label beginner issues and bootcamp mentors."
        ),
        "why_matters": (
            "A welcoming issue list turns curiosity into a merged pull request. A "
            "bad pick wastes days and discourages new contributors."
        ),
        "approaches": [
            "Search GitHub issues by label, language and recency, then fetch repository metadata in batches.",
            "Cache API responses with ETags and show when cached data was last refreshed.",
            "Rank repositories with explainable signals: activity, contributing guide, response time and issue turnover.",
            "Let users save issues and track their own contribution progress.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A first pull request should be a fit, not a guess, so we rank "
                "issues by how welcoming the repository actually looks."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "The first open-source issue someone picks is often why they "
                        "never contribute again."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "GitHub search can find issue labels, but it does not tell a "
                        "newcomer whether maintainers respond, whether the "
                        "repository is active, or whether the issue is still a good "
                        "fit."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We pull beginner-friendly issues, cache them and rank "
                        "repositories by maintainer response time, contributing "
                        "guide, recent activity and language fit. Users can save "
                        "issues and track progress from first look to merged pull "
                        "request."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Filter to a language and topic, compare two issue cards, "
                        "save one and mark it in progress. Show the cached state "
                        "when the API is unavailable."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Personalised recommendations from a contributor's history, "
                        "maintainer-side issue quality checks and contribution "
                        "outcome tracking."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you stay inside GitHub rate limits?",
                    "answer": (
                        "We cache repository and issue responses, batch requests "
                        "and serve stale but labelled data when the limit is close. "
                        "The demo runs from the cache."
                    ),
                },
                {
                    "question": "Can repositories game the welcomeness score?",
                    "answer": (
                        "Any public score can be gamed. We show the signals behind "
                        "the rank, keep the formula transparent and would use "
                        "outcome data, not labels alone, to tune it."
                    ),
                },
                {
                    "question": "Why not use GitHub search?",
                    "answer": (
                        "Search gives a list, not a recommendation. We add response "
                        "behaviour, activity, contributor guidance and a saved "
                        "progress path that GitHub does not give newcomers."
                    ),
                },
                {
                    "question": "How do you know an issue is still open and suitable?",
                    "answer": (
                        "We check freshness and cached status, show the last update "
                        "and link to the live issue. Stale results are labelled "
                        "rather than quietly recommended."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Design the search and ranking contract",
                "summary": (
                    "Decide what a good first contribution means before you call "
                    "the API."
                ),
                "steps": [
                    "List the signals you will show: recent commit activity, issue response time, contributing guide, label quality and stars. Give each a clear input and weight.",
                    "Define the result shape: issue, repository, language, labels, last activity, score and the signal breakdown.",
                    "Write down the empty, rate-limited and stale-cache states so the UI does not treat them as success.",
                    "Create a small evaluation sheet with 15-20 repositories you have actually inspected and a note on whether each was welcoming.",
                ],
            },
            {
                "title": "Build the GitHub client and cache",
                "summary": (
                    "The wrapper must respect pagination, rate limits and "
                    "conditional requests."
                ),
                "steps": [
                    "Implement search and repository lookup calls with pagination and a server-side token. Keep the token out of the browser.",
                    "Cache responses with ETags and a fetched-at timestamp. Serve cached data with an age label when the API refuses or rate-limits.",
                    "Batch repository metadata fetches instead of one request per card. Store only the fields the ranking and UI need.",
                    "Add backoff and a clear error object for unauthorized, rate-limited and partial-response cases.",
                ],
            },
            {
                "title": "Implement explainable ranking",
                "summary": (
                    "Every score should be rebuildable from inputs the user can see."
                ),
                "steps": [
                    "Compute each signal separately and normalize it against the current result set or a documented range.",
                    "Combine the signals into one score, then render a breakdown with the raw value and the points contributed.",
                    "Add filters for language, label, minimum stars, recent activity and repository age.",
                    "Run the ranking against your evaluation sheet, adjust weights and write down what changed.",
                ],
            },
            {
                "title": "Build search, saved issues and progress",
                "summary": (
                    "The user needs a path from curiosity to a first pull request."
                ),
                "steps": [
                    "Build the search page with URL-synced filters, result pagination and a cache-age banner.",
                    "Add a repository detail panel with score inputs, contributing-guide status and direct links to the issue and repository.",
                    "Implement save, hide and progress states. Persist them per user and show a simple saved-issues board.",
                    "Add an empty state that suggests removing a narrow filter instead of showing a blank page.",
                ],
            },
            {
                "title": "Evaluate, document and demo",
                "summary": (
                    "The ranking is the claim and the evaluation is the evidence."
                ),
                "steps": [
                    "Add tests for cache hits, rate-limit fallback, filter combinations and pipeline transitions.",
                    "Write a short evaluation note with the repositories inspected, the false positives and the final thresholds.",
                    "Document the API limits, caching policy and how to run the app with a personal token locally.",
                    "Record a demo that searches, explains a score, saves an issue and moves it to pull-request-opened.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-005": {
        "summary": (
            "Build a shared board where disaster responders and community members "
            "post needs and offers for food, water, shelter, medical help or "
            "transport. The app matches nearby needs with offers and keeps a clear "
            "record of what was delivered.\n\n"
            "It should still work when the network drops, and contact details "
            "should only be visible to the people who need them. The board is a "
            "coordination record, not a social feed."
        ),
        "who_affected": (
            "Disaster response coordinators, relief volunteers and affected "
            "communities posting urgent needs."
        ),
        "why_matters": (
            "During a response, duplicate requests and slow matching leave "
            "resources idle while people wait."
        ),
        "approaches": [
            "Model needs and offers with location, quantity, contact visibility and fulfilment state.",
            "Match nearby complementary records with distance and category rules.",
            "Keep a live board over WebSockets and queue offline edits in the browser.",
            "Send an SMS or WhatsApp fallback when a coordinator cannot stay online.",
        ],
        "pitch_guide": {
            "one_liner": (
                "During a response, needs and nearby resources find each other on "
                "one shared map instead of five chat threads."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "In a disaster, supplies often sit in one place while the "
                        "need is two streets away because nobody has the same "
                        "picture."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Needs arrive through calls, chats and paper lists. Offers "
                        "arrive somewhere else. Duplicates waste effort, and a "
                        "disconnected responder cannot see the latest state."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Responders and community members post needs or offers on a "
                        "live map. We match nearby categories, show fulfilment state "
                        "and keep a PWA queue for weak connections. An SMS or "
                        "WhatsApp message acts as a fallback."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Post a water need, show nearby offers, accept one and mark "
                        "it fulfilled. Then switch the network off, queue another "
                        "post, reconnect and show the fallback message."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Verified organization accounts, transport capacity, "
                        "duplicate clustering and exports for incident commands."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you prevent duplicate or fake needs?",
                    "answer": (
                        "Posts have a location, category, contact and visible state. "
                        "Nearby similar posts are surfaced before submission, and "
                        "organization verification or a responder review can raise "
                        "trust."
                    ),
                },
                {
                    "question": "What works when the connection is poor?",
                    "answer": (
                        "The app shell and current map data are cached, new posts "
                        "enter an outbox, and the user sees queued or failed states. "
                        "SMS or WhatsApp is a deliberate fallback, not a hidden "
                        "promise."
                    ),
                },
                {
                    "question": "Why not use a WhatsApp group?",
                    "answer": (
                        "A group is good for conversation but poor for matching, "
                        "deduplication and fulfilment state. We can hand off to "
                        "WhatsApp for reach while the operational record stays on "
                        "the map."
                    ),
                },
                {
                    "question": "How do you avoid exposing vulnerable people?",
                    "answer": (
                        "Locations can be coarsened and contact details are opt-in. "
                        "Public views avoid identifying individuals, and sensitive "
                        "needs can be visible only to verified responders."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Model needs, offers and response roles",
                "summary": (
                    "A disaster board is a coordination record, not a social feed."
                ),
                "steps": [
                    "Define need, offer, match, delivery event and contact-reveal records with category, quantity, location and status.",
                    "Choose the role model: public viewer, field worker and coordinator. Write down which role can create, match, reveal contact details and close an item.",
                    "Separate public fields from coordinator-only fields at the query layer, not with a hidden field in the UI.",
                    "Seed a realistic response scenario with food, water, shelter, medical and transport records across a few neighbourhoods.",
                ],
            },
            {
                "title": "Build the live board and match flow",
                "summary": (
                    "The board must update for everyone and every match must leave "
                    "a trail."
                ),
                "steps": [
                    "Build the map and list views with category filters, status badges and a clear stale-data indicator.",
                    "Add WebSocket updates for create, update, match and fulfil events. Fall back to polling when the socket cannot connect.",
                    "Implement proximity and category matching that suggests complementary needs and offers, with distance and quantity shown.",
                    "Record proposed, accepted, picked up and delivered events with actor, timestamp and note. Never reduce the trail to one status field.",
                ],
            },
            {
                "title": "Add offline queue and fallback messaging",
                "summary": (
                    "Connectivity is a feature state, not an error page."
                ),
                "steps": [
                    "Queue board edits and match updates in the browser when offline and replay them with idempotency keys on reconnect.",
                    "Keep the last known board snapshot available and label its age so coordinators do not treat old data as live.",
                    "Generate a compact SMS or WhatsApp message for a match or urgent need, with an item reference and a short status line.",
                    "Test on a throttled connection: drop the socket, make an edit, reconnect and confirm the board reconciles.",
                ],
            },
            {
                "title": "Build privacy, verification and exports",
                "summary": (
                    "Contact data and offer quality need explicit controls."
                ),
                "steps": [
                    "Log every contact-detail reveal with the coordinator, item and time. Show the log to admins.",
                    "Add a simple offer verification state and a note field. Keep unverified offers visible but clearly marked.",
                    "Build a daily export with open needs, unmatched offers, active matches and completed deliveries.",
                    "Add an admin view for duplicate clusters so coordinators can link two reports without deleting either one.",
                ],
            },
            {
                "title": "Run a drill, test failures and document it",
                "summary": (
                    "The project is credible only if it works under a realistic "
                    "failure."
                ),
                "steps": [
                    "Write tests for role permissions, contact visibility, match transitions and offline replay.",
                    "Run a two-browser drill: create a need, match an offer, disconnect one browser, complete delivery, then reconnect.",
                    "Check the daily export against the board after the drill and reconcile any mismatch.",
                    "Document setup, the fallback message format, the drill script and the privacy model in the README.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-006": {
        "summary": (
            "Build a guided tool that helps a small business prepare its first "
            "export. The user picks a product and a country, and the app shows a "
            "checklist of documents, rules and duties.\n\n"
            "Every item links to an official source and shows the date it was last "
            "checked. A source-grounded chat can answer questions, but only from "
            "the selected passages, and it says when it does not know."
        ),
        "who_affected": (
            "Small exporters, trade consultants and small-business owners checking "
            "requirements before a first shipment."
        ),
        "why_matters": (
            "One missing document or duty can stop a shipment, and scattered "
            "unofficial advice makes a first export expensive and risky."
        ),
        "approaches": [
            "Model products, markets, documents and regulations as separate records with source links.",
            "Version each source with a last-checked date and show it beside the claim.",
            "Limit the chat assistant to retrieved source passages and require citations.",
            "Add a printable checklist and a clear not-legal-advice notice.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A small exporter gets a cited, dated checklist for one product "
                "and one country instead of scattered advice from five websites."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "One missing certificate can stop a shipment at the border "
                        "after the product, packaging and freight are already paid "
                        "for."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Export rules are spread across official portals, PDFs and "
                        "consultant advice. A small business cannot tell which "
                        "requirement is current or which source to trust."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Choose a product and a target country. We show a checklist "
                        "of documents, duties, regulations and market notes, each "
                        "tied to a source and a date. The assistant answers only "
                        "from those sources and says when it does not know."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Pick one product and country, open a requirement and its "
                        "official source, ask the assistant a supported question, "
                        "then ask something outside the sources and show the "
                        "refusal."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "More products and trade corridors, source freshness "
                        "monitoring, saved shipments and expert review workflows."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you keep regulations current?",
                    "answer": (
                        "Every item has an effective date and a source. The MVP "
                        "covers a deliberately small set and labels it as a "
                        "starting point. Freshness monitoring and review are the "
                        "next layer."
                    ),
                },
                {
                    "question": "How do you stop the chat from hallucinating?",
                    "answer": (
                        "The assistant is grounded in the selected checklist and "
                        "source snippets. If retrieval returns no support, it "
                        "refuses instead of making up legal advice."
                    ),
                },
                {
                    "question": "Who is liable if the checklist is wrong?",
                    "answer": (
                        "The product is an information aid, not legal advice. We "
                        "show sources and dates, ask users to review with an "
                        "official authority, and keep the disclaimer visible."
                    ),
                },
                {
                    "question": "Why only three products and three countries?",
                    "answer": (
                        "Depth beats breadth for trust. A narrow, well-cited demo "
                        "is more useful than a shallow database that looks "
                        "authoritative but cannot be checked."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Curate the source corpus and checklist model",
                "summary": (
                    "Three markets done properly beat thirty markets with claims "
                    "you cannot check."
                ),
                "steps": [
                    "Pick three products and three destination markets. Collect official documents, forms and tariff pages for each pair.",
                    "Define requirement, source, source-version, product, market and coverage records. Keep the checklist derived from those records.",
                    "Write a plain-language note for each requirement and mark the exact source passage that supports it.",
                    "Define the source review date and a rule for what happens when an item is past its review window.",
                ],
            },
            {
                "title": "Build the checklist engine and coverage view",
                "summary": (
                    "The checklist must be a query over structured rules, not a "
                    "hand-written page."
                ),
                "steps": [
                    "Implement product-country selection and generate a checklist grouped by documents, duties, labeling and market notes.",
                    "Show the source link, source date and plain-language note for every item. Add a printable view that keeps citations.",
                    "Build a coverage matrix that shows incomplete product-country pairs instead of hiding gaps.",
                    "Add a reviewer workflow to update a rule and see which checklist items changed.",
                ],
            },
            {
                "title": "Build grounded retrieval and citations",
                "summary": (
                    "The assistant is useful only when it can prove where an "
                    "answer came from."
                ),
                "steps": [
                    "Chunk the curated sources with stable ids and embed or index them for retrieval.",
                    "Retrieve passages for the question, pass only those passages to the model and require a citation id for each claim.",
                    "Return a refusal when retrieval is weak or the passages do not answer the question. Show the retrieved passages beside the answer.",
                    "Log the question, retrieved ids and refusal reason so failures can be reviewed.",
                ],
            },
            {
                "title": "Build the user-facing workflow",
                "summary": (
                    "The interface should guide a first exporter without pretending "
                    "to be a lawyer."
                ),
                "steps": [
                    "Create a short intake flow for product, destination and shipment context, then land on the generated checklist.",
                    "Add progress checkboxes, notes and a summary the user can share with a trade consultant.",
                    "Show the not-legal-advice notice beside the checklist and in the printable view, not buried in the footer.",
                    "Add source freshness warnings when any supporting item is past its review date.",
                ],
            },
            {
                "title": "Validate, document and demo",
                "summary": (
                    "Traceability is the resume claim, so show the evidence."
                ),
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
