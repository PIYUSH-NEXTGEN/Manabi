"""Plain-language overrides for MANABI Web Dev hackathon briefs 013 to 017."""

OVERRIDES = {
    "manabi-web-hackathon-013": {
        "summary": (
            "Students apply for a scholarship in one portal. Staff review the "
            "documents, approve or reject the application, and record the payment. "
            "Students can check their own status and read any rejection reason "
            "without emailing the office.\n\n"
            "Every action belongs to a role and lands in an audit trail. A reviewer "
            "cannot approve, and a student cannot open another student's file. "
            "Payments are mocked, but the path from approval to payment is real."
        ),
        "who_affected": (
            "Students applying for scholarships, reviewers, finance staff and "
            "program administrators."
        ),
        "why_matters": (
            "Paper applications get lost, and status emails eat staff time. A "
            "permissioned workflow makes each decision and payment traceable."
        ),
        "approaches": [
            "Store applications, documents, verification states and approval steps as real records.",
            "Check the reviewer and approver role on every workflow transition.",
            "Log an audit entry for each document view, decision and payment.",
            "Tie mock disbursements to approved applications and export a report.",
        ],
        "pitch_guide": {
            "one_liner": (
                "Scholarship decisions stop vanishing into paper because every "
                "application, review and payment has an owner and a timestamp."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A student sends a scholarship application and then has no "
                        "idea whether a person has even opened it."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Paper and email applications get lost. Reviewers work from "
                        "different copies, and finance cannot show how a decision "
                        "became a payment."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Students apply and upload documents. Reviewers work a queue "
                        "with a clear checklist. Each status change goes into an "
                        "append-only audit trail, and admins export a disbursement "
                        "report. Payments are mocked."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Submit an application. Switch to the reviewer, verify a "
                        "document and approve it. Show the student timeline and the "
                        "audit entry. Then try a finance action as the wrong role."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Document OCR, duplicate checks, real payment integration "
                        "and an appeals workflow."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you protect sensitive documents?",
                    "answer": (
                        "Uploads get type and size validation. Access is role-based, "
                        "and reviewers only see the applications assigned to them. "
                        "The audit log records who opened or changed what."
                    ),
                },
                {
                    "question": "Are you moving real money?",
                    "answer": (
                        "No. Disbursement is mocked in the MVP. Real payments would "
                        "need a licensed provider, reconciliation and a much "
                        "stricter compliance review."
                    ),
                },
                {
                    "question": "Why keep an audit trail?",
                    "answer": (
                        "Scholarship decisions affect people's lives, and they often "
                        "have to be explained later. An append-only record makes "
                        "approvals, rejections and payments traceable."
                    ),
                },
                {
                    "question": "What stops a reviewer from approving everything?",
                    "answer": (
                        "The workflow requires document checks before approval. The "
                        "audit trail also shows unusual sequences. A second approval "
                        "step or sampling is a later control."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Model roles, applications and documents",
                "summary": (
                    "A workflow is a state machine with permissions. A status "
                    "dropdown is not enough."
                ),
                "steps": [
                    "Define student, reviewer, approver, finance and admin roles. Add records for applications, documents, decisions and disbursements.",
                    "Draw the application state machine: draft, submitted, under review, changes requested, approved, rejected, paid and closed.",
                    "Decide which roles can see each document type, and store that rule with the type.",
                    "Seed one application in each important state, so every role has something to test.",
                ],
            },
            {
                "title": "Build submission and document handling",
                "summary": (
                    "Students need a clear checklist and a safe upload path."
                ),
                "steps": [
                    "Build the application form with required fields, document slots, size limits and file-type checks.",
                    "Store documents privately and serve them through signed links that expire fast.",
                    "Add draft save, a submit confirmation and a status timeline that says what happens next.",
                    "Add the rejection path with a reason and a resubmission flow that keeps the old version.",
                ],
            },
            {
                "title": "Build the review and approval workflow",
                "summary": (
                    "Every transition checks the actor, the current state and the "
                    "reason."
                ),
                "steps": [
                    "Build a reviewer queue with document checks, notes and a request-changes action.",
                    "Build an approver view that shows only verified applications and records a decision with a reason.",
                    "Enforce transitions on the server. Log the actor, old state, new state, timestamp and reason for every change.",
                    "Add an admin audit view that filters by application, actor and action.",
                ],
            },
            {
                "title": "Build finance records and reporting",
                "summary": (
                    "The report is built from the workflow. Nobody types it in "
                    "twice."
                ),
                "steps": [
                    "Create mock disbursement records tied to an approved application and a signed-off amount.",
                    "Build a finance queue with clear paid and pending states. Label every payment as mock or test mode.",
                    "Add an export that reconciles approved amounts, recorded disbursements and open items.",
                    "Show the student a payment status without exposing internal reviewer notes.",
                ],
            },
            {
                "title": "Test permissions, audit and the full case",
                "summary": (
                    "A complete case proves the boundaries held."
                ),
                "steps": [
                    "Add tests proving a student cannot read another student's documents and a reviewer cannot approve.",
                    "Test every illegal state transition. Assert that a rejected action creates no audit entry.",
                    "Run one end-to-end case through rejection, resubmission, approval and mock payment.",
                    "Document the role matrix, workflow diagram, setup and data limits in the README.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-014": {
        "summary": (
            "A traveller shares a live trip with trusted contacts for a limited "
            "time. Contacts get an alert if the traveller leaves the expected "
            "route, stops for too long or misses a check-in.\n\n"
            "The traveller can stop sharing at any moment, and location history is "
            "deleted when the share expires. The app is honest about browser "
            "limits. Location updates only while the page is open."
        ),
        "who_affected": (
            "People travelling alone at night, parents, late-shift workers and the "
            "friends or family who act as trusted contacts."
        ),
        "why_matters": (
            "A quick 'text me when you're home' is fragile. A shared trip with "
            "clear check-ins gives contacts context without constant manual updates."
        ),
        "approaches": [
            "Create a share link with an explicit expiry, a destination and a contact list.",
            "Update location only while the share page is open, and state that limit clearly.",
            "Use check-in timers and simple route or dwell rules instead of promising background tracking.",
            "Let the traveller revoke at once, notify contacts in the app with an SMS or email fallback, and delete history after expiry.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A live trip share tells the right person when something looks "
                "wrong. It does not pretend the browser can track you forever."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "Walking home alone, 'I left' is not the useful message. 'I "
                        "stopped moving and missed my check-in' is."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Manual texts depend on the traveller remembering. "
                        "Background location is unreliable in mobile browsers, and "
                        "constant tracking raises privacy concerns."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "Share a trip for a limited time. Contacts see the latest "
                        "location while the page is open. They get alerts for a "
                        "missed check-in, a long stop or leaving the route. The "
                        "traveller can revoke at once, and the app is honest about "
                        "browser limits."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Open the traveller and contact views on two devices. Move, "
                        "stop, miss a check-in and show the alert. Then revoke the "
                        "link and show it stop updating."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Trusted-contact groups, native background modes, handoff to "
                        "emergency services and a safer route suggestion layer."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Does this track location in the background?",
                    "answer": (
                        "Not reliably in a browser, and we say so. The design relies "
                        "on an open page, check-in timers and a manual or SMS "
                        "fallback. It does not promise background tracking."
                    ),
                },
                {
                    "question": "What if the alert is a false alarm?",
                    "answer": (
                        "The contact can dismiss it, and the traveller can check in "
                        "or cancel. Grace periods and a visible last-updated time "
                        "keep stale data from looking like an emergency."
                    ),
                },
                {
                    "question": "Who can see the trip?",
                    "answer": (
                        "Only people with the share link, and only for a limited "
                        "time. The traveller can revoke it. Location history is "
                        "deleted or anonymized after expiry."
                    ),
                },
                {
                    "question": "Is this a replacement for emergency services?",
                    "answer": (
                        "No. It helps trusted contacts coordinate. The UI must never "
                        "suggest that it sends help or replaces a call to emergency "
                        "services."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Define the safety contract",
                "summary": (
                    "The app must be clear about what it can and cannot detect."
                ),
                "steps": [
                    "Write down what a share contains, who can see it and when it expires.",
                    "Pick a check-in interval and a grace period before an alert.",
                    "State that mobile browsers may pause location in the background.",
                    "Add consent, revoke and delete-history controls before you build the map.",
                ],
            },
            {
                "title": "Build the live share page",
                "summary": (
                    "The contact view should work on an ordinary phone browser."
                ),
                "steps": [
                    "Let the traveller create a trip from a start, a destination and a route estimate.",
                    "Show the latest location and the last-updated time on a simple map.",
                    "Add a check-in button and an obvious 'I'm safe' completion action.",
                    "Test the view on a narrow phone screen with slow updates.",
                ],
            },
            {
                "title": "Add three useful alerts",
                "summary": (
                    "Three rules people understand beat a vague promise of AI "
                    "safety."
                ),
                "steps": [
                    "Alert when a check-in is missed past the grace period.",
                    "Alert when the traveller stops moving for longer than expected.",
                    "Alert when the location moves far from the expected route corridor.",
                    "Add a false-alarm dismissal and test that each alert is sent only once.",
                ],
            },
            {
                "title": "Fallbacks and privacy",
                "summary": (
                    "A safety tool that needs perfect connectivity is not safe."
                ),
                "steps": [
                    "Show the contact a manual refresh and a last-known-state message.",
                    "Add an SMS or email fallback for the most important alert.",
                    "Delete or anonymize location history at expiry.",
                    "Test that a revoked link stops updating at once.",
                ],
            },
            {
                "title": "Rehearse a two-device demo",
                "summary": (
                    "The story lands when the audience sees both sides at once."
                ),
                "steps": [
                    "Open the traveller view on one device and the contact view on another.",
                    "Trigger a late check-in and a stop alert in a controlled way.",
                    "Show the revoke action and the expired-link state.",
                    "Prepare a recorded backup in case the venue blocks geolocation.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-015": {
        "summary": (
            "A shared pixel canvas where many people place pixels at the same "
            "time. It has a cooldown timer, abuse limits, live cursors and a replay "
            "of the canvas history.\n\n"
            "The server keeps the truth, so every pixel can be explained and "
            "abusive art can be rolled back. Clients just draw what the server "
            "accepts."
        ),
        "who_affected": (
            "Online communities, classrooms, event organizers and anyone who wants "
            "a small shared creative space."
        ),
        "why_matters": (
            "A shared canvas looks simple. It still needs consistent state, fair "
            "rate limits and a history that explains every pixel."
        ),
        "approaches": [
            "Keep the server authoritative for the grid, and broadcast each accepted pixel event.",
            "Store an append-only event history, so the canvas can be rebuilt and replayed.",
            "Add a per-user cooldown and per-IP rate limits, both enforced on the server.",
            "Show live cursors without extra identity data, plus moderation tools and a timelapse scrubber.",
        ],
        "pitch_guide": {
            "one_liner": (
                "A crowd builds one canvas together in real time, with fair "
                "cooldowns and a replay that makes every pixel accountable."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A blank canvas plus a crowd is a strong social product. "
                        "That only works if the state stays consistent and nobody "
                        "can spam it."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Real-time drawing breaks when clients disagree. A dropped "
                        "connection forks the board, and one script can overwrite "
                        "the whole canvas."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "The server owns the grid and broadcasts accepted pixel "
                        "events. We add per-user cooldowns, server-side rate limits, "
                        "live cursors, moderation rollback and an append-only "
                        "history for timelapse replay."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Open two windows and draw together. Trigger the cooldown, "
                        "show a reconnect resync, roll back a region, and play the "
                        "timelapse."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Redis for horizontal scale, community canvases, palette "
                        "voting and scheduled art battles."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How do you stop one script from filling the canvas?",
                    "answer": (
                        "Every placement is authenticated or rate-limited. "
                        "Cooldowns are enforced on the server, and moderation can "
                        "roll back a region. The client timer only shows the wait."
                    ),
                },
                {
                    "question": "How does the canvas stay consistent after a disconnect?",
                    "answer": (
                        "The server keeps an ordered event log. On reconnect, the "
                        "client asks for events after its last sequence number and "
                        "rebuilds from there."
                    ),
                },
                {
                    "question": "Why store history instead of only the current grid?",
                    "answer": (
                        "History powers the timelapse, makes moderation auditable "
                        "and lets us rebuild the canvas. Snapshots keep replay fast "
                        "as history grows."
                    ),
                },
                {
                    "question": "How would you scale this?",
                    "answer": (
                        "Move the grid and pub/sub to Redis, shard by canvas, and "
                        "snapshot old history. The MVP stays single-process, so the "
                        "consistency story is easy to explain."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Choose the canvas contract",
                "summary": (
                    "The server owns the truth. The client only draws it."
                ),
                "steps": [
                    "Choose a grid size, a palette and an event shape: x, y, color, user and timestamp.",
                    "Decide how the server validates placement and rejects stale or duplicate events.",
                    "Write the cooldown rule per user, and the fallback rule when identity is unknown.",
                    "Define how the full canvas loads on the first join.",
                ],
            },
            {
                "title": "Make the realtime loop work",
                "summary": (
                    "A pixel should appear for everyone before the user can doubt "
                    "it."
                ),
                "steps": [
                    "Open a WebSocket, send accepted pixels, and broadcast them to every client.",
                    "Draw the canvas once, then patch single cells instead of redrawing everything.",
                    "Add reconnect and resync, so a dropped connection does not fork the board.",
                    "Show a visible cooldown timer after a placement.",
                ],
            },
            {
                "title": "Cursors, cooldowns, and abuse limits",
                "summary": (
                    "The social layer makes the canvas feel alive and fair."
                ),
                "steps": [
                    "Broadcast lightweight cursor positions with a short expiry.",
                    "Enforce cooldown and rate limits on the server. A client-side check alone is not enough.",
                    "Add a moderation action that can overwrite or roll back a region.",
                    "Test a scripted spam attempt and confirm it is throttled.",
                ],
            },
            {
                "title": "History and timelapse",
                "summary": (
                    "The append-only event log is both an audit trail and a "
                    "feature."
                ),
                "steps": [
                    "Store each accepted pixel event with a sequence number and a timestamp.",
                    "Rebuild the canvas from events at any point in time.",
                    "Add a scrubber and a play control for the timelapse.",
                    "Compress or snapshot old history so replay stays fast.",
                ],
            },
            {
                "title": "Demo a crowd, not a single click",
                "summary": (
                    "The magic shows when several clients act at once."
                ),
                "steps": [
                    "Seed a recognizable starting image and a short event history.",
                    "Open two or three browser windows and place pixels while the audience watches.",
                    "Trigger a cooldown and show the moderation rollback.",
                    "Play the timelapse as the closing beat.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-016": {
        "summary": (
            "A browser app uses the webcam to measure how much a crowd is moving. "
            "That energy then changes the music and the visuals. Frames are "
            "processed locally, and nobody uses face recognition.\n\n"
            "A panel shows the measured energy and explains why the music changed. "
            "The point is a playful feedback loop without identity analysis."
        ),
        "who_affected": (
            "Party and event organizers, installation artists, dancers and "
            "educators who show responsive media without face recognition."
        ),
        "why_matters": (
            "Responsive visuals usually need opaque AI or manual controls. "
            "Motion-only sensing gives a playful feedback loop without identity "
            "analysis."
        ),
        "approaches": [
            "Downscale webcam frames and compare consecutive frames to estimate motion energy.",
            "Smooth the signal, so one hand wave does not cause a chaotic audio jump.",
            "Map energy bands to a few musical layers and visual parameters, rather than every possible control.",
            "Show a panel with the measured value, the current band and the reason for each change. Skip face detection, recording and uploads, and offer a camera-off mode.",
        ],
        "pitch_guide": {
            "one_liner": (
                "The crowd moves, the music responds, and the screen explains the "
                "measurement without ever looking at a face."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "A DJ reads the room by watching energy. We let a browser "
                        "do that with motion only, and we show exactly what it "
                        "measures."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Responsive visuals often rely on opaque AI or manual "
                        "controls. Camera-based sentiment analysis brings privacy "
                        "and accuracy problems that a party app does not need."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We compare downscaled webcam frames to measure motion "
                        "energy. Smoothed bands drive a small Web Audio graph and a "
                        "canvas visual. A panel shows the value, the band and why "
                        "the music changed. Nothing is recorded or uploaded."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Calibrate a still room, then have the audience move. Show "
                        "the energy rise, the audio layers enter, and the panel "
                        "explain the change. Cover the camera and show the fallback."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "More instrument layers, spatial region controls, "
                        "accessibility modes and optional DMX or lighting output."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Are you identifying people in the crowd?",
                    "answer": (
                        "No. We compare downscaled frames and never run face "
                        "detection or recognition. Nothing is recorded or uploaded."
                    ),
                },
                {
                    "question": "What if the lighting changes?",
                    "answer": (
                        "The motion score is calibrated against a still baseline "
                        "and smoothed with hysteresis. A sudden light change can "
                        "look like motion for a moment, so we expose a recalibrate "
                        "control."
                    ),
                },
                {
                    "question": "How do you keep the music from sounding random?",
                    "answer": (
                        "Only a few smoothed energy bands map to a small set of "
                        "audio layers. The transitions are gradual, and the "
                        "mapping is visible, so the response feels intentional."
                    ),
                },
                {
                    "question": "What about accessibility?",
                    "answer": (
                        "The visual respects reduced-motion preferences. There is a "
                        "mute control, and a manual mode lets the app run without a "
                        "camera."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Measure motion, never faces",
                "summary": (
                    "The privacy boundary is part of the product, so it ships with "
                    "the feature."
                ),
                "steps": [
                    "Capture frames locally and compare consecutive downscaled grayscale frames.",
                    "Compute a motion score from changed pixels and smooth it over a short window.",
                    "Show the score and a small threshold meter so the user can calibrate.",
                    "Write a notice that says: no face recognition, no recording, no upload. Keep it on screen.",
                ],
            },
            {
                "title": "Map motion to music",
                "summary": (
                    "A few stable layers sound intentional. Constant random "
                    "changes sound broken."
                ),
                "steps": [
                    "Create a small Web Audio graph with a base loop and two or three intensity layers.",
                    "Map smoothed energy bands to layer gain, filter or tempo with gradual transitions.",
                    "Add a manual sensitivity slider and a mute control.",
                    "Start audio only after a user gesture, and recover when the audio context is blocked.",
                ],
            },
            {
                "title": "Make the visuals respond",
                "summary": (
                    "The visual should explain the audio change. It should not "
                    "compete with it."
                ),
                "steps": [
                    "Draw a simple canvas visual whose speed and density follow the same energy bands.",
                    "Avoid rapid flashing, and respect reduced-motion preferences.",
                    "Show the current band and the mapped musical change in the transparency panel.",
                    "Test the app with a still frame, one moving person and a busy crowd.",
                ],
            },
            {
                "title": "Calibrate instead of guessing",
                "summary": (
                    "Every room has a different baseline, so the app has to adapt."
                ),
                "steps": [
                    "Record a short baseline while the room is still, and set the zero point.",
                    "Apply hysteresis so small changes do not flip bands constantly.",
                    "Add a reset-calibration action and show when calibration is stale.",
                    "Log the measured values during rehearsal to tune the thresholds.",
                ],
            },
            {
                "title": "Demo with a safe fallback",
                "summary": (
                    "Camera permissions and venue lighting are the two most likely "
                    "demo failures."
                ),
                "steps": [
                    "Prepare a recorded motion clip that can drive the visual if the webcam fails.",
                    "Rehearse the explanation of the motion metric before the music starts.",
                    "Test with the projector and house audio at realistic volume.",
                    "Have a silent visual-only mode ready.",
                ],
            },
        ],
    },
    "manabi-web-hackathon-017": {
        "summary": (
            "A browser tool tells you when bright satellites like the ISS will "
            "pass over your location. It lists only passes you can actually see, "
            "and draws the path on a globe and a sky chart.\n\n"
            "The tool shows how old the orbital data is. It also explains why a "
            "high pass can still be invisible when you or the satellite are in "
            "daylight."
        ),
        "who_affected": (
            "Astronomy hobbyists, educators and anyone who plans to watch the ISS "
            "or another bright satellite pass."
        ),
        "why_matters": (
            "Most trackers list every overhead pass, including ones you cannot "
            "see. Visibility logic makes the result actually useful."
        ),
        "approaches": [
            "Load and cache public TLE data, and show how old the elements are.",
            "Propagate orbits in the browser with SGP4, and compute passes relative to the observer.",
            "Check observer darkness and satellite sunlight before you call a pass visible.",
            "Draw the ground track on a 3D globe, and the pass on a sky chart.",
        ],
        "pitch_guide": {
            "one_liner": (
                "The ISS is about to pass overhead and you can really see it, "
                "because the tracker filters for darkness and observer visibility."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "The ISS just flew over your city. Most trackers also told "
                        "you about ten passes you could not see."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Orbital pass lists ignore a few things. Is the observer in "
                        "darkness? Is the satellite sunlit? Where in the sky should "
                        "you look? A generic list is technically true and "
                        "practically useless."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "We compute passes in the browser with SGP4. We filter by "
                        "observer darkness and satellite sunlight, and show the path "
                        "on a globe and a sky chart. Alerts fire only for passes "
                        "worth watching."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "Pick a location and scrub to a visible pass. Show the sky "
                        "path and the countdown. Then compare it with a pass we "
                        "filtered out."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Weather-aware visibility, camera field-of-view guides, "
                        "group viewing events and more satellite catalogues."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "How fresh are the orbital elements?",
                    "answer": (
                        "We cache published TLEs, show their age and refresh within "
                        "the source's guidance. Accuracy degrades over time, so "
                        "stale elements are labeled and not hidden."
                    ),
                },
                {
                    "question": "Can you guarantee someone will see it?",
                    "answer": (
                        "No. We show the geometric and illumination conditions. "
                        "Weather, buildings and local light pollution can still "
                        "block the view, and the UI says so."
                    ),
                },
                {
                    "question": "Why compute in the browser?",
                    "answer": (
                        "SGP4 is small enough to run locally. That keeps the demo "
                        "responsive and avoids a server round trip for every scrub. "
                        "The TLE data is still fetched and cached."
                    ),
                },
                {
                    "question": "What about the source's usage terms?",
                    "answer": (
                        "We credit the orbital-element source, cache requests and "
                        "follow its guidance. The app does not hit the feed for "
                        "every page view."
                    ),
                },
            ],
        },
        "build_guide": [
            {
                "title": "Build the orbital data layer",
                "summary": (
                    "Predictions start with fresh elements and a clean observer "
                    "model."
                ),
                "steps": [
                    "Choose a TLE provider and cache the element sets with a fetched-at timestamp.",
                    "Parse TLE lines into a typed satellite record, and reject malformed or stale entries.",
                    "Convert observer latitude, longitude and elevation into the frames the propagator uses.",
                    "Show the element age in the UI, and document the provider's usage rules.",
                ],
            },
            {
                "title": "Compute passes and visibility",
                "summary": (
                    "Above the horizon does not mean visible to a person."
                ),
                "steps": [
                    "Use SGP4 to propagate the satellite over a time window and find rise, culmination and set events.",
                    "Compute azimuth and elevation relative to the observer for each sample.",
                    "Compute the sun altitude at the observer, and whether the satellite is in sunlight.",
                    "Mark a pass visible only when the observer is dark enough and the satellite is sunlit.",
                ],
            },
            {
                "title": "Render the globe and sky chart",
                "summary": (
                    "Two views answer two questions: where it is and where to "
                    "look."
                ),
                "steps": [
                    "Render the observer, the satellite position and the ground track on a 3D globe with time controls.",
                    "Render the current pass on a sky chart using azimuth and elevation, with labels for the cardinal directions.",
                    "Add a timeline that scrubs the pass and updates both views together.",
                    "Keep the orbital math in a worker or a pure module, so rendering never owns it.",
                ],
            },
            {
                "title": "Add alerts, location and degraded states",
                "summary": (
                    "A pass predictor must handle a bad location, stale data and "
                    "days with no visible pass."
                ),
                "steps": [
                    "Add location search and a manual coordinate fallback, both with clear validation.",
                    "Add an alert for the next visible pass above a chosen elevation threshold.",
                    "Show empty states for no visible passes in the next 24 hours and for stale elements.",
                    "Cache the last good prediction, so a short provider outage does not blank the page.",
                ],
            },
            {
                "title": "Validate against known passes",
                "summary": (
                    "The science claim needs a reference. A nice animation is not "
                    "enough."
                ),
                "steps": [
                    "Compare rise time, maximum elevation and direction for one pass against a public tracker or published data.",
                    "Add unit tests for coordinate transforms and pass-event detection.",
                    "Document the accuracy limits, TLE freshness and visibility assumptions.",
                    "Record a demo that explains an invisible but high-elevation pass.",
                ],
            },
        ],
    },
}
