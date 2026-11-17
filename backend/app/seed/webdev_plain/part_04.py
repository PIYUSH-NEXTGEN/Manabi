"""Plain-language overrides for web-dev resume briefs 016 to 020."""

OVERRIDES = {
    "manabi-web-resume-016": {
        "summary": (
            "This lab lets a biology student paste a DNA or protein sequence, run "
            "Needleman-Wunsch or Smith-Waterman, and watch the scoring matrix fill "
            "cell by cell. They can trace back the best alignment, change gap or "
            "substitution scores, and see the result move. The same input also "
            "powers an open-reading-frame finder, codon translation and a "
            "restriction-site map.\n\n"
            "You write the algorithms yourself, so the visualization is the whole "
            "point. Keep the matrix and traceback in one tested core that both "
            "global and local modes share. Real sequences come from NCBI or "
            "UniProt with rate-limit handling and a cache."
        ),
        "who_affected": (
            "Biology students, educators and developers who are learning sequence "
            "algorithms."
        ),
        "why_matters": (
            "Alignment sits at the center of bioinformatics, and an interactive "
            "traceback makes the scoring choices and their consequences easy to see."
        ),
        "approaches": [
            "Implement global and local alignment on one shared matrix and traceback core.",
            "Animate the matrix fill and traceback without freezing the interface.",
            "Add ORF finding, codon translation and restriction-site mapping.",
            "Fetch and cache public sequences with rate-limit handling.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "Two sequences run a global alignment, the score appears, "
                        "and the aligned result shows matches and gaps."
                    ),
                    "checks": [
                        "Needleman-Wunsch returns the correct score for a small test pair.",
                        "The traceback produces an alignment with gaps and matches.",
                        "The user can change gap and mismatch scores and rerun.",
                        "Invalid nucleotides or proteins produce a clear error.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The matrix fills step by step, local mode shares the core, "
                        "and the lab adds ORF, translation and restriction views."
                    ),
                    "checks": [
                        "Matrix filling animates without freezing the page.",
                        "Smith-Waterman and Needleman-Wunsch share one tested alignment core.",
                        "ORF finding, translation and restriction-site mapping work on the same input.",
                        "A fetched NCBI or UniProt sequence is cached and shown with its source.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "The step-by-step matrix and traceback show advanced state "
                        "handling and visualization work."
                    ),
                },
                {
                    "role": "Bioinformatics engineer",
                    "how_it_helps": (
                        "Alignment, translation and ORF logic are directly relevant "
                        "domain skills."
                    ),
                },
                {
                    "role": "Software engineer / educator",
                    "how_it_helps": (
                        "You can explain a dynamic program and make its intermediate "
                        "state clear."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built an interactive sequence alignment lab for global and "
                        "local alignment with step-by-step matrix traceback."
                    ),
                    "example": (
                        "Built an interactive sequence alignment lab covering "
                        "Needleman-Wunsch and Smith-Waterman, with step-by-step "
                        "matrix filling and traceback for both."
                    ),
                },
                {
                    "bullet": (
                        "Shared one tested alignment core across two algorithms and "
                        "added ORF, translation and restriction-site views."
                    ),
                    "example": (
                        "Shared one tested alignment core across global and local "
                        "modes, then added ORF finding, codon translation and "
                        "restriction-site mapping on the same sequence input."
                    ),
                },
                {
                    "bullet": (
                        "Added cached NCBI and UniProt lookup so real sequences load "
                        "without repeated API calls."
                    ),
                    "example": (
                        "Added cached NCBI and UniProt lookup, so a demo sequence "
                        "loaded once and could be reused without hitting public API "
                        "limits."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "What is the difference between global and local alignment?",
                    "answer": (
                        "Global alignment lines up the full sequences from end to "
                        "end. Local alignment finds the best-scoring substring pair "
                        "and resets negative scores to zero. They share the matrix "
                        "and traceback structure, but they start differently and "
                        "trace back from different cells."
                    ),
                },
                {
                    "question": "How did you keep the matrix animation responsive?",
                    "answer": (
                        "I compute the matrix in small batches and render between "
                        "them instead of blocking on the whole job. For larger "
                        "inputs I use a worker or a step control so the user can "
                        "advance the fill on purpose."
                    ),
                },
                {
                    "question": "How did you test the alignment code?",
                    "answer": (
                        "I used small hand-checked pairs, known textbook cases and "
                        "edge cases like empty input, all mismatches and repeated "
                        "bases. I compared scores and traceback output. I did not "
                        "stop at checking that an alignment came back."
                    ),
                },
            ],
            "differentiators": [
                "A visible dynamic-programming traceback instead of a black-box alignment result.",
                "One shared core for global and local alignment.",
                "Public sequence lookup with caching and source display.",
            ],
        },
        "build_guide": [
            {
                "title": "Implement the alignment core",
                "summary": (
                    "The algorithm must work and pass tests without any animation."
                ),
                "steps": [
                    "Define a scoring model with match, mismatch, gap-open and gap-extend values.",
                    "Implement global Needleman-Wunsch and local Smith-Waterman on a shared matrix and traceback layer.",
                    "Return the score, the aligned sequences and the traceback path as plain data.",
                    "Add tests for identical, shifted, gapped and empty sequences against hand-checked results.",
                ],
            },
            {
                "title": "Build the step-through visualization",
                "summary": (
                    "The matrix is the teaching artifact, so make its state easy to see."
                ),
                "steps": [
                    "Render the matrix with row and column labels, scores and a highlight on the current cell.",
                    "Add step, play, pause and reset controls that read from a precomputed trace, not a second implementation.",
                    "Show the recurrence for the current cell with the chosen predecessor highlighted.",
                    "Render the traceback path and the final alignment side by side.",
                ],
            },
            {
                "title": "Add ORF, translation and restriction tools",
                "summary": (
                    "One sequence input should drive several small teaching tools."
                ),
                "steps": [
                    "Implement six-frame translation with a clear codon table and stop-codon handling.",
                    "Find open reading frames above a configurable minimum length and show their strand and frame.",
                    "Map common restriction sites and show cut positions on the sequence.",
                    "Keep every tool on the same normalized sequence and share the input state.",
                ],
            },
            {
                "title": "Fetch public sequences safely",
                "summary": (
                    "Outside sequence data needs caching, validation and clear provenance."
                ),
                "steps": [
                    "Add NCBI or UniProt lookup by accession with a server-side request and rate-limit handling.",
                    "Validate and normalize the returned sequence, then show the accession and source beside it.",
                    "Cache fetched sequences and handle bad accessions and network failures with clear messages.",
                    "Allow pasted FASTA input and parse headers without losing the sequence.",
                ],
            },
            {
                "title": "Test the teaching path and document it",
                "summary": (
                    "The project works when a learner can explain the result."
                ),
                "steps": [
                    "Add tests for scoring changes that flip a gap placement or switch from global to local alignment.",
                    "Check the ORF and translation tools against a short known sequence.",
                    "Document the scoring model, algorithm choice and public-data limits in the README.",
                    "Record a demo that steps through a matrix and explains one traceback decision.",
                ],
            },
        ],
    },
    "manabi-web-resume-017": {
        "summary": (
            "This simulator spreads a disease through a contact network of "
            "households, schools and workplaces. A user can add vaccination, "
            "masking or school closure and compare the result with a classic SIR "
            "curve.\n\n"
            "The model tracks contacts as a network, not one mixed pool, so "
            "network structure changes the shape of the outbreak. The simulation "
            "runs in a Web Worker, assumptions stay visible, and the user can "
            "pause, step and change parameters mid-run. A fit to a small real "
            "case-count dataset shows how the estimate shifts with assumptions, "
            "and the app labels itself as an educational model, not a forecast."
        ),
        "who_affected": (
            "Public-health students, educators and policy teams who are exploring "
            "intervention trade-offs."
        ),
        "why_matters": (
            "Network structure and timing change outbreak outcomes, and an "
            "interactive model makes assumptions and uncertainty easier to discuss."
        ),
        "approaches": [
            "Generate a contact network from households, schools and workplaces.",
            "Simulate infection states over daily steps in a Web Worker.",
            "Add vaccination, masking and closure interventions with visible parameters.",
            "Fit a simple model to sample case counts and show uncertainty and assumptions.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "A contact network spreads an infection over time, and the "
                        "user can compare one intervention against no intervention."
                    ),
                    "checks": [
                        "The simulation runs on a generated household, school and workplace network.",
                        "Infection states update over daily steps and produce an epidemic curve.",
                        "The user can turn one intervention on and rerun the simulation.",
                        "The UI states the model assumptions and says it is not a forecast.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The simulator runs smoothly in a worker, compares several "
                        "interventions and fits sample case counts with uncertainty."
                    ),
                    "checks": [
                        "The simulation runs in a Web Worker and the UI stays responsive during long runs.",
                        "Vaccination, masking and school closure can be combined and compared against a baseline.",
                        "A fit view shows observed case counts, model output and a stated uncertainty band.",
                        "The reproduction number is plotted over time and responds to interventions.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "You built a responsive simulation UI with charts, controls "
                        "and long-running state."
                    ),
                },
                {
                    "role": "Data / scientific software engineer",
                    "how_it_helps": (
                        "Network modelling, fitting and uncertainty display are "
                        "directly relevant."
                    ),
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "The project combines simulation logic, data fitting and a "
                        "complete interface."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a network epidemic simulator that compared {N} "
                        "interventions and kept the UI responsive with a Web Worker."
                    ),
                    "example": (
                        "Built a network epidemic simulator that compared "
                        "vaccination, masking and school closure against a baseline "
                        "while running the model in a Web Worker."
                    ),
                },
                {
                    "bullet": (
                        "Fitted the model to sample case counts and showed "
                        "uncertainty instead of a single forecast line."
                    ),
                    "example": (
                        "Fitted the model to sample case counts and displayed an "
                        "uncertainty band, keeping the educational scope visible "
                        "next to the chart."
                    ),
                },
                {
                    "bullet": (
                        "Made assumptions and parameters visible so users could "
                        "change them mid-run and see the effect."
                    ),
                    "example": (
                        "Made contact assumptions and intervention parameters "
                        "visible, so users could pause, change a value and compare "
                        "the new curve without restarting the page."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "Why model contacts as a network?",
                    "answer": (
                        "A single mixed population hides who meets whom. Households "
                        "and schools create clusters that change the outbreak shape "
                        "and the effect of school closure. A network model lets those "
                        "structures matter."
                    ),
                },
                {
                    "question": "Why is this not a forecast?",
                    "answer": (
                        "The model is simplified and fitted to limited sample data. "
                        "It teaches mechanisms and trade-offs, but it leaves out a "
                        "lot of real-world behavior. The UI states the assumptions "
                        "and shows uncertainty instead of one exact future."
                    ),
                },
                {
                    "question": "How does vaccination change the result?",
                    "answer": (
                        "Vaccination removes or lowers susceptibility for selected "
                        "nodes, which can break transmission chains. The effect "
                        "depends on coverage and on who gets the dose, so the "
                        "simulator lets the user change both instead of assuming one "
                        "fixed number."
                    ),
                },
            ],
            "differentiators": [
                "A contact-network model instead of a single pooled SIR curve.",
                "Visible assumptions and uncertainty right beside the simulation.",
                "Worker-based runs that stay responsive during long simulations.",
            ],
        },
        "build_guide": [
            {
                "title": "Define the network and disease model",
                "summary": (
                    "The network is where interventions land, and the disease model "
                    "sets the time step."
                ),
                "steps": [
                    "Define person, contact edge, setting, infection state and daily event records.",
                    "Generate a synthetic population with households, schools and workplaces, and document the contact assumptions.",
                    "Choose states such as susceptible, exposed, infectious, hospitalized, recovered and deceased.",
                    "Write the transition rules and parameters in one module with units and defaults.",
                ],
            },
            {
                "title": "Build the simulation loop",
                "summary": (
                    "Move the model into a worker before any UI complexity shows up."
                ),
                "steps": [
                    "Implement a daily step that updates states from contacts, recovery and intervention effects.",
                    "Add a seeded random generator so runs can be reproduced.",
                    "Run the loop in a Web Worker and stream daily summaries to the UI.",
                    "Support pause, step, reset and parameter changes without rebuilding the page.",
                ],
            },
            {
                "title": "Add interventions and comparison",
                "summary": (
                    "Interventions should change explicit parameters, not hidden "
                    "constants."
                ),
                "steps": [
                    "Add vaccination coverage and timing, masking effectiveness and school-closure windows.",
                    "Show every active intervention and its parameter values beside the charts.",
                    "Implement a classic SIR run with the same population size for comparison.",
                    "Let the user clone a run and change one assumption to see the difference.",
                ],
            },
            {
                "title": "Fit a small real dataset",
                "summary": (
                    "A model that never meets data is just a toy animation."
                ),
                "steps": [
                    "Load a small public case-count series and line its dates up with simulation days.",
                    "Fit one or two parameters with a simple grid or least-squares search and show the fit quality.",
                    "Display uncertainty by running several parameter sets and shading the outcome range.",
                    "Label the result as an educational model, not a forecast.",
                ],
            },
            {
                "title": "Validate assumptions and demo the trade-offs",
                "summary": (
                    "The story is honest modelling, including what the model cannot "
                    "say."
                ),
                "steps": [
                    "Add tests for deterministic runs with a fixed seed and for intervention parameter changes.",
                    "Check that the SIR comparison and the network run use consistent population and time units.",
                    "Document the contact assumptions, fitting limits and uncertainty method in the README.",
                    "Record a demo that compares two networks and explains the peak difference.",
                ],
            },
        ],
    },
    "manabi-web-resume-018": {
        "summary": (
            "This lab solves the one-dimensional time-dependent Schrodinger "
            "equation in the browser. A user draws a potential barrier or well, "
            "launches a wave packet and watches it tunnel, reflect and "
            "interfere.\n\n"
            "The numerical solver is the product, so it needs a stable scheme and "
            "visible grid and time step. Heavy compute runs in WebAssembly or on "
            "the GPU to keep the animation smooth. A validation panel compares "
            "measured transmission with the analytic rectangular-barrier result "
            "and says when the number drifts outside tolerance."
        ),
        "who_affected": (
            "Physics students, educators and anyone learning quantum tunneling "
            "through visual experiments."
        ),
        "why_matters": (
            "Tunneling is hard to build intuition for, and an interactive solver "
            "with a known-answer check makes the approximation and its limits "
            "visible."
        ),
        "approaches": [
            "Implement a stable 1D time-dependent Schrodinger solver on a configurable grid.",
            "Render probability density and wave-function components in real time.",
            "Run the compute-heavy solver in WebAssembly or on the GPU.",
            "Compare transmission with the analytic rectangular-barrier result and show the tolerance.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "A wave packet hits a rectangular barrier, and the user sees "
                        "reflection and transmission on screen."
                    ),
                    "checks": [
                        "The solver evolves a Gaussian wave packet on a fixed grid.",
                        "The UI draws probability density and the barrier over time.",
                        "The user can change barrier height or width and rerun.",
                        "The simulation does not blow up inside the supported parameter range.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The solver stays smooth under real-time compute, and "
                        "measured transmission is checked against the analytic result."
                    ),
                    "checks": [
                        "WebAssembly or GPU compute keeps the animation responsive at the chosen grid size.",
                        "The UI shows grid spacing, time step and total probability as diagnostics.",
                        "Measured transmission is compared with the analytic rectangular-barrier value.",
                        "A warning appears when the numerical result falls outside the stated tolerance.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "You built a real-time scientific visualization under real "
                        "performance constraints."
                    ),
                },
                {
                    "role": "Web performance engineer",
                    "how_it_helps": (
                        "WASM or GPU compute for a numerical solver is a strong "
                        "performance story."
                    ),
                },
                {
                    "role": "Scientific software engineer",
                    "how_it_helps": (
                        "You can discuss numerical stability, validation and where "
                        "the approximation breaks down."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built an interactive 1D Schrodinger solver that kept a "
                        "{N}x{N} grid running smoothly with WebAssembly compute."
                    ),
                    "example": (
                        "Built an interactive 1D Schrodinger solver that kept a "
                        "2,048-point grid running smoothly by moving the time step "
                        "into WebAssembly."
                    ),
                },
                {
                    "bullet": (
                        "Validated simulated transmission against the analytic "
                        "barrier result and warned when error passed tolerance."
                    ),
                    "example": (
                        "Validated simulated transmission against the analytic "
                        "rectangular-barrier result and warned users when error "
                        "exceeded the stated tolerance."
                    ),
                },
                {
                    "bullet": (
                        "Visualized probability density and wave-function "
                        "components in real time instead of a canned animation."
                    ),
                    "example": (
                        "Visualized probability density plus the real and imaginary "
                        "components in real time, so users could see interference "
                        "and reflection as they happened."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "Why is numerical stability the main challenge?",
                    "answer": (
                        "A bad time step or a coarse spatial grid makes the wave "
                        "function grow without bound. I picked a stable scheme for "
                        "the supported parameter range. The UI shows grid spacing, "
                        "time step and total probability so users can see when the "
                        "simulation stops being trustworthy."
                    ),
                },
                {
                    "question": "Why move the solver to WebAssembly or the GPU?",
                    "answer": (
                        "The time loop touches every grid point on every step, which "
                        "is too slow in plain JavaScript for smooth animation. WASM "
                        "or GPU compute keeps the frame rate usable while the same "
                        "numerical model runs underneath."
                    ),
                },
                {
                    "question": "How do you know the simulation is correct?",
                    "answer": (
                        "For a rectangular barrier I compare measured transmission "
                        "with the analytic result. I also check that total "
                        "probability stays near one and test a free-particle case. "
                        "The validation panel states the tolerance instead of "
                        "pretending the numbers agree exactly."
                    ),
                },
            ],
            "differentiators": [
                "A real numerical PDE solver instead of a scripted animation.",
                "Analytic validation with a visible error tolerance.",
                "WASM or GPU compute for smooth real-time output.",
            ],
        },
        "build_guide": [
            {
                "title": "Choose the numerical scheme",
                "summary": (
                    "Stability and boundary conditions decide whether the animation "
                    "means anything."
                ),
                "steps": [
                    "Pick a time-dependent 1D solver approach and document its stability condition.",
                    "Define the grid, time step, spatial domain and absorbing boundaries.",
                    "Implement a Gaussian wave packet as the initial state and normalize it.",
                    "Write a small command-line or test harness that prints total probability over time.",
                ],
            },
            {
                "title": "Implement the solver core",
                "summary": (
                    "Get a correct numerical result before building the visual layer."
                ),
                "steps": [
                    "Implement the update step for the chosen scheme and keep the real and imaginary parts separate.",
                    "Add a potential barrier and well that can change without recompiling the core.",
                    "Track probability conservation and warn when it drifts past a threshold.",
                    "Test the free-particle case and a rectangular barrier against known behavior.",
                ],
            },
            {
                "title": "Move compute to WASM or the GPU",
                "summary": (
                    "A smooth animation is part of what makes the lab teach."
                ),
                "steps": [
                    "Profile the plain JavaScript solver and confirm the update loop is the bottleneck.",
                    "Move the update loop to WebAssembly or a GPU shader and copy only the visible field back to the UI.",
                    "Keep grid size and time step user-configurable, with a warning for unstable combinations.",
                    "Add a fallback path for browsers without the accelerated backend.",
                ],
            },
            {
                "title": "Build the interactive lab",
                "summary": (
                    "The user should change the experiment and understand the "
                    "response."
                ),
                "steps": [
                    "Render probability density and the real and imaginary parts with a clear legend and axis labels.",
                    "Add controls for barrier height, width, packet energy and initial position.",
                    "Add play, pause, step and reset controls, plus a live time readout.",
                    "Show transmission and reflection measurements taken from the simulated field.",
                ],
            },
            {
                "title": "Validate against the analytic result",
                "summary": (
                    "The tolerance panel is what separates a lab from a demo."
                ),
                "steps": [
                    "Compute analytic transmission for a rectangular barrier and compare it with the measured simulation result.",
                    "Show the difference, the tolerance and a warning when the grid is too coarse.",
                    "Test probability conservation and a few barrier widths, then document the error trend.",
                    "Record a demo that changes barrier width and explains the tunneling change.",
                ],
            },
        ],
    },
    "manabi-web-resume-019": {
        "summary": (
            "You build a small React-like library from scratch, including element "
            "creation, a virtual DOM, diffing, a reconciler, function components, "
            "state and effect hooks, an event system and keyed list updates. Then "
            "you build a demo app on top of it and benchmark it against real "
            "React.\n\n"
            "The learning lives in the update path. A state change has to schedule "
            "work, the reconciler has to match old and new trees, keys have to "
            "keep identity, and effects have to clean up. Keep the API small, "
            "document the differences from React, and test each piece before you "
            "put them together."
        ),
        "who_affected": (
            "Frontend engineers preparing for interviews and developers who want "
            "to understand how UI libraries work."
        ),
        "why_matters": (
            "Most frontend bugs come from state, reconciliation and effect timing, "
            "and rebuilding the core makes those ideas concrete."
        ),
        "approaches": [
            "Implement element creation, virtual nodes and a reconciler with keyed children.",
            "Add function components plus state and effect hooks with a small scheduler.",
            "Build a demo app and test each layer on its own.",
            "Benchmark render and list updates against React and document the differences.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "A demo app renders components, updates state and handles a "
                        "keyed list without breaking."
                    ),
                    "checks": [
                        "Element creation and rendering produce the expected DOM.",
                        "A state update rerenders only the affected component subtree.",
                        "Keyed list reordering keeps component state.",
                        "The library has tests for rendering and updates.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "Hooks, effects and a scheduler work together, and a "
                        "benchmark plus a write-up explain the trade-offs."
                    ),
                    "checks": [
                        "State and effect hooks run in a defined order with cleanup between renders.",
                        "The reconciler handles insertions, removals, moves and keyed updates.",
                        "A demo app exercises forms, effects and list updates end to end.",
                        "A benchmark compares render and update time with React, and a write-up explains the differences.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Frontend engineer",
                    "how_it_helps": (
                        "You can explain rendering, reconciliation and hook "
                        "semantics from experience building them."
                    ),
                },
                {
                    "role": "UI platform engineer",
                    "how_it_helps": (
                        "A small renderer, scheduler and effect system are the core "
                        "of UI platform work."
                    ),
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "The project shows deep client-side architecture and steady "
                        "test discipline."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a React-like library with virtual DOM diffing, a "
                        "reconciler, hooks and keyed updates, plus a demo app."
                    ),
                    "example": (
                        "Built a React-like library with virtual DOM diffing, a "
                        "reconciler, state and effect hooks and keyed list updates, "
                        "then used it to build a small demo app."
                    ),
                },
                {
                    "bullet": (
                        "Benchmarked render and list-update performance against "
                        "React and documented where the small implementation "
                        "diverges."
                    ),
                    "example": (
                        "Benchmarked render and list-update performance against "
                        "React and documented where the simpler reconciler diverged "
                        "on large keyed lists."
                    ),
                },
                {
                    "bullet": (
                        "Added tests for each layer, including keyed moves and "
                        "effect cleanup, before composing the library."
                    ),
                    "example": (
                        "Added tests for rendering, keyed moves and effect cleanup "
                        "before composing the library, so regressions were caught at "
                        "the layer that caused them."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "Why do keys matter in a list?",
                    "answer": (
                        "Keys tell the reconciler which old node matches which new "
                        "node. Without stable keys, a reorder can look like a series "
                        "of content updates and component state gets lost. I test "
                        "insertions, removals and moves on purpose."
                    ),
                },
                {
                    "question": "How do effects run after a render?",
                    "answer": (
                        "The render phase builds the new tree. After commit, the "
                        "scheduler runs pending effects and cleans up the previous "
                        "ones first. Dependencies decide whether an effect runs "
                        "again, and cleanup is not optional."
                    ),
                },
                {
                    "question": "What did you learn by rebuilding React?",
                    "answer": (
                        "JSX is the easy part. Most of the complexity is in "
                        "scheduling and reconciliation. Keys, batching and effect "
                        "cleanup are small details that decide whether updates keep "
                        "state, and whether components behave predictably."
                    ),
                },
            ],
            "differentiators": [
                "A working reconciler with keyed updates, beyond a bare render function.",
                "Hook and effect semantics covered by tests.",
                "A benchmark and an honest write-up instead of a claim of React parity.",
            ],
        },
        "build_guide": [
            {
                "title": "Build elements and the first renderer",
                "summary": (
                    "Start with a tree that renders once before you add updates."
                ),
                "steps": [
                    "Define the element shape and a createElement helper with props and children.",
                    "Write the DOM renderer for host elements, text nodes, fragments and basic props.",
                    "Add tests for nested children, null children, attributes and event listeners.",
                    "Build a static demo page that renders only through the library.",
                ],
            },
            {
                "title": "Add reconciliation and keys",
                "summary": (
                    "The update path is the project, so one render will not do."
                ),
                "steps": [
                    "Implement a diff that compares previous and next element trees and patches the DOM.",
                    "Add keyed child reconciliation and tests for insert, remove, reorder and replace.",
                    "Handle component boundaries and prop changes without remounting every subtree.",
                    "Build a debug panel that shows the previous tree, the next tree and the reused nodes.",
                ],
            },
            {
                "title": "Add function components, hooks and scheduling",
                "summary": (
                    "State and effects need a defined order and a work loop."
                ),
                "steps": [
                    "Implement function components and component instances with stable hook slots.",
                    "Add useState with queued updates and a scheduler that batches work.",
                    "Add useEffect with dependency checks, cleanup and a defined run order.",
                    "Test re-renders, conditional hooks, cleanup and state updates inside effects.",
                ],
            },
            {
                "title": "Add events and the demo app",
                "summary": (
                    "A library becomes believable when a real app runs on it."
                ),
                "steps": [
                    "Implement event wiring and cleanup for the supported event types.",
                    "Build a demo with a keyed list, a form, conditional panels and an effect that syncs the document title.",
                    "Add a stress control that inserts, moves and removes many rows.",
                    "Compare the observable behavior with the same demo written in React.",
                ],
            },
            {
                "title": "Benchmark, document and explain",
                "summary": (
                    "The claim here is understanding, not a replacement for React."
                ),
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
        "summary": (
            "You rebuild the core of Git. That means content-addressed storage "
            "for blobs, trees and commits with SHA-1 hashing, a staging index, "
            "commit, log, branch and checkout, diff, and a three-way merge with "
            "conflict markers. Then you add a web page that draws the commit "
            "graph and shows what each command changes inside the "
            "repository.\n\n"
            "The object model and the index carry the weight. A commit points at "
            "a tree, a tree points at blobs and other trees, and a branch is a "
            "movable reference to a commit. Keep those rules clear and test them "
            "by reading repos made by real Git. The merge path shows base, ours "
            "and theirs, and writes conflict markers when it cannot merge cleanly."
        ),
        "who_affected": (
            "Developers learning version-control internals and interviewers who "
            "want to see systems reasoning."
        ),
        "why_matters": (
            "Git is used every day but its object model and merge behavior are "
            "often opaque, and rebuilding the core makes both concrete."
        ),
        "approaches": [
            "Store blobs, trees and commits as content-addressed objects with SHA-1 hashes.",
            "Implement a staging index plus commit, log, branch and checkout.",
            "Add diff and a three-way merge with explicit conflict markers.",
            "Render the commit graph and object changes in a small web view.",
        ],
        "resume_kit": {
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "A repository can stage files, create a commit, show log "
                        "output and check out a branch."
                    ),
                    "checks": [
                        "Blobs, trees and commits are stored with content-derived hashes.",
                        "The index stages additions and changes correctly.",
                        "Commit and log match the expected parent and tree structure.",
                        "Branch checkout restores the working tree for a simple case.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "Diff, branch operations and a three-way merge work, and "
                        "the repository can read real Git objects."
                    ),
                    "checks": [
                        "Diff shows added, removed and changed lines between commits.",
                        "A three-way merge writes conflict markers when changes overlap.",
                        "The implementation reads a repository created by real Git.",
                        "A web page draws the commit graph and shows the object changes behind each command.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "Content-addressed storage, object graphs and merge logic "
                        "are strong systems fundamentals."
                    ),
                },
                {
                    "role": "Developer tools engineer",
                    "how_it_helps": (
                        "Git internals and command behavior are directly relevant "
                        "to tooling work."
                    ),
                },
                {
                    "role": "Full-stack engineer",
                    "how_it_helps": (
                        "You built the core engine and a web view that makes it "
                        "inspectable."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Implemented Git-style content-addressed storage, index, "
                        "commits, branches, checkout and three-way merge."
                    ),
                    "example": (
                        "Implemented Git-style blob, tree and commit storage with "
                        "SHA-1 hashing, plus the index, commit, log, branch, "
                        "checkout and a three-way merge."
                    ),
                },
                {
                    "bullet": (
                        "Verified compatibility by reading and walking repositories "
                        "created by real Git."
                    ),
                    "example": (
                        "Verified the object model by reading and walking real Git "
                        "repositories, including nested trees and merge commits."
                    ),
                },
                {
                    "bullet": (
                        "Built a web commit-graph view that showed how each command "
                        "changed the object store."
                    ),
                    "example": (
                        "Built a web commit-graph view that showed the object "
                        "changes behind commit, branch and merge commands instead "
                        "of only the final log."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "What makes Git storage content-addressed?",
                    "answer": (
                        "Every object is named by a hash of its content. A blob hash "
                        "names file content, a tree hash names a directory listing, "
                        "and a commit hash names a snapshot plus metadata. If the "
                        "content changes, the hash changes, so integrity checks come "
                        "naturally."
                    ),
                },
                {
                    "question": "How does a three-way merge work?",
                    "answer": (
                        "It finds a merge base, compares base to ours and base to "
                        "theirs, and applies the changes that do not overlap. When "
                        "both sides change the same region in different ways, it "
                        "writes conflict markers. A clean merge is not a diff "
                        "between the two branch tips."
                    ),
                },
                {
                    "question": "Why add a web view to a Git implementation?",
                    "answer": (
                        "The object graph is the hard concept. Seeing commits, "
                        "parents, trees and branch refs makes the implementation "
                        "inspectable. It also pushes the command layer to expose "
                        "what it actually changed instead of only printing a log "
                        "line."
                    ),
                },
            ],
            "differentiators": [
                "Compatibility checked against repositories created by real Git.",
                "A real three-way merge with conflict markers.",
                "A web view of the object graph beyond a command-line demo.",
            ],
        },
        "build_guide": [
            {
                "title": "Build the object store",
                "summary": (
                    "Everything else depends on getting blobs, trees and commits "
                    "exactly right."
                ),
                "steps": [
                    "Implement blob, tree and commit writing with the real object header, SHA-1 hash and zlib compression.",
                    "Implement object reading and walking, including nested trees and commit parents.",
                    "Add tests that read objects written by real Git and verify the hashes match.",
                    "Expose a small debug command that prints the object type, hash and content ladder.",
                ],
            },
            {
                "title": "Add the index and core commands",
                "summary": (
                    "The index is the bridge between the working tree and a commit."
                ),
                "steps": [
                    "Implement index add, remove and status with file mode, path, size and hash entries.",
                    "Implement commit, log and branch creation on top of the object store.",
                    "Add checkout for a branch or commit, including restoring and removing files from the working tree.",
                    "Test add, commit, log, branch and checkout against a simple real repository.",
                ],
            },
            {
                "title": "Add diff and three-way merge",
                "summary": (
                    "The merge path carries the most risk and the most value."
                ),
                "steps": [
                    "Implement line diff between two blobs with a stable output format.",
                    "Find the merge base by walking commit parents, then implement three-way file merge for base, ours and theirs.",
                    "Write conflict markers when both sides change the same region, and keep clean changes automatic.",
                    "Add fixtures for clean merge, conflict, delete-vs-edit and add-vs-add cases.",
                ],
            },
            {
                "title": "Build the web inspection view",
                "summary": (
                    "The web page should explain the object graph instead of "
                    "printing logs."
                ),
                "steps": [
                    "Read the repository and expose commits, parents, trees and refs to the web view.",
                    "Draw the commit graph with branch labels and highlight the selected commit.",
                    "For each commit, show the tree diff and the object hashes behind the changed files.",
                    "Add a merge view that shows base, ours, theirs and the resulting conflict markers.",
                ],
            },
            {
                "title": "Prove compatibility and document limits",
                "summary": (
                    "Real Git compatibility is the strongest evidence for this "
                    "project."
                ),
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
