"""Curated team plans, pitch kits, and new briefs for Web Dev hackathons.

The 22-project list comes from ``webdev_projects.md``. Thirteen of those
projects already exist as resume briefs, so the seed composer reuses their
curated summaries, approaches, and build guides. The nine projects in
``NEW_PROJECTS`` only exist on the hackathon track and are documented here.
"""


NEW_PROJECTS = {
    3: dict(
        title="Skill Exchange Matching Platform",
        summary=(
            "Build a skill barter platform where people list what they can teach "
            "and what they want to learn. Match reciprocal pairs and three-way "
            "cycles, schedule sessions, and add ratings plus a report button."
        ),
        who_affected=(
            "Students, hobbyists, freelancers, and community groups who want to "
            "learn a practical skill without paying for a course."
        ),
        why_matters=(
            "Useful knowledge is unevenly distributed, while money and formal "
            "courses block many learners. A trustworthy exchange turns unused "
            "teaching capacity into real learning."
        ),
        field="web-dev",
        domain="education",
        difficulty="intermediate",
        est_hours=70,
        tech_tags=[
            "typescript",
            "react",
            "postgres",
            "matching",
            "scheduling",
            "websockets",
        ],
        datasets=[{"name": "Sample member skills and availability", "url": None}],
        approaches=[
            "Model each person as a set of offered and wanted skills with a proficiency level and availability.",
            "Find two-way swaps first, then use a bounded search for three-way cycles where no direct pair exists.",
            "Explain every match with the exact skills exchanged and why both people are a fit.",
            "Add request, accept, decline, scheduling, completion, rating, report, and block flows.",
            "Rate-limit requests and suppress duplicate matches so the graph does not turn into spam.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "People list skills they can teach and skills they want to learn. "
            "The platform matches reciprocal pairs and three-way cycles, then "
            "schedules sessions, with ratings and a report button."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Model the exchange before writing UI",
                "summary": "The match is the product. Nail the skills graph and the request lifecycle first.",
                "steps": [
                    "Define profile, offered skill, wanted skill, availability, and request states on paper.",
                    "Decide how proficiency and preferred format (online or in person) affect a match.",
                    "Write the allowed request transitions: pending, accepted, declined, completed, cancelled.",
                    "List the safety rules: report, block, contact limits, and what is shown publicly.",
                ],
            },
            {
                "title": "Build the skill graph",
                "summary": "A small realistic graph is enough to prove the matching idea.",
                "steps": [
                    "Create profile and skill tables with a normalized skill name and a free-text note.",
                    "Build profile editing and a searchable list of offered skills.",
                    "Seed 20-30 profiles containing a deliberate two-way pair and one three-way cycle.",
                    "Write queries that list candidates for a person, with the direction of each skill edge.",
                ],
            },
            {
                "title": "Match, rank, and explain",
                "summary": "A match without an explanation looks like random luck and will not be trusted.",
                "steps": [
                    "Implement direct pair matching by intersecting wanted and offered skills.",
                    "Add a depth-limited cycle search for three-person exchanges.",
                    "Score matches with skill overlap, availability overlap, and a reciprocity signal.",
                    "Show a match card that spells out who teaches what to whom and why it qualified.",
                ],
            },
            {
                "title": "Requests, sessions, and trust",
                "summary": "The exchange must survive acceptance, scheduling, and a bad experience.",
                "steps": [
                    "Implement request accept or decline, with duplicate and spam suppression.",
                    "Add session scheduling with time zones, reminders, and a completion confirmation.",
                    "Add ratings and a private report flow; make blocking remove future matches.",
                    "Rate-limit outgoing requests and test that declining does not create a loop.",
                ],
            },
            {
                "title": "Make the demo obvious",
                "summary": "Show a pair and a cycle, not just a profile page.",
                "steps": [
                    "Seed one obvious two-way match and one three-way cycle with readable names.",
                    "Rehearse the path from editing skills to an explained match and an accepted session.",
                    "Test the empty and no-match states so the demo never shows a blank screen.",
                    "Capture screenshots of the match explanations for the pitch deck.",
                ],
            },
        ],
    ),
    7: dict(
        title="Nonprofit Volunteer & Donor Management Hub",
        summary=(
            "Give a small nonprofit one place to manage volunteer sign-ups and "
            "shifts, donor pledges and receipts, and beneficiary records, with "
            "role-based access and a simple impact report."
        ),
        who_affected=(
            "Small nonprofit staff, volunteers, recurring donors, and the "
            "beneficiaries whose services depend on reliable coordination."
        ),
        why_matters=(
            "Small organizations often run on spreadsheets, messaging groups, and "
            "memory. Missed shifts and forgotten donor follow-ups cost time and "
            "trust that they cannot spare."
        ),
        field="web-dev",
        domain="social-impact",
        difficulty="intermediate",
        est_hours=85,
        tech_tags=[
            "typescript",
            "react",
            "postgres",
            "rbac",
            "notifications",
            "reporting",
        ],
        datasets=[{"name": "Sample nonprofit volunteer and donor data", "url": None}],
        approaches=[
            "Model volunteers, shifts, sign-ups, donors, pledges, receipts, and beneficiaries as separate records.",
            "Give staff, volunteers, and finance different permissions enforced in the API, not only the UI.",
            "Send shift reminders and donor follow-ups from a small notification queue with a visible log.",
            "Generate an impact report from aggregate volunteer hours, donations, and people served.",
            "Keep beneficiary records private and show only aggregate numbers unless a role needs details.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "Helps a real nonprofit manage volunteers (sign-ups, shifts, "
            "reminders), donors (pledges, receipts, follow-ups) and "
            "beneficiaries, with role-based access and a simple impact report."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Interview first, model second",
                "summary": "A nonprofit hub fails when it models an imaginary organization.",
                "steps": [
                    "Interview one real nonprofit or use a detailed fictional brief with real workflows.",
                    "List the nouns: volunteer, shift, sign-up, donor, pledge, receipt, beneficiary, program.",
                    "Draw the three roles and the exact actions each role can take.",
                    "Write explicit non-goals such as payroll, accounting, and medical records.",
                ],
            },
            {
                "title": "Volunteer shifts and sign-ups",
                "summary": "The volunteer path is the most visible daily workflow.",
                "steps": [
                    "Create shifts with a program, location, start, end, and capacity.",
                    "Let a volunteer sign up, cancel, and see their upcoming shifts.",
                    "Prevent double booking and waitlist a full shift instead of silently rejecting people.",
                    "Add reminders and a simple attendance check-in for staff.",
                ],
            },
            {
                "title": "Donors, pledges, and receipts",
                "summary": "Trust depends on a clean record of what was promised and what was received.",
                "steps": [
                    "Record donors and pledges with amount, date, campaign, and status.",
                    "Generate a receipt record without storing real card data.",
                    "Add follow-up notes and a next-action date for staff.",
                    "Show totals by campaign and flag overdue pledges without pretending they are received.",
                ],
            },
            {
                "title": "Permissions and the impact report",
                "summary": "Sensitive beneficiary data is the main reason this needs real roles.",
                "steps": [
                    "Enforce staff, volunteer, and finance permissions in every relevant endpoint.",
                    "Aggregate volunteer hours, donation totals, and people served by program.",
                    "Build a one-page impact report with filters and an export for the board.",
                    "Test that a volunteer cannot read donor or beneficiary records.",
                ],
            },
            {
                "title": "Demo with credible operations",
                "summary": "The demo should tell one complete story for each role.",
                "steps": [
                    "Seed a small organization with two programs, ten volunteers, and five donors.",
                    "Demo a shift sign-up, a donor pledge, a finance check, and the impact report.",
                    "Show the permission boundary by attempting a forbidden action.",
                    "Rehearse the five-minute story and prepare the data reset command.",
                ],
            },
        ],
    ),
    8: dict(
        title="NGO Impact Dashboard",
        summary=(
            "Let small organizations upload program data as CSV and turn it into "
            "impact metrics, trends, and a map of underserved areas so they can "
            "decide where limited resources should go next."
        ),
        who_affected=(
            "Small NGO program managers and funders who have field data but no "
            "in-house analyst or business-intelligence team."
        ),
        why_matters=(
            "The data usually exists in spreadsheets, but it is not shaped into "
            "decisions. A clear dashboard helps a small team see coverage gaps "
            "without hiring an analyst."
        ),
        field="web-dev",
        domain="social-impact",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=[
            "typescript",
            "react",
            "postgres",
            "csv-import",
            "charts",
            "geospatial",
        ],
        datasets=[{"name": "Sample program and region CSV", "url": None}],
        approaches=[
            "Start from five decision questions and a documented data dictionary, not a chart gallery.",
            "Upload a CSV, preview the column mapping, and reject invalid rows with specific messages.",
            "Compute program metrics and period-over-period trends from the imported records.",
            "Aggregate coverage by region and join a population estimate to highlight underserved areas.",
            "Show data quality, coverage, and the source date beside every conclusion.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "Small organisations upload program data (CSV) and get impact "
            "metrics, trends and a map of underserved areas, so they can decide "
            "where to spend limited resources."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Choose the decisions before the charts",
                "summary": "A dashboard is only useful if it changes what someone does next.",
                "steps": [
                    "Write five questions a program manager would actually ask this data.",
                    "Define one metric per question, including its numerator, denominator, and period.",
                    "Document the expected CSV columns and how missing values are treated.",
                    "Agree what must stay private and what can appear in an aggregate view.",
                ],
            },
            {
                "title": "Make CSV upload trustworthy",
                "summary": "Bad rows are the fastest way to lose a nonprofit's confidence.",
                "steps": [
                    "Build upload, header detection, and a column-mapping preview.",
                    "Validate types, dates, region names, and duplicates before import.",
                    "Show a per-row error report and let the user fix and retry.",
                    "Store the original file metadata and the import timestamp.",
                ],
            },
            {
                "title": "Metrics and trends",
                "summary": "The first screen should answer the most common question without a filter hunt.",
                "steps": [
                    "Compute program totals and per-period changes from imported records.",
                    "Add filters for program, region, and date range.",
                    "Add drill-down from a chart to the rows behind it.",
                    "Handle sparse periods explicitly instead of drawing fake zeroes.",
                ],
            },
            {
                "title": "Coverage map and underserved areas",
                "summary": "A map earns its place when it joins need to service coverage.",
                "steps": [
                    "Aggregate served people or activities by region.",
                    "Join a population or need estimate and calculate a coverage indicator.",
                    "Render a choropleth or region table with a clear legend and missing-data state.",
                    "Explain that the indicator is descriptive, not proof of causation.",
                ],
            },
            {
                "title": "Demo the insight, not the dashboard",
                "summary": "Judges remember a decision, not a wall of widgets.",
                "steps": [
                    "Seed three programs with realistic regional gaps and a messy import example.",
                    "Show one import error being fixed and then the resulting coverage insight.",
                    "Add a short data-quality and assumptions panel.",
                    "Rehearse the one-minute story: question, evidence, next action.",
                ],
            },
        ],
    ),
    12: dict(
        title="Green Shopping Platform with Environmental Scores",
        summary=(
            "Build an online store that shows each product's environmental score, "
            "suggests greener alternatives, estimates the carbon footprint of a "
            "cart, and flags sustainable packaging."
        ),
        who_affected=(
            "Shoppers trying to make greener choices, small sustainable brands, "
            "and store owners who need a defensible way to present product impact."
        ),
        why_matters=(
            "Sustainability claims are hard to compare and easy to fake. A "
            "transparent score with provenance helps buyers choose without "
            "pretending the estimate is perfect."
        ),
        field="web-dev",
        domain="climate",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=[
            "typescript",
            "react",
            "postgres",
            "open-food-facts",
            "caching",
            "data-visualization",
        ],
        datasets=[
            {"name": "Open Food Facts product sample", "url": "https://world.openfoodfacts.org/data"}
        ],
        approaches=[
            "Use Open Food Facts Green-Score data for food with attribution, caching, and coverage checks.",
            "For non-food items, publish a transparent internal scoring method instead of inventing authority.",
            "Show greener alternatives from the same category with the factor that improved the score.",
            "Estimate cart footprint from product weight, transport assumptions, and packaging.",
            "Surface missing data and uncertainty so a weak score is not mistaken for a strong claim.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "An online store that shows each product's sustainability score, "
            "suggests greener alternatives, estimates the carbon footprint of a "
            "cart and flags sustainable packaging."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Decide what the score can honestly claim",
                "summary": "The greenest-looking app can be the least trustworthy one.",
                "steps": [
                    "Separate food scores from non-food scores and document the source of each.",
                    "Read the Open Food Facts Green-Score terms and plan attribution and caching.",
                    "Write the internal non-food method, including weights and missing-data behavior.",
                    "Add a visible 'estimate, not certification' notice to the product UI.",
                ],
            },
            {
                "title": "Product catalogue and score badges",
                "summary": "The score needs context to be useful.",
                "steps": [
                    "Import or search a small product set with category, price, and packaging fields.",
                    "Show the score with a source, date, and plain-language explanation.",
                    "Handle unknown and low-coverage products without inventing a number.",
                    "Add category filters and a comparison view.",
                ],
            },
            {
                "title": "Greener alternatives",
                "summary": "A score only changes behavior if a better option is easy to find.",
                "steps": [
                    "Find same-category alternatives with a better score or lower footprint.",
                    "Explain the one or two factors that make the alternative greener.",
                    "Avoid recommending a product with missing data as if it were better.",
                    "Add a clear path from the original product to the alternative.",
                ],
            },
            {
                "title": "Cart footprint and packaging",
                "summary": "The cart estimate is useful only when the assumptions are visible.",
                "steps": [
                    "Compute a per-item footprint from the available weight and transport factors.",
                    "Add packaging flags and a cart-level estimate with a range.",
                    "Show which items lack enough data to estimate.",
                    "Let the user compare the cart with a greener swap.",
                ],
            },
            {
                "title": "Demo without greenwashing",
                "summary": "The pitch should be as careful as the product.",
                "steps": [
                    "Seed Indian products where possible and include a missing-data example.",
                    "Show one score, one greener alternative, and one cart-estimate explanation.",
                    "Put the method, source date, and limitations on screen during the demo.",
                    "Rehearse the answer to 'how do you know this is accurate?'",
                ],
            },
        ],
    ),
    13: dict(
        title="Earth Change Explorer",
        summary=(
            "Build an interactive map that compares NASA Earth observation layers "
            "over time, with a time slider, side-by-side comparison, and "
            "plain-language explanations for non-experts."
        ),
        who_affected=(
            "Students, educators, journalists, and local communities trying to "
            "understand environmental change without a remote-sensing background."
        ),
        why_matters=(
            "Climate and land data are public but scattered across technical "
            "portals. A guided comparison makes change visible and discussable."
        ),
        field="web-dev",
        domain="climate",
        difficulty="intermediate",
        est_hours=75,
        tech_tags=[
            "typescript",
            "react",
            "map-tiles",
            "nasa-gibs",
            "time-series",
            "caching",
        ],
        datasets=[{"name": "NASA Earth observation tile layers", "url": "https://earthdata.nasa.gov/"}],
        approaches=[
            "Start with ready-made NASA GIBS or Worldview tile layers instead of raw science files.",
            "Add a time slider with preloading so comparing dates does not feel broken.",
            "Provide side-by-side or swipe comparison with locked dates and a shared location.",
            "Write short explainers for what each layer measures and what it cannot show.",
            "Cache tiles and credits, and follow the data service's usage terms.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "An interactive map that compares NASA Earth observation layers over "
            "time (vegetation, temperature, aerosols) with a time slider and "
            "side-by-side comparison, plus short explanations for non-experts."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Choose three layers and a usable date range",
                "summary": "A focused explorer beats a map with fifty unexplained toggles.",
                "steps": [
                    "Pick vegetation, temperature, and one air-quality or aerosol layer.",
                    "Check the available dates and tile resolution for each layer.",
                    "Read the NASA GIBS or Worldview attribution and caching guidance.",
                    "Write one sentence for what each layer measures and one for its limitation.",
                ],
            },
            {
                "title": "Build the time slider map",
                "summary": "Scrubbing time is the core interaction, so it must feel immediate.",
                "steps": [
                    "Render a base map and one selected tile layer with a visible date.",
                    "Add a slider constrained to the valid dates for that layer.",
                    "Preload adjacent dates and show a loading state when tiles are late.",
                    "Keep the map location stable while dates change.",
                ],
            },
            {
                "title": "Add comparison mode",
                "summary": "The change is easier to see when two dates are on screen together.",
                "steps": [
                    "Add a split or side-by-side view with two date controls.",
                    "Allow the user to lock one date and scrub the other.",
                    "Keep the legend consistent across both sides.",
                    "Handle layers with different date coverage gracefully.",
                ],
            },
            {
                "title": "Explain the colors",
                "summary": "A beautiful layer without interpretation invites wrong conclusions.",
                "steps": [
                    "Add an in-context legend and a short explainer panel per layer.",
                    "State that color changes can reflect seasons, clouds, or processing, not only long-term change.",
                    "Credit NASA and link the source dataset.",
                    "Add a missing-data and low-resolution warning where relevant.",
                ],
            },
            {
                "title": "Demo one local change story",
                "summary": "Pick a place and a date pair that produce a clear, honest comparison.",
                "steps": [
                    "Seed three locations with contrasting but defensible stories.",
                    "Rehearse the transition from overview to one location to comparison.",
                    "Show the explainer and limitation text during the pitch.",
                    "Cache the demo dates so the venue network cannot break the story.",
                ],
            },
        ],
    ),
    15: dict(
        title="Journey Safety Share",
        summary=(
            "Let someone share a live trip with trusted contacts for a limited "
            "time. Alert those contacts if the traveller leaves the expected "
            "route, stops for too long, or misses a check-in."
        ),
        who_affected=(
            "People travelling alone at night, parents, late-shift workers, and "
            "friends or family acting as trusted contacts."
        ),
        why_matters=(
            "A quick 'text me when you're home' is fragile. A shared trip with "
            "clear check-ins gives contacts useful context without constant "
            "manual updates."
        ),
        field="web-dev",
        domain="social-impact",
        difficulty="intermediate",
        est_hours=75,
        tech_tags=[
            "typescript",
            "react",
            "geolocation",
            "realtime",
            "sms",
            "notifications",
        ],
        datasets=[{"name": "Sample trip route and check-in schedule", "url": None}],
        approaches=[
            "Create a share link with an explicit expiry, destination, and contact list.",
            "Update location only while the share page is open, and say that limitation clearly.",
            "Use check-in timers and simple route-bound or dwell-time rules instead of promising background tracking.",
            "Notify contacts through an in-app view and an SMS or email fallback.",
            "Let the traveller revoke the share immediately and delete location history after expiry.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "Share a live trip with trusted contacts for a limited time. "
            "Contacts are alerted automatically if you leave the route, stop for "
            "too long or miss a check-in."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Define the safety contract",
                "summary": "The app must be clear about what it can and cannot detect.",
                "steps": [
                    "Write what a share contains, who can see it, and when it expires.",
                    "Choose a check-in interval and a grace period before alerting.",
                    "State that mobile browsers may pause location in the background.",
                    "Add consent, revoke, and delete-history controls before building the map.",
                ],
            },
            {
                "title": "Build the live share page",
                "summary": "The contact view should work on an ordinary phone browser.",
                "steps": [
                    "Let the traveller create a trip from a start, destination, and route estimate.",
                    "Show the latest location and last-updated time on a simple map.",
                    "Add a check-in button and an obvious 'I'm safe' completion action.",
                    "Test the view on a narrow mobile screen with slow updates.",
                ],
            },
            {
                "title": "Add three useful alerts",
                "summary": "Three understandable rules beat a vague promise of AI safety.",
                "steps": [
                    "Alert when a check-in is missed past the grace period.",
                    "Alert when the traveller stops moving for longer than expected.",
                    "Alert when the location moves far from the expected route corridor.",
                    "Add a false-alarm dismissal and test that the alert is not sent twice.",
                ],
            },
            {
                "title": "Fallbacks and privacy",
                "summary": "A safety tool that depends on perfect connectivity is not safe.",
                "steps": [
                    "Show the contact a manual refresh and a last-known-state message.",
                    "Add an SMS or email fallback for the most important alert.",
                    "Delete or anonymize location history at expiry.",
                    "Test that a revoked link stops updating immediately.",
                ],
            },
            {
                "title": "Rehearse a two-device demo",
                "summary": "The story works when the audience sees both sides at once.",
                "steps": [
                    "Open the traveller view on one device and the contact view on another.",
                    "Trigger a late check-in and a stop alert in a controlled way.",
                    "Show the revoke action and the expired-link state.",
                    "Prepare a recorded backup in case geolocation is blocked at the venue.",
                ],
            },
        ],
    ),
    19: dict(
        title="Real-Time Collaborative Pixel Canvas",
        summary=(
            "Build a multiplayer pixel canvas inspired by r/place: users place "
            "pixels in real time over WebSockets, with cooldown timers, live "
            "cursors, abuse limits, and a timelapse replay of the board's history."
        ),
        who_affected=(
            "Online communities, classrooms, event organizers, and anyone who "
            "wants a lightweight shared creative space."
        ),
        why_matters=(
            "A shared canvas looks simple but requires consistent state, fair "
            "rate limits, and a history that makes every pixel explainable."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=[
            "typescript",
            "react",
            "websockets",
            "canvas",
            "realtime",
            "rate-limiting",
        ],
        datasets=[{"name": "Sample canvas palette and event history", "url": None}],
        approaches=[
            "Keep the server authoritative for the canvas grid and broadcast each accepted pixel event.",
            "Store an append-only event history so the canvas can be rebuilt and replayed.",
            "Add a per-user cooldown and per-IP rate limits, enforced server-side.",
            "Show live cursors and recently active users without exposing unnecessary identity data.",
            "Add moderation tools for overwriting abusive art and a timelapse scrubber.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "A multiplayer pixel canvas inspired by r/place. Users place pixels "
            "in real time over WebSockets, with cooldown timers, live cursors, "
            "abuse limits and a timelapse replay of the board's history."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Choose the canvas contract",
                "summary": "The server owns the truth; the client only draws it.",
                "steps": [
                    "Choose a grid size, palette, and event shape: x, y, color, user, timestamp.",
                    "Decide how the server validates placement and rejects stale or duplicate events.",
                    "Write the cooldown rule per user and the fallback rule when identity is unknown.",
                    "Define how the full canvas is loaded on first join.",
                ],
            },
            {
                "title": "Make the realtime loop work",
                "summary": "A pixel should appear for everyone before the user has time to doubt it.",
                "steps": [
                    "Open a WebSocket, send accepted pixels, and broadcast them to every client.",
                    "Draw the canvas once, then patch individual cells instead of redrawing everything.",
                    "Add reconnect and resync so a dropped connection does not fork the board.",
                    "Show a visible cooldown timer after a placement.",
                ],
            },
            {
                "title": "Cursors, cooldowns, and abuse limits",
                "summary": "The social layer is what makes the canvas feel alive and fair.",
                "steps": [
                    "Broadcast lightweight cursor positions with a short expiry.",
                    "Enforce cooldown and rate limits in the server, never only in the client.",
                    "Add a moderation action that can overwrite or roll back a region.",
                    "Test a scripted spam attempt and confirm it is throttled.",
                ],
            },
            {
                "title": "History and timelapse",
                "summary": "The append-only event log is both an audit trail and a feature.",
                "steps": [
                    "Store each accepted pixel event with a sequence number and timestamp.",
                    "Rebuild the canvas from events at an arbitrary point in time.",
                    "Add a scrubber and a play control for the timelapse.",
                    "Compress or snapshot old history so the replay stays fast.",
                ],
            },
            {
                "title": "Demo a crowd, not a single click",
                "summary": "The magic is visible when several clients act at once.",
                "steps": [
                    "Seed a recognizable starting image and a short event history.",
                    "Open two or three browser windows and place pixels while the audience watches.",
                    "Trigger a cooldown and show the moderation rollback.",
                    "Play the timelapse as the closing beat.",
                ],
            },
        ],
    ),
    22: dict(
        title="Crowd-Reactive Music Visualizer",
        summary=(
            "Build a browser app that measures crowd movement energy from the "
            "webcam using frame differencing, then adapts music and visuals "
            "through the Web Audio API, with a panel that explains what changed."
        ),
        who_affected=(
            "Party and event organizers, installation artists, dancers, and "
            "educators demonstrating responsive media without face recognition."
        ),
        why_matters=(
            "Responsive visuals usually depend on opaque AI or manual controls. "
            "Motion-only sensing creates a playful feedback loop while avoiding "
            "identity analysis."
        ),
        field="web-dev",
        domain="other",
        difficulty="advanced",
        est_hours=120,
        tech_tags=[
            "typescript",
            "webcam",
            "canvas",
            "web-audio",
            "web-workers",
            "signal-processing",
        ],
        datasets=[{"name": "Sample crowd motion clip", "url": None}],
        approaches=[
            "Downscale webcam frames and compare consecutive frames to estimate motion energy.",
            "Smooth the signal so one hand wave does not produce a chaotic audio jump.",
            "Map energy bands to a few musical layers and visual parameters rather than every possible control.",
            "Show a transparency panel with the measured value, current band, and why the music changed.",
            "Avoid face detection, recording, or uploads; process frames locally and provide a camera-off mode.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "A browser app that uses the webcam to measure crowd movement energy "
            "(frame differencing, no face recognition) and adapts music and "
            "visuals through the Web Audio API, with a transparent panel showing "
            "what it measures and why the music changed."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Measure motion, never faces",
                "summary": "The privacy boundary is part of the product, not a disclaimer added later.",
                "steps": [
                    "Capture frames locally and compare consecutive downscaled grayscale frames.",
                    "Compute a motion score from changed pixels and smooth it over a short window.",
                    "Display the score and a small threshold meter so the user can calibrate.",
                    "Write and show a 'no face recognition, no recording, no upload' notice.",
                ],
            },
            {
                "title": "Map motion to music",
                "summary": "A few stable layers sound intentional; constant random changes sound broken.",
                "steps": [
                    "Create a small Web Audio graph with a base loop and two or three intensity layers.",
                    "Map smoothed energy bands to layer gain, filter, or tempo with gradual transitions.",
                    "Add a manual sensitivity slider and a mute control.",
                    "Ensure audio starts only after a user gesture and recovers from a blocked context.",
                ],
            },
            {
                "title": "Make the visuals respond",
                "summary": "The visual should explain the audio change, not compete with it.",
                "steps": [
                    "Draw a simple canvas visual whose speed and density follow the same energy bands.",
                    "Avoid rapid flashing and respect reduced-motion preferences.",
                    "Show the current band and the mapped musical change in the transparency panel.",
                    "Test the app with a still frame, one moving person, and a busy crowd.",
                ],
            },
            {
                "title": "Calibrate instead of guessing",
                "summary": "Every room has a different baseline, so the app must adapt.",
                "steps": [
                    "Record a short baseline while the room is still and set the zero point.",
                    "Apply hysteresis so small changes do not flip bands constantly.",
                    "Add a reset-calibration action and show when calibration is stale.",
                    "Log the measured values during rehearsal to tune the thresholds.",
                ],
            },
            {
                "title": "Demo with a safe fallback",
                "summary": "Camera permissions and venue lighting are the two most likely demo failures.",
                "steps": [
                    "Prepare a recorded motion clip that can drive the visual if the webcam fails.",
                    "Rehearse the explanation of the motion metric before the music starts.",
                    "Test with the projector and house audio at realistic volume.",
                    "Have a silent visual-only mode ready.",
                ],
            },
        ],
    ),
    33: dict(
        title="Seismic Activity Explorer & b-Value Analyzer",
        summary=(
            "Build a live earthquake map from the USGS feed with filters, plus a "
            "statistics view that plots magnitude-frequency data and estimates the "
            "Gutenberg-Richter b-value and its uncertainty for any region and "
            "time window."
        ),
        who_affected=(
            "Earth-science students, educators, journalists, and local planners "
            "who need to inspect a seismic catalogue rather than just view dots."
        ),
        why_matters=(
            "A map alone hides whether a catalogue is complete enough for "
            "analysis. Showing b-value with uncertainty and a completeness check "
            "turns a visual into a defensible estimate."
        ),
        field="web-dev",
        domain="climate",
        difficulty="intermediate",
        est_hours=85,
        tech_tags=[
            "typescript",
            "react",
            "usgs-feed",
            "statistics",
            "charts",
            "geospatial",
        ],
        datasets=[{"name": "USGS earthquake catalogue feed", "url": "https://earthquake.usgs.gov/earthquakes/feed/"}],
        approaches=[
            "Fetch and cache the USGS feed, then filter by region, time window, depth, and magnitude.",
            "Plot the magnitude-frequency distribution on a log scale with the fitted line.",
            "Estimate the b-value with a maximum-likelihood method and report a confidence interval.",
            "Estimate the magnitude of completeness and warn when the sample is too incomplete or too small.",
            "Show the feed timestamp, filter summary, and method notes beside every result.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development hackathon brief.",
        original_text=(
            "A live map of recent earthquakes from the public USGS feed with "
            "filters, plus a statistics view that plots magnitude-frequency data "
            "and estimates the Gutenberg-Richter b-value, with its uncertainty, "
            "for any region and time window. It warns when the catalogue is too "
            "incomplete to trust the result."
        ),
        ai_fields=[
            "field",
            "domain",
            "difficulty",
            "est_hours",
            "who_affected",
            "why_matters",
            "tech_tags",
        ],
        build_guide=[
            {
                "title": "Ingest and filter the catalogue",
                "summary": "Science starts with a clear, reproducible filter.",
                "steps": [
                    "Fetch the USGS feed, cache the response, and record its timestamp.",
                    "Add region, date range, magnitude, and depth filters.",
                    "Display the event count for the current filter before any analysis.",
                    "Read the feed's usage terms and keep the request rate modest.",
                ],
            },
            {
                "title": "Plot magnitude frequency",
                "summary": "The Gutenberg-Richter relation is easiest to judge on a log scale.",
                "steps": [
                    "Bin events by magnitude and count how many meet or exceed each bin.",
                    "Plot the cumulative counts on a logarithmic frequency axis.",
                    "Show the filter summary and the number of events in the plot.",
                    "Handle empty and single-event filters explicitly.",
                ],
            },
            {
                "title": "Estimate b-value and uncertainty",
                "summary": "A number without an interval is not an analysis.",
                "steps": [
                    "Implement the maximum-likelihood b-value for the filtered catalogue.",
                    "Bootstrap or otherwise estimate a confidence interval.",
                    "Show the fitted line and the estimate on the chart.",
                    "Explain the method and its assumptions in a short note.",
                ],
            },
            {
                "title": "Check completeness before trusting the result",
                "summary": "The most common seismic-analysis mistake is skipping the completeness check.",
                "steps": [
                    "Estimate the magnitude of completeness for the current catalogue.",
                    "Flag small samples, gaps, and catalogues dominated by tiny events.",
                    "Disable or caveat the b-value when the completeness threshold is not met.",
                    "Make the warning visible next to the result, not buried in a footnote.",
                ],
            },
            {
                "title": "Demo a real regional comparison",
                "summary": "Two regions with different catalogue quality make the point better than one number.",
                "steps": [
                    "Pick two regions and a time window with different sample sizes.",
                    "Show the map, the magnitude-frequency plot, and the b-value interval.",
                    "Trigger the completeness warning on the weaker catalogue.",
                    "Rehearse the limits of the estimate and credit the USGS feed.",
                ],
            },
        ],
    ),
}
