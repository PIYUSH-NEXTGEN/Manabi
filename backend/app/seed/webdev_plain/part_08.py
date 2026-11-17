"""Plain-language overrides for web-dev hackathon briefs 018 to 022."""

OVERRIDES = {
    "manabi-web-hackathon-018": {
        "summary": (
            "Build a browser sandbox that compares spacecraft transfers between orbits. "
            "The user picks a start and target orbit, plans the burns, and sees the fuel "
            "cost for each path. Students, space fans and educators can use it to learn "
            "mission design.\n\n"
            "A real physics integrator drives the path. The user changes the step size and "
            "watches energy error grow, and one scenario is checked against JPL Horizons data."
        ),
        "who_affected": (
            "Students, space enthusiasts and educators who are learning orbital mechanics "
            "and mission design."
        ),
        "why_matters": (
            "A trajectory that hides integration error teaches the wrong lesson, so the app "
            "shows its error and assumptions to make the result trustworthy."
        ),
        "approaches": [
            "Compute Hohmann and bi-elliptic transfer delta-v from the analytic formulas.",
            "Propagate the state with RK4 under point-mass gravity inside a Web Worker.",
            "Show step size, energy drift and simulated time beside the trajectory.",
            "Validate a simple case against JPL Horizons and add one gravity-assist scenario.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Plan a burn, watch the real integrated trajectory, and compare it with a "
                "known reference instead of trusting an animation."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "Orbital mechanics looks like magic until you move one burn and watch "
                        "the whole path change."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Canned animations teach the wrong lesson. A visible path can ignore "
                        "integration error, units or the real delta-v cost of a maneuver."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Choose orbits, plan Hohmann or bi-elliptic burns, and integrate the "
                        "path with RK4 in a Web Worker. The app shows delta-v and an error "
                        "panel, and it checks one scenario against JPL Horizons."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Start in a low orbit, plan a transfer, change one parameter, and show "
                        "the new path and delta-v. Open the validation panel and compare the "
                        "result."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "More bodies, plane changes, a proper mission timeline, and guided "
                        "challenges for classrooms."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Why RK4 instead of a canned animation?",
                    "answer": (
                        "The goal is to show the numerical method and its error. RK4 is a "
                        "readable balance of accuracy and speed, and the validation panel makes "
                        "the approximation visible."
                    ),
                },
                {
                    "question": "How do you know the simulation is right?",
                    "answer": (
                        "The app compares a known scenario with published Horizons positions "
                        "and shows the difference. It also displays units and integration "
                        "settings so the result is reproducible."
                    ),
                },
                {
                    "question": "Is the gravity assist realistic?",
                    "answer": (
                        "It is a simplified two-body or patched-conic demo, not a full n-body "
                        "mission design. The app labels that simplification and keeps the focus "
                        "on transfer mechanics."
                    ),
                },
                {
                    "question": "Why use a Web Worker?",
                    "answer": (
                        "Integration can block the main thread and make the controls feel "
                        "broken. The worker keeps the UI responsive while the trajectory updates."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Define the orbital model and units",
                "summary": "Most simulation bugs come from units or mismatched frames.",
                "steps": [
                    "Choose the central body, gravitational parameter, distance unit and time unit, then document them in one constants module.",
                    "Represent state as position and velocity and define the coordinate frame used for rendering.",
                    "Write circular-orbit helpers for radius, speed and period, with tests.",
                    "Write the Hohmann and bi-elliptic delta-v formulas with worked examples before you build the UI.",
                ],
            },
            {
                "title": "Build transfer comparison",
                "summary": "The user should understand the trade before the animation starts.",
                "steps": [
                    "Add inputs for start radius, target radius and transfer type, with clear ranges and units.",
                    "Compute total delta-v, burn count and transfer time for Hohmann and bi-elliptic transfers.",
                    "Show a side-by-side comparison with the assumptions and the point where one option becomes cheaper.",
                    "Reject impossible or degenerate orbits with a clear message instead of returning NaN.",
                ],
            },
            {
                "title": "Implement the RK4 propagator",
                "summary": "The trajectory has to come from the integrator, not a scripted path.",
                "steps": [
                    "Implement an RK4 step for point-mass gravity with a configurable time step.",
                    "Track energy and angular momentum so drift is shown honestly.",
                    "Move integration into a Web Worker and stream state samples back with a cancel path.",
                    "Add step-size controls and show how energy error grows as the step gets larger.",
                ],
            },
            {
                "title": "Render and control the trajectory",
                "summary": "The visual layer should let the user inspect the physics.",
                "steps": [
                    "Render the central body, orbit paths, burns and the moving spacecraft in a 3D scene.",
                    "Add camera controls, pause, play, speed and a timeline scrubber.",
                    "Show burn markers with delta-v and time, and highlight the current orbital state.",
                    "Keep rendering separate from the worker so the UI stays responsive during a long run.",
                ],
            },
            {
                "title": "Validate, document and demo",
                "summary": "A trajectory that ignores error teaches the wrong lesson.",
                "steps": [
                    "Test the analytic transfer delta-v against hand calculations.",
                    "Validate one simple propagated state against a JPL Horizons reference within a stated tolerance.",
                    "Add one gravity-assist scenario or document it clearly as an extension.",
                    "Write the assumptions, error display and validation results in the README, then record the comparison demo.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-019": {
        "summary": (
            "Build a browser tool where a user types a compound name or draws a molecule and "
            "sees it in 3D. It computes basic drug-likeness properties locally with a real "
            "chemistry library. Chemistry students, educators and early-stage researchers can "
            "check a compound without installing anything.\n\n"
            "Each Lipinski rule comes with a plain-language note, so the user learns why a "
            "value passes or fails. The chemistry bundle is large, so the app loads it lazily "
            "and caches structures it has already resolved."
        ),
        "who_affected": (
            "Chemistry students, educators and early-stage researchers who check basic "
            "drug-likeness properties."
        ),
        "why_matters": (
            "Property calculations are easy to get subtly wrong, so a transparent, "
            "library-backed tool teaches the rules and shows its assumptions."
        ),
        "approaches": [
            "Parse SMILES or resolve a compound name through PubChem, then render the molecule in 3D.",
            "Compute weight, logP, donors, acceptors and Lipinski checks with a real chemistry library.",
            "Load the heavy chemistry bundle lazily and cache resolved structures.",
            "Add substructure search and a two-molecule comparison with plain-language explanations.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A molecule becomes a shape with explainable drug-likeness properties instead "
                "of a formula on a slide."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A molecule is a three-dimensional shape, but most chemistry tools show "
                        "it as a line of text and a table of rules."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Property calculations are easy to get subtly wrong. A Lipinski verdict "
                        "without an explanation teaches memorization, not understanding."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Type a SMILES string or a compound name, see the structure in 3D, and "
                        "get weight, logP, donors, acceptors and a Lipinski verdict with each "
                        "rule explained. Users can compare two molecules and search a small "
                        "library by substructure."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Load a familiar drug, show its 3D structure and properties, then compare "
                        "it with a failed analogue and point to the Lipinski rule that changed."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Larger libraries, saved workspaces, more descriptor sets, and "
                        "exportable teaching worksheets."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Are the property calculations correct?",
                    "answer": (
                        "They come from a proven cheminformatics library, and the app checks "
                        "known molecules. The UI shows which method produced each value and "
                        "avoids claiming more precision than it has."
                    ),
                },
                {
                    "question": "Why is the app slow on first load?",
                    "answer": (
                        "The cheminformatics bundle is large, so the app lazy-loads it only when "
                        "the molecule tool opens. A small initial shell keeps the catalogue fast."
                    ),
                },
                {
                    "question": "Is this medical advice?",
                    "answer": (
                        "No. It is an educational explorer, and the disclaimer stays visible. A "
                        "Lipinski verdict is not a prediction that a compound is safe or effective."
                    ),
                },
                {
                    "question": "Where does compound data come from?",
                    "answer": (
                        "PubChem is one lookup source, with rate limits and attribution. The "
                        "user can also paste a SMILES string, so the app still works without a "
                        "lookup."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Choose the chemistry stack and scope",
                "summary": "Use a real library and state its limits before you build the UI.",
                "steps": [
                    "Pick a browser-compatible chemistry library for parsing, properties and rendering, and check its bundle size.",
                    "Define the supported inputs, SMILES and compound names, with clear errors for salts, mixtures and invalid strings.",
                    "Write down the property list and the exact Lipinski thresholds you will display.",
                    "Add a visible educational disclaimer that this is not a medical or research decision tool.",
                ],
            },
            {
                "title": "Build input and structure resolution",
                "summary": "The same molecule can arrive as a name, a SMILES string or a PubChem record.",
                "steps": [
                    "Build a SMILES input with validation and a small example gallery.",
                    "Add compound-name lookup through PubChem with rate-limit handling and a cached response.",
                    "Normalize the molecule and store the canonical identifier so comparisons and caching stay stable.",
                    "Show a clear error panel when lookup fails, including a suggestion to try a SMILES string.",
                ],
            },
            {
                "title": "Compute and explain properties",
                "summary": "The explanation carries the teaching, not the number alone.",
                "steps": [
                    "Compute molecular weight, logP, donors and acceptors with the chemistry library.",
                    "Render each Lipinski rule with the measured value, the threshold, the pass state and a plain-language note.",
                    "Add a property table with units and the source of each value.",
                    "Test a few known molecules against published values and document any differences.",
                ],
            },
            {
                "title": "Add 3D rendering and comparison",
                "summary": "The 3D view and the side-by-side view turn a calculator into an explorer.",
                "steps": [
                    "Render the molecule in 3D with rotate, zoom and reset controls.",
                    "Add a two-molecule comparison with aligned property rows and highlighted differences.",
                    "Add substructure search over a small seeded library and list the matching molecules.",
                    "Lazy-load the rendering and chemistry bundles so the first page stays small.",
                ],
            },
            {
                "title": "Test performance and document the limits",
                "summary": "A heavy scientific bundle needs evidence that the app stays usable.",
                "steps": [
                    "Measure initial load, first molecule render and comparison time on a mid-range device.",
                    "Add tests for invalid SMILES, a failed PubChem lookup and a cache hit.",
                    "Document the property method, known limits and educational scope in the README.",
                    "Record a demo that shows local computation, a rule explanation and a two-molecule comparison.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-020": {
        "summary": (
            "Build an educational simulator that spreads a disease through a network of "
            "households, schools and workplaces. Users can add vaccination or school closure "
            "and watch how the outbreak changes. Public-health students, educators and policy "
            "teams can explore the trade-offs.\n\n"
            "A network model and a plain SIR model run on the same population, so the user sees "
            "what contact structure changes. Every assumption stays on screen, and a small real "
            "case series is used to fit one or two parameters, so nobody mistakes the model for "
            "a forecast."
        ),
        "who_affected": (
            "Public-health students, educators and policy teams who are exploring "
            "intervention trade-offs."
        ),
        "why_matters": (
            "Network structure and timing change how an outbreak unfolds, and an interactive "
            "model makes the assumptions and uncertainty easier to discuss."
        ),
        "approaches": [
            "Generate a contact network from households, schools and workplaces.",
            "Simulate infection states over daily steps in a Web Worker.",
            "Add vaccination, masking and closure interventions with visible parameters.",
            "Fit a simple model to sample case counts and show the uncertainty and assumptions.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Different networks and interventions produce different outbreaks, and the "
                "simulator shows why without pretending to forecast."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "One school closure can bend an outbreak curve, but only if you can see "
                        "how the contact network changes."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "A single SIR line hides who meets whom. Policy talks need a model that "
                        "shows households, schools and workplaces and admits its assumptions."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Simulate a population as a contact network, run an SIR process, and "
                        "toggle vaccination, masking and school closure. Users compare outcomes, "
                        "fit real case counts and watch R change over time."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Run the baseline, add vaccination and school closure, compare the curves, "
                        "and show the assumptions panel and the fitted R trend."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Age structure, waning immunity, mobility data, and scenario exports for "
                        "classrooms."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Is this a forecast?",
                    "answer": (
                        "No. It is an educational model. The app shows assumptions, uncertainty, "
                        "and the fact that real outcomes depend on behavior and data we do not "
                        "have."
                    ),
                },
                {
                    "question": "Why model a network instead of a single SIR curve?",
                    "answer": (
                        "Contact structure changes how fast an outbreak spreads and who gets "
                        "hit. A network makes interventions like school closure easier to read."
                    ),
                },
                {
                    "question": "How do you fit real data?",
                    "answer": (
                        "The app calibrates a small set of parameters to reported case counts and "
                        "shows the fit error. It does not claim to predict the future, only to "
                        "explain a past window."
                    ),
                },
                {
                    "question": "How does it stay responsive?",
                    "answer": (
                        "The simulation runs in a Web Worker, so the controls and charts stay "
                        "usable while the network steps forward."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Define the network and disease model",
                "summary": "The network is the surface the interventions touch, and the disease model sets the time step.",
                "steps": [
                    "Define person, contact edge, setting, infection state and daily event records.",
                    "Generate a synthetic population with households, schools and workplaces, and document the contact assumptions.",
                    "Choose states such as susceptible, exposed, infectious, hospitalized, recovered and deceased.",
                    "Write the transition rules and parameters in one module with units and defaults.",
                ],
            },
            {
                "title": "Build the simulation loop",
                "summary": "Move the model into a worker before you add any UI complexity.",
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
                "summary": "An honest model says what it cannot know, and that honesty makes a good story.",
                "steps": [
                    "Add tests for deterministic runs with a fixed seed and for intervention parameter changes.",
                    "Check that the SIR comparison and the network run use the same population and time units.",
                    "Document the contact assumptions, fitting limits and uncertainty method in the README.",
                    "Record a demo that compares two networks and explains the difference in peaks.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-021": {
        "summary": (
            "Build an interactive lab where a user draws a potential barrier and launches a "
            "wave packet at it. The app animates the wave, measures how much tunnels through, "
            "and shows the part that reflects. Physics students and educators can build "
            "intuition by changing the experiment.\n\n"
            "A known-answer check keeps the visuals honest. The app compares its measured "
            "transmission with the analytic result for a rectangular barrier and warns when the "
            "simulation drifts outside tolerance."
        ),
        "who_affected": (
            "Physics students, educators and anyone who is learning quantum tunneling through "
            "visual experiments."
        ),
        "why_matters": (
            "Tunneling is hard to picture, and an interactive solver with a known-answer check "
            "makes the approximation and its limits visible."
        ),
        "approaches": [
            "Implement a stable 1D time-dependent Schrodinger solver on a configurable grid.",
            "Render probability density and the wave-function components in real time.",
            "Run the compute-heavy solver in WebAssembly or on the GPU.",
            "Compare transmission with the analytic rectangular-barrier result and show the tolerance.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Draw a barrier, launch a wave packet, and watch quantum tunneling happen while "
                "the result is checked against the known answer."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A quantum particle can show up on the wrong side of a wall. The audience "
                        "gets to draw that wall and watch it happen."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Schrodinger simulations are easy to make visually impressive and "
                        "numerically wrong. Without a known-answer check, the animation teaches "
                        "nothing reliable."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "An interactive 1D time-dependent Schrodinger solver lets users draw a "
                        "potential, launch a wave packet and see transmission and reflection. The "
                        "app compares the measured transmission with the analytic "
                        "rectangular-barrier result."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Draw a barrier, launch the packet, pause at the split, and show the "
                        "analytic and measured transmission. Then widen the barrier and watch "
                        "the probability fall."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "2D potentials, absorbing boundaries, parameter sweeps, and classroom "
                        "experiment presets."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you know the solver is accurate?",
                    "answer": (
                        "The rectangular barrier has an analytic transmission result. The app "
                        "runs that case and shows the measured value beside the expected value, "
                        "including the error."
                    ),
                },
                {
                    "question": "Why WebAssembly or the GPU?",
                    "answer": (
                        "The time step updates every grid point. A fast path keeps the animation "
                        "smooth, and the MVP can start on the main thread and move the hot loop "
                        "when it becomes the bottleneck."
                    ),
                },
                {
                    "question": "What numerical issues can break the simulation?",
                    "answer": (
                        "An unstable time step, reflections from the grid edge, and a poorly "
                        "resolved barrier can all produce nonsense. The app shows units, "
                        "stability limits and an absorbing-boundary option."
                    ),
                },
                {
                    "question": "Is this a physical quantum computer?",
                    "answer": (
                        "No. It is a numerical visualization of the wave equation. It teaches "
                        "the model and its approximations, not hardware behavior."
                    ),
                },
            ],
        },
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
                "summary": "Get a correct numerical result before you build the visual layer.",
                "steps": [
                    "Implement the update step for the chosen scheme, keeping the real and imaginary parts separate.",
                    "Add a potential barrier and well that can change without recompiling the core.",
                    "Track probability conservation and warn when it drifts past a threshold.",
                    "Test the free-particle case and a rectangular barrier against known behavior.",
                ],
            },
            {
                "title": "Move compute to WASM or the GPU",
                "summary": "A smooth animation is part of the teaching value.",
                "steps": [
                    "Profile the plain JavaScript solver and confirm the update loop is the bottleneck.",
                    "Move the update loop to WebAssembly or a GPU shader and copy only the visible field back to the UI.",
                    "Keep the grid size and time step user-configurable, with a warning for unstable combinations.",
                    "Add a fallback path for browsers without the accelerated backend.",
                ],
            },
            {
                "title": "Build the interactive lab",
                "summary": "The user should be able to change the experiment and understand the response.",
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
                    "Record a demo that changes barrier width and explains the change in tunneling.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-022": {
        "summary": (
            "Build an earthquake map from live USGS data with filters for region, time, depth "
            "and magnitude. A statistics view estimates the Gutenberg-Richter b-value and shows "
            "its uncertainty. Earth-science students, educators, journalists and local planners "
            "can inspect a catalogue rather than view a set of dots.\n\n"
            "A map alone hides whether the data is complete enough to analyze. The app "
            "estimates the magnitude of completeness, warns when the sample is too small or too "
            "incomplete, and shows the feed timestamp beside every result."
        ),
        "who_affected": (
            "Earth-science students, educators, journalists and local planners who need to "
            "inspect a seismic catalogue."
        ),
        "why_matters": (
            "A map hides whether a catalogue is complete enough for analysis, so a b-value with "
            "uncertainty and a completeness check turns a picture into a defensible estimate."
        ),
        "approaches": [
            "Fetch and cache the USGS feed, then filter by region, time window, depth and magnitude.",
            "Plot the magnitude-frequency distribution on a log scale with the fitted line.",
            "Estimate the b-value with a maximum-likelihood method, report a confidence interval and estimate the magnitude of completeness.",
            "Warn when the sample is too incomplete or too small, and show the feed timestamp, filter summary and method notes beside every result.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A seismic catalogue becomes an honest b-value estimate with the completeness "
                "warning right beside the number."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "An earthquake map shows where the dots are. It does not tell you whether "
                        "the catalogue is complete enough to analyze."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "The Gutenberg-Richter b-value is easy to compute badly. Small samples, "
                        "missing tiny events and loose filters produce confident-looking numbers "
                        "that should not be trusted."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Filter the USGS catalogue by region, time, depth and magnitude. Plot "
                        "magnitude frequency on a log scale, estimate b with a maximum-likelihood "
                        "method and an interval, and warn when completeness or sample size fails."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Compare a well-sampled region with a sparse one. Show the plot, the "
                        "b-value interval, and the completeness warning that changes the "
                        "conclusion."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Time-varying b-value, spatial smoothing, aftershock declustering, and "
                        "saved analyses for classrooms."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "What is the b-value actually telling us?",
                    "answer": (
                        "It describes how often small and large earthquakes happen in the "
                        "selected catalogue. It is not a prediction of when the next earthquake "
                        "will strike."
                    ),
                },
                {
                    "question": "How do you handle incomplete catalogues?",
                    "answer": (
                        "The app estimates the magnitude of completeness and warns when the "
                        "selected data fall below it. The result is caveated or disabled rather "
                        "than shown as reliable."
                    ),
                },
                {
                    "question": "Why show uncertainty?",
                    "answer": (
                        "A b-value from a small sample can move a lot. The interval makes the "
                        "sample-size problem visible instead of hiding it behind one decimal "
                        "place."
                    ),
                },
                {
                    "question": "Where does the data come from?",
                    "answer": (
                        "The public USGS earthquake feed. The app caches responses, shows the "
                        "feed timestamp, credits the source and keeps the request rate modest."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Ingest and filter the catalogue",
                "summary": "Science starts with a clear, reproducible filter.",
                "steps": [
                    "Fetch the USGS feed, cache the response and record its timestamp.",
                    "Add region, date range, magnitude and depth filters.",
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
                    "Flag small samples, gaps and catalogues dominated by tiny events.",
                    "Disable or caveat the b-value when the completeness threshold is not met.",
                    "Make the warning visible next to the result, not buried in a footnote.",
                ],
            },
            {
                "title": "Demo a real regional comparison",
                "summary": "Two regions with different catalogue quality make the point better than one number.",
                "steps": [
                    "Pick two regions and a time window with different sample sizes.",
                    "Show the map, the magnitude-frequency plot and the b-value interval.",
                    "Trigger the completeness warning on the weaker catalogue.",
                    "Rehearse the limits of the estimate and credit the USGS feed.",
                ],
            },
        ],
    },
}
