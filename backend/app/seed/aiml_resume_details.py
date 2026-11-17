"""Long-form descriptions and build guides for the AI/ML resume pack."""

DETAILS = {
    "manabi-aiml-resume-001": {
        "description": (
            "In the complete build, turn the detector into a review tool rather "
            "than a truth machine. Add adapters for a licensed or synthetic "
            "review export, a reproducible label sheet, text features such as "
            "near-duplicate n-grams and rating-sentiment mismatch, and "
            "behaviour features such as posting bursts and single-product "
            "histories. Build the reviewer-product graph, score communities, and "
            "combine those signals in a calibrated classifier.\n\n"
            "The finished repo should include a product trust page, a review "
            "queue with the strongest reasons for each flag, threshold controls, "
            "precision and recall at a chosen operating point, and tests for "
            "duplicate detection, missing reviewer history and empty graphs. A "
            "reviewer should be able to open one product, see why it was flagged, "
            "inspect the linked cluster, and record a human decision without the "
            "system treating that decision as proof."
        ),
        "build_guide": [
            {
                "title": "Define the review data and label contract",
                "summary": "A defensible label set matters more than a clever model here.",
                "steps": [
                    "Choose a licensed or synthetic review export and write down every field you will use: review text, rating, timestamp, reviewer id, product id and any available device or account signal.",
                    "Create a label sheet with genuine, fake and uncertain examples. Record who labelled each row and why, because ambiguous reviews are part of the problem.",
                    "Define the product trust score and its output fields before modelling: score, confidence band, top reasons and linked reviewer cluster.",
                    "Add a small fixture with duplicate reviews, a posting burst and an honest one-product reviewer so later tests exercise realistic edge cases.",
                ],
            },
            {
                "title": "Build text, behaviour and graph features",
                "summary": "Each signal should be inspectable on its own before it is combined.",
                "steps": [
                    "Extract text features such as near-duplicate n-grams, template phrases, all-caps ratio and the gap between star rating and sentiment.",
                    "Add reviewer-behaviour features: reviews per day, share of reviews on one product, rating distribution and account age where the data provides it.",
                    "Build a reviewer-product graph and compute shared-neighbour, component-size and burst-window features for each reviewer and product.",
                    "Store feature values with the review id so an explanation can quote the exact evidence instead of only a model weight.",
                ],
            },
            {
                "title": "Train and calibrate an explainable classifier",
                "summary": "The operating point should follow the cost of a false accusation.",
                "steps": [
                    "Train a simple logistic or gradient-boosting baseline first, then compare it with a stronger text model only if the baseline leaves obvious errors.",
                    "Split by product or time, not randomly by review, so near-duplicate text cannot leak from train to test.",
                    "Calibrate probabilities and choose a threshold from a stated precision target for human review, then report precision, recall, F1 and AUROC.",
                    "Generate per-review reason codes from the strongest features and test that every flagged row has at least one concrete reason.",
                ],
            },
            {
                "title": "Build the product trust and review screens",
                "summary": "The UI has to help a person verify a signal, not just display a number.",
                "steps": [
                    "Build a product page with the trust score, confidence band, suspicious-review list and a short explanation of each flag.",
                    "Add a cluster view that shows the reviewers, shared products and timing pattern behind a coordinated group.",
                    "Create a review queue where a moderator can mark a flag as confirmed, dismissed or needs-more-evidence, with a required note.",
                    "Show the evaluation summary inside the app so a viewer can see the measured error rates beside the score.",
                ],
            },
            {
                "title": "Test, document and demo the limits",
                "summary": "The project is credible because it shows where the detector fails.",
                "steps": [
                    "Add tests for near-duplicate detection, missing reviewer history, empty graphs and a product with only one review.",
                    "Run a small adversarial check with paraphrased fake reviews and document which signals disappeared.",
                    "Write a README covering the label definition, split strategy, metrics, threshold choice and responsible-use limits.",
                    "Record a walkthrough that opens a flagged product, explains the evidence, inspects a cluster and records a human decision.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-002": {
        "description": (
            "The complete project is an inspection workstation, not a notebook "
            "score. Add a category loader for MVTec AD or a licensed dataset, a "
            "training command that uses only good images, an autoencoder "
            "baseline, and a PatchCore-style feature method. Every prediction "
            "should produce an image-level score, a pixel heatmap and a "
            "threshold chosen from an inspector's required defect recall.\n\n"
            "Finish with per-category evaluation, a sensitivity slider, an upload "
            "screen that shows the heatmap and original image side by side, "
            "latency measurements and a short report that recommends where each "
            "method is usable. A reviewer should be able to switch categories, "
            "upload a held-out image, change the threshold, and see both the "
            "false-alarm rate and the localised defect evidence."
        ),
        "build_guide": [
            {
                "title": "Set up categories and the good-image split",
                "summary": "Anomaly detection starts with a clean definition of normal.",
                "steps": [
                    "Download one small benchmark category and record its licence, image count, defect types and the official train-test split.",
                    "Build a manifest with image paths, category, split and optional defect mask. Verify that training contains only good images.",
                    "Create a preprocessing pipeline with a fixed resize, normalisation and augmentation policy that you can reuse at inference.",
                    "Add a baseline command that reports the number of training images and produces a visual sample grid for a quick sanity check.",
                ],
            },
            {
                "title": "Train an autoencoder baseline",
                "summary": "The simple baseline gives you a reference and a failure mode to explain.",
                "steps": [
                    "Implement a convolutional autoencoder that reconstructs good images and compute a per-pixel reconstruction error.",
                    "Aggregate pixel error into an image score and save both the score and the heatmap for every test image.",
                    "Measure image-level AUROC and inspect false positives to see whether lighting, background or alignment is driving them.",
                    "Record inference time per image and the model size before adding a more complex method.",
                ],
            },
            {
                "title": "Add a PatchCore-style feature method",
                "summary": "A stronger method should be compared on the same split, not a new one.",
                "steps": [
                    "Extract patch embeddings from a pretrained backbone and build a memory bank from good images only.",
                    "Score test patches by nearest-neighbour distance, then upsample the patch scores into a pixel heatmap.",
                    "Tune the neighbourhood and coreset size on a validation category while keeping the test categories untouched.",
                    "Compare the two methods per category with image-level and pixel-level AUROC plus false positives at a fixed defect recall.",
                ],
            },
            {
                "title": "Build the inspector workstation",
                "summary": "The heatmap and threshold control are the product.",
                "steps": [
                    "Build an upload screen that accepts one image and shows the original, the heatmap and the score in one view.",
                    "Add a sensitivity slider that changes the operating threshold and displays the expected false-alarm rate from the held-out set.",
                    "Show a short reason line such as localised texture anomaly or edge defect, derived from where the heatmap concentrates.",
                    "Add a category picker and a small history list so an inspector can compare several images without losing context.",
                ],
            },
            {
                "title": "Evaluate, package and document",
                "summary": "A deployment recommendation is stronger than a single headline AUROC.",
                "steps": [
                    "Run the full evaluation on at least three categories and save the metrics as a JSON or CSV artifact.",
                    "Test lighting changes, rotated images and a non-defect background object to expose false-positive modes.",
                    "Write a report that says which method wins where, at what latency, and which categories remain unreliable.",
                    "Package the training and inference commands in a README and record a short demo of an uploaded defect and a clean part.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-003": {
        "description": (
            "The complete pipeline starts with a packaging photo, detects the "
            "label region, runs OCR, parses quantity and unit patterns, and "
            "normalises the result into grams, millilitres or a count. Add a "
            "strict confidence policy so the system returns cannot-tell when no "
            "quantity is visible, the image is blurry or the parser sees "
            "conflicting values. A single photo must not be used to claim "
            "physical dimensions without a visible reference object.\n\n"
            "Finish with a review screen that shows the original crop, OCR text "
            "and suggested field, field-level exact-match accuracy, numeric error "
            "after unit conversion, correct-abstention rate and a sample of the "
            "hardest package formats. The repo should make the difference between "
            "an OCR failure and a parsing failure obvious."
        ),
        "build_guide": [
            {
                "title": "Define the extraction schema and sample",
                "summary": "The output contract decides what the pipeline is allowed to claim.",
                "steps": [
                    "Write the target schema for product name, net weight, volume, count, unit and confidence, with a separate cannot-tell state.",
                    "Collect a labelled sample from open product data or photos you have permission to use, including several unit formats and low-quality images.",
                    "Record the ground-truth value in a base unit, the visible text and the crop region so each error can be traced.",
                    "Split the sample into development and held-out sets before tuning any OCR or parsing rule.",
                ],
            },
            {
                "title": "Build packaging detection and OCR",
                "summary": "Reading the whole image creates avoidable noise.",
                "steps": [
                    "Detect the label or the largest text-bearing region, then crop and deskew it before OCR.",
                    "Run OCR with a confidence score per text box and keep the raw boxes for the review screen.",
                    "Filter boxes by size, angle and language, and group nearby lines into candidate quantity phrases.",
                    "Log OCR text and confidence per image so parsing failures can be separated from reading failures.",
                ],
            },
            {
                "title": "Parse and normalise quantities",
                "summary": "Unit conversion is where many extraction demos quietly break.",
                "steps": [
                    "Write patterns for common forms such as 500 g, 1.5 kg, 750 ml, 2 x 100 g and 12 pieces.",
                    "Normalise weights to grams and volumes to millilitres with explicit conversion factors and a tolerance for spacing and punctuation.",
                    "Detect conflicting values such as 500 g and 1 kg on the same package, then abstain or ask for review instead of choosing silently.",
                    "Add a confidence score that combines OCR confidence, pattern match quality and the number of supporting boxes.",
                ],
            },
            {
                "title": "Build the review and abstention flow",
                "summary": "The correct answer is sometimes no answer.",
                "steps": [
                    "Create a review screen that shows the original image, the crop, the OCR text and the suggested normalised value.",
                    "Allow a human to correct the value and unit without losing the original evidence.",
                    "Route low-confidence, conflicting and dimension-only predictions to review rather than publishing them.",
                    "Expose a cannot-tell reason such as no quantity visible, blurry label or unsupported unit.",
                ],
            },
            {
                "title": "Measure extraction and refusal quality",
                "summary": "Separate metrics stop a good OCR demo from hiding a bad parser.",
                "steps": [
                    "Report exact-match accuracy for weight, volume and count separately, plus mean absolute error after unit normalisation.",
                    "Measure correct abstention on images with no visible quantity and incorrect abstention on images with a clear value.",
                    "Inspect the hardest formats and document whether the failure came from detection, OCR or parsing.",
                    "Write setup instructions and a short demo that includes one successful extraction and one honest refusal.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-004": {
        "description": (
            "The finished project is a catalogue pricing workbench. Build a "
            "product table with price, title, description, brand, pack size and "
            "image, then create a text-only baseline before adding image "
            "embeddings and structured features. Use a time-based split when the "
            "data has timestamps so the model is tested on future listings, and "
            "report MAE and SMAPE for the full set and for cheap and expensive "
            "slices.\n\n"
            "Add an ablation that removes text, image or structured fields one at "
            "a time, plus a listing screen that explains the strongest price "
            "drivers for one prediction. The repo should include the price "
            "distribution review, outlier policy, error slices and a clear note "
            "that estimates are not professional valuations or pricing advice."
        ),
        "build_guide": [
            {
                "title": "Build the catalogue table and baselines",
                "summary": "A trustworthy split and a simple baseline prevent a flashy but meaningless result.",
                "steps": [
                    "Assemble a licensed product table with a documented price target, currency and observation date.",
                    "Inspect the price distribution, remove or flag obvious data errors, and write down how you handle extreme outliers.",
                    "Create a structured-only baseline using brand, category and pack size, then a text-only baseline using title and description.",
                    "Use a time-based split when possible and record the exact cutoff so every later model sees the same test set.",
                ],
            },
            {
                "title": "Add text and image embeddings",
                "summary": "Embeddings are features, not magic; each one needs a controlled comparison.",
                "steps": [
                    "Generate text embeddings for the title and description with a small pretrained model and cache them by product id.",
                    "Generate image embeddings for a subset with a vision model and keep the model version in the artifact metadata.",
                    "Train a gradient-boosting or small neural regressor on each feature set and compare MAE and SMAPE on the held-out split.",
                    "Check for leakage from fields that would not exist before a price is set, such as margin or post-sale metadata.",
                ],
            },
            {
                "title": "Run ablations and error slices",
                "summary": "The ablation is the evidence that multimodal features are worth the cost.",
                "steps": [
                    "Compare structured-only, text-only, image-only and combined models on the same split and target.",
                    "Report MAE and SMAPE overall and by price band, category and pack size so a long-tail failure cannot hide.",
                    "Inspect the largest errors and classify them as bad input, rare product, mismatch between title and image, or genuine uncertainty.",
                    "Write a short recommendation for which feature set a catalogue team should deploy.",
                ],
            },
            {
                "title": "Explain predictions and build a listing view",
                "summary": "A price estimate is more useful when a person can audit the drivers.",
                "steps": [
                    "Compute feature attributions or permutation importance for a sample of predictions.",
                    "Build a listing screen that shows the suggested price, a range or confidence band, and the top three drivers.",
                    "Add a side-by-side comparison with the current listed price and a flag when the estimate is far outside the category range.",
                    "Keep the language as an estimate and link to the model card and evaluation summary.",
                ],
            },
            {
                "title": "Test, document and demo",
                "summary": "The result should hold up when someone asks what the model does not know.",
                "steps": [
                    "Add tests for missing images, unseen categories, empty descriptions and extreme prices.",
                    "Verify that the training pipeline reproduces the reported MAE and SMAPE from a clean artifact.",
                    "Write a README with the target definition, split, metrics, ablations, limitations and licence notes.",
                    "Record a demo that compares a text-only estimate with the multimodal estimate and explains the difference.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-005": {
        "description": (
            "The complete tutor is a small retrieval application with a hard "
            "network budget. Ingest openly licensed course material, chunk it "
            "with stable section ids, build a compact index and answer only from "
            "retrieved passages. Add a citation checker that compares each claim "
            "with its source, a refusal path for weak retrieval, and a "
            "translation step that keeps the original passage visible beside the "
            "translated answer.\n\n"
            "The learner UI should be a lightweight PWA with cached lesson text "
            "and a clear offline state. The teacher view should show aggregate "
            "struggle topics without exposing personal data. Finish with an "
            "expert-written question set, answer accuracy, citation support, "
            "median response time on a throttled profile and measured page "
            "weight."
        ),
        "build_guide": [
            {
                "title": "Choose sources and build the retrieval index",
                "summary": "The source licence and chunk structure are the foundation of trust.",
                "steps": [
                    "Select openly licensed textbooks or notes, record the licence per source and exclude anything with unclear reuse terms.",
                    "Chunk by heading and paragraph with stable source ids, page or section numbers and enough context to read the passage alone.",
                    "Build a small embedding index and a keyword fallback, then test retrieval on ten questions you wrote from the material.",
                    "Measure index size and retrieval time so the low-bandwidth constraint is visible from the start.",
                ],
            },
            {
                "title": "Build cited answering and refusal",
                "summary": "Every answer needs a passage a learner can open and check.",
                "steps": [
                    "Generate an answer only from the retrieved passages and require at least one source id in the response.",
                    "Add a citation checker that asks whether the cited passage supports each claim and rejects unsupported answers.",
                    "Define a refusal response when retrieval confidence is low or the checker cannot verify the claim.",
                    "Log the retrieved ids, checker result and final answer so a failure can be audited later.",
                ],
            },
            {
                "title": "Add multilingual answers without hiding the source",
                "summary": "Translation should help access, not obscure what the source actually says.",
                "steps": [
                    "Choose one additional language and test a small translation model on curriculum sentences before using it in the answer path.",
                    "Show the translated answer and the original source passage side by side with a clear language label.",
                    "Handle untranslatable terms by keeping the source term in brackets instead of inventing a fluent equivalent.",
                    "Add a feedback control for a learner to mark a translation as unclear without collecting unnecessary personal data.",
                ],
            },
            {
                "title": "Build the low-bandwidth PWA and teacher view",
                "summary": "A correct answer behind a heavy bundle is not usable in the target setting.",
                "steps": [
                    "Build a minimal learner UI with cached lesson text, a single question box and a citation panel.",
                    "Set a page-weight budget, compress assets, lazy-load optional content and show a clear offline or slow-connection state.",
                    "Create a teacher view that groups questions by topic and shows counts and common gaps without names or free-text personal data.",
                    "Test the flow on a throttled 3G profile and record initial load, time to first answer and response size.",
                ],
            },
            {
                "title": "Evaluate answer quality and cite the limits",
                "summary": "Fluency is not accuracy; the evaluation must use expert-written questions.",
                "steps": [
                    "Create at least 150 questions with reference answers and the supporting source section.",
                    "Measure answer correctness, citation support, refusal correctness and median response time on the held-out set.",
                    "Inspect failures by category: retrieval miss, unsupported claim, translation error or unclear question.",
                    "Write a README and demo script that includes a correct cited answer, a translated answer and an honest refusal.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-006": {
        "description": (
            "The complete build is a guarded support agent with a small, fixed "
            "tool surface. Implement test-mode adapters for a payment provider, "
            "strict schemas for each tool, a policy engine outside the model and "
            "an approval step for refunds, disputes and amounts above a limit. "
            "Every decision, tool call and approval goes into an append-only "
            "audit log with an idempotency key for each payment action.\n\n"
            "Add a reviewer console that shows the proposed action, the policy "
            "reason and the evidence, plus a scenario suite covering ambiguous "
            "requests, retries, duplicate messages and prompt injection. Report "
            "task success, policy violations, escalation accuracy and duplicate "
            "prevention. The repo must make test mode and the no-real-money "
            "boundary impossible to miss."
        ),
        "build_guide": [
            {
                "title": "Define tools, policies and test-mode boundaries",
                "summary": "The model should choose from a small surface, not invent payment actions.",
                "steps": [
                    "List the supported tasks: checkout help, subscription change, refund and dispute status. Exclude anything that requires real customer data.",
                    "Define a JSON schema per tool with required fields, allowed ranges and a test-mode-only credential check.",
                    "Write the policy engine in code: refund limits, dispute rules, required approvals and blocked actions.",
                    "Create a visible test-mode banner and a startup check that refuses to run with live keys.",
                ],
            },
            {
                "title": "Build the agent loop and human approval",
                "summary": "High-risk actions should leave the model and enter a human workflow.",
                "steps": [
                    "Implement an agent loop that turns a customer message into a proposed plan with a tool call and a policy check.",
                    "Treat customer text as untrusted data and reject any message that tries to change policy or reveal another customer's data.",
                    "Route risky actions to a reviewer screen with the proposed action, amount, policy reason and source message.",
                    "Execute only after approval and record the approver, timestamp and final provider response.",
                ],
            },
            {
                "title": "Add idempotency and an audit trail",
                "summary": "Retries are normal; duplicate refunds are not.",
                "steps": [
                    "Generate an idempotency key per intended payment action and store it with the request and result.",
                    "Make repeated customer messages and network retries return the stored outcome instead of calling the provider again.",
                    "Write an append-only audit event for every plan, policy decision, approval, tool call and provider response.",
                    "Add a reviewer history view that can replay one case from the first message to the final action.",
                ],
            },
            {
                "title": "Build the scenario evaluation suite",
                "summary": "Safety claims need adversarial tests, not a friendly demo.",
                "steps": [
                    "Write scripted scenarios for routine requests, ambiguous requests, requests above the limit and out-of-scope tasks.",
                    "Add prompt-injection cases that ask the agent to ignore policy, reveal keys or refund another customer.",
                    "Measure task success, policy violations, correct escalation, duplicate prevention and time to approval.",
                    "Record every failure with the exact step and add a regression test before changing the prompt or policy.",
                ],
            },
            {
                "title": "Document the safety case and demo it",
                "summary": "A reviewer should see the guardrails working, not just the happy path.",
                "steps": [
                    "Add unit tests for policy limits, idempotent retries, audit ordering and test-mode enforcement.",
                    "Write a README that explains the tool surface, trust boundary, approval policy and data rules.",
                    "Create a demo script with one successful routine action and one blocked high-risk action.",
                    "Show the audit log for both cases and explain why the model alone is never allowed to move money.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-007": {
        "description": (
            "The complete converter turns a consented social post and its images "
            "into a draft listing with a fixed schema: title, description, "
            "category, price, quantity, variants and attributes. Use "
            "schema-constrained extraction, attach confidence to each field and "
            "send weak fields to a seller review screen beside the source text "
            "and image crop. Never scrape a platform or process personal "
            "information; use synthetic, public or explicitly consented posts.\n\n"
            "Finish with listing persistence, edit tracking, field-level accuracy "
            "on a hand-labelled set and a measured comparison against manual "
            "entry. The demo should show a good draft, a low-confidence price and "
            "a missing variant, then show how the seller corrects them and what "
            "the system learns about which fields are reliable."
        ),
        "build_guide": [
            {
                "title": "Define the listing schema and consent rules",
                "summary": "A fixed schema prevents plausible output from becoming unusable data.",
                "steps": [
                    "Write the listing schema with required and optional fields, allowed types, units and a explicit unknown value.",
                    "Define what data may be processed: synthetic examples, public product data or posts with written consent, and document the exclusion rule.",
                    "Create a labelled sample of posts and images with the correct field values and a note for each ambiguous case.",
                    "Decide which fields always require review, such as price, quantity and variant, before building the extractor.",
                ],
            },
            {
                "title": "Extract text and image evidence",
                "summary": "The model needs the seller's own words and the visible product details.",
                "steps": [
                    "Normalise the post text and preserve the original snippet for each extracted field.",
                    "Run OCR on the seller's image and merge recognised size, quantity or price text into the candidate evidence.",
                    "Use schema-constrained extraction so the output is valid JSON with a confidence value per field.",
                    "Record the source snippet or crop behind every field so the review screen can show why a value was suggested.",
                ],
            },
            {
                "title": "Build the seller review experience",
                "summary": "The product is the correction flow, not the first draft.",
                "steps": [
                    "Build a review screen with the original post, image, suggested fields and confidence markers side by side.",
                    "Mark low-confidence and always-review fields clearly, and require a decision before publishing.",
                    "Allow every field to be edited or cleared, and keep the edit history for later field-level analysis.",
                    "Add a missing-value state instead of guessing a price, size or variant that is not present.",
                ],
            },
            {
                "title": "Measure field quality and seller effort",
                "summary": "A converter that saves no time has not solved the listing problem.",
                "steps": [
                    "Report accuracy per field on the hand-labelled set, not one overall extraction score.",
                    "Track edit rate per field and compare high-confidence and low-confidence suggestions.",
                    "Run a small timed comparison of manual entry versus the converter on the same posts.",
                    "Inspect the worst fields and write down whether the cause was OCR, missing evidence or the extraction prompt.",
                ],
            },
            {
                "title": "Harden and document the workflow",
                "summary": "The final repo should show consent, confidence and measurable effort.",
                "steps": [
                    "Add tests for missing images, multiple variants, conflicting prices and an empty description.",
                    "Check that the app never stores source posts or images beyond the documented retention period.",
                    "Write a README with the schema, consent policy, evaluation results and setup steps.",
                    "Record a demo of one clean draft and one draft where the seller corrects a weak price and adds a missing variant.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-008": {
        "description": (
            "The complete project is a graph analytics workbench for synthetic or "
            "licensed fraud data. Build a typed graph of accounts, devices, "
            "phones, addresses and transfers, then a rules baseline for obvious "
            "clusters. Add community detection and a graph model or node "
            "embeddings, evaluate ring-level precision and recall against "
            "planted labels, and measure lift over the rule-only baseline.\n\n"
            "Add a camouflage test with legitimate shared devices and a reviewer "
            "screen that shows the shared entities and transfer path behind each "
            "cluster. Report scoring time for a stated graph size and include a "
            "clear note that flags are signals for human review, not proof. The "
            "repo should make ring-level evaluation and false-positive cost "
            "visible, not hide them behind one accuracy number."
        ),
        "build_guide": [
            {
                "title": "Build a synthetic graph with planted rings",
                "summary": "You need known group labels before you can claim ring-level performance.",
                "steps": [
                    "Define node types for accounts, devices, phones, addresses and transactions, with a documented edge schema.",
                    "Generate normal behaviour and plant several rings that share devices, timing and transfer patterns.",
                    "Add realistic noise such as families sharing a device and small shops sharing an address.",
                    "Save the planted membership and a graph snapshot so every experiment uses the same labelled fixture.",
                ],
            },
            {
                "title": "Build rules and community baselines",
                "summary": "The baseline is what a fraud team already trusts.",
                "steps": [
                    "Write rules for many accounts on one device, circular transfers and bursts of new accounts.",
                    "Run community detection and rank components by suspicious edge density and timing.",
                    "Match predicted clusters to planted rings with an overlap threshold and report ring-level precision and recall.",
                    "Record the rules that produce the most false positives before adding a learned model.",
                ],
            },
            {
                "title": "Add graph learning and compare lift",
                "summary": "Graph learning is only interesting if it beats the baseline on the same rings.",
                "steps": [
                    "Create node features from degree, shared-entity counts, transfer statistics and account age.",
                    "Train node embeddings or a graph neural network against the planted ring labels while keeping the graph split honest.",
                    "Score clusters from learned embeddings and compare ring-level precision and recall with the rule baseline.",
                    "Report lift, scoring time and the graph size so the result has a deployment context.",
                ],
            },
            {
                "title": "Test camouflage and build the analyst view",
                "summary": "Legitimate sharing is the hard case that a demo usually omits.",
                "steps": [
                    "Add more legitimate shared devices and addresses, then measure the false-positive cost for both methods.",
                    "Build a cluster page that shows shared devices, transfer paths and the reasons the cluster was ranked highly.",
                    "Let an analyst mark a cluster as confirmed, dismissed or needs-more-evidence and store the decision.",
                    "Show the ring-level metrics beside the ranked queue so an analyst understands the tool's error rate.",
                ],
            },
            {
                "title": "Document the evaluation and limits",
                "summary": "Synthetic evidence is useful only when its assumptions are explicit.",
                "steps": [
                    "Add tests for empty graphs, isolated nodes, a single shared device and a large component.",
                    "Write a data card covering the generator, planted patterns, noise levels and the limits of synthetic labels.",
                    "Document why account-level accuracy is not the main metric and how ring matching works.",
                    "Record a demo that shows a recovered ring, a camouflaged false positive and the evidence behind both.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-009": {
        "description": (
            "The complete tool reads synthetic lab reports, extracts the test "
            "table, validates units and reference ranges, flags out-of-range "
            "values and explains each result in plain language with a source. "
            "It does not diagnose, and it refuses when a test is unknown, a range "
            "is missing or the document is too poor to read. Keep the original "
            "value and unit visible beside every explanation so a patient can "
            "check the claim.\n\n"
            "Finish with separate extraction metrics for test name, value, unit "
            "and range, out-of-range recall, a readability score and a review of "
            "the refusal path. The repo should use synthetic reports only and "
            "show a not-medical-advice notice in the product, not only in the "
            "README."
        ),
        "build_guide": [
            {
                "title": "Generate synthetic reports and define the schema",
                "summary": "Health data needs a safe fixture before any model work begins.",
                "steps": [
                    "Create synthetic lab reports with varied layouts, units, reference ranges and a few intentionally out-of-range values.",
                    "Define the extraction schema for test name, value, unit, range, flag and source page or crop.",
                    "Collect public reference-range information with a citation and a note on how ranges vary by lab and population.",
                    "Write the not-medical-advice boundary and the refusal rules before building the explanation step.",
                ],
            },
            {
                "title": "Extract tables from PDFs and photos",
                "summary": "The parser must preserve which range belongs to which test.",
                "steps": [
                    "Build a PDF path with table extraction and an image path with OCR, then normalise both into the same intermediate table.",
                    "Map columns by header and position so a value is never attached to the wrong test or range.",
                    "Validate numeric values and units, and flag rows with missing or contradictory fields.",
                    "Keep the original text and crop for each row so a reviewer can verify the extraction.",
                ],
            },
            {
                "title": "Flag values and explain them safely",
                "summary": "The explanation should inform a conversation, not replace a clinician.",
                "steps": [
                    "Compare each value with its parsed range, handle open-ended ranges and mark values that cannot be compared.",
                    "Generate a plain-language explanation from a small, reviewed template set with a source for each statement.",
                    "Refuse to explain unknown tests, missing ranges or values that fail validation.",
                    "Show the original value, unit and range beside the explanation and repeat the not-medical-advice notice.",
                ],
            },
            {
                "title": "Measure extraction and explanation quality",
                "summary": "A single accuracy number hides whether OCR or interpretation failed.",
                "steps": [
                    "Report test-name, value, unit and range accuracy separately on held-out synthetic reports.",
                    "Measure out-of-range recall and the false-flag rate on in-range values.",
                    "Score explanation readability and review a sample with a non-expert to catch confusing language.",
                    "Measure correct refusal on unknown tests and unreadable documents.",
                ],
            },
            {
                "title": "Harden privacy and document the limits",
                "summary": "The safest demo is one that cannot accidentally process a real patient record.",
                "steps": [
                    "Add a startup and upload check that rejects files containing obvious real patient identifiers or documents the synthetic-only policy.",
                    "Test malformed PDFs, rotated images, missing units and unsupported tests.",
                    "Write a README with the synthetic data policy, extraction metrics, refusal rules and medical disclaimer.",
                    "Record a demo of one clear out-of-range result and one case where the tool correctly refuses to explain.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-010": {
        "description": (
            "The complete detector processes short videos end to end: face "
            "extraction, frame sampling, a frame-level artifact model and a "
            "temporal consistency signal. Train on one dataset and reserve a "
            "second dataset only for testing, so the cross-dataset gap is real. "
            "Add compression tests, a frame-level confidence chart and a "
            "Grad-CAM or temporal attention view that a reviewer can inspect.\n\n"
            "Finish with in-dataset and cross-dataset AUROC, accuracy loss under "
            "compression, frames per second and a clear statement that a score is "
            "probabilistic evidence, not proof about a person. The repo should "
            "show the generalisation gap prominently rather than leading with a "
            "clean benchmark number."
        ),
        "build_guide": [
            {
                "title": "Build video ingestion and face extraction",
                "summary": "Bad face crops make every later metric meaningless.",
                "steps": [
                    "Write a loader that samples frames at a fixed rate and records the original frame index and timestamp.",
                    "Detect and align faces consistently, then reject or pad clips where the face is missing or too small.",
                    "Create a manifest with video id, label, dataset, frame count, compression level and face-crop quality.",
                    "Inspect a sample of real and manipulated clips to confirm the crops align across frames.",
                ],
            },
            {
                "title": "Train a frame-level baseline",
                "summary": "Start with the simplest model that can expose dataset shortcuts.",
                "steps": [
                    "Train a small image classifier on face frames with the official subject-level split from the first dataset.",
                    "Aggregate frame scores into a video score using a documented rule such as mean or top-k mean.",
                    "Measure in-dataset AUROC and inspect false positives for compression, occlusion or unusual lighting.",
                    "Save a frame-level confidence chart for every test video so the aggregate score is explainable.",
                ],
            },
            {
                "title": "Add temporal consistency and generalisation tests",
                "summary": "A second dataset is the only honest test of whether the model learned manipulation cues.",
                "steps": [
                    "Add a temporal model or a consistency feature that compares identity, boundaries and flicker across frames.",
                    "Train only on the first dataset and evaluate on the second without fine-tuning or threshold tuning on test.",
                    "Report in-dataset and cross-dataset AUROC and explain the gap by dataset, generator and compression differences.",
                    "Add heavy-compression and low-resolution variants to show how quickly performance falls.",
                ],
            },
            {
                "title": "Build the reviewer experience",
                "summary": "The evidence view matters as much as the score.",
                "steps": [
                    "Show the video score, per-frame confidence and the frames that contributed most to the decision.",
                    "Add a Grad-CAM or temporal attention overlay that a reviewer can toggle on and off.",
                    "Display the dataset and compression conditions used for evaluation beside the score.",
                    "Keep a persistent note that the result is probabilistic and not an accusation about a named person.",
                ],
            },
            {
                "title": "Measure speed, document and demo",
                "summary": "A detector that cannot process a video in reasonable time is not deployable.",
                "steps": [
                    "Measure end-to-end inference in frames per second on a stated device and report the bottleneck.",
                    "Write a model card with training data, evaluation splits, cross-dataset results and known failure modes.",
                    "Add tests for a missing face, a very short clip, a corrupted file and a video with no audio.",
                    "Record a demo that shows a correct detection, a cross-dataset failure and the evidence view.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-011": {
        "description": (
            "The complete digitizer handles a scanned synthetic form end to end: "
            "field detection, label-value association, OCR for printed and "
            "handwritten values, format validation and a review screen for "
            "low-confidence fields. Keep the original crop beside every value, "
            "allow corrections without losing the OCR text, and export clean "
            "structured data with an audit of edits.\n\n"
            "Measure field accuracy before and after review, auto-accept rate, "
            "validation catch rate and seconds per form against manual entry. The "
            "repo should use synthetic forms with fake data only, show why a field "
            "was routed to review, and make the review step measurably worth its "
            "cost."
        ),
        "build_guide": [
            {
                "title": "Generate forms and define the field schema",
                "summary": "The review screen needs a stable map from label to value.",
                "steps": [
                    "Create synthetic forms with printed labels, handwritten values, checkboxes and a few blurry or rotated scans.",
                    "Define the output schema for each field, its validation rule and its confidence threshold.",
                    "Label a development and held-out set with the correct values and crop regions.",
                    "Write the fake-data policy and ensure no real personal information can enter the pipeline.",
                ],
            },
            {
                "title": "Detect fields and associate values",
                "summary": "A good value attached to the wrong label is still a bad extraction.",
                "steps": [
                    "Detect text boxes and group them into labels, values, checkboxes and table cells.",
                    "Associate each value with the nearest label using position, reading order and a small set of layout rules.",
                    "Run OCR with confidence per box and preserve the original crop for every field.",
                    "Flag fields with no label, multiple candidate values or an unsupported layout.",
                ],
            },
            {
                "title": "Validate values and route weak fields",
                "summary": "Validation catches errors that OCR confidence alone misses.",
                "steps": [
                    "Implement validators for dates, phone numbers, PIN codes, amounts and required fields.",
                    "Combine OCR confidence, association confidence and validation result into a review priority.",
                    "Route low-confidence or invalid fields to a review queue while auto-accepting only fields that pass every check.",
                    "Show the original crop, OCR text and suggested value together so correction is fast.",
                ],
            },
            {
                "title": "Build review, export and audit",
                "summary": "The correction trail is what makes the output trustworthy.",
                "steps": [
                    "Build a review screen that lets a person correct a value, mark it unreadable or skip it with a reason.",
                    "Persist every edit with the field id, previous value, new value, reviewer and timestamp.",
                    "Export structured data only after review, with a manifest of corrected and unreadable fields.",
                    "Add a form-level status view for pending review, completed and exported.",
                ],
            },
            {
                "title": "Measure the human-in-the-loop value",
                "summary": "Review is a cost; the project should show what it buys.",
                "steps": [
                    "Report field accuracy before and after review, auto-accept rate and validation catch rate.",
                    "Time the review flow and compare total seconds per form with manual entry on the same sample.",
                    "Inspect the fields that still fail after review and classify layout, OCR and validation causes.",
                    "Write a README and demo that covers one auto-accepted form and one form with a corrected date and code.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-012": {
        "description": (
            "The complete detector starts with public Kepler or TESS light "
            "curves, cleans gaps and outliers, searches for periodic transit-like "
            "dips and builds a feature table from each candidate. Train a "
            "classifier with star-grouped splits to avoid leakage, then check "
            "recovery on known confirmed planets and break false positives into "
            "eclipsing binaries, instrumental noise and other causes.\n\n"
            "Finish with precision, recall, F1 and PR-AUC, a folded light-curve "
            "view for every candidate and a threshold choice tied to a review "
            "budget. The repo should make the scientific cleaning and the "
            "leakage control visible, not hide them behind one model score."
        ),
        "build_guide": [
            {
                "title": "Acquire and clean light curves",
                "summary": "Transit signals are small, so cleaning choices change the result.",
                "steps": [
                    "Download a small set of public light curves and record the mission, target id and data release.",
                    "Remove gaps, normalise flux and flag outliers with a documented rule rather than silent interpolation.",
                    "Plot raw and cleaned curves for a few known planets and a few false positives to verify the pipeline.",
                    "Save the cleaning parameters with each processed curve so the step is reproducible.",
                ],
            },
            {
                "title": "Search for periodic transit candidates",
                "summary": "Box least squares gives the candidate; the features decide whether it is believable.",
                "steps": [
                    "Run a box least squares search over a documented period grid and record the best period, depth and duration.",
                    "Fold the light curve at each candidate period and compute features such as depth, duration, shape and secondary-eclipse evidence.",
                    "Keep the top candidates per star, not only the single best period, so later classification can compare them.",
                    "Inspect a sample of folded curves to catch period aliases and artefacts before training.",
                ],
            },
            {
                "title": "Train with star-grouped evaluation",
                "summary": "A random split can memorise a star and inflate the score.",
                "steps": [
                    "Build a feature table with candidate, star and label, and split by star id rather than by candidate.",
                    "Train a simple tree-based baseline and compare it with a stronger model only if the baseline is clearly limited.",
                    "Report precision, recall, F1 and PR-AUC on the held-out stars and choose a threshold from a review budget.",
                    "Check for features that leak the label, such as catalogue flags unavailable in a real search.",
                ],
            },
            {
                "title": "Validate recovery and false positives",
                "summary": "Known planets and a false-positive taxonomy make the result scientifically useful.",
                "steps": [
                    "Run the pipeline on confirmed planets and report how often the correct period is recovered in the top candidates.",
                    "Group false positives by cause such as eclipsing binary, blended star, stellar variability and noise.",
                    "Inspect the confusion between planet-like binaries and real planets and propose the next feature to add.",
                    "Write a short evaluation note that separates detection, classification and ranking performance.",
                ],
            },
            {
                "title": "Build the candidate review view",
                "summary": "An astronomer needs the folded curve and the evidence behind a rank.",
                "steps": [
                    "Build a page that shows the folded light curve, period, depth, duration and classifier score for one candidate.",
                    "Add a ranked list with filters for score, period and false-positive cause.",
                    "Show the known-planet recovery result and the evaluation split in the app so the score has context.",
                    "Document setup and record a demo of one recovered planet and one high-scoring false positive.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-013": {
        "description": (
            "The complete screener parses public orbital elements, propagates "
            "positions over a stated window, prunes candidate pairs cheaply and "
            "computes time, distance and relative velocity at closest approach. "
            "Build a distance-only rule first, then a risk model on conjunction "
            "features and compare recall at a fixed false-alarm budget.\n\n"
            "Finish with a ranked event list, a detail view showing the approach "
            "geometry, screening throughput and a clear note that outputs are "
            "estimates, not official collision warnings. The repo should show the "
            "pruning step and the baseline comparison because they are what make "
            "the project credible."
        ),
        "build_guide": [
            {
                "title": "Parse orbits and define the screening window",
                "summary": "The time window and element freshness set the limits of every later claim.",
                "steps": [
                    "Download a small public orbital element set and record the epoch and source for each object.",
                    "Parse the elements into a common structure and validate required fields before propagation.",
                    "Choose a screening window and time step that balance coverage with runtime, and write down the assumption.",
                    "Flag stale or incomplete elements so the risk list does not treat them as equally reliable.",
                ],
            },
            {
                "title": "Propagate orbits and prune candidate pairs",
                "summary": "A useful screener cannot propagate every pair at full resolution.",
                "steps": [
                    "Implement SGP4 propagation and compute position and velocity at each time step.",
                    "Use a coarse filter such as altitude band or bounding box to remove pairs that cannot come close.",
                    "Propagate only surviving pairs at a finer step and compute the minimum distance and time of closest approach.",
                    "Measure pairs screened per second and report how much work the pruning step removed.",
                ],
            },
            {
                "title": "Build a distance baseline and a risk model",
                "summary": "The model has to beat the simple rule at the same false-alarm cost.",
                "steps": [
                    "Rank events by minimum distance and record the baseline recall at a stated false-alarm rate.",
                    "Create features such as relative velocity, time to approach, element age and uncertainty proxy where available.",
                    "Train a risk classifier on conjunction data and compare recall and PR-AUC with the distance rule.",
                    "Inspect false positives and document whether they come from stale elements, close but diverging orbits or label noise.",
                ],
            },
            {
                "title": "Build the event review screen",
                "summary": "An operator needs the geometry and the assumptions, not just a rank.",
                "steps": [
                    "Build a ranked event list with time, minimum distance, relative velocity and model score.",
                    "Add a detail view that shows the two objects, the approach time and the input element epoch.",
                    "Display the false-alarm budget and the baseline comparison beside the ranking controls.",
                    "Keep a visible note that the output is a screening aid and not an official alert.",
                ],
            },
            {
                "title": "Evaluate, optimise and document",
                "summary": "Throughput and uncertainty are part of the result.",
                "steps": [
                    "Report recall of high-risk events at a fixed false-alarm rate, PR-AUC and screening throughput.",
                    "Profile the propagation and pruning steps, then optimise the largest bottleneck without changing the evaluation.",
                    "Add tests for stale elements, missing fields, a single object and an empty candidate set.",
                    "Write a README with the time window, assumptions, metrics and a demo of one close approach.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-014": {
        "description": (
            "The complete assistant reads a soil report with OCR, validates the "
            "fields, adds satellite and weather context, and answers questions "
            "from verified agricultural guidance with citations. It refuses when "
            "retrieved evidence is weak or the question is outside the corpus. "
            "Every answer shows the input values, their dates, the cited passage "
            "and a decision-support notice.\n\n"
            "Finish with expert-written questions, answer accuracy, citation "
            "support, OCR field accuracy and a measured refusal path. The repo "
            "should keep soil, satellite and weather data visibly separate rather "
            "than blending them into an unexplained score, and it should say "
            "clearly that local agricultural officers remain the authority."
        ),
        "build_guide": [
            {
                "title": "Build the soil report and context schema",
                "summary": "The assistant needs structured inputs before it can reason about them.",
                "steps": [
                    "Define a schema for soil pH, organic carbon, nitrogen, phosphorus, potassium and any locally relevant fields with units.",
                    "Extract those fields from a synthetic or consented soil report and keep the source crop and confidence per value.",
                    "Add optional satellite and weather inputs with timestamps, units and an explicit uncertainty label.",
                    "Write the decision-support notice and refusal policy before generating any advice.",
                ],
            },
            {
                "title": "Assemble verified guidance and retrieval",
                "summary": "The corpus is the boundary of what the assistant is allowed to claim.",
                "steps": [
                    "Collect guidance you have reuse rights for, record the source and date, and exclude material with unclear terms.",
                    "Chunk the guidance by recommendation, crop, region and season with stable citation ids.",
                    "Build a retrieval index and test it on questions that combine a soil value with a crop or season.",
                    "Record retrieval scores and the returned passages so a weak answer can be traced to a retrieval miss.",
                ],
            },
            {
                "title": "Answer with citations and refusal",
                "summary": "Local advice needs a source, not fluent general knowledge.",
                "steps": [
                    "Generate an answer only from the retrieved passages and the structured soil and weather inputs.",
                    "Cite the exact passage behind each recommendation and keep the passage visible beside the answer.",
                    "Refuse when retrieval is weak, the crop is outside the corpus or the question asks for a guarantee.",
                    "Keep satellite and weather statements separate from measured soil values and label their dates and uncertainty.",
                ],
            },
            {
                "title": "Evaluate with expert questions",
                "summary": "Accuracy and citation support must be measured separately.",
                "steps": [
                    "Write at least 120 questions with reference answers and the supporting guidance section.",
                    "Measure answer accuracy, citation support, refusal correctness and OCR field accuracy on held-out reports.",
                    "Inspect failures by input error, retrieval miss, citation mismatch and overconfident language.",
                    "Ask a domain expert to review a small sample and record where the answer is technically correct but locally inappropriate.",
                ],
            },
            {
                "title": "Build the farmer view and document limits",
                "summary": "The interface should make uncertainty and sources easy to see.",
                "steps": [
                    "Build an upload and question flow that shows extracted soil values, the cited answer and the decision-support notice.",
                    "Add a source drawer where a farmer can read the exact guidance passage.",
                    "Show a refusal state with a next step such as contacting a local agricultural officer.",
                    "Write a README and demo covering a supported question, a weak-retrieval refusal and one corrected OCR field.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-015": {
        "description": (
            "The complete copilot ingests engineering documents with page and "
            "section ids, builds hybrid retrieval and answers specification "
            "questions with exact citations. Add a citation checker that verifies "
            "whether each passage supports the claim, plus a documentation draft "
            "path from structured product data. Measure retrieval recall@k, "
            "citation support, answer accuracy and latency separately.\n\n"
            "Finish with a source viewer, a labelled question set drawn from real "
            "design reviews and a report that explains the main failure modes, "
            "especially tables and diagrams. The repo should be clear that this "
            "is a learning aid and every answer must be checked against the cited "
            "document."
        ),
        "build_guide": [
            {
                "title": "Ingest documents with stable source ids",
                "summary": "If a citation cannot be opened exactly, the answer is not usable.",
                "steps": [
                    "Collect engineering documents you have permission to process and record the source and version.",
                    "Parse pages and sections into chunks with document id, page number, section heading and character offsets.",
                    "Preserve tables as structured rows when possible and flag figures or diagrams that the text pipeline cannot read.",
                    "Build a source viewer that opens the exact page and highlights the cited text.",
                ],
            },
            {
                "title": "Build hybrid retrieval and cited answers",
                "summary": "Keyword and semantic retrieval fail in different ways.",
                "steps": [
                    "Combine a keyword index with an embedding index and merge results with a documented rule.",
                    "Answer only from retrieved chunks and require at least one exact source id per claim.",
                    "Show the cited passage beside the generated answer, not only a document link.",
                    "Refuse when retrieval returns no relevant chunk or the question is outside the corpus.",
                ],
            },
            {
                "title": "Check citation support",
                "summary": "A relevant document does not always support the specific claim.",
                "steps": [
                    "Build a checker that compares each claim with its cited passage and labels support as supported, partial or unsupported.",
                    "Evaluate the checker on a hand-labelled set of answer-citation pairs and report precision and recall.",
                    "Block or visibly flag answers with unsupported citations before they reach an engineer.",
                    "Keep the checker output in the response so a reviewer can inspect the decision.",
                ],
            },
            {
                "title": "Add the documentation draft path",
                "summary": "The second workflow makes the project more than a document chatbot.",
                "steps": [
                    "Define a documentation template with product data fields and required source links.",
                    "Generate a draft from structured data and retrieved specifications, leaving placeholders for missing values.",
                    "Show every sentence that needs a citation and prevent export when a required source is missing.",
                    "Add a reviewer screen that compares the draft with the source documents side by side.",
                ],
            },
            {
                "title": "Evaluate, measure latency and document",
                "summary": "Retrieval quality and speed are the claims that matter.",
                "steps": [
                    "Create at least 75 labelled questions with the correct source sections and reference answers.",
                    "Report recall@5, answer accuracy, verified-citation rate and latency for retrieval and generation separately.",
                    "Inspect failures by table, diagram, ambiguous wording and missing document, and prioritise the next fix.",
                    "Write a README and demo that includes one cited answer, one rejected citation and one generated draft.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-016": {
        "description": (
            "The complete project treats attribution as a probabilistic "
            "investigation aid. Assemble text from HC3, M4 or MAGE with model and "
            "prompt labels, build stylometric and token-statistics features, and "
            "compare a simple baseline with a fine-tuned transformer. Keep a "
            "held-out prompt split and a separate unseen-model test so the result "
            "shows generalisation rather than memorised fingerprints.\n\n"
            "Finish with per-model accuracy and F1, a calibration curve, an "
            "ablation for the stylometric features and a demo that shows a "
            "low-confidence prediction. The UI must say that attribution is not "
            "proof of authorship and must not present a label as an accusation."
        ),
        "build_guide": [
            {
                "title": "Assemble labelled text and define splits",
                "summary": "Prompt and model leakage decide whether the evaluation means anything.",
                "steps": [
                    "Collect datasets with clear model labels, prompt ids and licences, and record the source for each subset.",
                    "Normalise text length and encoding, and remove duplicated passages before splitting.",
                    "Create a seen-model split with held-out prompts and a separate unseen-model set that is never used for training.",
                    "Write a dataset card with label counts, prompt sources, model versions and known gaps.",
                ],
            },
            {
                "title": "Build stylometric and baseline features",
                "summary": "A simple baseline shows how much the transformer really adds.",
                "steps": [
                    "Extract features such as sentence length, punctuation, function-word rates, vocabulary richness and repetition.",
                    "Train a logistic regression or gradient-boosting baseline on those features only.",
                    "Evaluate per model on seen and unseen prompts and inspect which features carry the most weight.",
                    "Keep the feature extraction deterministic so the same passage always produces the same vector.",
                ],
            },
            {
                "title": "Fine-tune and test on unseen models",
                "summary": "The unseen-model number is the honest headline.",
                "steps": [
                    "Fine-tune a small transformer on the seen-model training split with a fixed seed and documented budget.",
                    "Evaluate on held-out prompts and then on the unseen-model set without further tuning.",
                    "Report accuracy and F1 per model and the generalisation gap between seen and unseen conditions.",
                    "Run an ablation that combines stylometric features with the transformer to see whether they help.",
                ],
            },
            {
                "title": "Calibrate confidence and explain failures",
                "summary": "A confident wrong attribution is the main harm.",
                "steps": [
                    "Measure calibration on held-out data and apply temperature scaling or isotonic calibration.",
                    "Show a reliability curve and the share of predictions that fall below a usable confidence threshold.",
                    "Inspect misattributions after editing, translation or short passages and document the failure modes.",
                    "Add a warning and a no-conclusion state for low-confidence outputs.",
                ],
            },
            {
                "title": "Build the demo and responsible-use note",
                "summary": "The product language should prevent misuse before it happens.",
                "steps": [
                    "Build a page that shows the predicted source, per-model probabilities and the calibration status.",
                    "Add a prominent note that attribution is probabilistic and not proof of authorship.",
                    "Include a sample of an edited passage where the model correctly becomes uncertain.",
                    "Write a README with the splits, metrics, calibration method and ethical limits.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-017": {
        "description": (
            "The complete identifier parses tandem mass spectra, predicts a "
            "molecular fingerprint or substructures, ranks candidates from a "
            "compound database and shows the evidence to a chemist. Use RDKit "
            "for molecule handling and keep the candidate database size visible, "
            "because a molecule absent from the database can never be ranked.\n\n"
            "Finish with top-1, top-5 and top-10 accuracy, mean Tanimoto "
            "similarity, runtime per spectrum and a spectrum viewer beside the "
            "ranked candidates. The repo should explain the top-k shortlist "
            "workflow and document database coverage as a limitation."
        ),
        "build_guide": [
            {
                "title": "Parse spectra and build candidate molecules",
                "summary": "The representation and candidate library define the ceiling.",
                "steps": [
                    "Download a public spectral library, record the licence and normalise peaks into a consistent m/z and intensity representation.",
                    "Filter or flag spectra with missing precursor mass, adduct information or inconsistent metadata.",
                    "Build a candidate molecule table with RDKit fingerprints and valid structures, and record the database size.",
                    "Split spectra by molecule or source so the same compound cannot appear in both train and test.",
                ],
            },
            {
                "title": "Train a fingerprint prediction model",
                "summary": "Predicting a stable intermediate is easier than generating a structure.",
                "steps": [
                    "Convert spectra into a fixed-length input and train a small neural network to predict molecular fingerprints.",
                    "Choose a loss that handles sparse fingerprint bits and report mean Tanimoto similarity on validation spectra.",
                    "Inspect predictions on a few known molecules to see which substructures are systematically missed.",
                    "Save the model version and preprocessing parameters with the evaluation artifact.",
                ],
            },
            {
                "title": "Rank candidates and measure top-k",
                "summary": "A chemist reviews a shortlist, so top-10 is a practical metric.",
                "steps": [
                    "Compute fingerprint similarity between the predicted fingerprint and every candidate in the database.",
                    "Rank candidates and report top-1, top-5 and top-10 accuracy on the held-out split.",
                    "Measure runtime per spectrum and repeat the ranking with a smaller database to show the scaling effect.",
                    "Inspect cases where the correct molecule is absent and report them separately from ranking failures.",
                ],
            },
            {
                "title": "Build the chemist review view",
                "summary": "The spectrum and candidate evidence should be inspectable together.",
                "steps": [
                    "Build a page that shows the input spectrum, predicted fingerprint similarity and the ranked candidate list.",
                    "Show the candidate structure, database id and the score contribution or similarity value.",
                    "Add a clear missing-candidate state when no result passes a usable threshold.",
                    "Let a chemist mark a candidate as plausible or rejected and store the decision for later analysis.",
                ],
            },
            {
                "title": "Ablate, document and demo",
                "summary": "Preprocessing and database size are part of the result.",
                "steps": [
                    "Ablate peak normalisation, fingerprint type and database size to show their effect on top-k accuracy.",
                    "Write a README with the spectral source, candidate database, metrics and coverage limitation.",
                    "Add tests for an empty spectrum, a malformed peak list and a molecule that fails RDKit parsing.",
                    "Record a demo where the correct molecule appears in the top five and one where coverage prevents a correct answer.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-018": {
        "description": (
            "The complete agent solves engineering problems through tools, not "
            "prose arithmetic. Define unit-aware calculation, symbolic maths, "
            "structural and circuit tools, make the agent show its constraints, "
            "and add a verifier for dimensions, magnitudes and domain checks. "
            "Evaluate on textbook problems with known answers and keep a visible "
            "trace of every tool call.\n\n"
            "Finish with solve rate, verification pass rate, a failure taxonomy "
            "for unit, constraint and reasoning errors, and a reviewer view that "
            "replays the calculation. The app should state that answers are not a "
            "substitute for official engineering or safety decisions."
        ),
        "build_guide": [
            {
                "title": "Define the tool surface and problem schema",
                "summary": "The agent is only as trustworthy as its tools and their contracts.",
                "steps": [
                    "Choose two domains, such as structural analysis and circuits, and list the calculations the agent may perform.",
                    "Write strict schemas for each tool with required units, input ranges and output types.",
                    "Create a problem schema with given values, unknowns, constraints and the expected answer format.",
                    "Define which actions are pure calculations and which require an explicit assumption from the user.",
                ],
            },
            {
                "title": "Build the agent and tool trace",
                "summary": "The model should choose a tool, not invent the arithmetic.",
                "steps": [
                    "Implement an agent loop that restates the knowns and unknowns, selects a tool and records each call.",
                    "Use a unit-aware calculator and symbolic solver so dimensions are carried through every step.",
                    "Show the tool inputs, outputs and assumptions in a trace that a reviewer can inspect.",
                    "Stop and ask for clarification when a required value or unit is missing instead of guessing.",
                ],
            },
            {
                "title": "Add an independent verifier",
                "summary": "A second opinion from the same model is not verification.",
                "steps": [
                    "Check dimensional consistency, expected units, plausible magnitude and domain constraints such as equilibrium or power balance.",
                    "Recompute critical arithmetic independently from the agent's prose and compare the result.",
                    "Block an answer when verification fails and show the exact failed check.",
                    "Add tests with deliberately wrong units and inconsistent values to prove the verifier catches them.",
                ],
            },
            {
                "title": "Build the known-solution evaluation",
                "summary": "Objective answers make this project measurable.",
                "steps": [
                    "Collect at least 140 textbook or designed problems with published answers and unit expectations.",
                    "Score each answer automatically with a tolerance and a unit check, then classify every failure by hand.",
                    "Report solve rate, verification pass rate and the share of answers that were corrected or blocked by the verifier.",
                    "Compare the agent with a no-tool language-model baseline on the same set.",
                ],
            },
            {
                "title": "Package the trace and document the limits",
                "summary": "The failure taxonomy is more useful than a single solve rate.",
                "steps": [
                    "Build a page that accepts a problem, shows the trace and highlights the verification result.",
                    "Add a reviewer note that the output is educational and not an official engineering decision.",
                    "Write a README with tool schemas, evaluation design, failure examples and setup instructions.",
                    "Record a demo of one correct multi-step solve and one answer blocked by a unit error.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-019": {
        "description": (
            "The complete library implements tensors, a computation graph, "
            "reverse-mode automatic differentiation, layers, activations, losses "
            "and SGD and Adam. Every operation has a numerical gradient check, "
            "and a small network trains on Fashion-MNIST or a comparable dataset. "
            "Compare accuracy and training time with an equivalent PyTorch model "
            "under the same data and architecture.\n\n"
            "Finish with a documented operation list, a graph visualisation for "
            "one backward pass, convergence tests and a README that explains what "
            "the library does not support. The strongest demo shows a failed "
            "gradient check being caught before training, then a successful run "
            "that matches PyTorch within a stated tolerance."
        ),
        "build_guide": [
            {
                "title": "Implement tensors and the computation graph",
                "summary": "Autograd starts with a small set of correct operations.",
                "steps": [
                    "Implement a tensor wrapper around NumPy with shape, data and a gradient buffer.",
                    "Record parent operations and local backward functions for add, multiply, matrix multiply and reshape.",
                    "Implement reverse-mode traversal in topological order and accumulate gradients for shared subgraphs.",
                    "Write a numerical gradient checker and run it on every operation before adding layers.",
                ],
            },
            {
                "title": "Add layers, losses and optimisers",
                "summary": "The training stack should be built from tested primitives.",
                "steps": [
                    "Implement linear layers, ReLU, sigmoid or softmax and cross-entropy with clear shape expectations.",
                    "Add SGD with momentum and Adam with documented defaults and state handling.",
                    "Build a small training loop with batching, shuffling, loss logging and a validation pass.",
                    "Test convergence on a tiny synthetic problem before touching a real dataset.",
                ],
            },
            {
                "title": "Train on a real dataset and compare with PyTorch",
                "summary": "The comparison proves correctness beyond a toy example.",
                "steps": [
                    "Train a small classifier on Fashion-MNIST or a comparable public dataset with a fixed seed.",
                    "Report test accuracy and per-epoch training time for your library.",
                    "Train an equivalent PyTorch model with the same architecture, optimiser and data split.",
                    "Report the accuracy gap and explain any difference in speed or numerical behaviour.",
                ],
            },
            {
                "title": "Make the graph inspectable",
                "summary": "A visual backward pass turns the implementation into a teaching tool.",
                "steps": [
                    "Expose a graph export for one forward and backward pass with operation names and shapes.",
                    "Build a simple visualisation or notebook that shows the path from output to inputs.",
                    "Add a demo that intentionally breaks a gradient and shows the numerical check failing.",
                    "Document the supported operations and the ones that are deliberately out of scope.",
                ],
            },
            {
                "title": "Test, document and demo",
                "summary": "The library is a software project, not only a maths exercise.",
                "steps": [
                    "Add tests for shape errors, broadcasting, shared subgraphs, zero gradients and optimizer state.",
                    "Verify that the reported accuracy and timing can be reproduced from a clean command.",
                    "Write a README with the API, graph model, gradient-check method and PyTorch comparison.",
                    "Record a demo of a gradient check, a short training run and the graph view.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-020": {
        "description": (
            "The complete project is a small GPT-style language model built from "
            "scratch: a character-level or byte-pair tokenizer, causal "
            "self-attention, transformer blocks, a training loop and sampling with "
            "temperature and top-k. Train on a public-domain corpus and track "
            "training loss and validation perplexity, with a fixed seed and a "
            "stated compute budget.\n\n"
            "Finish with an ablation on model size or context length, tokens per "
            "second, a prompt-and-sampling demo and a model card that labels "
            "generated text as machine-generated. The repo should show perplexity "
            "and sample quality together, because a low loss does not guarantee "
            "useful or truthful output."
        ),
        "build_guide": [
            {
                "title": "Build the tokenizer and data pipeline",
                "summary": "Tokenisation choices show up in every later result.",
                "steps": [
                    "Choose a character-level tokenizer for the first version and record vocabulary size and special tokens.",
                    "Clean a public-domain corpus, split train and validation by document, and create fixed-length training sequences.",
                    "Add a batching pipeline with a seed and a reproducible shuffle.",
                    "Inspect decoded samples from the dataset to catch encoding, boilerplate or licence issues before training.",
                ],
            },
            {
                "title": "Implement causal self-attention and the model",
                "summary": "The architecture should be understandable enough to explain in an interview.",
                "steps": [
                    "Implement scaled dot-product attention with a causal mask and verify that future tokens cannot influence a prediction.",
                    "Add multi-head attention, feed-forward blocks, layer normalisation and residual connections.",
                    "Build a small decoder-only model with a configurable layer count, width and context length.",
                    "Write shape tests for a single sequence and a batch before running a full training job.",
                ],
            },
            {
                "title": "Train and track validation perplexity",
                "summary": "A fixed budget and validation split make the run comparable.",
                "steps": [
                    "Write a training loop with gradient clipping, learning-rate warmup and periodic validation.",
                    "Log train loss and validation perplexity by step and save a checkpoint with the config.",
                    "Train a tiny model first to confirm the loss decreases before spending more compute.",
                    "Record tokens seen, wall-clock time and hardware so the budget is explicit.",
                ],
            },
            {
                "title": "Add sampling and run ablations",
                "summary": "Generation behaviour is part of the evaluation.",
                "steps": [
                    "Implement temperature and top-k sampling with a fixed prompt and seed for comparisons.",
                    "Compare at least two model sizes or context lengths on validation perplexity and tokens per second.",
                    "Inspect repetition, coherence and nonsense at low and high temperatures, and document the trade-off.",
                    "Add a small prompt demo where a reviewer can change the sampling settings.",
                ],
            },
            {
                "title": "Write the model card and demo",
                "summary": "The limits of a tiny model should be stated, not hidden.",
                "steps": [
                    "Document the corpus, tokenizer, architecture, parameter count, compute budget and validation perplexity.",
                    "Add a model card with known biases, memorisation risk and the instruction to label generated text.",
                    "Write setup and training commands and include one reproducible sample output.",
                    "Record a demo of a prompt, a low-temperature response and a high-temperature response.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-021": {
        "description": (
            "The complete project is a playable board-game AI. Build a correct "
            "rules engine, minimax with alpha-beta pruning and a heuristic "
            "evaluation, then Monte Carlo Tree Search. Run a fixed tournament "
            "against a random player and between agents, measuring win rate, "
            "positions searched, time per move and the pruning reduction.\n\n"
            "Finish with a browser board, difficulty levels, a search-tree view "
            "and a reproducible tournament command. The repo should show that "
            "pruning preserves the chosen move while reducing work, not just "
            "claim that alpha-beta is faster."
        ),
        "build_guide": [
            {
                "title": "Build and test the rules engine",
                "summary": "Every search result is only as correct as the game state.",
                "steps": [
                    "Implement board state, legal moves, move application and terminal detection for one game.",
                    "Write tests for wins, draws, illegal moves and a nearly full board.",
                    "Add a canonical state key for transposition detection and tournament replay.",
                    "Build a random agent to exercise the engine and establish a baseline.",
                ],
            },
            {
                "title": "Implement minimax with alpha-beta",
                "summary": "Pruning should return the same move with less search.",
                "steps": [
                    "Implement plain minimax with a depth limit and terminal scoring.",
                    "Add alpha-beta bounds and record the number of positions searched with and without pruning.",
                    "Design a simple heuristic evaluation and document every term and weight.",
                    "Test that pruned and unpruned search choose the same move on a small depth.",
                ],
            },
            {
                "title": "Add Monte Carlo Tree Search",
                "summary": "A second search family makes the comparison meaningful.",
                "steps": [
                    "Implement selection, expansion, simulation and backpropagation with a fixed simulation budget.",
                    "Use the random agent for playouts first, then try a light heuristic policy.",
                    "Record the chosen move, visit counts and time per move.",
                    "Tune the exploration constant on a small tournament and document the choice.",
                ],
            },
            {
                "title": "Run a reproducible tournament",
                "summary": "One lucky game is not evidence of strength.",
                "steps": [
                    "Create a tournament harness with fixed starting positions, seeds and alternating first-player roles.",
                    "Report win rate with confidence intervals, positions searched and average time per move.",
                    "Compare random, minimax with pruning and MCTS at a fixed time or simulation budget.",
                    "Save the tournament output as an artifact and summarise the strongest and weakest cases.",
                ],
            },
            {
                "title": "Build the playable UI and document search",
                "summary": "The search evidence should be visible while playing.",
                "steps": [
                    "Build a browser board with legal-move hints, undo and difficulty levels tied to search depth or simulation budget.",
                    "Show the chosen move, time taken and a small search-tree view with pruned branches marked.",
                    "Add a tournament summary page with the measured win rates and pruning reduction.",
                    "Write a README and record a demo of a win against the hardest level and the search view.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-022": {
        "description": (
            "The complete project is a simulation study of reinforcement-learning "
            "traffic control. Build one intersection in SUMO or a documented "
            "lightweight simulator, define the state, action and reward, and "
            "measure fixed-timing and rule-based baselines before training. Start "
            "with tabular Q-learning and add a deep method only if the state "
            "space requires it.\n\n"
            "Finish with average waiting time, queue length, throughput and a "
            "demand-shift test that shows how much of the gain survives. Include "
            "a reward ablation that explains unstable or unfair signal behaviour, "
            "a dashboard and a clear note that this is simulation only and not a "
            "live traffic-safety system."
        ),
        "build_guide": [
            {
                "title": "Build the simulator and baselines",
                "summary": "The environment and baselines must exist before training begins.",
                "steps": [
                    "Set up a single intersection in SUMO or a small documented simulator with reproducible demand files.",
                    "Implement a fixed-timing controller and record waiting time, queue length and throughput.",
                    "Implement a rule-based adaptive controller as a stronger baseline.",
                    "Define the observation interval, simulation horizon and random seeds used for every comparison.",
                ],
            },
            {
                "title": "Formulate the MDP and train Q-learning",
                "summary": "A small, inspectable state space is a feature, not a limitation.",
                "steps": [
                    "Define state as queue lengths and current phase timing, action as the next phase, and reward as waiting time minus a switching penalty.",
                    "Implement a tabular Q-learning loop with epsilon decay and a fixed training demand pattern.",
                    "Track episode reward, average waiting time and queue length during learning.",
                    "Compare the trained policy with fixed timing on the same seed set.",
                ],
            },
            {
                "title": "Test demand shift and add a deep method if needed",
                "summary": "A policy that only works on the training pattern has memorised it.",
                "steps": [
                    "Create at least two unseen demand patterns and evaluate every controller on them.",
                    "Report how much of the training gain survives and inspect the failure cases.",
                    "Add a deep Q-network only if the tabular state cannot represent the needed information.",
                    "Keep the fixed and rule-based baselines in every comparison.",
                ],
            },
            {
                "title": "Ablate the reward and check fairness",
                "summary": "Reward design can create efficient but unfair intersections.",
                "steps": [
                    "Run ablations that remove the switching penalty and that weight side-road queues differently.",
                    "Measure average wait overall and per approach so a main-road gain cannot hide side-road starvation.",
                    "Document switching frequency and unstable behaviour at high learning rates.",
                    "Choose the final reward from the measured trade-off, not from the training curve alone.",
                ],
            },
            {
                "title": "Build the dashboard and document limits",
                "summary": "The result should be interpretable to a transport modeller.",
                "steps": [
                    "Build a dashboard with waiting time, queue length and throughput over time for each controller.",
                    "Add a demand-pattern selector and show the training versus shifted result side by side.",
                    "Write a README with the MDP definition, reward, seeds, metrics and simulation-only limitation.",
                    "Record a demo of a trained policy, a baseline comparison and one demand-shift failure.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-023": {
        "description": (
            "The complete project compares molecular representations on the same "
            "task. Build a fingerprint plus random-forest baseline and a graph "
            "neural network for one regression and one classification property, "
            "using MoleculeNet data and RDKit. Evaluate under both a random split "
            "and a scaffold split, then report the performance drop and the "
            "training cost.\n\n"
            "Finish with the correct metric per target, calibration or uncertainty "
            "and a report that says when the GNN is worth the complexity. The app "
            "should show a molecule, its prediction, the uncertainty and the "
            "reminder that predictions are not laboratory results or a safety "
            "assessment."
        ),
        "build_guide": [
            {
                "title": "Load molecules and define the tasks",
                "summary": "The split and metric decide whether the comparison is fair.",
                "steps": [
                    "Load ESOL and Tox21 from MoleculeNet, record the licence and inspect missing labels and duplicates.",
                    "Clean invalid structures with RDKit and keep a mapping from molecule id to the original record.",
                    "Choose RMSE for solubility and AUROC or PR-AUC for toxicity, with a documented reason for each.",
                    "Create random and scaffold splits with saved indices so every model uses the same test sets.",
                ],
            },
            {
                "title": "Build the fingerprint baseline",
                "summary": "A strong classical baseline prevents a GNN from winning by default.",
                "steps": [
                    "Compute Morgan fingerprints and train a random forest or gradient-boosting model for each property.",
                    "Tune only on a validation split and keep the scaffold test set untouched.",
                    "Report the metric on both random and scaffold splits and the gap between them.",
                    "Save the trained baseline and its feature settings as a reproducible artifact.",
                ],
            },
            {
                "title": "Train the graph neural network",
                "summary": "Atom and bond features should be documented, not treated as magic.",
                "steps": [
                    "Convert molecules into graphs with atom, bond and optional global features.",
                    "Train a small message-passing network for the regression and classification tasks with a fixed seed.",
                    "Report the same metrics and splits as the baseline, plus training time and parameter count.",
                    "Inspect predictions on the largest errors and check whether the molecule is outside the training distribution.",
                ],
            },
            {
                "title": "Report uncertainty and the cost trade-off",
                "summary": "A small accuracy gain may not justify a much more expensive model.",
                "steps": [
                    "Use an ensemble or a calibrated head to produce an uncertainty estimate for each prediction.",
                    "Compare predicted confidence with observed error or calibration curves on the scaffold split.",
                    "Show accuracy, training cost and inference cost for the fingerprint and graph models side by side.",
                    "Write a recommendation for which model to use by property and data size.",
                ],
            },
            {
                "title": "Build the review view and document limits",
                "summary": "The final output should be honest about experimental follow-up.",
                "steps": [
                    "Build a page that accepts a SMILES string and shows the structure, prediction and uncertainty.",
                    "Add a visible note that predictions are research and education outputs, not lab results.",
                    "Write a README with datasets, splits, metrics, calibration method and licence notes.",
                    "Record a demo of a random-split result, a scaffold-split drop and one uncertain prediction.",
                ],
            },
        ],
    },
    "manabi-aiml-resume-024": {
        "description": (
            "The complete project recovers governing equations from simulated and "
            "recorded dynamical systems. Generate trajectories for a pendulum, "
            "spring or predator-prey system, add noise, differentiate carefully "
            "and use sparse regression such as SINDy to recover candidate terms. "
            "Validate by predicting future states and by comparing coefficients "
            "with the true equations.\n\n"
            "Finish with a noise sweep, a video-tracked real system and a neural "
            "network comparison on fit and extrapolation. The repo should show "
            "when discovery fails, why a readable equation can be more useful "
            "than a black-box fit, and how measurement noise changes the answer."
        ),
        "build_guide": [
            {
                "title": "Simulate systems with known equations",
                "summary": "Ground truth is required before you can measure recovery.",
                "steps": [
                    "Implement at least two systems, such as a damped pendulum and a spring-mass system, with documented parameters.",
                    "Generate trajectories at a fixed time step and save the state, derivative and true governing terms.",
                    "Add controlled Gaussian noise at several levels and keep the clean trajectory for comparison.",
                    "Plot phase portraits and trajectories to confirm the simulation is physically plausible.",
                ],
            },
            {
                "title": "Recover equations with sparse regression",
                "summary": "Derivative estimation is the fragile step in equation discovery.",
                "steps": [
                    "Build a candidate library of polynomial and trigonometric terms relevant to the chosen systems.",
                    "Estimate derivatives with smoothing or a differentiation method suited to noisy data.",
                    "Fit sparse regression with a threshold sweep and select the model using a documented criterion.",
                    "Compare recovered coefficients with the true values and report coefficient error.",
                ],
            },
            {
                "title": "Validate prediction and noise limits",
                "summary": "A recovered equation should earn trust by predicting forward.",
                "steps": [
                    "Integrate the recovered equation and compare its trajectory with held-out measurements over increasing horizons.",
                    "Sweep noise levels and find the point where the wrong terms are selected or coefficients become unstable.",
                    "Inspect failures and document whether smoothing, derivative choice or library completeness caused them.",
                    "Report coefficient error and prediction error separately.",
                ],
            },
            {
                "title": "Compare with a neural network baseline",
                "summary": "The comparison should be about interpretability and extrapolation, not only fit.",
                "steps": [
                    "Train a small neural network to predict the next state or derivative on the same data.",
                    "Compare one-step fit, long-horizon prediction and behaviour outside the observed range.",
                    "Show where the network fits well but fails to extrapolate or explain the system.",
                    "Include the comparison in the evaluation report rather than claiming the equation always wins.",
                ],
            },
            {
                "title": "Track a real system and build the demo",
                "summary": "A recorded system makes the project more than a simulation exercise.",
                "steps": [
                    "Track a physical pendulum or spring from video with a reference marker and convert pixel positions to angles or distances.",
                    "Run the discovery pipeline on the tracked data and compare it with the simulated result.",
                    "Build a notebook or page that shows the true and recovered trajectories and the selected equation.",
                    "Write a README with the systems, noise sweep, failure point and limitations of the measurement setup.",
                ],
            },
        ],
    },
}
