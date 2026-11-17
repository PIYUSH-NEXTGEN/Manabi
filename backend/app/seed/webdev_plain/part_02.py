"""Plain-language overrides for Web Dev resume briefs 006-010."""

OVERRIDES = {
    "manabi-web-resume-006": {
        "summary": (
            "Build a trip planner that reads bus and train schedules from GTFS feeds. "
            "It returns multi-leg journeys and shows each leg, walking transfer and wait "
            "time on a map. Commuters, transit agencies and city planners can compare "
            "route quality.\n\n"
            "Schedules change by day and time, so a plain shortest-path search can return "
            "a trip that does not exist. You load stops, routes, trips and stop times, then "
            "run a timetable-aware algorithm like RAPTOR or Connection Scan. The planner "
            "returns both the fastest arrival and the fewest transfers, and a small "
            "benchmark shows the difference."
        ),
        "who_affected": (
            "Commuters, transit agencies and city planners who compare route quality "
            "across a network."
        ),
        "why_matters": (
            "A planner that ignores transfer time or service calendars sends people on "
            "trips that do not exist."
        ),
        "approaches": [
            "Import GTFS stops, routes, trips, stop times and calendars into a model you can query.",
            "Run RAPTOR or Connection Scan over timetable events instead of fixed edge weights.",
            "Treat fastest arrival and fewest transfers as two separate goals.",
            "Draw legs and transfers on a map and expose the same planner through an API.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "One GTFS feed produces a correct multi-leg trip with walking "
                        "transfers and a map preview."
                    ),
                    "checks": [
                        "GTFS stops, trips and stop times import without losing service-calendar data.",
                        "A query returns a valid itinerary with departure, arrival and transfer times.",
                        "The map shows each transit leg and walking transfer on its own.",
                        "A missing or invalid feed returns a clear error instead of a broken route.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The planner compares fastest and fewest-transfer trips and beats a "
                        "naive graph search on a benchmark set."
                    ),
                    "checks": [
                        "RAPTOR or Connection Scan respects departure times and service calendars.",
                        "The API returns both fastest and fewest-transfer options for the same query.",
                        "A benchmark compares travel time and transfer counts against a baseline.",
                        "Time zones, overnight trips and feed validity are handled on purpose.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "Timetable modelling, graph algorithms and API design are the core "
                        "of this project."
                    ),
                },
                {
                    "role": "Data engineer",
                    "how_it_helps": (
                        "GTFS ingestion, calendar handling, feed validation and benchmark "
                        "data are practical pipeline work."
                    ),
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You connected a real algorithm to a map UI and an API without "
                        "hiding the data model."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a GTFS journey planner using {ALGO} over timetables, "
                        "returning fastest and fewest-transfer routes."
                    ),
                    "example": (
                        "Built a GTFS journey planner using RAPTOR over timetable events, "
                        "returning fastest and fewest-transfer routes for the same "
                        "origin-destination query."
                    ),
                },
                {
                    "bullet": (
                        "Cut average query time to {MS} ms on a benchmark of {N} trips "
                        "while keeping transfer counts correct."
                    ),
                    "example": (
                        "Cut average query time to 180 ms on a 2,000-trip benchmark by "
                        "scanning timetable events instead of running a time-expanded "
                        "graph search."
                    ),
                },
                {
                    "bullet": (
                        "Handled service calendars, time zones and overnight trips that a "
                        "naive shortest-path planner breaks on."
                    ),
                    "example": (
                        "Handled service calendars, time zones and overnight trips, so "
                        "weekend and after-midnight queries returned valid itineraries "
                        "instead of phantom routes."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "Why not use Dijkstra on a static graph?",
                    "answer": (
                        "A transit network changes with time. An edge only works at a "
                        "specific departure. Dijkstra on a static graph can return a path "
                        "you cannot travel. RAPTOR or Connection Scan works over timetable "
                        "events and respects waiting and transfer time."
                    ),
                },
                {
                    "question": "How do you compare fastest and fewest transfers?",
                    "answer": (
                        "They are different goals, so I keep separate labels during the "
                        "search. The API returns both and the UI lets the user choose. One "
                        "blended score would hide the trade-off."
                    ),
                },
                {
                    "question": "What was the hardest part of the GTFS import?",
                    "answer": (
                        "Service calendars and time zones. A trip can cross midnight, and "
                        "the same route can run on different days. I normalize calendar "
                        "dates before building events and test overnight and weekend cases."
                    ),
                },
            ],
            "differentiators": [
                "A real timetable-aware algorithm instead of a static shortest-path demo.",
                "Two clear goals, fastest and fewest transfers, returned side by side.",
                "A benchmark that shows correctness and speed, not a screenshot.",
            ],
        },
        "build_guide": [
            {
                "title": "Import and validate GTFS",
                "summary": "The algorithm is only as correct as the feed model under it.",
                "steps": [
                    "Download one city feed and load stops, routes, trips, stop_times and calendar records into a staging schema.",
                    "Check required files, missing stop times, duplicate ids and calendar ranges. Fail loudly with a report you can read.",
                    "Normalize dates and time zones. Keep GTFS times as seconds from noon-minus-twelve so after-midnight trips do not wrap.",
                    "Build a queryable timetable index of stop events, route ids and service dates.",
                ],
            },
            {
                "title": "Implement a timetable-aware search",
                "summary": "Use RAPTOR or Connection Scan instead of a static Dijkstra graph.",
                "steps": [
                    "Represent a trip as an ordered list of stop events and a route as a sequence of stops.",
                    "Implement round-based RAPTOR or a connection scan that tracks arrival time and transfers for each stop.",
                    "Carry two labels through the search, earliest arrival and fewest transfers. Keep them apart instead of blending them into one score.",
                    "Add walking transfers with a configurable maximum distance and transfer time.",
                ],
            },
            {
                "title": "Expose the planner API",
                "summary": "A thin UI needs a clear contract you can test.",
                "steps": [
                    "Create an endpoint that accepts origin, destination, departure date and time, plus an objective.",
                    "Return both fastest and fewest-transfer itineraries with legs, departure, arrival, waiting time and transfer walk.",
                    "Handle no-service, invalid stop and missing-feed cases with specific errors instead of empty results.",
                    "Add a benchmark endpoint or script that runs stored origin-destination pairs and reports time and transfer counts.",
                ],
            },
            {
                "title": "Build the map itinerary UI",
                "summary": "The map should explain the trip, not decorate it.",
                "steps": [
                    "Build stop search with keyboard selection and a clear origin-destination swap control.",
                    "Draw each leg in a different style and split walking transfers, waiting time and vehicle time in the itinerary list.",
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
        "summary": (
            "Build a web app that scans or takes a pasted payment QR code, works out its "
            "format and sends the user to the right payment flow. It reads UPI links, "
            "Bharat QR, EMV-style merchant payloads and plain payment links. Shoppers, "
            "small merchants and fintech developers are the people it serves.\n\n"
            "This is a parsing and safety project. It does not process payments. You build "
            "a format detector, a checked parser for each format and a router that opens an "
            "app or a sandbox page. The app shows the merchant, amount and currency before "
            "it routes, and it never stores real card data."
        ),
        "who_affected": (
            "Shoppers facing mismatched payment apps, small merchants making QR codes and "
            "fintech developers building payment flows."
        ),
        "why_matters": (
            "Payment QR formats are fragmented. A clear parser and safe routing layer "
            "prevent failed payments and leaked data."
        ),
        "approaches": [
            "Detect the payload format before parsing and reject input that is ambiguous or malformed.",
            "Write a checked parser for each format and test the edge cases.",
            "Route to a payment app or sandbox checkout without touching real card data.",
            "Generate merchant QR codes and keep a test history that is clearly labelled.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "A scanned UPI or payment link is parsed, shown for confirmation "
                        "and routed to the correct app or sandbox page."
                    ),
                    "checks": [
                        "The app reads a QR image and pulls out the payload text.",
                        "A parser identifies at least two formats and shows merchant, amount and currency.",
                        "Malformed payloads are rejected with a clear reason.",
                        "Routing opens a sandbox or app link without storing card data.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "Several formats share one tested parser pipeline, and merchant QR "
                        "generation plus history work end to end."
                    ),
                    "checks": [
                        "Format detection and parsing are separate, tested stages with valid and invalid fixtures.",
                        "The app generates merchant QR codes and round-trips them through its own parser.",
                        "Transaction history is marked as test data and stores no sensitive payloads.",
                        "Ambiguous payloads ask for confirmation instead of guessing silently.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "The camera flow, confirmation screen, error states and QR "
                        "generation are practical browser UI work."
                    ),
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You built parsing, routing, QR generation and history in one "
                        "small, coherent product."
                    ),
                },
                {
                    "role": "Fintech engineer",
                    "how_it_helps": (
                        "You can discuss format validation, sandbox boundaries and "
                        "sensitive-data handling."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a payment QR parser that identifies {N} formats and checks "
                        "payloads before routing."
                    ),
                    "example": (
                        "Built a payment QR parser that identifies UPI, Bharat QR and "
                        "payment-link payloads, validating merchant, amount and currency "
                        "before routing."
                    ),
                },
                {
                    "bullet": (
                        "Added {N} parser fixtures covering valid, malformed and ambiguous "
                        "payloads, with zero unhandled inputs."
                    ),
                    "example": (
                        "Added 40 parser fixtures covering valid, malformed and ambiguous "
                        "payloads. Every rejected case returned a specific reason."
                    ),
                },
                {
                    "bullet": (
                        "Kept the app inside sandbox boundaries with no real card storage "
                        "and clear test-mode labels."
                    ),
                    "example": (
                        "Kept all routing inside sandbox or app-handoff flows, stored no "
                        "card data and labelled every test transaction in the UI."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "How do you avoid misrouting a payment?",
                    "answer": (
                        "I detect the format first, check the fields and show the parsed "
                        "merchant, amount and currency before routing. Ambiguous payloads "
                        "ask the user to confirm. I do not guess when a field is missing or "
                        "inconsistent."
                    ),
                },
                {
                    "question": "Why not process real payments?",
                    "answer": (
                        "Payment processing needs licensed partners, compliance and real "
                        "settlement. This project is a parser and router with sandbox or app "
                        "handoff. Keeping that boundary clear is part of the design."
                    ),
                },
                {
                    "question": "What do you store in transaction history?",
                    "answer": (
                        "Only test-mode metadata: format, masked merchant reference, "
                        "amount, status and timestamp. I do not store full QR payloads, card "
                        "data or anything sensitive in a real payment."
                    ),
                },
            ],
            "differentiators": [
                "A tested parser pipeline with clear reasons for each rejection.",
                "Sandbox boundaries and test-mode labels that match the project scope.",
                "Merchant QR generation that round-trips through the same parser.",
            ],
        },
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
                    "Implement a format detector that returns a confidence and a reason instead of a bare best guess.",
                    "Write one parser per format with typed output and specific validation errors.",
                    "Add fixtures for valid, malformed, ambiguous and unsupported payloads. Make every rejection return a reason a person can read.",
                    "Create a shared parsed-payment shape so the confirmation UI and router do not depend on format-specific details.",
                ],
            },
            {
                "title": "Build scanning, confirmation and routing",
                "summary": "The user must see and confirm the payment details before anything opens.",
                "steps": [
                    "Add camera scanning plus paste and image-upload fallbacks. Handle permission denial cleanly.",
                    "Show merchant, amount, currency, format and warnings on a confirmation screen before routing.",
                    "Route only to an app deep link or sandbox page. Never build a real payment request from a payload the user has not confirmed.",
                    "Add a test-mode label and a visible cancel path on every routed screen.",
                ],
            },
            {
                "title": "Add generator, history and test fixtures",
                "summary": "Round-tripping your own QR codes proves the parser is consistent with itself.",
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
        "summary": (
            "Build an online catalogue where shoppers see stock per store, reserve an item "
            "and pick it up in person. Store staff update stock by scanning barcodes, and "
            "QR codes in the shop open the matching product page. Local retailers, "
            "shoppers and store staff are the people it serves.\n\n"
            "Inventory consistency is the main problem. A reservation must hold stock for a "
            "short window, a pickup must reduce it, and an expired reservation must release "
            "it. Keep those operations in one transactional path and test the race when two "
            "users reserve the last unit."
        ),
        "who_affected": (
            "Local retailers, shoppers who want reliable pickup and store staff who manage "
            "stock across shelves and online orders."
        ),
        "why_matters": (
            "Stale stock data causes cancelled pickups and wasted trips. One reservation "
            "path keeps online promises and shelf reality aligned."
        ),
        "approaches": [
            "Model stock per store and keep reservations, pickups and adjustments in one transaction log.",
            "Expire unpaid reservations automatically and return the held stock.",
            "Give staff a phone-friendly barcode scan flow for stock updates.",
            "Use in-store QR codes that deep-link to the product page and store availability.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "Shoppers see per-store stock, reserve an item and get a pickup "
                        "code. Staff can adjust stock."
                    ),
                    "checks": [
                        "Product pages show stock for a selected store.",
                        "A reservation holds one unit for a short window and shows a pickup code.",
                        "Staff can change stock and the shopper view reflects it.",
                        "An expired reservation releases the held unit on its own.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "Concurrent reservations cannot oversell the last unit, and every "
                        "stock change can be traced."
                    ),
                    "checks": [
                        "Reservation, pickup and adjustment operations use one consistent transactional path.",
                        "A concurrency test proves two shoppers cannot both reserve the last unit.",
                        "The stock audit trail shows whether a change came from a reservation, pickup or manual adjustment.",
                        "A staff barcode-scan flow updates stock from a phone and handles unknown barcodes cleanly.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You built catalogue, inventory, reservations, staff tools and audit "
                        "history end to end."
                    ),
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "Transactional stock handling, expiry and race-condition tests are "
                        "the strongest part of the project."
                    ),
                },
                {
                    "role": "E-commerce engineer",
                    "how_it_helps": (
                        "Reservation holds, pickup state and stock consistency are core "
                        "commerce problems."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a click-and-collect flow that held stock per store and "
                        "prevented overselling across {N} concurrent reservations."
                    ),
                    "example": (
                        "Built a click-and-collect flow that held stock per store and "
                        "prevented overselling in a 50-user concurrency test for the last "
                        "unit."
                    ),
                },
                {
                    "bullet": (
                        "Cut stock mismatches by adding a single reservation, pickup and "
                        "adjustment ledger with an audit trail."
                    ),
                    "example": (
                        "Cut stock mismatches by recording every reservation, pickup and "
                        "manual adjustment in one ledger, making each change traceable to "
                        "its source."
                    ),
                },
                {
                    "bullet": (
                        "Added a phone barcode-scan flow that let staff update shelf stock "
                        "without a desktop terminal."
                    ),
                    "example": (
                        "Added a phone-friendly barcode flow that let staff update shelf "
                        "stock during a shift without returning to a desktop terminal."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "How do you prevent two shoppers from reserving the last unit?",
                    "answer": (
                        "I do the availability check and the reservation write in one "
                        "transaction with a row lock or a conditional update on available "
                        "stock. The second request sees the held stock and fails cleanly. It "
                        "never creates an oversold reservation."
                    ),
                },
                {
                    "question": "Why hold stock instead of only checking it at pickup?",
                    "answer": (
                        "A pickup promise without a hold lets the shop sell the item before "
                        "the shopper arrives. A short hold protects the shopper. An expiry "
                        "then releases abandoned reservations so stock does not stay frozen."
                    ),
                },
                {
                    "question": "How do you debug an inventory mismatch?",
                    "answer": (
                        "Every change is a permanent ledger entry with a reason and "
                        "reference: reservation, pickup, expiry or manual adjustment. I can "
                        "sum the entries for a product and store and compare that to the "
                        "shelf count."
                    ),
                },
            ],
            "differentiators": [
                "A concurrency test for the last-unit reservation instead of only a happy-path checkout.",
                "One inventory ledger for reservations, pickups and manual edits.",
                "A staff barcode flow built for a phone on the shop floor.",
            ],
        },
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
                    "Reserve stock inside a transaction using a row lock or conditional update that checks the available quantity.",
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
                    "Make out-of-stock and expired-hold states explicit instead of silently removing the button.",
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
                "summary": "Stock correctness is the main claim, so prove it under load and failure.",
                "steps": [
                    "Add tests for expiry, cancellation, double pickup, manual adjustment and concurrent reservations.",
                    "Run a small load test with parallel reservations and check that available stock never goes negative.",
                    "Create an in-store QR demo that opens a product page for the correct store.",
                    "Write the stock model, transaction rules and setup in the README, then record the last-unit demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-009": {
        "summary": (
            "Build a platform for scholarship applications. Students submit documents, "
            "reviewers check them, approvers move applications through a workflow and "
            "finance records disbursements. Students, reviewers, finance staff and program "
            "administrators are the people it serves.\n\n"
            "Role-based workflow is the core here. You define reviewer and approver "
            "permissions, document-verification states, rejection reasons and a clear "
            "resubmission path. Every action lands in an audit trail, and each student can "
            "see their own status without emailing the office."
        ),
        "who_affected": (
            "Students applying for scholarships, scholarship reviewers, finance staff and "
            "program administrators."
        ),
        "why_matters": (
            "Paper applications get lost and status questions eat staff time. A "
            "permissioned workflow makes decisions and payments traceable."
        ),
        "approaches": [
            "Model applications, documents, verification states and approval steps as explicit records.",
            "Enforce reviewer and approver permissions on every workflow transition.",
            "Write an audit entry for each view of a sensitive document, decision and payment.",
            "Use mock disbursements tied to approved applications and exportable reports.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "Students apply with documents, reviewers check them, and approved "
                        "applications go on to a mock disbursement."
                    ),
                    "checks": [
                        "A student can submit an application and upload the required documents.",
                        "A reviewer can approve or reject a document with a reason.",
                        "An approved application can be marked for mock disbursement.",
                        "Each student sees only their own application status.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The full role-based workflow enforces boundaries, records every "
                        "action and exports a reconciliation report."
                    ),
                    "checks": [
                        "Reviewer and approver permissions are enforced on API routes and UI actions.",
                        "Every decision, document view and disbursement writes an audit entry.",
                        "A rejected student can resubmit only the affected document without restarting the application.",
                        "The finance export reconciles approved amounts against mock disbursement records.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You built the student flow, role model, workflow and reporting "
                        "layer together."
                    ),
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "Permissions, state transitions, audit logs and reconciliation are "
                        "real backend concerns."
                    ),
                },
                {
                    "role": "Product engineer",
                    "how_it_helps": (
                        "You can explain a workflow with rejection, resubmission and "
                        "finance handoff instead of a single form."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a role-based scholarship workflow covering {N} applications, "
                        "document verification and mock disbursements."
                    ),
                    "example": (
                        "Built a role-based scholarship workflow covering 500 sample "
                        "applications, document verification, approvals and mock "
                        "disbursements."
                    ),
                },
                {
                    "bullet": (
                        "Enforced reviewer and approver permissions with an audit trail for "
                        "every sensitive document view and decision."
                    ),
                    "example": (
                        "Enforced reviewer and approver permissions on all API routes, with "
                        "an audit trail for every document view, decision and disbursement."
                    ),
                },
                {
                    "bullet": (
                        "Cut resubmission work by letting students replace only the rejected "
                        "document instead of the whole application."
                    ),
                    "example": (
                        "Cut resubmission work by letting students replace only the "
                        "rejected document. The rest of the application stayed intact and "
                        "reviewable."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "How do you stop a reviewer from approving their own application?",
                    "answer": (
                        "Permissions are checked on the server for each transition, and the "
                        "actor is stored with the decision. A reviewer cannot act on an "
                        "application tied to their own account. The UI hides the action, but "
                        "the API enforces it."
                    ),
                },
                {
                    "question": "Why keep an audit trail for document views?",
                    "answer": (
                        "Scholarship documents are sensitive. Knowing who opened a document "
                        "and when makes misuse detectable and supports a real review "
                        "process. The audit entry is separate from the workflow state, so a "
                        "normal update cannot edit it."
                    ),
                },
                {
                    "question": "How do you keep disbursement reports consistent?",
                    "answer": (
                        "A disbursement points to an approved application and a fixed "
                        "amount. Finance records are append-only in the mock flow. The "
                        "export reconciles approved applications against recorded "
                        "disbursements instead of recalculating from mutable fields."
                    ),
                },
            ],
            "differentiators": [
                "Server-enforced role boundaries, with a test for self-approval.",
                "A resubmission path that keeps the rest of the application.",
                "An append-only audit trail around sensitive documents and payments.",
            ],
        },
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
                    "Build the application form with required fields, document slots, size limits and file-type checks.",
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
                    "Build an approver view that only shows checked applications and records a decision with a reason.",
                    "Enforce transitions on the server and log actor, old state, new state, timestamp and reason for every change.",
                    "Add an audit view for admins that filters by application, actor and action.",
                ],
            },
            {
                "title": "Build finance records and reporting",
                "summary": "The report must come from the workflow, not be typed in separately.",
                "steps": [
                    "Create mock disbursement records tied to an approved application and a signed-off amount.",
                    "Build a finance queue with a clear paid and pending state. Label every payment as mock or test mode.",
                    "Add an export that reconciles approved amounts, recorded disbursements and open items.",
                    "Show a student-facing payment status without exposing internal reviewer notes.",
                ],
            },
            {
                "title": "Test permissions, audit and the full case",
                "summary": "The best evidence is a complete case that proves the boundaries held.",
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
        "summary": (
            "Build a multi-tenant storefront builder for small local shops. A shop owner "
            "signs up, adds products, picks a simple theme and shares a branded link. "
            "Shoppers browse the catalogue and start an order through a WhatsApp enquiry or "
            "a QR code in the shop. Small shop owners, local customers and freelancers are "
            "the people it serves.\n\n"
            "Multi-tenancy is the main engineering problem. Every shop has its own slug, "
            "products and settings, but one codebase and one database serve all of them. You "
            "enforce tenant boundaries in every query and test that one owner cannot read or "
            "edit another shop's data."
        ),
        "who_affected": (
            "Small shop owners without a website, local customers and freelancers building "
            "low-cost commerce tools."
        ),
        "why_matters": (
            "A local shop needs a credible online catalogue and a simple order path, not a "
            "full marketplace with heavy setup."
        ),
        "approaches": [
            "Give each shop a slug, settings and isolated product records behind an ownership check.",
            "Support draft and published storefronts with image uploads and size limits.",
            "Generate WhatsApp order links and QR codes that point at the shop or product.",
            "Add an optional test-mode subscription plan without real payment processing.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "One owner can create a shop, add products and share a published "
                        "storefront link."
                    ),
                    "checks": [
                        "A shop owner signs up, creates a shop and adds products with images.",
                        "A published storefront is reachable at a clean shop slug.",
                        "A shopper can start a WhatsApp enquiry from a product.",
                        "Draft shops are not publicly reachable.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "Many shops share the same app with enforced tenant boundaries, QR "
                        "links and a test-mode plan."
                    ),
                    "checks": [
                        "Every query and mutation checks tenant ownership on the server.",
                        "A test proves one owner cannot read or edit another shop's products.",
                        "Shop and product QR codes resolve to the right public page.",
                        "A test-mode subscription state can be changed without touching real payment data.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You built tenant-aware data, owner flows and a public storefront in "
                        "one product."
                    ),
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "Ownership checks, tenant isolation and slug routing are practical "
                        "multi-tenant backend work."
                    ),
                },
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "The editor, live preview and public storefront show both internal "
                        "and customer-facing UI."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a multi-tenant storefront builder serving {N} shops from one "
                        "codebase with server-enforced ownership checks."
                    ),
                    "example": (
                        "Built a multi-tenant storefront builder serving 25 sample shops "
                        "from one codebase, with server-enforced ownership checks on every "
                        "product query."
                    ),
                },
                {
                    "bullet": (
                        "Added branded links, WhatsApp enquiries and QR codes that turned a "
                        "shop catalogue into a shareable order path."
                    ),
                    "example": (
                        "Added branded shop links, WhatsApp enquiry links and printable QR "
                        "codes, giving each shop a shareable catalogue without a full "
                        "checkout."
                    ),
                },
                {
                    "bullet": (
                        "Tested tenant isolation so no owner could read or edit another "
                        "shop's catalogue."
                    ),
                    "example": (
                        "Added tests proving a shop owner could not read or edit another "
                        "tenant's products, including direct ID-based requests."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "What does multi-tenant mean in this project?",
                    "answer": (
                        "Many shops share one application and database, but each shop's data "
                        "is isolated by a tenant ID. Every query includes the tenant, and "
                        "every mutation checks ownership on the server. A shop slug "
                        "identifies the public storefront, not a trusted permission."
                    ),
                },
                {
                    "question": "Why use WhatsApp instead of a cart and checkout?",
                    "answer": (
                        "Small shops often close orders in WhatsApp already. A lightweight "
                        "enquiry link avoids payment and delivery complexity while still "
                        "giving the shop an online catalogue. A full checkout would be a "
                        "later step, not the first version."
                    ),
                },
                {
                    "question": "How do you test tenant isolation?",
                    "answer": (
                        "I sign in as one owner and request another shop's product by ID "
                        "through the API instead of only clicking the UI. The request must "
                        "fail. I repeat that for edits, image uploads and settings."
                    ),
                },
            ],
            "differentiators": [
                "A real tenant model with isolation tests instead of a shop ID in the URL.",
                "A shareable WhatsApp and QR order path that fits how small shops already work.",
                "A narrow first version with billing explicitly optional and test-mode only.",
            ],
        },
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
                    "Build a live preview beside the editor so theme and layout changes show up right away.",
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
                "summary": "Optional monetisation should not turn into a fake payment flow.",
                "steps": [
                    "Add an optional test-mode plan page with product and image limits. Label it as a demo and never charge a card.",
                    "Enforce limits on the server and show the remaining allowance in the owner dashboard.",
                    "Log publish, unpublish and plan changes in an owner-visible activity list.",
                    "Add a tenant-safe media cleanup job for deleted or unused images.",
                ],
            },
            {
                "title": "Demo multi-tenancy and document the model",
                "summary": "Safe isolation is the main claim, so show the negative test.",
                "steps": [
                    "Create two seeded shops and show the ownership block in both the UI and an API test.",
                    "Publish one shop, open its public URL, scan the QR and start a WhatsApp order from a product page.",
                    "Test slug collisions, image limits and unpublished storefront behavior.",
                    "Write the tenant model, access rules and local setup in the README, then record the two-shop demo.",
                ],
            },
        ],
    },
}
