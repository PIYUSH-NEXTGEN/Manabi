"""Plain-language overrides for MANABI Web Dev hackathon briefs 007 to 012."""

OVERRIDES = {
    "manabi-web-hackathon-007": {
        "summary": (
            "Build one workspace for a small nonprofit to track volunteers, shifts, "
            "donors, pledges, receipts, and the people it serves. Staff, volunteers, "
            "and finance each see only what their role allows. The app also builds a "
            "simple impact report from the work people actually record.\n\n"
            "The tricky part is balance. Beneficiary records must stay private while "
            "staff still get answers. Every endpoint checks the role, so a volunteer "
            "cannot read donor or beneficiary data even with a crafted request."
        ),
        "who_affected": (
            "Small nonprofit staff, volunteers, recurring donors, and the people who "
            "depend on their services."
        ),
        "why_matters": (
            "Many small groups run on spreadsheets, group chats, and memory, so a "
            "missed shift or forgotten donor follow-up costs time and trust."
        ),
        "approaches": [
            "Model volunteers, shifts, sign-ups, donors, pledges, receipts, and beneficiaries as separate records.",
            "Enforce staff, volunteer, and finance permissions in the API too, so the UI alone is never the guard.",
            "Send shift reminders and donor follow-ups from a small queue with a visible log.",
            "Build an impact report from volunteer hours, donations, and people served, and keep beneficiary details private.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Small nonprofits get one home for volunteers, donors, and impact "
                "instead of five spreadsheets and a group chat."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A small nonprofit can lose a volunteer and a donor in the same "
                        "week because both relationships live in one person's inbox."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Shifts run on messages, pledges sit in spreadsheets, and the "
                        "board asks for impact numbers that take a day to assemble."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "One hub for shifts and sign-ups, donor pledges and receipts, "
                        "and a simple impact report. Staff, volunteers, and finance see "
                        "different views, and the API enforces it."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Sign up a volunteer, record a pledge, switch to finance to see "
                        "the total, and generate the report. Then try a forbidden action "
                        "to show the permission boundary."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Recurring donation reminders, program targets, board exports, "
                        "and links to accounting tools."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you protect beneficiary data?",
                    "answer": (
                        "Beneficiary details are private by default. Only roles that need "
                        "them can read them, and other views show aggregate counts "
                        "instead."
                    ),
                },
                {
                    "question": "Are you storing card payments?",
                    "answer": (
                        "No. The app records pledges and receipts, not card data. Real "
                        "payments would need a licensed provider and a separate "
                        "compliance review."
                    ),
                },
                {
                    "question": "Why would a nonprofit switch from spreadsheets?",
                    "answer": (
                        "They get one place for the workflows they already run, with "
                        "reminders and permissions. They write things down once and miss "
                        "fewer follow-ups. It is a small move, not a big migration."
                    ),
                },
                {
                    "question": "How do you handle multiple programs or chapters?",
                    "answer": (
                        "The first version covers one organization with multiple "
                        "programs. Multi-tenant chapters come later and need a clear "
                        "data-separation design."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Interview first, model second",
                "summary": (
                    "A hub fails when it models an imaginary organization."
                ),
                "steps": [
                    "Interview one real nonprofit, or write a detailed fictional brief with real workflows.",
                    "List the nouns: volunteer, shift, sign-up, donor, pledge, receipt, beneficiary, and program.",
                    "Draw the three roles and the exact actions each one can take.",
                    "Write down what you will not build, such as payroll, accounting, and medical records.",
                ],
            },
            {
                "title": "Volunteer shifts and sign-ups",
                "summary": (
                    "The volunteer path is the most visible daily workflow."
                ),
                "steps": [
                    "Create shifts with a program, location, start, end, and capacity.",
                    "Let a volunteer sign up, cancel, and see upcoming shifts.",
                    "Block double booking and put a full shift on a waitlist instead of rejecting people silently.",
                    "Add reminders and a simple attendance check-in for staff.",
                ],
            },
            {
                "title": "Donors, pledges, and receipts",
                "summary": (
                    "Trust depends on a clean record of what was promised and what "
                    "arrived."
                ),
                "steps": [
                    "Record donors and pledges with amount, date, campaign, and status.",
                    "Create a receipt record without storing real card data.",
                    "Add follow-up notes and a next-action date for staff.",
                    "Show totals by campaign and flag overdue pledges without counting them as received.",
                ],
            },
            {
                "title": "Permissions and the impact report",
                "summary": (
                    "Sensitive beneficiary data is why this needs real roles."
                ),
                "steps": [
                    "Enforce staff, volunteer, and finance permissions on every relevant endpoint.",
                    "Aggregate volunteer hours, donation totals, and people served by program.",
                    "Build a one-page impact report with filters and an export for the board.",
                    "Test that a volunteer cannot read donor or beneficiary records.",
                ],
            },
            {
                "title": "Demo with credible operations",
                "summary": (
                    "The demo should tell one complete story for each role."
                ),
                "steps": [
                    "Seed a small organization with two programs, ten volunteers, and five donors.",
                    "Demo a shift sign-up, a donor pledge, a finance check, and the impact report.",
                    "Show the permission boundary by attempting a forbidden action.",
                    "Rehearse the five-minute story and prepare the data reset command.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-008": {
        "summary": (
            "Build a dashboard that turns a nonprofit's CSV program data into clear "
            "impact numbers, trends, and a map of underserved areas. A small team can "
            "decide where to spend limited resources without hiring an analyst.\n\n"
            "Every conclusion sits beside its data quality and coverage, so the team "
            "knows how much to trust it. The work is mostly in messy input and honest "
            "framing. Bad rows get named and fixed, sparse periods show as gaps, and "
            "the map says what it can and cannot prove."
        ),
        "who_affected": (
            "Small NGO program managers and funders who have field data but no "
            "in-house analyst or business-intelligence team."
        ),
        "why_matters": (
            "The data usually exists in spreadsheets, but nobody shapes it into "
            "decisions, so coverage gaps stay invisible."
        ),
        "approaches": [
            "Start from five decision questions and a written data dictionary, not a wall of charts.",
            "Upload a CSV, preview the column mapping, and reject bad rows with specific messages.",
            "Compute program metrics and period-over-period trends from the imported records.",
            "Join region coverage with a population estimate to show underserved areas, and label each result with its source date.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Small NGOs turn program spreadsheets into one evidence-backed "
                "decision about where to spend the next rupee."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A small NGO has the data and the mission, but not the analyst "
                        "who can turn a spreadsheet into a decision."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Program data lives in inconsistent CSVs. Counting people "
                        "served is manual, coverage gaps are invisible, and every funder "
                        "wants a different summary."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Upload a CSV, map the columns, and fix validation errors before "
                        "anything imports. The dashboard computes the metrics tied to "
                        "five decisions and joins coverage to population so weak areas "
                        "stand out."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Upload a file with one bad date, fix it, and show the program "
                        "trend. Then open the coverage map, drill into a weak region, "
                        "and state the next action."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Saved imports, scheduled refreshes, funder-specific exports, "
                        "and a versioned indicator library."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "What happens when the CSV is a mess?",
                    "answer": (
                        "The app previews the mapping and checks dates, regions, "
                        "duplicates, and required values. It shows a per-row error "
                        "report and does not import partial data silently."
                    ),
                },
                {
                    "question": "How do you protect beneficiary privacy?",
                    "answer": (
                        "The dashboard works from aggregated program records. "
                        "Beneficiary-level data stays out of the shared view, and small "
                        "regions can be suppressed."
                    ),
                },
                {
                    "question": "Is the coverage map causal?",
                    "answer": (
                        "No. It compares service coverage with a need estimate. The app "
                        "labels it as descriptive and shows the source, the denominator, "
                        "and missing-data caveats."
                    ),
                },
                {
                    "question": "Why not use Excel instead?",
                    "answer": (
                        "Excel can calculate, but it does not give a shared, validated "
                        "view with a map and drill-down. This gives a small team "
                        "repeatable analysis without an analyst."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Choose the decisions before the charts",
                "summary": (
                    "A dashboard is useful only if it changes what someone does next."
                ),
                "steps": [
                    "Write five questions a program manager would actually ask this data.",
                    "Define one metric per question, including its numerator, denominator, and period.",
                    "Document the expected CSV columns and how missing values are treated.",
                    "Agree what stays private and what can appear in an aggregate view.",
                ],
            },
            {
                "title": "Make CSV upload trustworthy",
                "summary": (
                    "Bad rows are the fastest way to lose a nonprofit's confidence."
                ),
                "steps": [
                    "Build upload, header detection, and a column-mapping preview.",
                    "Validate types, dates, region names, and duplicates before import.",
                    "Show a per-row error report and let the user fix and retry.",
                    "Store the original file metadata and the import timestamp.",
                ],
            },
            {
                "title": "Metrics and trends",
                "summary": (
                    "The first screen should answer the most common question without a "
                    "filter hunt."
                ),
                "steps": [
                    "Compute program totals and per-period changes from imported records.",
                    "Add filters for program, region, and date range.",
                    "Add drill-down from a chart to the rows behind it.",
                    "Handle sparse periods clearly instead of drawing fake zeroes.",
                ],
            },
            {
                "title": "Coverage map and underserved areas",
                "summary": (
                    "A map earns its place when it joins need to service coverage."
                ),
                "steps": [
                    "Aggregate served people or activities by region.",
                    "Join a population or need estimate and calculate a coverage indicator.",
                    "Render a choropleth or region table with a clear legend and a missing-data state.",
                    "Explain that the indicator describes coverage and does not prove cause.",
                ],
            },
            {
                "title": "Demo the insight, not the dashboard",
                "summary": (
                    "Judges remember a decision, not a wall of widgets."
                ),
                "steps": [
                    "Seed three programs with realistic regional gaps and one messy import example.",
                    "Show one import error being fixed, then the coverage insight it produces.",
                    "Add a short data-quality and assumptions panel.",
                    "Rehearse the one-minute story: question, evidence, next action.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-009": {
        "summary": (
            "Build a web app that reads a payment QR code, works out its format, and "
            "sends the user to the right payment app or a clearly labelled sandbox "
            "checkout. It shows the merchant, amount, and currency before any "
            "routing.\n\n"
            "The app never stores real card data. Broken or ambiguous codes get a "
            "clear reason and a safe stop. Most of the work is a careful parser with "
            "tests, plus a confirmation screen the user reads before anything opens."
        ),
        "who_affected": (
            "Shoppers facing mismatched payment apps, small merchants who print QR "
            "codes, and fintech developers building payment flows."
        ),
        "why_matters": (
            "Payment QR formats are fragmented, so a clear parser and a safe routing "
            "layer prevent failed payments and accidental data leaks."
        ),
        "approaches": [
            "Detect the payload format before parsing, and reject ambiguous or malformed input.",
            "Write one validated parser per format with tests for edge cases.",
            "Route to a payment app or sandbox checkout without touching real card data.",
            "Generate merchant QR codes and keep a clearly labelled test history.",
        ],
        "pitch_guide": {
            "one_liner": (
                "One scanner reads the payment QR in front of you and sends you to "
                "the right app without guessing or exposing data."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "How many payment apps does it take to use one QR code? Today "
                        "the answer depends on which format the merchant happened to "
                        "print."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "UPI links, Bharat QR, EMV-style codes, and plain payment links "
                        "all look similar. Users open the wrong app, merchants lose "
                        "sales, and malicious payloads are hard to spot."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We detect the format, validate the payload, show the amount and "
                        "destination, and route to the right app or a sandbox checkout. "
                        "Merchants can generate their own QR and see a test history."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Scan a UPI code and a malformed code. Show the correct route, "
                        "the safe rejection, a generated merchant QR, and one history "
                        "entry."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Licensed payment partnerships, deeper bank-app handoff, fraud "
                        "signals, and receipt reconciliation."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Are you processing real payments?",
                    "answer": (
                        "No. The app routes to sandbox gateways and never handles real "
                        "card data. Production would need licensed partners and a "
                        "compliance review."
                    ),
                },
                {
                    "question": "What stops a malicious QR from taking over?",
                    "answer": (
                        "Every payload is parsed and checked against known formats and "
                        "allowlists. We show the destination before routing, reject "
                        "unexpected schemes, and never run embedded data."
                    ),
                },
                {
                    "question": "How do you know which app is installed?",
                    "answer": (
                        "We do not need to. We identify the format and offer a deep link "
                        "plus a fallback route. The user always sees the destination "
                        "before leaving."
                    ),
                },
                {
                    "question": "What is the hardest part of interoperability?",
                    "answer": (
                        "Payment formats and bank handoffs are fragmented and controlled "
                        "by partners. So we built the routing and UX against test "
                        "gateways first."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Define formats and safety boundaries",
                "summary": (
                    "A payment QR router is a parser with a strict no-real-money "
                    "boundary."
                ),
                "steps": [
                    "Collect public format docs for UPI, Bharat QR, EMV merchant payloads, and plain payment links.",
                    "Write the supported-fields table and a clear rejection rule for missing, conflicting, or unsupported fields.",
                    "Define what you store: format, masked merchant reference, amount, currency, status, and timestamp only.",
                    "Say in the README that the app never processes real payments and every checkout is sandbox or an app handoff.",
                ],
            },
            {
                "title": "Build the parser pipeline",
                "summary": (
                    "Keep detect, parse, validate, and explain as separate stages."
                ),
                "steps": [
                    "Write a format detector that returns a confidence and a reason, not a bare best guess.",
                    "Write one parser per format with typed output and specific validation errors.",
                    "Add fixtures for valid, malformed, ambiguous, and unsupported payloads. Every rejection returns a human-readable reason.",
                    "Create one shared parsed-payment shape so the confirmation UI and router do not depend on format details.",
                ],
            },
            {
                "title": "Build scanning, confirmation, and routing",
                "summary": (
                    "The user must see and confirm the payment details before anything "
                    "opens."
                ),
                "steps": [
                    "Add camera scanning plus paste and image-upload fallbacks. Handle permission denial cleanly.",
                    "Show merchant, amount, currency, format, and warnings on a confirmation screen before routing.",
                    "Route only to an app deep link or sandbox page. Never build a real payment request from an unconfirmed payload.",
                    "Add a test-mode label and a visible cancel path on every routed screen.",
                ],
            },
            {
                "title": "Add a generator, history, and test fixtures",
                "summary": (
                    "Parsing your own QR codes back proves the parser is consistent."
                ),
                "steps": [
                    "Build a merchant QR generator for at least two supported formats with preview and download.",
                    "Parse the generated payload back through the same pipeline and show a round-trip success result.",
                    "Store only test-mode history and mark it clearly. Add a clear-history action.",
                    "Add a fixture viewer so a reviewer can load a bad payload and see the exact rejection path.",
                ],
            },
            {
                "title": "Harden edge cases and document",
                "summary": (
                    "Ambiguous input is normal, so the UI must ask instead of guessing."
                ),
                "steps": [
                    "Test conflicting amount fields, missing currency, unsupported schemes, oversized input, and duplicate payloads.",
                    "Add a manual confirmation step for ambiguous formats and never auto-route when confidence is low.",
                    "Write the format support matrix, privacy rules, and local setup in the README.",
                    "Record a demo with a valid parse, an ambiguous confirmation, and a rejected malformed payload.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-010": {
        "summary": (
            "Build an online catalogue where shoppers see which local store has an "
            "item, reserve it, and pick it up in person. Store staff update stock fast "
            "by scanning a barcode.\n\n"
            "The race is the point. Two shoppers may try to reserve the last unit at "
            "the same moment. A database transaction takes the hold, expiry returns "
            "stock when a hold runs out, and a test fires both requests to prove only "
            "one wins."
        ),
        "who_affected": (
            "Local retailers, shoppers who want a reliable pickup, and store staff "
            "who manage stock across shelves and online orders."
        ),
        "why_matters": (
            "Stale stock data causes cancelled pickups and wasted trips, so one "
            "reservation path keeps online promises and shelf reality together."
        ),
        "approaches": [
            "Model stock per store and log reservations, pickups, and adjustments in one transaction log.",
            "Expire unpaid reservations automatically and return held stock.",
            "Give staff a phone-friendly barcode scan flow for stock updates.",
            "Use in-store QR codes that deep-link to the product page and that store's availability.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Shoppers reserve what is actually on the shelf, and staff keep online "
                "stock tied to the real shelf."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "The website says one left, you drive to the store, and the "
                        "shelf says otherwise."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Online stock is often a nightly guess. Pickup orders get "
                        "cancelled, staff hunt for items, and the shopper wastes a trip."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Each store keeps its own stock. Shoppers reserve with an atomic "
                        "hold and get a pickup code. Staff scan barcodes to correct "
                        "stock and confirm handover. A shelf QR opens the exact product "
                        "page."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Scan the shelf QR, reserve the last unit, and show stock drop. "
                        "Switch to staff, scan the barcode, confirm the pickup, and show "
                        "a second shopper being blocked."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Multi-store allocation, low-stock alerts, click-and-collect "
                        "routing, and links to existing POS systems."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you prevent overselling?",
                    "answer": (
                        "A reservation takes an atomic hold in the database. The last "
                        "unit cannot be promised twice, and expired holds release stock "
                        "back to the shelf."
                    ),
                },
                {
                    "question": "What if staff forget to update stock?",
                    "answer": (
                        "The system cannot fix bad input, but the scan flow is faster "
                        "than a spreadsheet and every correction is timestamped. Pickup "
                        "confirmation reconciles the final state."
                    ),
                },
                {
                    "question": "Do you need special hardware?",
                    "answer": (
                        "The demo can use a phone camera as a barcode scanner. A real "
                        "store could use a USB scanner, but the workflow does not depend "
                        "on custom hardware."
                    ),
                },
                {
                    "question": "Why would a small shop use this?",
                    "answer": (
                        "It gives them a credible online catalogue and pickup flow "
                        "without a full marketplace. The shelf QR ties the physical "
                        "store to the same stock record."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Model catalogue, stores, and stock events",
                "summary": (
                    "Availability is a transaction log, not a number someone edits."
                ),
                "steps": [
                    "Define product, store, stock level, stock event, reservation, and pickup records.",
                    "Choose the availability rule: on-hand minus active holds. Store events for reservation, release, pickup, and manual adjustment.",
                    "Add store-specific product visibility and in-store QR mappings.",
                    "Seed two stores, a hundred products, and a few live reservations so both views have realistic data.",
                ],
            },
            {
                "title": "Build transactional reservations",
                "summary": (
                    "The last unit is the whole project, so make the race safe in the "
                    "database."
                ),
                "steps": [
                    "Reserve stock inside a transaction with a row lock or a conditional update that checks available quantity.",
                    "Set an expiry timestamp and a background job that releases expired holds back to available stock.",
                    "Record every reservation and release with the reservation id so pickups cannot subtract stock twice.",
                    "Add a test that fires two reservations for the last unit at the same time and asserts exactly one succeeds.",
                ],
            },
            {
                "title": "Build the shopper pickup flow",
                "summary": (
                    "Shoppers need confidence about what is available at which store."
                ),
                "steps": [
                    "Create catalogue and product pages with per-store availability, a pickup window, and a clear reservation state.",
                    "Show a pickup code and instructions after reservation. Allow cancellation before the hold expires.",
                    "Add store search and a filter for items available nearby.",
                    "Make out-of-stock and expired-hold states clear instead of removing the button silently.",
                ],
            },
            {
                "title": "Build the staff scan and reconciliation flow",
                "summary": (
                    "Staff work on a phone with one hand, so the flow must be fast and "
                    "forgiving."
                ),
                "steps": [
                    "Build a barcode-scan screen that updates stock or marks a pickup in two taps.",
                    "Show recent stock events for a product with the source: reservation, pickup, or adjustment.",
                    "Add a reconciliation view that lists reservations without pickups and stock levels that disagree with the event sum.",
                    "Protect staff actions with a store-scoped role and log the staff member on every event.",
                ],
            },
            {
                "title": "Test, demo, and document the consistency story",
                "summary": (
                    "The claim is stock correctness, so prove it under load and failure."
                ),
                "steps": [
                    "Add tests for expiry, cancellation, double pickup, manual adjustment, and concurrent reservations.",
                    "Run a small load test with parallel reservations and check that available stock never goes negative.",
                    "Create an in-store QR demo that opens a product page for the correct store.",
                    "Write the stock model, transaction rules, and setup in the README, then record the last-unit demo.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-011": {
        "summary": (
            "Build an online store that shows an environmental score for each product, "
            "suggests greener alternatives, estimates the carbon footprint of a cart, "
            "and flags sustainable packaging.\n\n"
            "The app must stay honest when data is missing or uncertain. Food items "
            "use Open Food Facts Green-Score data with attribution and caching. Other "
            "items use a published internal method. Each score shows its source, its "
            "date, and its limits, so a weak estimate never looks like a firm claim."
        ),
        "who_affected": (
            "Shoppers trying to make greener choices, small sustainable brands, and "
            "store owners who need a defensible way to show product impact."
        ),
        "why_matters": (
            "Sustainability claims are hard to compare and easy to fake, so a "
            "transparent score with provenance helps buyers without pretending the "
            "estimate is exact."
        ),
        "approaches": [
            "Use Open Food Facts Green-Score data for food with attribution, caching, and coverage checks.",
            "Publish a transparent internal scoring method for non-food items instead of inventing authority.",
            "Show greener alternatives from the same category and the one or two factors that improved the score.",
            "Estimate cart footprint from weight, transport assumptions, and packaging, and surface missing data.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Green shopping becomes a cited comparison instead of a label, because "
                "every score shows its source and its uncertainty."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A green leaf on a package is marketing until you can trace the "
                        "number behind it."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Environmental claims are inconsistent. Shoppers cannot compare "
                        "products, and stores have no defensible way to show impact "
                        "without inventing authority."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We use Open Food Facts Green-Score for food with attribution "
                        "and show missing coverage. Non-food items use a transparent "
                        "internal method. The cart gives a footprint range, and "
                        "alternatives explain the one factor that improves."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Open a product, show the source and date, compare a greener "
                        "alternative, add both to the cart, and show the estimated range "
                        "plus a product with missing data."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "More categories, supplier packaging data, regional transport "
                        "factors, and third-party method review."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How accurate is the carbon estimate?",
                    "answer": (
                        "It is an estimate with a range, not a measurement. We show the "
                        "factors, the missing inputs, and the source date so users can "
                        "judge how much to trust it."
                    ),
                },
                {
                    "question": "What about products with no score?",
                    "answer": (
                        "We show unknown instead of guessing. A missing score never "
                        "becomes a green recommendation, and the UI explains what data "
                        "would be needed."
                    ),
                },
                {
                    "question": "How do you avoid greenwashing?",
                    "answer": (
                        "Every score has a source or a documented method. We surface "
                        "uncertainty and avoid claims the data cannot support. Non-food "
                        "scoring is clearly labelled as our own method."
                    ),
                },
                {
                    "question": "Why not use an AI model to score everything?",
                    "answer": (
                        "An opaque model would make the trust problem worse. A cited "
                        "public score plus a transparent internal method is easier to "
                        "audit and explain."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Decide what the score can honestly claim",
                "summary": (
                    "The greenest-looking app can be the least trustworthy one."
                ),
                "steps": [
                    "Separate food scores from non-food scores and document the source of each.",
                    "Read the Open Food Facts Green-Score terms and plan attribution and caching.",
                    "Write the internal non-food method, including weights and missing-data behavior.",
                    "Add a visible 'estimate, not certification' notice to the product UI.",
                ],
            },
            {
                "title": "Product catalogue and score badges",
                "summary": (
                    "A score needs context to be useful."
                ),
                "steps": [
                    "Import or search a small product set with category, price, and packaging fields.",
                    "Show the score with a source, a date, and a plain-language explanation.",
                    "Handle unknown and low-coverage products without inventing a number.",
                    "Add category filters and a comparison view.",
                ],
            },
            {
                "title": "Greener alternatives",
                "summary": (
                    "A score only changes behavior when a better option is easy to find."
                ),
                "steps": [
                    "Find same-category alternatives with a better score or a lower footprint.",
                    "Explain the one or two factors that make the alternative greener.",
                    "Avoid recommending a product with missing data as if it were better.",
                    "Add a clear path from the original product to the alternative.",
                ],
            },
            {
                "title": "Cart footprint and packaging",
                "summary": (
                    "The cart estimate is useful only when the assumptions are visible."
                ),
                "steps": [
                    "Compute a per-item footprint from the available weight and transport factors.",
                    "Add packaging flags and a cart-level estimate with a range.",
                    "Show which items lack enough data to estimate.",
                    "Let the user compare the cart with a greener swap.",
                ],
            },
            {
                "title": "Demo without greenwashing",
                "summary": (
                    "The pitch should be as careful as the product."
                ),
                "steps": [
                    "Seed Indian products where possible and include a missing-data example.",
                    "Show one score, one greener alternative, and one cart-estimate explanation.",
                    "Put the method, source date, and limits on screen during the demo.",
                    "Rehearse the answer to 'how do you know this is accurate?'",
                ],
            },
        ],
    },
    "manabi-web-hackathon-012": {
        "summary": (
            "Build an interactive map that lets non-experts compare NASA satellite "
            "images of the same place over time. A time slider and a side-by-side view "
            "make change easy to see.\n\n"
            "Short plain-language notes explain what each layer shows and what it "
            "cannot show. The app starts from ready-made NASA GIBS or Worldview tiles, "
            "keeps credits visible, and warns that seasons, clouds, and processing can "
            "change the colors too."
        ),
        "who_affected": (
            "Students, educators, journalists, and local communities who want to "
            "understand environmental change without a remote-sensing background."
        ),
        "why_matters": (
            "Climate and land data are public but scattered across technical portals, "
            "so a guided comparison makes change visible and discussable."
        ),
        "approaches": [
            "Start with ready-made NASA GIBS or Worldview tile layers instead of raw science files.",
            "Add a time slider with preloading so comparing dates does not feel broken.",
            "Offer side-by-side or swipe comparison with locked dates and a shared location.",
            "Write short explainers for what each layer measures, and cache tiles and credits under the data terms.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Earth observation data becomes a clear before-and-after story, with "
                "the credit and caveats built into the screen."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "The evidence of environmental change already exists in public "
                        "NASA data. Most people have never seen it arranged as a story."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Scientific portals are built for researchers. Raw layers are "
                        "hard to compare, dates are confusing, and a pretty map can "
                        "easily suggest the wrong conclusion."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We use ready-made NASA tile layers with a time slider and a "
                        "split comparison. Each layer has a plain-language explanation, "
                        "a legend, and a limitation note, so people can see change "
                        "without overclaiming."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Start global, choose a location, compare two dates side by "
                        "side, and read the explainer. Show the source credit and the "
                        "caveat during the demo."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Guided tours, local datasets, annotation layers, and "
                        "classroom-ready explainer packs."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "What do the colors actually mean?",
                    "answer": (
                        "Each layer has its own legend and explainer. We state what is "
                        "measured and warn that seasons, clouds, and processing can "
                        "affect the color as well as long-term change."
                    ),
                },
                {
                    "question": "How current is the data?",
                    "answer": (
                        "Each layer has a valid date range and a source timestamp. We "
                        "show the selected date and the source credit instead of "
                        "implying the map is real-time."
                    ),
                },
                {
                    "question": "Why not build on NASA Worldview directly?",
                    "answer": (
                        "Worldview is a strong scientific tool. We focus on a guided "
                        "comparison and explanation for non-experts, which is a "
                        "different product from a full data portal."
                    ),
                },
                {
                    "question": "How do you handle slow tiles?",
                    "answer": (
                        "We preload adjacent dates, show loading states, and cache the "
                        "demo dates. The pitch also has a recorded fallback in case the "
                        "venue network fails."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Choose three layers and a usable date range",
                "summary": (
                    "A focused explorer beats a map with fifty unexplained toggles."
                ),
                "steps": [
                    "Pick vegetation, temperature, and one air-quality or aerosol layer.",
                    "Check the available dates and tile resolution for each layer.",
                    "Read the NASA GIBS or Worldview attribution and caching guidance.",
                    "Write one sentence for what each layer measures and one for its limitation.",
                ],
            },
            {
                "title": "Build the time slider map",
                "summary": (
                    "Scrubbing time is the core interaction, so it must feel immediate."
                ),
                "steps": [
                    "Render a base map and one selected tile layer with a visible date.",
                    "Add a slider limited to the valid dates for that layer.",
                    "Preload adjacent dates and show a loading state when tiles are late.",
                    "Keep the map location stable while dates change.",
                ],
            },
            {
                "title": "Add comparison mode",
                "summary": (
                    "Change is easier to see when two dates share the screen."
                ),
                "steps": [
                    "Add a split or side-by-side view with two date controls.",
                    "Allow the user to lock one date and scrub the other.",
                    "Keep the legend consistent across both sides.",
                    "Handle layers with different date coverage gracefully.",
                ],
            },
            {
                "title": "Explain the colors",
                "summary": (
                    "A beautiful layer without interpretation invites wrong "
                    "conclusions."
                ),
                "steps": [
                    "Add an in-context legend and a short explainer panel for each layer.",
                    "State that color changes can reflect seasons, clouds, or processing as well as long-term change.",
                    "Credit NASA and link the source dataset.",
                    "Add a missing-data and low-resolution warning where relevant.",
                ],
            },
            {
                "title": "Demo one local change story",
                "summary": (
                    "Pick a place and a date pair that produce a clear, honest "
                    "comparison."
                ),
                "steps": [
                    "Seed three locations with contrasting but defensible stories.",
                    "Rehearse the move from overview to one location to comparison.",
                    "Show the explainer and limitation text during the pitch.",
                    "Cache the demo dates so the venue network cannot break the story.",
                ],
            },
        ],
    },
}
