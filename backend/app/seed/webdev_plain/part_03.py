"""Plain-language overrides for MANABI Web Dev resume briefs 011 to 015."""

OVERRIDES = {
    "manabi-web-resume-011": {
        "summary": "Build and publish a small TypeScript package that turns durations like 90, 1h 30m or 2 days 4 hours into clean text and reads them back. Developers can install it from npm or a tarball and use it in browser or Node code.\n\nThe work is mostly in the edges. You ship ESM and CommonJS builds, generated type declarations and source maps, then test negative values, decimal hours, rounding and bad input. CI runs the tests and a bundle-size check, and every version gets a changelog and an automated release.",
        "who_affected": "Frontend and Node developers who need a small typed utility, and maintainers who count on predictable releases.",
        "why_matters": "Small utilities spread through teams, so tests, types and release automation decide whether they save time or become a maintenance burden.",
        "approaches": [
            "Pick one narrow problem and define a small typed API with clear error behavior.",
            "Build ESM and CommonJS outputs with generated declarations and source maps.",
            "Test the edge cases in CI and check bundle size or benchmarks.",
            "Automate releases, changelog entries and publishing to npm.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A typed utility with tests, a README and a package build that another project can install.",
                    "checks": [
                        "The package exposes a small API with generated type declarations.",
                        "Unit tests cover normal, boundary and invalid inputs.",
                        "A local consumer can install the built package and use it.",
                        "The README shows install steps, usage and one limitation.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "The package ships both module formats, releases on its own and has a written compatibility policy.",
                    "checks": [
                        "ESM and CommonJS builds both work in a small smoke-test consumer.",
                        "CI runs tests, type checks and a build on every pull request.",
                        "Release automation creates version tags and changelog entries.",
                        "The README lists browser and Node support, bundle size or benchmark results.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "You can show typed API design, package use and compatibility work that frontend teams rely on.",
                },
                {
                    "role": "Library / platform engineer",
                    "how_it_helps": "Build outputs, types, compatibility policy and releases are the core of library upkeep.",
                },
                {
                    "role": "Developer experience engineer",
                    "how_it_helps": "Docs, examples, bundle-size checks and release automation are direct developer-experience work.",
                },
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
                    "answer": "Different consumers use different module systems. A dual build saves them from a bundler workaround. I test both in a small consumer project, because a build that compiles can still fail when someone imports it.",
                },
                {
                    "question": "How do you decide the API surface?",
                    "answer": "I start from one real use case. I expose the smallest set of functions that solves it and hold off on options until a second real case needs them. A narrow API is easier to test, document and keep stable.",
                },
                {
                    "question": "How do you handle breaking changes?",
                    "answer": "Semantic versioning, a changelog and a clear compatibility note. A breaking change gets a major version and a migration example. Automation creates the release, but I read the changelog before I publish.",
                },
            ],
            "differentiators": [
                "A real installable package with both module formats, instead of a local helper file.",
                "Automated releases and a compatibility policy, instead of a bare version number.",
                "Tests and docs for the edge cases consumers actually hit.",
            ],
        },
        "build_guide": [
            {
                "title": "Define the API and compatibility policy",
                "summary": "A small package needs a sharp promise about what it will and will not do.",
                "steps": [
                    "Write the two or three exported functions and their input and output types before you write implementation code.",
                    "Decide the supported runtimes, module formats and TypeScript versions, plus the semantic-versioning policy.",
                    "List clear non-goals such as time zones, localization or calendar math, so the scope stays narrow.",
                    "Write a short design note with examples and the error behavior for invalid input.",
                ],
            },
            {
                "title": "Implement and test the utility",
                "summary": "The code is small. The edge cases are the project.",
                "steps": [
                    "Implement the parser and formatter as pure functions with no dependencies.",
                    "Add tests for zero, negative, decimal, overflow, whitespace, mixed units and malformed input.",
                    "Add property-style or table-driven tests for round-trip parsing and formatting.",
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
                    "Check the published file list and keep only the build, types, README and license.",
                ],
            },
            {
                "title": "Add CI, releases and documentation",
                "summary": "A package is a maintenance product, not a folder of helpers.",
                "steps": [
                    "Run lint, typecheck, tests and the tarball smoke test in CI on every pull request.",
                    "Set up conventional commits, changelog generation and a release workflow that publishes only after checks pass.",
                    "Write a README with install, API reference, examples, error behavior and a compatibility table.",
                    "Add a CONTRIBUTING note and a versioned upgrade example, so consumers know how to handle breaking changes.",
                ],
            },
            {
                "title": "Publish and prove consumption",
                "summary": "The final proof is another project using the package.",
                "steps": [
                    "Publish a dry-run tarball and inspect the contents before you release.",
                    "Publish version 1.0.0 and install it into a small demo app that uses the formatter in a real UI.",
                    "Record the bundle-size result and add it to the README.",
                    "Link the release, changelog and demo from the repo description.",
                ],
            },
        ],
    },
    "manabi-web-resume-012": {
        "summary": "Build a background job system with a Postgres-backed queue, a pool of workers and an operator dashboard. It runs email, report, media and sync jobs, and it shows the team what is stuck before a user complains.\n\nFailure and recovery are where the work sits. A worker can die after it takes a job but before it records success, so the queue promises at-least-once delivery and handlers must be idempotent. Visibility timeouts, heartbeats and a dead-letter queue keep that honest. A load test kills workers on purpose to prove the system recovers.",
        "who_affected": "Backend teams that run email, report, media or sync jobs, and on-call engineers who debug stuck work.",
        "why_matters": "Background jobs fail in partial ways, so retries, timeouts and dead-letter handling decide whether a failure is recoverable or silent.",
        "approaches": [
            "Store each job with its state, attempts, visibility timeout and scheduled run time.",
            "Run a worker pool with heartbeats and reclaim jobs from workers that stop responding.",
            "Retry with exponential backoff and move exhausted jobs to a dead-letter queue.",
            "Show queue depth, retry counts and worker health in a dashboard.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "Workers pull stored jobs, retry failures and show queue depth in a dashboard.",
                    "checks": [
                        "Jobs are stored before a worker picks them up.",
                        "A failed job retries with backoff and eventually stops.",
                        "Exhausted jobs move to a dead-letter state instead of disappearing.",
                        "The dashboard shows queued, running, failed and completed counts.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Abandoned jobs come back to the queue, side effects stay idempotent, and a failure test shows the system recovering.",
                    "checks": [
                        "Visibility timeouts and worker heartbeats reclaim jobs from crashed workers.",
                        "Handlers use idempotency keys, so redelivery does not duplicate side effects.",
                        "Scheduled jobs run once at the intended time even with several workers.",
                        "A load test kills workers mid-job and the queue returns to a healthy state without losing work.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Backend engineer",
                    "how_it_helps": "Queue state, retries, timeouts and worker coordination are core backend work.",
                },
                {
                    "role": "Distributed systems engineer",
                    "how_it_helps": "You can discuss delivery guarantees, failure recovery and idempotency from a real test.",
                },
                {
                    "role": "DevOps / SRE",
                    "how_it_helps": "The dashboard, health signals and failure drills map straight onto running a job system.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a distributed task queue that processed {N} jobs with retries, visibility timeouts and a dead-letter path.",
                    "example": "Built a distributed task queue that processed 100,000 sample jobs with exponential retries, visibility timeouts and a dead-letter queue.",
                },
                {
                    "bullet": "Kept job side effects idempotent under at-least-once delivery and worker crashes.",
                    "example": "Kept email-style job side effects idempotent under at-least-once delivery, so a crash and redelivery did not send duplicates.",
                },
                {
                    "bullet": "Load-tested worker failure and recovered abandoned jobs without losing queued work.",
                    "example": "Load-tested with workers killed mid-job. Heartbeat-based reclamation returned abandoned jobs to the queue without losing work.",
                },
            ],
            "interview_points": [
                {
                    "question": "What delivery guarantee does your queue provide?",
                    "answer": "At least once. A worker can crash after it does the work but before it acknowledges it, so redelivery is possible. That is why handlers use idempotency keys. Exactly-once delivery is much harder and usually the wrong promise.",
                },
                {
                    "question": "How do you tell a stuck worker from a slow one?",
                    "answer": "Workers send heartbeats while they process. A visibility timeout gets extended as long as heartbeats arrive. If the timeout expires, the job counts as abandoned and can be reclaimed. The dashboard shows both heartbeat age and attempts.",
                },
                {
                    "question": "Why keep a dead-letter queue?",
                    "answer": "A job that fails again and again should stop taking worker time and become visible to an operator. The dead-letter queue keeps the payload, the attempts and the last error, so you can inspect the failure and replay it after a fix.",
                },
            ],
            "differentiators": [
                "Heartbeat-based recovery for crashed workers, tested under load.",
                "Idempotent side effects under at-least-once delivery.",
                "An operator dashboard with queue depth, retries and worker health.",
            ],
        },
        "build_guide": [
            {
                "title": "Model jobs and worker leases",
                "summary": "The database is the source of truth. A claim is just a lock on a row.",
                "steps": [
                    "Define job, attempt, worker, schedule and dead-letter records with status, run time, lease expiry and payload.",
                    "Choose the delivery guarantee. Use at-least-once, and require handlers to be idempotent.",
                    "Write the claim query so two workers cannot take the same job at the same time.",
                    "Write the state machine: queued, claimed, running, succeeded, retry-wait, dead and cancelled.",
                ],
            },
            {
                "title": "Build the worker loop and retries",
                "summary": "Abandonment, backoff and duplicate side effects are the tricky parts.",
                "steps": [
                    "Implement claim, heartbeat, complete and fail operations with lease expiry checks.",
                    "Reclaim expired leases and raise the attempt count without losing the original payload.",
                    "Add exponential backoff with jitter and a maximum-attempts rule that moves the job to dead-letter.",
                    "Add a scheduler path for delayed and recurring jobs that uses the same claim table.",
                ],
            },
            {
                "title": "Build the operator dashboard",
                "summary": "Operators need to see stuck work before users report it.",
                "steps": [
                    "Show queue depth, oldest queued job, retry counts, dead-letter count and worker heartbeats.",
                    "Add a job detail view with attempts, errors, a payload preview and a safe retry or cancel action.",
                    "Add filters by queue, status, handler and time range.",
                    "Show an alert when no heartbeat arrives inside the expected window.",
                ],
            },
            {
                "title": "Add failure injection and idempotency",
                "summary": "A queue that has never lost a worker has not been tested.",
                "steps": [
                    "Provide example handlers: one idempotent write, one always-fails job and one slow job with a heartbeat.",
                    "Add a fault-injection mode that kills workers, delays completion and drops connections on demand.",
                    "Check that a repeated job does not duplicate the side effect, using an idempotency key in the handler.",
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
        "summary": "Build a browser tool that tells a user when the ISS and other bright satellites will pass overhead. It draws the path on a 3D globe and a sky chart, so people know where to look and when.\n\nA pass above the horizon is not always visible. The tool checks how dark the sky is at the observer and whether the satellite sits in sunlight. It runs SGP4 on public orbital elements in the browser, caches the element sets and shows how old the data is.",
        "who_affected": "Astronomy hobbyists, educators and anyone who plans to watch the ISS or a bright satellite pass.",
        "why_matters": "Most trackers list every overhead pass, including ones the observer cannot see, so real visibility logic makes the result useful.",
        "approaches": [
            "Load and cache public TLE data, and show how old the elements are.",
            "Propagate orbits in the browser with SGP4 and compute passes from the observer's point of view.",
            "Check observer darkness and satellite illumination before you call a pass visible.",
            "Draw the ground track on a 3D globe and the pass on a sky chart.",
        ],
        "resume_kit": {
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
                    "text": "Visibility comes from observer darkness and satellite illumination, and the predictions are checked against known passes.",
                    "checks": [
                        "Sun altitude decides whether the observer is dark enough to see the pass.",
                        "The satellite is checked for sunlight as well as line of sight.",
                        "A 3D globe shows the ground track and the observer's location.",
                        "A small test set compares predicted pass times with published results within a tolerance.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "You combined real orbital math with a globe and sky-chart interface in the browser.",
                },
                {
                    "role": "Geospatial / visualization engineer",
                    "how_it_helps": "Coordinate transforms, ground tracks and sky projections are hands-on visualization work.",
                },
                {
                    "role": "Science software engineer",
                    "how_it_helps": "You can explain the orbital model, its inputs and how you checked it against known passes.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a browser satellite tracker using SGP4 that predicted {N} passes with visibility checks for observer darkness.",
                    "example": "Built a browser satellite tracker using SGP4 that predicted 40 ISS passes and filtered out passes the observer could not see because of daylight or Earth shadow.",
                },
                {
                    "bullet": "Cut unnecessary API calls by caching TLE sets and showing element age in the UI.",
                    "example": "Cut TLE API calls by caching element sets locally and showing their age, so users saw when predictions used older orbital data.",
                },
                {
                    "bullet": "Rendered ground tracks on a 3D globe and pass paths on a sky chart from the same prediction model.",
                    "example": "Rendered ground tracks on a 3D globe and pass paths on a sky chart from one prediction model, so the two views stayed consistent.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why is a pass above the horizon not always visible?",
                    "answer": "The observer needs darkness and the satellite needs sunlight for a bright pass. A satellite can be overhead in daylight, or it can sit in Earth's shadow, so the user sees nothing. I check sun altitude at the observer and illumination at the satellite.",
                },
                {
                    "question": "Why run SGP4 in the browser?",
                    "answer": "It keeps the interaction local and avoids a server round trip every time the location changes. The model is small enough to run client-side, and the TLE data is cached. The cost is that I must show element age clearly instead of pretending the orbit is current.",
                },
                {
                    "question": "How did you validate the predictions?",
                    "answer": "I compared a small set of passes with published predictions and checked that the differences stayed inside a reasonable tolerance. I also tested coordinate edge cases and stale TLE handling. The model is not perfect, so the UI shows the data age.",
                },
            ],
            "differentiators": [
                "Visibility logic that rules out passes the observer cannot see.",
                "A 3D globe and a sky chart driven by the same prediction code.",
                "Element age shown right in the UI.",
            ],
        },
        "build_guide": [
            {
                "title": "Build the orbital data layer",
                "summary": "Predictions start with fresh elements and a clean observer model.",
                "steps": [
                    "Choose a TLE provider and cache the element sets with a fetched-at timestamp.",
                    "Parse TLE lines into a typed satellite record and reject malformed or stale entries.",
                    "Convert observer latitude, longitude and elevation into the coordinate frames the propagator uses.",
                    "Show the element age in the UI and document the provider's usage rules.",
                ],
            },
            {
                "title": "Compute passes and visibility",
                "summary": "Above the horizon does not mean a person can see it.",
                "steps": [
                    "Use SGP4 to propagate the satellite over a time window and find rise, culmination and set events.",
                    "Compute azimuth and elevation relative to the observer for each sample.",
                    "Compute sun altitude at the observer and check whether the satellite is lit by the sun.",
                    "Mark a pass visible only when the observer is dark enough and the satellite is sunlit.",
                ],
            },
            {
                "title": "Render the globe and sky chart",
                "summary": "The two views answer different questions: where it is and where to look.",
                "steps": [
                    "Render the observer, the satellite position and the ground track on a 3D globe with time controls.",
                    "Render the current pass on a sky chart using azimuth and elevation, with labels for the cardinal directions.",
                    "Add a timeline that scrubs the pass and updates both views together.",
                    "Keep the orbital computation in a worker or a pure module, so rendering never owns the math.",
                ],
            },
            {
                "title": "Add alerts, location and degraded states",
                "summary": "A pass predictor must handle a bad location, stale data and a day with no visible pass.",
                "steps": [
                    "Add location search and a manual coordinate fallback, with clear validation.",
                    "Add an alert for the next visible pass above a chosen elevation threshold.",
                    "Show empty states for no visible passes in the next 24 hours and for stale elements.",
                    "Cache the last good prediction, so a short provider outage does not blank the page.",
                ],
            },
            {
                "title": "Validate against known passes",
                "summary": "The science claim needs a reference, not a nice animation.",
                "steps": [
                    "Compare rise time, maximum elevation and direction for one pass with a public tracker or published data.",
                    "Add unit tests for coordinate transforms and pass-event detection.",
                    "Document the accuracy limits, TLE freshness and visibility assumptions.",
                    "Record a demo that explains an invisible but high-elevation pass.",
                ],
            },
        ],
    },
    "manabi-web-resume-014": {
        "summary": "Build a physics sandbox for planning spacecraft transfers between orbits. A user picks a start and a target orbit, compares Hohmann and bi-elliptic transfers and sees the delta-v each burn needs.\n\nThen the trajectory runs through an RK4 integrator under point-mass gravity, not a scripted animation. The heavy math runs in a Web Worker so the page stays responsive, and the UI shows step size, energy drift and simulated time. A JPL Horizons case checks the numbers.",
        "who_affected": "Students, space enthusiasts and educators who explore orbital mechanics and mission design.",
        "why_matters": "A visible trajectory that hides integration error teaches the wrong lesson, so validation and an error readout make the sandbox trustworthy.",
        "approaches": [
            "Compute Hohmann and bi-elliptic transfer delta-v with the analytic formulas.",
            "Propagate the state with RK4 under point-mass gravity in a Web Worker.",
            "Show step size, energy drift and simulated time next to the trajectory.",
            "Check a simple case against JPL Horizons and add one gravity-assist scenario.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A user compares Hohmann and bi-elliptic delta-v for two circular orbits and sees the simulated transfer.",
                    "checks": [
                        "The app computes delta-v for both transfer types from the chosen orbits.",
                        "The transfer animates from the integrated state, not from a fixed path.",
                        "The user can change the start and target orbit radii and see the result update.",
                        "A clear label explains the units and assumptions.",
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
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "You built a responsive simulation UI around real numerical work.",
                },
                {
                    "role": "Scientific software engineer",
                    "how_it_helps": "You can explain integrators, error and validation against an outside reference.",
                },
                {
                    "role": "Game / graphics engineer",
                    "how_it_helps": "Trajectory rendering, camera controls and worker-driven updates are hands-on graphics work.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a mission trajectory sandbox that compared Hohmann and bi-elliptic delta-v and integrated transfers with RK4 in a Web Worker.",
                    "example": "Built a mission trajectory sandbox that compared Hohmann and bi-elliptic delta-v and integrated each transfer with RK4 in a Web Worker without blocking the UI.",
                },
                {
                    "bullet": "Validated simulated positions against JPL Horizons and showed integration error instead of hiding it.",
                    "example": "Validated a reference trajectory against JPL Horizons within a stated tolerance and displayed energy drift, so users could judge the simulation.",
                },
                {
                    "bullet": "Added an inspectable gravity-assist scenario on top of the transfer planner.",
                    "example": "Added a gravity-assist scenario that changed the trajectory and let users inspect the orbital elements before and after the assist.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why use RK4 instead of a simple Euler step?",
                    "answer": "Euler builds up error quickly in orbital motion, and that shows up as drift in energy and position. RK4 gives much better accuracy for about the same step size. I still show the error, because numerical integration is an approximation and not truth.",
                },
                {
                    "question": "Why run the simulation in a Web Worker?",
                    "answer": "Integration and rendering compete for the main thread. A worker keeps the interface responsive while the state propagates. The worker sends position samples or state updates, and the UI draws them.",
                },
                {
                    "question": "How did you validate the physics?",
                    "answer": "I used a simple case with known inputs, compared positions with JPL Horizons over a fixed interval and stated the tolerance. I also checked how energy behaved and made the assumptions visible in the UI.",
                },
            ],
            "differentiators": [
                "A real integrator with visible error, instead of a canned animation.",
                "Validation against an outside reference source.",
                "Worker-based simulation that keeps the UI responsive.",
            ],
        },
        "build_guide": [
            {
                "title": "Define the orbital model and units",
                "summary": "Most simulation bugs are unit bugs or mismatched frames.",
                "steps": [
                    "Choose the central body, gravitational parameter, distance unit and time unit, and document them in one constants module.",
                    "Represent state as position and velocity, and define the coordinate frame used for rendering.",
                    "Implement circular-orbit helpers for radius, speed and period, with tests.",
                    "Write the Hohmann and bi-elliptic delta-v formulas with worked examples before you build the UI.",
                ],
            },
            {
                "title": "Build transfer comparison",
                "summary": "The user needs to understand the trade before the animation starts.",
                "steps": [
                    "Create inputs for start radius, target radius and transfer type, with clear ranges and units.",
                    "Compute total delta-v, burn count and transfer time for Hohmann and bi-elliptic transfers.",
                    "Show a side-by-side comparison with the assumptions and the point where one becomes cheaper.",
                    "Add validation for impossible or degenerate orbits instead of returning NaN.",
                ],
            },
            {
                "title": "Implement the RK4 propagator",
                "summary": "The trajectory has to come from the integrator, not a scripted path.",
                "steps": [
                    "Implement an RK4 step for point-mass gravity with a configurable time step.",
                    "Track energy and angular momentum, so drift can be shown honestly.",
                    "Move integration into a Web Worker and stream state samples back with a cancel path.",
                    "Add step-size controls and show what happens to energy error as the step grows.",
                ],
            },
            {
                "title": "Render and control the trajectory",
                "summary": "The visual layer should make the physics easy to inspect.",
                "steps": [
                    "Render the central body, orbit paths, burns and the moving spacecraft on a 3D scene.",
                    "Add camera controls, pause, play, speed and a timeline scrubber.",
                    "Show burn markers with delta-v and time, and highlight the current orbital state.",
                    "Keep rendering separate from the worker, so the UI stays responsive during a long run.",
                ],
            },
            {
                "title": "Validate, document and demo",
                "summary": "A trajectory that ignores error teaches the wrong lesson.",
                "steps": [
                    "Test the analytic transfer delta-v against hand calculations.",
                    "Validate one simple propagated state against a JPL Horizons reference within a stated tolerance.",
                    "Add one gravity-assist scenario, or clearly document it as an extension.",
                    "Write the assumptions, error display and validation results in the README, then record the comparison demo.",
                ],
            },
        ],
    },
    "manabi-web-resume-015": {
        "summary": "Build a browser tool where a user types or draws a molecule, sees it in 3D and gets basic properties computed on the page. That covers molecular weight, logP, hydrogen-bond donors and acceptors, plus a Lipinski rule-of-five verdict in plain words.\n\nA real chemistry library does the math, so the numbers hold up better than a hand-written table. Structures come from SMILES or PubChem lookups, which need caching and respect for rate limits. The heavy chemistry bundle loads only when someone opens the explorer, so the first page stays fast.",
        "who_affected": "Chemistry students, educators and early-stage researchers who check basic drug-likeness properties.",
        "why_matters": "Property calculations are easy to get subtly wrong, so a transparent explorer built on a tested library teaches the rules and shows its assumptions.",
        "approaches": [
            "Parse a SMILES string or resolve a compound name through PubChem, then draw the molecule in 3D.",
            "Compute weight, logP, donors, acceptors and Lipinski checks with a real chemistry library.",
            "Load the heavy chemistry bundle lazily and cache resolved structures.",
            "Add substructure search and a two-molecule comparison with plain-language notes.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": "A SMILES string renders in 3D and shows the five Lipinski properties with a clear verdict.",
                    "checks": [
                        "The app parses a valid SMILES string and renders a 3D structure.",
                        "Molecular weight, logP, donors and acceptors are computed locally.",
                        "The Lipinski verdict explains which rule passed or failed.",
                        "Invalid input gives a useful error instead of an empty viewer.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": "Name lookup, lazy loading, substructure search and comparison all work without slowing the first page.",
                    "checks": [
                        "Compound names resolve through PubChem with caching and rate-limit handling.",
                        "The chemistry bundle loads only when someone uses the explorer.",
                        "Substructure search works over a small local library.",
                        "Two molecules can be compared side by side with the property differences highlighted.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": "You brought a heavy scientific library into a responsive, accessible browser interface.",
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": "PubChem lookup, caching, local compute and the comparison flow form a complete application.",
                },
                {
                    "role": "Science software engineer",
                    "how_it_helps": "You can explain the property calculations, their limits and the educational scope.",
                },
            ],
            "resume_bullets": [
                {
                    "bullet": "Built a browser molecule explorer with local Lipinski calculations and 3D rendering, cutting first-load JS by {X}% with lazy loading.",
                    "example": "Built a browser molecule explorer with local Lipinski calculations and 3D rendering, cutting initial JavaScript by 40% by loading the chemistry bundle only on demand.",
                },
                {
                    "bullet": "Added PubChem name lookup with caching and rate-limit handling for {N} compounds.",
                    "example": "Added PubChem name lookup with caching and rate-limit handling, covering 500 compound lookups without going over the public API limits.",
                },
                {
                    "bullet": "Explained each drug-likeness rule in plain language instead of showing a bare pass or fail.",
                    "example": "Explained each Lipinski rule in plain language, so users could see which property failed and why it matters.",
                },
            ],
            "interview_points": [
                {
                    "question": "Why use a chemistry library instead of calculating properties yourself?",
                    "answer": "Lipinski properties have edge cases around aromaticity, protonation and how descriptors are defined. A maintained library is more correct than a quick formula. I keep the explanation custom, but the numbers come from a tested implementation.",
                },
                {
                    "question": "How did you keep the page fast with a large chemistry bundle?",
                    "answer": "The explorer loads the chemistry and 3D bundles only when the user opens it. The landing page never imports them. I also cache resolved structures, so repeat lookups do not refetch or recompute.",
                },
                {
                    "question": "What does the tool not tell the user?",
                    "answer": "It does not predict safety, efficacy or clinical suitability. The Lipinski rules are a rough drug-likeness filter, not a medical verdict. The UI says this plainly and keeps the tone educational.",
                },
            ],
            "differentiators": [
                "Real cheminformatics in the browser with lazy loading.",
                "Plain-language notes next to each rule.",
                "PubChem lookup with caching and visible rate-limit handling.",
            ],
        },
        "build_guide": [
            {
                "title": "Choose the chemistry stack and scope",
                "summary": "Use a real library and state its limits before you build the UI.",
                "steps": [
                    "Pick a browser-compatible chemistry library for parsing, properties and rendering, and check its bundle size.",
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
                    "Normalize the molecule and store the canonical identifier, so comparisons and caching stay stable.",
                    "Show a clear error panel when lookup fails, with a suggestion to try a SMILES string.",
                ],
            },
            {
                "title": "Compute and explain properties",
                "summary": "The teaching value sits in the explanation, more than the number.",
                "steps": [
                    "Compute molecular weight, logP, donors and acceptors with the chemistry library.",
                    "Render each Lipinski rule with the measured value, the threshold, the pass state and a plain-language note.",
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
                    "Add substructure search over a small seeded library and show the matching molecules.",
                    "Lazy-load the rendering and chemistry bundles, so the initial page stays small.",
                ],
            },
            {
                "title": "Test performance and document the limits",
                "summary": "A heavy scientific bundle needs evidence that the app stays usable.",
                "steps": [
                    "Measure initial load, first molecule render and comparison time on a mid-range device.",
                    "Add tests for invalid SMILES, failed PubChem lookup and cache hits.",
                    "Document the property method, known limitations and educational scope in the README.",
                    "Record a demo that shows local computation, a rule explanation and a two-molecule comparison.",
                ],
            },
        ],
    },
}
