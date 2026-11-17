"""Team plans and pitch kits for the 22 Web Dev hackathon briefs.

Each entry is keyed by the project number in ``webdev_projects.md``. The seed
composer combines these kits with either the existing resume brief or the new
hackathon-only brief, so campaign content stays separate from project facts.
"""


def _kit(*, note, roles, milestones, one_liner, beats, questions):
    return {
        "team_plan": {
            "note": note,
            "roles": [{"role": role, "covers": covers} for role, covers in roles],
            "milestones": milestones,
        },
        "pitch_guide": {
            "one_liner": one_liner,
            "beats": [{"heading": heading, "text": text} for heading, text in beats],
            "judge_questions": [
                {"question": question, "answer": answer}
                for question, answer in questions
            ],
        },
    }


KITS = {
    1: _kit(
        note=(
            "3 people, one long weekend. The sync path is the product, so protect "
            "it from feature creep and demo it in airplane mode."
        ),
        roles=[
            (
                "Sync and data",
                "IndexedDB schema, outbox, idempotency keys, record versions, and "
                "the conflict API. Owns the data contract everyone else uses.",
            ),
            (
                "Field app",
                "The form, camera and GPS capture, sync status, and the field-by-field "
                "merge screen. Optimizes for a phone with one hand.",
            ),
            (
                "Failure lab and demo",
                "Airplane-mode rehearsal, a second browser profile for conflicts, seed "
                "data, screenshots, and the pitch. Joins whoever is behind.",
            ),
        ],
        milestones=[
            "Hour 8: a form saves a draft and survives a page reload offline.",
            "Hour 16: queued records upload after reconnect without creating duplicates.",
            "Hour 24: two offline edits produce a visible conflict and a field-by-field merge.",
            "Hour 30: the full airplane-mode demo works twice in a row.",
        ],
        one_liner=(
            "Field data stops disappearing when the network does, and conflicting "
            "edits become a decision instead of a silent overwrite."
        ),
        beats=[
            (
                "Hook",
                "Ask the judges how many forms their last field survey lost to bad connectivity. We built the app that answers that question.",
            ),
            (
                "The problem",
                "Field teams work where Wi-Fi dies. Paper gets lost, photos sit in camera rolls, and last-write-wins sync silently throws away someone's visit.",
            ),
            (
                "Our solution",
                "An offline-first PWA stores drafts, photos, and GPS in IndexedDB. A versioned record and a queued outbox sync when the network returns. If two workers edit the same record, the app shows both versions and asks for a merge.",
            ),
            (
                "Live demo",
                "Put the laptop in airplane mode, create a record, reload, edit from a second profile, reconnect, and resolve the conflict. Then show the queue status and a safe retry.",
            ),
            (
                "What's next",
                "Background sync, photo compression, a map review screen, and conflict rules per field so low-risk data needs less human attention.",
            ),
        ],
        questions=[
            (
                "Why not just use localStorage?",
                "Photos, GPS points, and a queued outbox need blobs and larger records. localStorage is synchronous, string-only, and too small. IndexedDB handles async access without blocking the UI.",
            ),
            (
                "Why not let the last write win?",
                "For field data, an overwritten visit can waste a trip and destroy trust. We detect concurrent versions and ask the user to merge, only defaulting on fields where loss is acceptable.",
            ),
            (
                "How do you stop retries from duplicating records?",
                "Every queued write carries a client-generated idempotency key. The server stores the key with the result and returns the same response for a repeat attempt.",
            ),
            (
                "What happens if the server rejects a sync hours later?",
                "The record moves to a failed state with the server's reason and stays in the outbox. The user can fix it, retry, or export it instead of losing the work.",
            ),
        ],
    ),
    2: _kit(
        note=(
            "3 people, one weekend. Duplicate detection is the differentiator, but "
            "the public status page is what makes the demo understandable."
        ),
        roles=[
            (
                "Reports and dedupe",
                "Report table, photo and location storage, category rules, duplicate "
                "candidate query, and the service-level timer.",
            ),
            (
                "Resident and staff app",
                "Submit form with photo and map pin, public tracking page, staff "
                "queue, assignment, and merge or split controls.",
            ),
            (
                "Ops and demo",
                "Seed reports in several states, test false merges, prepare the pitch "
                "and screenshots, and keep the demo on the happy path.",
            ),
        ],
        milestones=[
            "Hour 8: a report with a photo and location is stored and has a public reference.",
            "Hour 16: nearby similar reports are grouped with a visible category and confidence.",
            "Hour 24: staff change status, the SLA clock updates, and the public page follows.",
            "Hour 30: merge and split work, and the full resident-to-resolution demo is rehearsed.",
        ],
        one_liner=(
            "Every civic complaint becomes one tracked issue, so residents can see "
            "progress and staff can see the real backlog."
        ),
        beats=[
            (
                "Hook",
                "A pothole gets reported three times, fixed once, and closes as three separate tickets. That is the reporting system failing both sides.",
            ),
            (
                "The problem",
                "Residents call or email and never hear back. Staff retype the same complaint and cannot tell whether two reports are the same problem.",
            ),
            (
                "Our solution",
                "Submit a photo and pin. We bucket by location, compare text similarity, and show likely duplicates before creating another ticket. Staff get one queue, categories, owners, and an SLA clock; residents get a public status page.",
            ),
            (
                "Live demo",
                "File a streetlight report, file a near-duplicate, show the merge prompt, then switch to staff view and move the issue to in-progress and resolved. Refresh the resident page to show the timeline.",
            ),
            (
                "What's next",
                "Ward-based assignment, escalation for overdue SLAs, duplicate feedback learning, and an open export of resolved issues.",
            ),
        ],
        questions=[
            (
                "How accurate is duplicate detection?",
                "It starts as a candidate system, not an automatic merge. Location plus text similarity gets us high recall, and staff make the final decision. We tune the threshold with a small labeled set.",
            ),
            (
                "How do you avoid merging two different problems nearby?",
                "We show a confidence score, category, photo, and distance before merging. False merges are reversible with a split action, and the audit trail keeps both original reports.",
            ),
            (
                "What does the public page hide?",
                "Reporter contact details are never public. The public sees the category, status, timestamps, and location at a coarse enough level to avoid exposing a home address.",
            ),
            (
                "Why would a municipal office adopt it?",
                "It replaces a phone-and-paper log with a queue staff can actually run. The first version needs only a browser and a small set of categories.",
            ),
        ],
    ),
    3: _kit(
        note=(
            "3 people, one weekend. Matching is the learning value; keep the graph "
            "small enough to explain every match in plain language."
        ),
        roles=[
            (
                "Matching and API",
                "Skill graph, pair and cycle search, scoring, request state machine, "
                "and the explanation payload behind each match.",
            ),
            (
                "Web app",
                "Profiles, offered and wanted skills, match cards, requests, session "
                "scheduling, ratings, report, and block flows.",
            ),
            (
                "Trust and demo",
                "Seed an obvious pair and a three-way cycle, test no-match states, "
                "write the pitch, and rehearse the safety story.",
            ),
        ],
        milestones=[
            "Hour 8: profiles list offered and wanted skills and are searchable.",
            "Hour 16: direct reciprocal pairs are matched and explained.",
            "Hour 24: a three-way cycle is found, requests can be accepted, and a session can be scheduled.",
            "Hour 30: ratings, reporting, and blocking work; the demo uses seeded pairs.",
        ],
        one_liner=(
            "Skill exchange turns unused knowledge into a structured swap, with a "
            "match explanation instead of a group-chat maybe."
        ),
        beats=[
            (
                "Hook",
                "Everyone knows something someone nearby wants to learn. The problem is finding that person without paying for a course or spamming a group chat.",
            ),
            (
                "The problem",
                "Informal skill barter depends on memory and luck. Direct swaps are hard enough; a three-person cycle is almost impossible to coordinate by hand.",
            ),
            (
                "Our solution",
                "People list teachable and wanted skills. We find reciprocal pairs first, then search a bounded graph for three-way cycles. Every match explains who teaches what to whom, and the request, schedule, rating, and report flows keep it safe.",
            ),
            (
                "Live demo",
                "Show two seeded profiles with an obvious pair, open the explanation, accept the request, and schedule a session. Then switch to the three-way cycle and show why no pair existed.",
            ),
            (
                "What's next",
                "Skill verification, group exchanges, calendar integrations, and a reputation system that is harder to game.",
            ),
        ],
        questions=[
            (
                "Why find three-way cycles at all?",
                "Many communities have useful knowledge but no direct two-way overlap. A bounded cycle search turns three people who each have something the next wants into one viable exchange.",
            ),
            (
                "How do you stop the matching graph from becoming spam?",
                "Outgoing requests are rate-limited, duplicate matches are suppressed, blocking removes future candidates, and a declined request cannot be retried immediately.",
            ),
            (
                "What stops someone from claiming a skill they do not have?",
                "The MVP uses ratings, completion confirmations, and reports. Verification is a later layer, and we are explicit that reputation is earned through completed exchanges.",
            ),
            (
                "How do you solve the cold-start problem?",
                "The graph needs density, so we would launch with a class, campus, or community rather than a whole city, and seed it through existing groups.",
            ),
        ],
    ),
    4: _kit(
        note=(
            "3 people, one weekend. A cached GitHub dataset makes the demo reliable "
            "even when the API is slow or rate-limited."
        ),
        roles=[
            (
                "GitHub ingestion and ranking",
                "Issue fetching, caching, language and topic filters, welcomeness "
                "signals, and the ranked result API.",
            ),
            (
                "Web app",
                "Search and filters, issue cards, repository detail, saved issues, "
                "and progress tracking.",
            ),
            (
                "Demo and rate limits",
                "Seed a cache, test expired and empty states, document the ranking, "
                "and prepare the pitch screenshots.",
            ),
        ],
        milestones=[
            "Hour 8: cached beginner-friendly issues render with repository context.",
            "Hour 16: language, topic, and welcomeness filters change the ranking.",
            "Hour 24: saved issues and a progress state persist across reloads.",
            "Hour 30: the cache fallback and the full search-to-save demo are rehearsed.",
        ],
        one_liner=(
            "A first pull request should be a fit, not a guess, so we rank issues "
            "by how welcoming the repository actually looks."
        ),
        beats=[
            (
                "Hook",
                "The first open-source issue someone picks is often the reason they never contribute again.",
            ),
            (
                "The problem",
                "GitHub search can find issue labels, but it does not tell a newcomer whether maintainers respond, whether the repository is active, or whether the issue is still a good fit.",
            ),
            (
                "Our solution",
                "We pull beginner-friendly issues, cache them, and rank repositories by maintainer response time, contributing guide, recent activity, and language fit. Users can save issues and track progress from first look to merged pull request.",
            ),
            (
                "Live demo",
                "Filter to a language and topic, compare two issue cards, save one, and mark it as in progress. Show the cached state when the API is unavailable.",
            ),
            (
                "What's next",
                "Personalized recommendations from a contributor's history, maintainer-side issue quality checks, and contribution outcome tracking.",
            ),
        ],
        questions=[
            (
                "How do you stay inside GitHub rate limits?",
                "We cache repository and issue responses, batch requests, and serve stale but labeled data when the limit is close. The demo runs from the cache.",
            ),
            (
                "Can repositories game the welcomeness score?",
                "Any public score can be gamed. We show the signals behind the rank, keep the formula transparent, and would use outcome data, not just labels, to tune it.",
            ),
            (
                "Why not just use GitHub search?",
                "Search is a list, not a recommendation. We add response behavior, activity, contributor guidance, and a saved progress path that GitHub does not provide for newcomers.",
            ),
            (
                "How do you know an issue is still open and suitable?",
                "We check freshness and cached status, show the last update, and link to the live issue. Stale results are labeled rather than silently recommended.",
            ),
        ],
    ),
    5: _kit(
        note=(
            "3 people, one weekend. Offline behavior and a clear need-to-offer match "
            "matter more than a beautiful map with no operational story."
        ),
        roles=[
            (
                "Needs and offers",
                "Resource posts, categories, urgency, matching by proximity, "
                "fulfilment state, and duplicate suppression.",
            ),
            (
                "Map and offline app",
                "Live map, posting flow, PWA cache, offline queue, and poor-network "
                "status that is honest about what is stale.",
            ),
            (
                "Fallback and demo",
                "SMS or WhatsApp fallback, seeded response scenario, rehearsal, and "
                "the coordination story for judges.",
            ),
        ],
        milestones=[
            "Hour 8: a need and an offer can be posted with category and location.",
            "Hour 16: nearby needs and offers are matched on a live map.",
            "Hour 24: fulfilment is tracked, and an offline post queues and syncs.",
            "Hour 30: the SMS fallback and the end-to-end response demo are ready.",
        ],
        one_liner=(
            "During a response, needs and nearby resources find each other in one "
            "shared map instead of five chat threads."
        ),
        beats=[
            (
                "Hook",
                "In a disaster, supplies often sit in one place while the need is two streets away because nobody has the same picture.",
            ),
            (
                "The problem",
                "Needs arrive through calls, chats, and paper lists. Offers arrive somewhere else. Duplicates waste effort, and a disconnected responder cannot see the latest state.",
            ),
            (
                "Our solution",
                "Responders and community members post needs or offers on a live map. We match nearby categories, show fulfilment state, and keep a PWA queue for poor connectivity with an SMS or WhatsApp fallback.",
            ),
            (
                "Live demo",
                "Post a water need, show nearby offers, accept one, mark it fulfilled. Then switch the network off, queue another post, reconnect, and show the fallback message.",
            ),
            (
                "What's next",
                "Verified organization accounts, transport capacity, duplicate clustering, and exports for incident commands.",
            ),
        ],
        questions=[
            (
                "How do you prevent duplicate or fake needs?",
                "Posts have location, category, contact, and a visible state. Nearby similar posts are surfaced before submission, and organization verification or a responder review can raise trust.",
            ),
            (
                "What works when the connection is poor?",
                "The app shell and current map data are cached, new posts enter an outbox, and the user sees queued or failed states. SMS or WhatsApp is a deliberate fallback, not a hidden promise.",
            ),
            (
                "Why not just use a WhatsApp group?",
                "A group is good for conversation but poor for matching, deduplication, and fulfilment state. We can hand off to WhatsApp for reach while keeping the operational record on the map.",
            ),
            (
                "How do you avoid exposing vulnerable people?",
                "Locations can be coarsened, contact details are opt-in, and public views avoid identifying individuals. Sensitive needs can be visible only to verified responders.",
            ),
        ],
    ),
    6: _kit(
        note=(
            "3 people, one weekend. Pick three products and three countries, and "
            "treat citations as a feature rather than a legal disclaimer."
        ),
        roles=[
            (
                "Source and retrieval",
                "Curated requirements, source URLs, effective dates, document "
                "checklists, and citation retrieval for the assistant.",
            ),
            (
                "Web app and assistant",
                "Product and country selection, checklist UI, source links, and a chat "
                "that answers only from the selected evidence.",
            ),
            (
                "Review and demo",
                "Source verification, not-legal-advice copy, a seeded scenario, and a "
                "pitch that is honest about coverage.",
            ),
        ],
        milestones=[
            "Hour 8: three products and three countries produce a cited checklist.",
            "Hour 16: every requirement has a source, date, and official link where possible.",
            "Hour 24: the assistant answers from the checklist and refuses unsupported questions.",
            "Hour 30: the demo shows a missing document, a source, and a clear limitation.",
        ],
        one_liner=(
            "A small exporter gets a cited, dated checklist for one product and one "
            "country instead of scattered advice from five websites."
        ),
        beats=[
            (
                "Hook",
                "One missing certificate can stop a shipment at the border after the product, packaging, and freight are already paid for.",
            ),
            (
                "The problem",
                "Export rules are spread across official portals, PDFs, and consultant advice. A small business cannot tell which requirement is current or which source to trust.",
            ),
            (
                "Our solution",
                "Choose a product and target country. We show a checklist of documents, duties, regulations, and market notes, each tied to a source and date. The assistant answers only from those sources and says when it does not know.",
            ),
            (
                "Live demo",
                "Pick one product and country, open a requirement and its official source, ask the assistant a supported question, then ask something outside the sources and show the refusal.",
            ),
            (
                "What's next",
                "More products and corridors, source freshness monitoring, saved shipments, and expert review workflows.",
            ),
        ],
        questions=[
            (
                "How do you keep regulations current?",
                "Every item has an effective date and a source. The MVP covers a deliberately small set and labels it as a starting point; freshness monitoring and review are the next layer.",
            ),
            (
                "How do you stop the chat from hallucinating?",
                "The assistant is grounded in the selected checklist and source snippets. If retrieval returns no support, it refuses instead of generating legal advice.",
            ),
            (
                "Who is liable if the checklist is wrong?",
                "The product is an information aid, not legal advice. We show sources and dates, require review with an official authority, and keep the disclaimer visible.",
            ),
            (
                "Why only three products and three countries?",
                "Depth beats breadth for trust. A narrow, well-cited demo is more useful than a shallow database that looks authoritative but cannot be checked.",
            ),
        ],
    ),
    7: _kit(
        note=(
            "3 people, one weekend. Pick one real nonprofit workflow and finish it; "
            "do not build a generic CRM for every possible organization."
        ),
        roles=[
            (
                "Data and permissions",
                "Volunteer, shift, donor, pledge, receipt, and beneficiary models, "
                "plus API-level role enforcement and audit fields.",
            ),
            (
                "Operations UI",
                "Volunteer sign-up and shift board, donor follow-ups, and the staff "
                "view with the few actions that matter each day.",
            ),
            (
                "Impact and demo",
                "Impact report, seeded nonprofit data, permission tests, and the "
                "volunteer-to-donor-to-report pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: volunteers can see shifts and sign up without double booking.",
            "Hour 16: staff can record donors, pledges, and follow-up dates.",
            "Hour 24: roles are enforced and the impact report aggregates real seeded data.",
            "Hour 30: the complete three-role demo is rehearsed with a permission failure.",
        ],
        one_liner=(
            "Small nonprofits get one operational home for volunteers, donors, and "
            "impact instead of five spreadsheets and a group chat."
        ),
        beats=[
            (
                "Hook",
                "A small nonprofit can lose a volunteer and a donor in the same week because both relationships live in someone's inbox.",
            ),
            (
                "The problem",
                "Shifts are coordinated by messages, pledges sit in spreadsheets, and the board asks for impact numbers that take a day to assemble.",
            ),
            (
                "Our solution",
                "One hub for volunteer shifts and sign-ups, donor pledges and receipts, and a simple impact report. Staff, volunteers, and finance see different views, enforced by the API.",
            ),
            (
                "Live demo",
                "Sign up a volunteer, record a donor pledge, switch to finance to see the total, and generate the impact report. Then try a forbidden action to show the permission boundary.",
            ),
            (
                "What's next",
                "Recurring donation reminders, program-level targets, board exports, and integrations with accounting tools.",
            ),
        ],
        questions=[
            (
                "How do you protect beneficiary data?",
                "Beneficiary details are private by default, visible only to the roles that need them, and the public or volunteer view uses aggregate counts instead.",
            ),
            (
                "Are you storing card payments?",
                "No. The MVP records pledges and receipts, not card data. Real payments would require a licensed provider and a separate compliance review.",
            ),
            (
                "Why would a nonprofit switch from spreadsheets?",
                "It gives them one place for the daily workflows they already run, with reminders and permissions. The value is less re-entry and fewer missed follow-ups, not a big migration.",
            ),
            (
                "How do you handle multiple programs or chapters?",
                "The first version models one organization with multiple programs. Multi-tenant chapters are a later step and would need a clear data-separation design.",
            ),
        ],
    ),
    8: _kit(
        note=(
            "3 people, one weekend. The win is a defensible insight from messy CSV, "
            "not a dashboard with every chart type."
        ),
        roles=[
            (
                "Data and metrics",
                "CSV mapping, validation, import errors, program metrics, coverage "
                "aggregation, and data-quality metadata.",
            ),
            (
                "Dashboard and map",
                "Metric cards, trends, filters, drill-down, and the underserved-area "
                "view with a clear legend.",
            ),
            (
                "Validation and demo",
                "A realistic seeded dataset, bad-row examples, assumption copy, and "
                "the question-evidence-action pitch.",
            ),
        ],
        milestones=[
            "Hour 8: a messy CSV uploads with a mapping preview and row errors.",
            "Hour 16: program metrics and trends render for the imported data.",
            "Hour 24: the coverage map highlights an underserved area with drill-down.",
            "Hour 30: the demo shows one data-quality problem and the decision it changes.",
        ],
        one_liner=(
            "Small NGOs turn program spreadsheets into one evidence-backed decision "
            "about where to spend the next rupee."
        ),
        beats=[
            (
                "Hook",
                "A small NGO has the data and the mission, but not the analyst who can turn a spreadsheet into a decision.",
            ),
            (
                "The problem",
                "Program data lives in inconsistent CSVs. Counting people served is manual, coverage gaps are invisible, and every funder asks for a different summary.",
            ),
            (
                "Our solution",
                "Upload a CSV, map the columns, and see validation errors before anything is imported. The dashboard computes the metrics tied to five decisions and joins coverage to population so underserved areas stand out.",
            ),
            (
                "Live demo",
                "Upload a file with one bad date, fix it, and show the resulting program trend. Then open the coverage map, drill into a weak region, and state the next action.",
            ),
            (
                "What's next",
                "Saved imports, scheduled refreshes, funder-specific exports, and a proper indicator library with versioned definitions.",
            ),
        ],
        questions=[
            (
                "What happens when the CSV is a mess?",
                "We preview the mapping, validate dates, regions, duplicates, and required values, and show a per-row error report. We do not silently import partial data.",
            ),
            (
                "How do you protect beneficiary privacy?",
                "The dashboard works from aggregated program records. Any beneficiary-level data stays out of the shared view, and small regions can be suppressed.",
            ),
            (
                "Is the coverage map causal?",
                "No. It shows service coverage against a need estimate. We label it as descriptive and show the source, denominator, and missing-data caveats.",
            ),
            (
                "Why not just use Excel?",
                "Excel can calculate, but it does not give a shared, validated, role-aware view with a map and drill-down. The win is repeatable analysis for a team with no analyst.",
            ),
        ],
    ),
    10: _kit(
        note=(
            "3 people, one weekend. Never touch real card data; the demo routes to "
            "sandbox checkout and treats every QR payload as hostile input."
        ),
        roles=[
            (
                "Parser and security",
                "QR format detection, UPI and payment-link parsing, validation, "
                "allowlists, sandbox routing, and malicious-payload tests.",
            ),
            (
                "User flow",
                "Scan or paste a QR, identify the format, show the destination and "
                "amount, and route to the right app or sandbox checkout.",
            ),
            (
                "Merchant and demo",
                "Merchant QR generation, transaction history, seeded formats, and the "
                "error-and-recovery pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: UPI, payment-link, and one merchant format are identified correctly.",
            "Hour 16: a scanned code routes to the right sandbox flow with a clear confirmation.",
            "Hour 24: merchant QR generation and history work; malformed codes fail safely.",
            "Hour 30: the full scan-to-history demo and the security story are ready.",
        ],
        one_liner=(
            "One scanner understands the payment QR in front of you and sends you "
            "to the right app without guessing or exposing data."
        ),
        beats=[
            (
                "Hook",
                "How many payment apps does it take to use one QR code? Today the answer depends on which format the merchant happened to print.",
            ),
            (
                "The problem",
                "UPI links, Bharat QR, EMV-style codes, and plain payment links all look similar. Users try the wrong app, merchants lose sales, and malicious QR payloads are hard to spot.",
            ),
            (
                "Our solution",
                "We detect the format, validate the payload, show the amount and destination, and route to the correct app or a sandbox checkout. Merchants can generate their own QR and see a transaction history.",
            ),
            (
                "Live demo",
                "Scan a UPI code and a malformed code. Show the correct route, the safe rejection, a generated merchant QR, and one history entry.",
            ),
            (
                "What's next",
                "Licensed payment partnerships, deeper bank-app handoff, fraud signals, and receipt reconciliation.",
            ),
        ],
        questions=[
            (
                "Are you processing real payments?",
                "No. The MVP routes to sandbox gateways and never handles real card data. Production would require licensed partners and a compliance review.",
            ),
            (
                "What stops a malicious QR from taking over?",
                "Every payload is parsed and validated against known formats and allowlists. We show the destination before routing, reject unexpected schemes, and never execute embedded data.",
            ),
            (
                "How do you know which app is installed?",
                "We do not need to. We identify the format and offer a deep link plus a fallback route. The user always sees the destination before leaving.",
            ),
            (
                "What is the hardest part of interoperability?",
                "Payment formats and bank handoffs are fragmented and partner-controlled. That is why we built the routing and UX against test gateways first.",
            ),
        ],
    ),
    11: _kit(
        note=(
            "3 people, one weekend. The demo needs one store, one shelf, and one "
            "reservation; do not try to build a full marketplace."
        ),
        roles=[
            (
                "Inventory and reservations",
                "Per-store stock, atomic reservation holds, pickup codes, and stock "
                "updates from barcode scans.",
            ),
            (
                "Store app",
                "Staff scan flow, stock corrections, reservation queue, and handover "
                "confirmation.",
            ),
            (
                "Shopper app and demo",
                "Catalogue, store selector, reserve flow, QR shelf entry, and the "
                "seeded product-to-pickup story.",
            ),
        ],
        milestones=[
            "Hour 8: products show stock for each store and can be reserved.",
            "Hour 16: a reservation holds stock atomically and produces a pickup code.",
            "Hour 24: staff scan a barcode, update stock, and confirm handover.",
            "Hour 30: the QR-shelf-to-pickup demo is rehearsed with an out-of-stock case.",
        ],
        one_liner=(
            "Shoppers reserve what is actually on the shelf, and store staff keep "
            "online stock tied to the real shelf."
        ),
        beats=[
            (
                "Hook",
                "The website says one left, you drive to the store, and the shelf says otherwise.",
            ),
            (
                "The problem",
                "Online stock is often a nightly guess. Pickup orders get cancelled, staff hunt for items, and the shopper wastes a trip.",
            ),
            (
                "Our solution",
                "Each store has its own stock. Shoppers reserve with an atomic hold and a pickup code. Staff scan barcodes to correct stock and confirm handover. A QR code on the shelf opens the exact product page.",
            ),
            (
                "Live demo",
                "Scan the shelf QR, reserve the last unit, show stock dropping. Switch to staff, scan the barcode, confirm the pickup, and show a second shopper being blocked.",
            ),
            (
                "What's next",
                "Multi-store allocation, low-stock alerts, click-and-collect routing, and integration with existing POS systems.",
            ),
        ],
        questions=[
            (
                "How do you prevent overselling?",
                "A reservation takes an atomic hold in the database. The last unit cannot be promised twice, and expired holds release stock back to the shelf.",
            ),
            (
                "What if staff forget to update stock?",
                "The system cannot fix bad input, but the scan flow is faster than a spreadsheet and every correction is timestamped. Pickup confirmation reconciles the final state.",
            ),
            (
                "Do you need special hardware?",
                "The demo can use a phone camera as a barcode scanner. A real store could use a USB scanner, but the workflow does not depend on custom hardware.",
            ),
            (
                "Why would a small shop use this?",
                "It gives them a credible online catalogue and pickup flow without a full marketplace. The shelf QR connects the physical store to the same stock record.",
            ),
        ],
    ),
    12: _kit(
        note=(
            "3 people, one weekend. Be explicit about data coverage and uncertainty; "
            "a careful score is more convincing than a green badge with no source."
        ),
        roles=[
            (
                "Scores and data",
                "Open Food Facts import, caching, non-food scoring method, category "
                "comparison, and missing-data rules.",
            ),
            (
                "Store UI",
                "Catalogue, score explanation, alternatives, comparison, and the "
                "packaging and cart footprint views.",
            ),
            (
                "Provenance and demo",
                "Source and date display, method copy, seeded Indian products, and the "
                "greenwashing questions in the pitch.",
            ),
        ],
        milestones=[
            "Hour 8: products show a sourced score with an unknown-data state.",
            "Hour 16: greener alternatives appear with the improving factor.",
            "Hour 24: the cart footprint shows assumptions and packaging flags.",
            "Hour 30: the provenance panel and the method explanation are demo-ready.",
        ],
        one_liner=(
            "Green shopping becomes a cited comparison, not a label, because every "
            "score shows its source and its uncertainty."
        ),
        beats=[
            (
                "Hook",
                "A green leaf on a package is marketing until you can trace the number behind it.",
            ),
            (
                "The problem",
                "Environmental claims are inconsistent. Shoppers cannot compare products, and stores have no defensible way to show impact without inventing authority.",
            ),
            (
                "Our solution",
                "We use Open Food Facts Green-Score for food with attribution and show missing coverage. Non-food items use a transparent internal method. The cart estimates footprint with a range, and alternatives explain the one factor that improves.",
            ),
            (
                "Live demo",
                "Open a product, show the source and date, compare a greener alternative, add both to the cart, and show the estimated range plus a missing-data product.",
            ),
            (
                "What's next",
                "More categories, supplier-provided packaging data, regional transport factors, and third-party method review.",
            ),
        ],
        questions=[
            (
                "How accurate is the carbon estimate?",
                "It is an estimate with a range, not a measurement. We show the factors, the missing inputs, and the source date so users can judge how much confidence to place in it.",
            ),
            (
                "What about products with no score?",
                "We show unknown rather than guessing. A missing score never becomes a green recommendation, and the UI explains what data would be needed.",
            ),
            (
                "How do you avoid greenwashing?",
                "Every score has a source or a documented method, we surface uncertainty, and we avoid claims the data cannot support. Non-food scoring is clearly labeled as our own method.",
            ),
            (
                "Why not use an AI model to score everything?",
                "An opaque model would make the trust problem worse. A cited public score plus a transparent internal method is easier to audit and explain.",
            ),
        ],
    ),
    13: _kit(
        note=(
            "3 people, one weekend. Choose three layers and one strong local story; "
            "the map is the stage, not the whole product."
        ),
        roles=[
            (
                "Layers and data",
                "NASA tile layers, valid date ranges, caching, attribution, and the "
                "layer metadata behind the explainers.",
            ),
            (
                "Map experience",
                "Base map, time slider, split comparison, legends, mobile layout, and "
                "loading and missing-data states.",
            ),
            (
                "Explainers and demo",
                "Plain-language copy, three local stories, source credits, and the "
                "rehearsal with cached demo dates.",
            ),
        ],
        milestones=[
            "Hour 8: one NASA layer renders on a map with a date control.",
            "Hour 16: the time slider switches dates without losing the map location.",
            "Hour 24: side-by-side comparison and layer explainers work.",
            "Hour 30: the three local stories are cached and rehearsed.",
        ],
        one_liner=(
            "Earth observation data becomes a clear before-and-after story, with the "
            "credit and caveats built into the screen."
        ),
        beats=[
            (
                "Hook",
                "The evidence of environmental change already exists in public NASA data. Most people have never seen it arranged as a story.",
            ),
            (
                "The problem",
                "Scientific portals are built for researchers. Raw layers are hard to compare, dates are confusing, and a pretty map can easily imply the wrong conclusion.",
            ),
            (
                "Our solution",
                "We use ready-made NASA tile layers with a time slider and a split comparison. Each layer has a plain-language explanation, a legend, and a limitation note, so the audience can see change without overclaiming.",
            ),
            (
                "Live demo",
                "Start global, choose a location, compare two dates side by side, and read the explainer. Show the source credit and the caveat during the demo.",
            ),
            (
                "What's next",
                "Guided tours, local datasets, annotation layers, and classroom-ready explainer packs.",
            ),
        ],
        questions=[
            (
                "What do the colors actually mean?",
                "Each layer has its own legend and explainer. We state what is measured and warn that seasonality, clouds, and processing can affect the color, not only long-term change.",
            ),
            (
                "How current is the data?",
                "Each layer has a valid date range and a source timestamp. We show the selected date and the source credit rather than implying the map is real-time.",
            ),
            (
                "Why not build on NASA Worldview directly?",
                "Worldview is a powerful scientific tool. We focus on a guided comparison and explanation for non-experts, which is a different product from a full data portal.",
            ),
            (
                "How do you handle slow tiles?",
                "We preload adjacent dates, show loading states, and cache the demo dates. The pitch also has a recorded fallback in case the venue network fails.",
            ),
        ],
    ),
    14: _kit(
        note=(
            "3 people, one weekend. Roles and the audit trail are the product; use "
            "mock payments and keep the student path painfully clear."
        ),
        roles=[
            (
                "Workflow and audit",
                "Application state machine, document review, role permissions, audit "
                "log, and disbursement records.",
            ),
            (
                "Student and reviewer app",
                "Application form, status timeline, reviewer queue, approval actions, "
                "and the admin export.",
            ),
            (
                "Finance and demo",
                "Mock disbursement, seeded applications, permission tests, and the "
                "application-to-payment pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: a student submits an application and sees its status timeline.",
            "Hour 16: a reviewer can verify documents and move the application forward.",
            "Hour 24: approval, mock disbursement, and an audit trail are connected.",
            "Hour 30: admin export and the role-boundary demo are rehearsed.",
        ],
        one_liner=(
            "Scholarship decisions stop disappearing into paper, because every "
            "application, review, and payment has an owner and a timestamp."
        ),
        beats=[
            (
                "Hook",
                "A student can submit a scholarship application and then have no idea whether a human has even opened it.",
            ),
            (
                "The problem",
                "Paper and email applications get lost, reviewers work from inconsistent copies, and finance cannot easily show how a decision became a payment.",
            ),
            (
                "Our solution",
                "Students apply and upload documents. Reviewers work a queue with a clear checklist. Every status change is recorded in an append-only audit trail, and admins export a disbursement report. Payments are mocked.",
            ),
            (
                "Live demo",
                "Submit an application, switch to the reviewer, verify a document, approve it, and show the student's timeline and the audit entry. Try a forbidden finance action to show roles.",
            ),
            (
                "What's next",
                "Document OCR, plagiarism or duplicate checks, real payment integration, and appeal workflows.",
            ),
        ],
        questions=[
            (
                "How are sensitive documents protected?",
                "Uploads have type and size validation, access is role-based, and reviewers only see the applications assigned to them. The audit log records who opened or changed what.",
            ),
            (
                "Are you moving real money?",
                "No. Disbursement is mocked in the MVP. Real payments would need a licensed provider, reconciliation, and a much stricter compliance review.",
            ),
            (
                "Why is an audit trail necessary?",
                "Scholarship decisions affect people's lives and often need to be explained later. An append-only record makes approvals, rejections, and payments traceable.",
            ),
            (
                "What stops a reviewer from approving everything?",
                "The workflow requires document checks before approval, and the audit trail exposes unusual sequences. A second approval step or sampling is a later control.",
            ),
        ],
    ),
    15: _kit(
        note=(
            "3 people, one weekend. Browser location limits are real; design around "
            "check-ins and a visible expiration instead of promising background GPS."
        ),
        roles=[
            (
                "Trip state and alerts",
                "Share links, expiry, check-in timers, route corridor and dwell rules, "
                "and notification delivery state.",
            ),
            (
                "Traveller and contact UI",
                "Trip creation, live share page, check-in control, contact view, and "
                "revoke and expired states.",
            ),
            (
                "Fallback and demo",
                "SMS or email fallback, two-device rehearsal, false-alarm handling, "
                "and the privacy story.",
            ),
        ],
        milestones=[
            "Hour 8: a trip creates an expiring share link with a destination.",
            "Hour 16: the contact sees the latest location and a working check-in.",
            "Hour 24: late check-in, long stop, and route deviation alerts fire once.",
            "Hour 30: revoke, expiry, and the SMS fallback are demonstrated.",
        ],
        one_liner=(
            "A live trip share tells the right person when something looks wrong, "
            "without pretending the browser can track you forever."
        ),
        beats=[
            (
                "Hook",
                "Walking home alone, the useful message is not 'I left'; it is 'I stopped moving and missed my check-in'.",
            ),
            (
                "The problem",
                "Manual text updates depend on the traveller remembering. Background location is unreliable in mobile browsers, and constant tracking raises privacy concerns.",
            ),
            (
                "Our solution",
                "Share a trip for a limited time. Contacts see the latest location while the page is open and get alerts for a missed check-in, a long stop, or leaving the route. The traveller can revoke instantly, and the app is honest about browser limits.",
            ),
            (
                "Live demo",
                "Open the traveller and contact views on two devices. Move, stop, miss a check-in, show the alert, then revoke the link and show it stop updating.",
            ),
            (
                "What's next",
                "Trusted-contact groups, native background modes, emergency-service handoff, and a safer route recommendation layer.",
            ),
        ],
        questions=[
            (
                "Does this track location in the background?",
                "Not reliably in a browser, and we say so. The design centers on an open page, check-in timers, and a manual or SMS fallback rather than promising background tracking.",
            ),
            (
                "What if the alert is a false alarm?",
                "The contact can dismiss it, and the traveller can check in or cancel. We use grace periods and a visible last-updated time to avoid treating stale data as an emergency.",
            ),
            (
                "Who can see the trip?",
                "Only people with the share link, for a limited time. The traveller can revoke it, and location history is deleted or anonymized after expiry.",
            ),
            (
                "Is this a replacement for emergency services?",
                "No. It is a coordination aid for trusted contacts. The UI must never imply that it dispatches help or replaces calling emergency services.",
            ),
        ],
    ),
    19: _kit(
        note=(
            "3 people, one weekend. The server must own the canvas; if the client "
            "is authoritative, the demo will fork under two browser windows."
        ),
        roles=[
            (
                "Realtime and state",
                "Authoritative grid, WebSocket protocol, event log, sequence numbers, "
                "cooldown and rate limits, and reconnect resync.",
            ),
            (
                "Canvas client",
                "Pixel drawing, live cursors, cooldown UI, reconnect state, mobile "
                "touch, and the timelapse scrubber.",
            ),
            (
                "Abuse and demo",
                "Moderation rollback, seeded art, multi-window rehearsal, and the "
                "timelapse closing beat.",
            ),
        ],
        milestones=[
            "Hour 8: two clients see the same pixel appear in real time.",
            "Hour 16: cooldown, live cursors, and reconnect resync work.",
            "Hour 24: server-side rate limits and a moderation rollback are in place.",
            "Hour 30: the seeded canvas and timelapse replay are demo-ready.",
        ],
        one_liner=(
            "A crowd builds one canvas together in real time, with fair cooldowns "
            "and a replay that makes every pixel accountable."
        ),
        beats=[
            (
                "Hook",
                "A blank canvas plus a crowd is a surprisingly strong social product, but only if the state stays consistent and nobody can spam it.",
            ),
            (
                "The problem",
                "Real-time drawing breaks when clients disagree, dropped connections fork the board, and one script can overwrite the whole canvas.",
            ),
            (
                "Our solution",
                "The server owns the grid and broadcasts accepted pixel events. We add per-user cooldowns, server-side rate limits, live cursors, moderation rollback, and an append-only history for timelapse replay.",
            ),
            (
                "Live demo",
                "Open two windows, draw together, trigger the cooldown, show a reconnect resync, roll back a region, and play the timelapse.",
            ),
            (
                "What's next",
                "Redis for horizontal scale, community canvases, palette voting, and scheduled art battles.",
            ),
        ],
        questions=[
            (
                "How do you stop one script from filling the canvas?",
                "Every placement is authenticated or rate-limited, cooldowns are enforced server-side, and moderation can roll back a region. The client timer is only feedback, not the control.",
            ),
            (
                "How does the canvas stay consistent after a disconnect?",
                "The server keeps an ordered event log. On reconnect, the client asks for events after its last sequence number and rebuilds from there.",
            ),
            (
                "Why store history instead of only the current grid?",
                "History powers the timelapse, makes moderation auditable, and lets us rebuild the canvas. Snapshots keep replay fast as history grows.",
            ),
            (
                "How would you scale this?",
                "Move the grid and pub/sub to Redis, shard by canvas, and snapshot old history. The MVP stays single-process so the consistency story is easy to explain.",
            ),
        ],
    ),
    22: _kit(
        note=(
            "3 people, one weekend. No face recognition and no recording; the "
            "transparency panel is part of the demo, not a legal footnote."
        ),
        roles=[
            (
                "Motion sensing",
                "Local frame capture, downscaling, frame differencing, smoothing, "
                "calibration, and the measured-energy API.",
            ),
            (
                "Audio and visuals",
                "Web Audio layers, energy-band mapping, canvas response, reduced-motion "
                "support, and the mute and camera-off fallbacks.",
            ),
            (
                "Transparency and demo",
                "Metric panel, privacy copy, recorded motion fallback, calibration "
                "rehearsal, and the crowd-energy pitch.",
            ),
        ],
        milestones=[
            "Hour 8: the webcam produces a stable motion score without storing frames.",
            "Hour 16: energy bands change the audio and visual output smoothly.",
            "Hour 24: calibration, hysteresis, and the transparency panel work.",
            "Hour 30: the live and recorded-motion demos both work at venue volume.",
        ],
        one_liner=(
            "The crowd moves, the music responds, and the screen explains the "
            "measurement without ever looking at a face."
        ),
        beats=[
            (
                "Hook",
                "A DJ reads the room by watching energy. We let a browser do that with motion only, and show exactly what it is measuring.",
            ),
            (
                "The problem",
                "Responsive visuals often rely on opaque AI or manual controls. Camera-based sentiment analysis raises privacy and accuracy problems that a party app does not need.",
            ),
            (
                "Our solution",
                "We compare downscaled webcam frames to measure motion energy. Smoothed bands drive a small Web Audio graph and a canvas visual. A panel shows the value, the band, and why the music changed; nothing is recorded or uploaded.",
            ),
            (
                "Live demo",
                "Calibrate a still room, have the audience move, show the energy rise, the audio layers enter, and the panel explain the change. Cover the camera and show the fallback.",
            ),
            (
                "What's next",
                "More instrument layers, spatial region controls, accessibility modes, and optional DMX or lighting output.",
            ),
        ],
        questions=[
            (
                "Are you identifying people in the crowd?",
                "No. We do frame differencing on downscaled frames and never run face detection or recognition. Nothing is recorded or uploaded.",
            ),
            (
                "What if the lighting changes?",
                "The motion score is calibrated against a still baseline and smoothed with hysteresis. A sudden light change can briefly register as motion, so we expose a recalibrate control.",
            ),
            (
                "How do you keep the music from sounding random?",
                "Only a few smoothed energy bands map to a small set of audio layers. The transitions are gradual and the mapping is visible, so the response feels intentional.",
            ),
            (
                "What about accessibility?",
                "The visual respects reduced-motion preferences, there is a mute control, and a manual mode lets the app run without a camera.",
            ),
        ],
    ),
    27: _kit(
        note=(
            "3 people, one weekend. The visibility calculation and an honest 3D view "
            "are more impressive than a list of every pass overhead."
        ),
        roles=[
            (
                "Orbits and visibility",
                "TLE caching, SGP4 propagation, pass windows, sun and observer "
                "darkness, and the visible-pass filter.",
            ),
            (
                "Globe and sky UI",
                "Location selection, 3D globe, sky chart, pass timeline, and the "
                "time scrubbing controls.",
            ),
            (
                "Alerts and demo",
                "Cached demo elements, alert preferences, source credits, and the "
                "missed-ISS pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: a location produces pass times from cached orbital elements.",
            "Hour 16: visibility filters remove passes the observer cannot see.",
            "Hour 24: the globe and sky chart update with the selected pass.",
            "Hour 30: the pass alert and the offline cache demo are rehearsed.",
        ],
        one_liner=(
            "The ISS is about to pass overhead and you can actually see it, because "
            "the tracker filters for darkness and observer visibility."
        ),
        beats=[
            (
                "Hook",
                "The ISS just flew over your city, but most trackers told you about ten passes you could not see anyway.",
            ),
            (
                "The problem",
                "Orbital pass lists ignore whether the observer is in darkness, whether the satellite is sunlit, and where in the sky to look. A generic list is technically true and practically useless.",
            ),
            (
                "Our solution",
                "We compute passes in the browser with SGP4, filter by observer darkness and satellite illumination, and show the path on a globe and a sky chart. Alerts fire only for passes that are actually worth watching.",
            ),
            (
                "Live demo",
                "Pick a location, scrub to a visible pass, show the sky path and the countdown, then compare it with a pass we filtered out.",
            ),
            (
                "What's next",
                "Weather-aware visibility, camera field-of-view guides, group viewing events, and more satellite catalogues.",
            ),
        ],
        questions=[
            (
                "How fresh are the orbital elements?",
                "We cache published TLEs, show their age, and refresh within the source's guidance. Accuracy degrades over time, so stale elements are labeled rather than hidden.",
            ),
            (
                "Can you guarantee someone will see it?",
                "No. We show the geometric and illumination conditions. Weather, buildings, and local light pollution can still block the view, and the UI says so.",
            ),
            (
                "Why compute in the browser?",
                "SGP4 is small enough to run locally, which keeps the demo responsive and avoids a server round-trip for every scrub. The TLE data is still fetched and cached.",
            ),
            (
                "What about the source's usage terms?",
                "We credit the orbital-element source, cache requests, and follow its guidance. The app does not hammer the feed for every page view.",
            ),
        ],
    ),
    28: _kit(
        note=(
            "3 people, one weekend. Validate one transfer against a known result "
            "instead of adding every maneuver in orbital mechanics."
        ),
        roles=[
            (
                "Physics and integrator",
                "Orbit state, Hohmann and bi-elliptic burns, delta-v math, RK4 "
                "integration, and validation against reference data.",
            ),
            (
                "Simulation UI",
                "Orbit controls, burn planning, trajectory playback, delta-v readout, "
                "and the Web Worker boundary.",
            ),
            (
                "Validation and demo",
                "Reference checks, error display, seeded scenarios, and the "
                "burn-to-trajectory pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: a Hohmann transfer produces a plausible trajectory and delta-v.",
            "Hour 16: RK4 integration runs in a worker without freezing the UI.",
            "Hour 24: bi-elliptic and one gravity-assist scenario are selectable.",
            "Hour 30: the validation panel and the full burn-to-orbit demo are ready.",
        ],
        one_liner=(
            "Plan a burn, see the real integrated trajectory, and compare the "
            "simulation with a known reference instead of trusting an animation."
        ),
        beats=[
            (
                "Hook",
                "Orbital mechanics looks like magic until you move one burn and watch the whole trajectory change.",
            ),
            (
                "The problem",
                "Canned animations teach the wrong lesson. A visible path may ignore integration error, units, or the actual delta-v cost of a maneuver.",
            ),
            (
                "Our solution",
                "Choose orbits, plan Hohmann or bi-elliptic burns, and integrate the trajectory with RK4 in a Web Worker. We show delta-v and an error panel, and validate a scenario against JPL Horizons data.",
            ),
            (
                "Live demo",
                "Start from a low orbit, plan a transfer, change one parameter, and show the new trajectory and delta-v. Open the validation panel and compare the result.",
            ),
            (
                "What's next",
                "More bodies, plane changes, a proper mission timeline, and guided challenges for classrooms.",
            ),
        ],
        questions=[
            (
                "Why RK4 instead of a canned animation?",
                "The point is to show the numerical method and its error. RK4 is a readable balance of accuracy and speed, and the validation panel makes the approximation visible.",
            ),
            (
                "How do you know the simulation is right?",
                "We compare a known scenario with published Horizons positions and show the difference. We also display units and integration settings so the result is reproducible.",
            ),
            (
                "Is the gravity assist realistic?",
                "It is a simplified two-body or patched-conic demonstration, not a full n-body mission design. We label the simplification and keep the focus on the transfer mechanics.",
            ),
            (
                "Why use a Web Worker?",
                "Integration can block the main thread and make the controls feel broken. The worker keeps the UI responsive while the trajectory updates.",
            ),
        ],
    ),
    29: _kit(
        note=(
            "3 people, one weekend. Use a proven cheminformatics library and make "
            "the Lipinski explanation readable; do not hand-roll molecular math."
        ),
        roles=[
            (
                "Cheminformatics",
                "SMILES parsing, descriptor calculation, Lipinski checks, PubChem "
                "lookup, and lazy loading for the heavy library.",
            ),
            (
                "3D and comparison UI",
                "Molecule input, 3D viewer, property panel, side-by-side comparison, "
                "and the substructure search view.",
            ),
            (
                "Validation and demo",
                "Known-molecule checks, source and disclaimer copy, seeded examples, "
                "and the formula-to-shape pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: a SMILES string renders in 3D and shows basic properties.",
            "Hour 16: the Lipinski verdict and plain-language explanation work.",
            "Hour 24: two molecules compare side by side and a small library supports substructure search.",
            "Hour 30: lazy-loading and the validation/disclaimer demo are ready.",
        ],
        one_liner=(
            "A molecule becomes a shape with explainable drug-likeness properties, "
            "not a formula on a slide."
        ),
        beats=[
            (
                "Hook",
                "A molecule is a three-dimensional shape, but most chemistry tools present it as a line of text and a table of rules.",
            ),
            (
                "The problem",
                "Property calculations are easy to get subtly wrong, and a Lipinski verdict without an explanation teaches memorization, not understanding.",
            ),
            (
                "Our solution",
                "Type a SMILES string or compound name, see it in 3D, and get molecular weight, logP, donors, acceptors, and a Lipinski verdict with each rule explained. Compare two molecules and search a small library by substructure.",
            ),
            (
                "Live demo",
                "Load a familiar drug, show the 3D structure and properties, compare it with a failed analogue, and explain which Lipinski rule changed.",
            ),
            (
                "What's next",
                "Larger libraries, saved workspaces, more descriptor sets, and exportable teaching worksheets.",
            ),
        ],
        questions=[
            (
                "Are the property calculations correct?",
                "They come from a proven cheminformatics library, and we validate known molecules. The UI shows which method produced each value and avoids claiming more precision than it has.",
            ),
            (
                "Why is the app slow on first load?",
                "The cheminformatics bundle is large, so we lazy-load it only when the molecule tool opens. A small initial shell keeps the catalogue fast.",
            ),
            (
                "Is this medical advice?",
                "No. It is an educational explorer. The disclaimer is visible, and a Lipinski verdict is not a prediction that a compound is safe or effective.",
            ),
            (
                "Where does compound data come from?",
                "PubChem is one lookup source, with rate limits and attribution. The user can also paste a SMILES string, so the app works without a lookup.",
            ),
        ],
    ),
    31: _kit(
        note=(
            "3 people, one weekend. Run the simulation in a worker, be explicit that "
            "this is an educational model, and show assumptions on screen."
        ),
        roles=[
            (
                "Simulation engine",
                "Contact-network model, SIR states, interventions, time steps, and "
                "the Web Worker API.",
            ),
            (
                "Controls and charts",
                "Network and intervention controls, SIR curves, R(t), comparisons, and "
                "the assumptions panel.",
            ),
            (
                "Fitting and demo",
                "Real case-count fitting, seeded scenarios, validation notes, and the "
                "intervention-comparison pitch.",
            ),
        ],
        milestones=[
            "Hour 8: a contact network runs a visible SIR outbreak.",
            "Hour 16: vaccination, masking, and school closure change the curve.",
            "Hour 24: scenarios compare and R(t) updates over time.",
            "Hour 30: the model fits a small real case series and labels its assumptions.",
        ],
        one_liner=(
            "Different networks and interventions produce different outbreaks, and "
            "the simulator shows why instead of pretending to forecast."
        ),
        beats=[
            (
                "Hook",
                "One school closure can bend an outbreak curve, but only if you can see how the contact network changes.",
            ),
            (
                "The problem",
                "A single SIR line hides who meets whom. Policy discussions need a model that shows households, schools, and workplaces and admits its assumptions.",
            ),
            (
                "Our solution",
                "Simulate a population as a contact network, run an SIR process, and toggle vaccination, masking, and school closure. Compare outcomes, fit real case counts, and show how R changes over time.",
            ),
            (
                "Live demo",
                "Run the baseline, add vaccination and school closure, compare the curves, and show the assumptions panel and the fitted R trend.",
            ),
            (
                "What's next",
                "Age structure, waning immunity, mobility data, and scenario exports for classrooms.",
            ),
        ],
        questions=[
            (
                "Is this a forecast?",
                "No. It is an educational model. We show assumptions, uncertainty, and the fact that real outcomes depend on behavior and data we do not have.",
            ),
            (
                "Why model a network instead of a single SIR curve?",
                "Contact structure changes how fast an outbreak spreads and who is affected. A network makes interventions like school closure interpretable.",
            ),
            (
                "How do you fit real data?",
                "We calibrate a small set of parameters to reported case counts and show the fit error. The model is not claiming to predict the future, only to explain a past window.",
            ),
            (
                "How does it stay responsive?",
                "The simulation runs in a Web Worker, so the controls and charts remain usable while the network steps forward.",
            ),
        ],
    ),
    32: _kit(
        note=(
            "3 people, one weekend. Validate the solver against the rectangular-barrier "
            "answer; a pretty wave animation without a known-answer check is not enough."
        ),
        roles=[
            (
                "Numerical solver",
                "Grid, wave packet, time stepping, potential barriers and wells, "
                "transmission and reflection measurement, and the analytic check.",
            ),
            (
                "Visualization",
                "Canvas or WebGL rendering, potential editing, wave playback, "
                "measurement readouts, and responsive controls.",
            ),
            (
                "Performance and demo",
                "WebAssembly or GPU path, seeded scenarios, validation panel, and the "
                "tunneling-to-known-answer pitch.",
            ),
        ],
        milestones=[
            "Hour 8: a wave packet moves on a grid without exploding.",
            "Hour 16: a barrier produces reflection and transmission with measured probabilities.",
            "Hour 24: the measured transmission matches the analytic rectangular-barrier result.",
            "Hour 30: the optimized solver and the full draw-launch-compare demo are ready.",
        ],
        one_liner=(
            "Draw a barrier, launch a wave packet, and watch quantum tunneling happen "
            "with the numerical result checked against the known answer."
        ),
        beats=[
            (
                "Hook",
                "A quantum particle can appear on the wrong side of a wall. We let the audience draw that wall and watch it happen.",
            ),
            (
                "The problem",
                "Schrodinger simulations are easy to make visually impressive and numerically wrong. Without a known-answer check, the animation teaches nothing reliable.",
            ),
            (
                "Our solution",
                "An interactive 1D time-dependent Schrodinger solver lets users draw a potential, launch a wave packet, and see transmission and reflection. We compare the measured transmission with the analytic rectangular-barrier result.",
            ),
            (
                "Live demo",
                "Draw a barrier, launch the packet, pause at the split, and show the analytic versus measured transmission. Then widen the barrier and watch the probability fall.",
            ),
            (
                "What's next",
                "2D potentials, absorbing boundaries, parameter sweeps, and classroom experiment presets.",
            ),
        ],
        questions=[
            (
                "How do you know the solver is accurate?",
                "The rectangular barrier has an analytic transmission result. We run that case and show the measured value beside the expected value, including the error.",
            ),
            (
                "Why WebAssembly or the GPU?",
                "The time step updates every grid point. A fast path keeps the animation smooth; the MVP can start on the main thread and move the hot loop when it becomes the bottleneck.",
            ),
            (
                "What numerical issues can break the simulation?",
                "An unstable time step, reflections from the grid edge, and a poorly resolved barrier can all produce nonsense. We show units, stability limits, and an absorbing-boundary option.",
            ),
            (
                "Is this a physical quantum computer?",
                "No. It is a numerical visualization of the wave equation. It teaches the model and its approximations, not hardware behavior.",
            ),
        ],
    ),
    33: _kit(
        note=(
            "3 people, one weekend. The b-value is only credible if the completeness "
            "warning is impossible to miss."
        ),
        roles=[
            (
                "Catalogue and statistics",
                "USGS ingestion, caching, filters, magnitude-frequency bins, maximum-"
                "likelihood b-value, confidence interval, and completeness check.",
            ),
            (
                "Map and charts",
                "Earthquake map, region selection, magnitude-frequency plot, fitted "
                "line, b-value result, and the warning states.",
            ),
            (
                "Validation and demo",
                "Method notes, two-region comparison, seeded cache, and the "
                "catalogue-quality pitch story.",
            ),
        ],
        milestones=[
            "Hour 8: cached USGS events render on a map with filters.",
            "Hour 16: the magnitude-frequency plot and event count update correctly.",
            "Hour 24: b-value, uncertainty, and the completeness warning are shown together.",
            "Hour 30: the two-region comparison and the source/date panel are demo-ready.",
        ],
        one_liner=(
            "A seismic catalogue becomes an honest b-value estimate, with the "
            "completeness warning shown beside the number."
        ),
        beats=[
            (
                "Hook",
                "An earthquake map shows where the dots are. It does not tell you whether the catalogue is complete enough to analyze.",
            ),
            (
                "The problem",
                "The Gutenberg-Richter b-value is easy to compute badly. Small samples, missing tiny events, and loose filters produce confident-looking numbers that should not be trusted.",
            ),
            (
                "Our solution",
                "Filter the USGS catalogue by region, time, depth, and magnitude. Plot magnitude frequency on a log scale, estimate b with a maximum-likelihood method and interval, and warn when completeness or sample size fails.",
            ),
            (
                "Live demo",
                "Compare a well-sampled region with a sparse one. Show the plot, the b-value interval, and the completeness warning that changes the conclusion.",
            ),
            (
                "What's next",
                "Time-varying b-value, spatial smoothing, aftershock declustering, and saved analyses for classrooms.",
            ),
        ],
        questions=[
            (
                "What is the b-value actually telling us?",
                "It describes the relative frequency of small and large earthquakes in the selected catalogue. It is not a prediction of when the next earthquake will happen.",
            ),
            (
                "How do you handle incomplete catalogues?",
                "We estimate the magnitude of completeness and warn when the selected data fall below it. The result is caveated or disabled rather than presented as reliable.",
            ),
            (
                "Why show uncertainty?",
                "A b-value from a small sample can move a lot. The interval makes the sample-size problem visible instead of hiding it behind one decimal place.",
            ),
            (
                "Where does the data come from?",
                "The public USGS earthquake feed. We cache responses, show the feed timestamp, credit the source, and keep the request rate modest.",
            ),
        ],
    ),
}
