"""Seed 24 AI/ML resume projects.

Every brief follows the resume-track template: an honest MVP, a standout
scope, target roles, CV bullet templates, interview talking points and a
curated five-phase build guide. Public data links are listed; the app never
hosts or mirrors a dataset.
"""

from app.seed.runner import seed_problems
from app.seed.aiml_resume_details import DETAILS as RESUME_DETAILS


def _kit(
    *,
    mvp,
    impressive,
    roles,
    bullets,
    interview,
    differentiators,
):
    return {
        "scope_levels": [
            {"level": "Good enough (MVP)", "text": mvp[0], "checks": mvp[1]},
            {"level": "Impressive", "text": impressive[0], "checks": impressive[1]},
        ],
        "target_roles": [
            {"role": role, "how_it_helps": how_it_helps}
            for role, how_it_helps in roles
        ],
        "resume_bullets": [
            {"bullet": bullet, "example": example}
            for bullet, example in bullets
        ],
        "interview_points": [
            {"question": question, "answer": answer}
            for question, answer in interview
        ],
        "differentiators": differentiators,
    }


PROBLEMS = [
    dict(
        source_id="manabi-aiml-resume-001",
        title="Review & Rating Manipulation Detector",
        summary=(
            "Online reviews decide what people buy, and fake reviews are cheap "
            "to commission. Build a detector that combines text signals "
            "(near-duplicate wording, template phrases, sentiment that does "
            "not match the star rating) with reviewer behaviour (burst posting, "
            "one-product reviewers, unusual rating patterns).\n\n"
            "Give every product a trust score with plain-language reasons, and "
            "use a reviewer-product graph to surface groups that post together. "
            "Report precision, recall, F1 and AUROC on a labelled held-out set, "
            "plus scoring time per review.\n\n"
            "Responsible use: flags are signals for human review, not proof of "
            "wrongdoing. Test only on synthetic or properly licensed data."
        ),
        who_affected="Shoppers, e-commerce platforms, and honest sellers who depend on trustworthy reviews.",
        why_matters="Fake reviews mislead buyers, punish honest sellers, and make every rating less useful.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=90,
        tech_tags=["python", "nlp", "scikit-learn", "graph-analytics", "explainability", "fastapi"],
        datasets=[
            {"name": "Ott deceptive opinion spam corpus", "url": "https://myleott.com/op-spam.html"},
            {"name": "Yelp Open Dataset", "url": "https://www.yelp.com/dataset"},
            {"name": "Amazon Reviews 2023 metadata", "url": "https://amazon-reviews-2023.github.io/"},
        ],
        approaches=[
            "Extract text features such as duplicate phrasing, template fragments and rating-sentiment mismatch.",
            "Add reviewer-behaviour features: posting bursts, single-product history and rating distribution.",
            "Build a reviewer-product graph and score clusters that post together.",
            "Train an explainable classifier and return the strongest reasons with each product score.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Check every dataset licence before use.",
        original_text="Build a review-manipulation detector that combines text and reviewer-behaviour features, explains each flag and groups coordinated reviewers.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A product page shows a trust score, a suspicious-review list and the top reasons behind each flag.",
                [
                    "Text and reviewer-behaviour features feed one classifier with a documented label set.",
                    "Every flagged review shows concrete reasons, not only a probability.",
                    "A held-out split reports precision, recall, F1 and AUROC.",
                    "Scoring runs locally from a reproducible command.",
                ],
            ),
            impressive=(
                "The graph step finds planted coordinated groups and the demo shows a reviewer-product cluster with shared behaviour.",
                [
                    "A reviewer-product graph surfaces communities with shared devices, timing or wording.",
                    "The evaluation includes planted groups, not only individual fake reviews.",
                    "A small API serves product and review scores with latency measured per review.",
                    "A short report separates model errors from ambiguous human labels.",
                ],
            ),
            roles=[
                ("Machine learning engineer", "Shows text features, imbalanced classification, graph features and measurable evaluation on a messy real problem."),
                ("Data scientist", "You can explain a model, choose the right metrics and separate correlation from proof of manipulation."),
                ("Trust & safety engineer", "The project combines detection, review workflow and careful language about uncertain flags."),
            ],
            bullets=[
                (
                    "Built a review-manipulation detector combining text and reviewer-behaviour features, reaching {F1} on {N} labelled reviews with a per-review explanation in {X} ms.",
                    "Built a review-manipulation detector combining text and reviewer-behaviour features, reaching 0.91 F1 on 12,000 labelled reviews with a per-review explanation in 18 ms.",
                ),
                (
                    "Added a reviewer-product graph that recovered {X}% of planted coordinated groups at {Y}% precision.",
                    "Added a reviewer-product graph that recovered 78% of planted coordinated groups at 86% precision.",
                ),
                (
                    "Reduced false accusations by reporting calibrated confidence and human-readable reasons instead of a single label.",
                    "Reduced false accusations by reporting calibrated confidence and the three strongest reasons behind every product score.",
                ),
            ],
            interview=[
                (
                    "Why is accuracy a poor metric here?",
                    "Fake reviews are rare, so a model that labels everything genuine can look accurate. I use precision, recall, F1 and AUROC, and I choose the threshold from the cost of a false accusation versus a missed fake review.",
                ),
                (
                    "How do you explain a flag to a platform reviewer?",
                    "I expose the strongest positive features for that review: near-duplicate text, rating-sentiment mismatch, burst timing or a shared reviewer cluster. The score is a summary; the reasons are what a person can verify.",
                ),
                (
                    "How would you know the graph step actually works?",
                    "I plant synthetic coordinated groups with known membership and measure group-level recall and precision. That is stronger than showing a pretty cluster on one dataset.",
                ),
            ],
            differentiators=[
                "A real held-out evaluation, not a demo on the training set.",
                "Group-level evidence from a reviewer-product graph, not only single-review classification.",
                "Human-readable reasons and calibrated confidence on every flag.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-002",
        title="Industrial Defect Detector (Anomaly Detection)",
        summary=(
            "Factories often have plenty of images of good products and very "
            "few labelled defects. Build an anomaly detector that learns what "
            "normal looks like, then highlights scratches, cracks or missing "
            "parts on new images.\n\n"
            "Compare an autoencoder with a stronger method such as PatchCore. "
            "Report image-level and pixel-level AUROC for each product "
            "category, the false-positive rate at a fixed defect recall, and "
            "inference time per image. Add a sensitivity slider so an inspector "
            "can trade missed defects against false alarms."
        ),
        who_affected="Manufacturing quality teams, inspectors, and small factories that cannot label thousands of defects.",
        why_matters="Manual inspection is slow and inconsistent, while missed defects reach customers and create costly recalls.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=100,
        tech_tags=["python", "pytorch", "computer-vision", "anomaly-detection", "opencv", "streamlit"],
        datasets=[
            {"name": "MVTec AD benchmark", "url": "https://www.mvtec.com/company/research/datasets/mvtec-ad"},
            {"name": "VisA anomaly detection dataset", "url": "https://github.com/amazon-science/spot-diff"},
        ],
        approaches=[
            "Train an autoencoder or feature-based anomaly model using only good images.",
            "Generate a pixel heatmap for every test image instead of one opaque score.",
            "Compare methods per category with image-level and pixel-level AUROC.",
            "Add a sensitivity slider and report the false-positive rate at a fixed defect recall.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. MVTec AD is a non-commercial benchmark; check its terms.",
        original_text="Build an anomaly detector that learns product defects from good samples, compares methods, reports image and pixel metrics and shows a defect heatmap.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "One product category runs from good images only, and an inspector sees a heatmap and a sensitivity control.",
                [
                    "The model trains without defect labels and scores held-out images.",
                    "Each prediction includes a pixel heatmap, not just a number.",
                    "Image-level AUROC and inference time are reported.",
                    "A slider changes the threshold and shows the effect on false alarms.",
                ],
            ),
            impressive=(
                "Two methods are compared across several categories with pixel metrics and a clear deployment recommendation.",
                [
                    "PatchCore or a comparable method is compared with the autoencoder baseline.",
                    "Every category has image-level and pixel-level AUROC plus a false-positive rate.",
                    "The report explains which categories are hard and why.",
                    "A small demo accepts an uploaded image and returns the same evidence an inspector sees.",
                ],
            ),
            roles=[
                ("Computer vision engineer", "Shows transfer learning, anomaly detection, heatmaps and evaluation beyond a single accuracy number."),
                ("ML engineer", "You can compare methods fairly, measure latency and turn a model into an inspection tool."),
                ("Manufacturing AI engineer", "The project is framed around inspector trust, false alarms and deployment constraints."),
            ],
            bullets=[
                (
                    "Implemented anomaly detection that finds product defects from only good samples, scoring {AUROC} image-level and {AUROC} pixel-level across {N} categories at {X} ms per image.",
                    "Implemented anomaly detection that finds product defects from only good samples, scoring 0.94 image-level AUROC and 0.91 pixel-level AUROC across five categories at 26 ms per image.",
                ),
                (
                    "Compared an autoencoder with PatchCore and documented where the simpler model failed.",
                    "Compared an autoencoder with PatchCore across MVTec categories and documented the texture categories where the baseline collapsed.",
                ),
                (
                    "Added a sensitivity control that made the missed-defect versus false-alarm trade-off explicit for inspectors.",
                    "Added a sensitivity control that let inspectors reach 90% defect recall with a measured false-positive rate instead of hiding the threshold.",
                ),
            ],
            interview=[
                (
                    "Why train only on good images?",
                    "Defects are rare and varied, so supervised labels are expensive and incomplete. Anomaly detection learns the normal distribution and flags deviations. I still compare it with a supervised upper bound where labels exist.",
                ),
                (
                    "What does pixel-level AUROC add?",
                    "Image-level AUROC says whether the product was flagged. Pixel-level AUROC says whether the heatmap localises the defect. An inspector needs the second to act, so a model that scores well globally but points at the wrong region is still weak.",
                ),
                (
                    "How do you choose the operating threshold?",
                    "I fix a defect recall the factory needs, then measure the false-positive rate at that recall. The slider exposes the trade-off instead of pretending there is one correct threshold.",
                ),
            ],
            differentiators=[
                "Two anomaly methods compared on the same categories and splits.",
                "Pixel-level evidence with a heatmap, not just image-level classification.",
                "A deployment-oriented metric: false positives at a required defect recall.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-003",
        title="Product Attribute Extraction from Images",
        summary=(
            "Product photos contain useful structured data: net weight, volume, "
            "quantity and sometimes dimensions. Build a pipeline that reads "
            "printed packaging text with OCR, parses values and units, and "
            "normalises them into a consistent schema.\n\n"
            "A single photo cannot reveal true height or width without a scale, "
            "so the honest project focuses on printed attributes and only "
            "estimates size when a reference object is visible. Otherwise it "
            "says it cannot tell. Report exact-match accuracy per attribute, "
            "MAE after unit normalisation, and the share of correct abstentions."
        ),
        who_affected="Marketplace sellers, catalogue teams, and shoppers comparing products with inconsistent listings.",
        why_matters="Missing or inconsistent package quantities make price comparison unreliable and create bad catalogue data.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=85,
        tech_tags=["python", "ocr", "computer-vision", "regex", "unit-normalization", "fastapi"],
        datasets=[
            {"name": "Open Food Facts product images and quantities", "url": "https://world.openfoodfacts.org/data"},
        ],
        approaches=[
            "Detect the packaging region and run OCR on the visible text.",
            "Parse quantity, unit and count patterns, then normalise grams, kilograms, millilitres and litres.",
            "Abstain when no value is visible or the confidence is too low.",
            "Evaluate exact match, numeric error and abstention quality on a labelled sample.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Open Food Facts database is ODbL and images are CC BY-SA; check each.",
        original_text="Build an OCR pipeline that extracts product weight, volume and quantity from packaging photos, normalises units and abstains when the value is not visible.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "An uploaded product photo returns a structured weight or volume value, or an explicit cannot-tell result.",
                [
                    "OCR runs on the packaging area and extracts candidate quantity text.",
                    "Values and units are normalised into a documented schema.",
                    "The system abstains when no quantity is visible.",
                    "A labelled sample reports exact-match accuracy per attribute.",
                ],
            ),
            impressive=(
                "The pipeline handles multiple formats, reports numeric error and measures how often it correctly refuses to answer.",
                [
                    "Weight, volume and count are evaluated separately instead of as one score.",
                    "Unit conversion is tested with metric and common package formats.",
                    "Correct abstention is measured and explained, not treated as a failure.",
                    "A small review screen lets a human correct low-confidence fields.",
                ],
            ),
            roles=[
                ("Computer vision engineer", "Shows OCR, packaging perception, unit parsing and careful evaluation of a real extraction pipeline."),
                ("Data engineer", "You built a normalisation schema and measured quality across messy catalogue data."),
                ("ML engineer", "The project demonstrates confidence handling and abstention, not only extraction."),
            ],
            bullets=[
                (
                    "Built an OCR-based pipeline extracting product weight and volume from packaging photos with {X}% exact-match accuracy on {N} products and {Y}% correct abstention when no value was visible.",
                    "Built an OCR-based pipeline extracting product weight and volume from packaging photos with 88% exact-match accuracy on 640 products and 93% correct abstention when no value was visible.",
                ),
                (
                    "Normalised {N} package formats into grams and millilitres with a {X}% reduction in unit errors.",
                    "Normalised 1,200 package formats into grams and millilitres with a 71% reduction in unit errors versus a regex-only baseline.",
                ),
                (
                    "Added a low-confidence review step instead of guessing dimensions that a single photo cannot prove.",
                    "Added a low-confidence review step and an explicit cannot-tell state for dimensions that a single photo cannot prove.",
                ),
            ],
            interview=[
                (
                    "Why not predict height and width directly from the image?",
                    "Without a known scale, pixel size does not determine physical size. The model can learn dataset biases and still fail on a new photo. I only estimate dimensions when a reference object is visible and state the assumption.",
                ),
                (
                    "How do you evaluate unit normalisation?",
                    "I compare the normalised value with a hand-labelled value in the base unit, report exact match and mean absolute error, and list the formats that fail. That separates OCR errors from parsing errors.",
                ),
                (
                    "What does correct abstention mean?",
                    "When the required value is not visible, the correct output is no answer. I measure the share of those cases where the system abstains, alongside the share where it abstains on a visible value.",
                ),
            ],
            differentiators=[
                "A real abstention policy instead of a confident guess.",
                "Separate metrics for extraction, unit conversion and refusal.",
                "Open catalogue data with a reviewable licence trail.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-004",
        title="Smart Product Pricing",
        summary=(
            "Predict a fair price for an e-commerce product from its title, "
            "description and image. Combine text embeddings, image embeddings "
            "and structured features such as brand and pack quantity in a "
            "gradient-boosting or neural model.\n\n"
            "Evaluate with MAE and SMAPE, then run an ablation that compares "
            "text only with text plus image. Explain which attributes move the "
            "price so the model is useful to a catalogue team.\n\n"
            "Responsible use: predictions are estimates with uncertainty, not "
            "professional valuations or advice."
        ),
        who_affected="Marketplace sellers, catalogue analysts, and small retailers setting prices without a pricing team.",
        why_matters="Bad price estimates hide margin problems and make listings inconsistent across a catalogue.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=95,
        tech_tags=["python", "pytorch", "sentence-transformers", "gradient-boosting", "multimodal", "shap"],
        datasets=[
            {"name": "Amazon Reviews 2023 product metadata", "url": "https://amazon-reviews-2023.github.io/"},
        ],
        approaches=[
            "Embed product titles and descriptions with a text model and images with a vision model.",
            "Combine embeddings with structured features such as brand and pack size.",
            "Train a gradient-boosting or neural regressor and report MAE and SMAPE.",
            "Run a text-only versus text-plus-image ablation and explain important features.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Product metadata has research-use terms; check before use.",
        original_text="Build a multimodal product price model from catalogue text, images and structured attributes, evaluated with MAE and SMAPE and explained with feature importance.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A product's text and structured fields produce a price estimate with MAE and SMAPE reported on a held-out split.",
                [
                    "The dataset has a documented price target and a time or random split.",
                    "A text-only baseline is trained before adding images.",
                    "MAE and SMAPE are reported on the held-out set.",
                    "The top price drivers are shown for a sample of products.",
                ],
            ),
            impressive=(
                "Image embeddings improve the baseline and an ablation shows exactly where the gain comes from.",
                [
                    "The multimodal model is compared with text-only and structured-only baselines.",
                    "An ablation isolates text, image and structured features.",
                    "Error slices show which categories are overpriced or underpriced.",
                    "A small UI explains one prediction with its strongest attributes.",
                ],
            ),
            roles=[
                ("ML engineer", "Shows multimodal feature engineering, regression metrics and disciplined ablations."),
                ("Data scientist", "You can explain a skewed target, choose MAE and SMAPE, and interpret feature importance."),
                ("E-commerce data scientist", "The project connects catalogue attributes to a business decision without overclaiming certainty."),
            ],
            bullets=[
                (
                    "Trained a multimodal price model on {N} products, reducing SMAPE from {A} to {B} versus a text-only baseline.",
                    "Trained a multimodal price model on 48,000 products, reducing SMAPE from 31.4% to 24.8% versus a text-only baseline.",
                ),
                (
                    "Ran an ablation that showed image embeddings helped categories where colour and form drive price.",
                    "Ran an ablation that showed image embeddings cut MAE by 9% in furniture and apparel, with little gain in books.",
                ),
                (
                    "Explained the top price drivers per listing so a catalogue team could audit estimates instead of trusting a black box.",
                    "Explained the top price drivers per listing with feature attributions so a catalogue team could audit outliers before publishing.",
                ),
            ],
            interview=[
                (
                    "Why use SMAPE as well as MAE?",
                    "MAE is easy to interpret in currency units but is dominated by expensive products. SMAPE shows relative error across cheap and expensive items. Reporting both stops a model from looking good only because it ignores the long tail.",
                ),
                (
                    "Why compare text only with text plus image?",
                    "The ablation is the evidence that images add value. Without it, a multimodal model can look impressive while the gain comes from extra structured fields or a bigger parameter count.",
                ),
                (
                    "How would you handle price outliers?",
                    "I inspect whether they are data errors, rare collector items or genuine premium products. I may clip or model them separately, and I always report the effect on both MAE and SMAPE rather than hiding them.",
                ),
            ],
            differentiators=[
                "A clean multimodal ablation, not just a single model score.",
                "Two metrics that expose different kinds of error.",
                "Per-listing explanations that a catalogue team can audit.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-005",
        title="Low-Bandwidth Multilingual AI Tutor",
        summary=(
            "Build a learning assistant for places with weak internet and "
            "limited devices. It answers questions in the learner's language "
            "using retrieval over openly licensed course material, runs as a "
            "lightweight web app, and shows the source behind every answer.\n\n"
            "Teachers get a simple view of the topics learners struggle with. "
            "Measure answer accuracy on expert-written questions, citation "
            "support, median response time and page weight on a throttled "
            "connection.\n\n"
            "Responsible use: this is a learning aid, not a replacement for "
            "teachers or source documents. Check answers against the cited "
            "sources."
        ),
        who_affected="Students on slow connections, teachers in low-resource schools, and learners who study in a non-English language.",
        why_matters="Most AI tutors assume fast internet and English, which leaves the learners who need help most without a usable tool.",
        field="aiml",
        domain="education",
        difficulty="intermediate",
        est_hours=110,
        tech_tags=["python", "rag", "embeddings", "fastapi", "react", "multilingual", "pwa"],
        datasets=[
            {"name": "OpenStax openly licensed textbooks", "url": "https://openstax.org/"},
            {"name": "IndicTrans2 translation models", "url": "https://github.com/AI4Bharat/IndicTrans2"},
        ],
        approaches=[
            "Chunk openly licensed course material and build a small retrieval index.",
            "Answer with citations and refuse when retrieval does not support a claim.",
            "Translate answers while keeping the source text available for checking.",
            "Measure accuracy, citation support and page weight on a throttled connection.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use openly licensed content and check every source licence.",
        original_text="Build a low-bandwidth multilingual tutor that retrieves openly licensed course material, cites every answer and works on a weak connection.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A learner asks a question, gets a short cited answer and can open the source passage.",
                [
                    "Course material is chunked and stored in a searchable index.",
                    "Every answer includes at least one source passage.",
                    "The app has a clear refuses-to-answer state when retrieval is weak.",
                    "The page loads and answers on a throttled connection.",
                ],
            ),
            impressive=(
                "The tutor answers in more than one language, verifies citations and gives teachers a struggle-topic view.",
                [
                    "Answers are available in English and at least one Indian language with the source preserved.",
                    "A citation checker measures whether each cited passage supports the claim.",
                    "The teacher view groups questions by topic without exposing personal data.",
                    "Answer accuracy is reported on expert-written questions, not only model confidence.",
                ],
            ),
            roles=[
                ("AI application engineer", "Shows retrieval, grounding, citation checks and refusal behaviour, not just an API call."),
                ("Full-stack engineer", "You built a low-bandwidth frontend, a retrieval backend and a teacher-facing view."),
                ("EdTech engineer", "The project balances learning value, source trust and real network constraints."),
            ],
            bullets=[
                (
                    "Built a multilingual tutor for low-bandwidth use that answered {X}% of {N} curriculum questions correctly with verified citations and loaded in under {Y} KB.",
                    "Built a multilingual tutor for low-bandwidth use that answered 84% of 150 curriculum questions correctly with verified citations and loaded in under 180 KB.",
                ),
                (
                    "Added a citation checker that rejected unsupported answers instead of presenting them as fact.",
                    "Added a citation checker that rejected 17% of generated answers whose cited passage did not support the claim.",
                ),
                (
                    "Cut median response time to {X} seconds on a throttled connection while keeping the source text visible.",
                    "Cut median response time to 2.4 seconds on a throttled 3G profile while keeping the source text visible on every answer.",
                ),
            ],
            interview=[
                (
                    "How do you stop the tutor from inventing answers?",
                    "The model only answers from retrieved passages and must return a source id. A separate check compares the claim with the cited passage. If the evidence is weak, the interface says it does not know rather than filling the gap.",
                ),
                (
                    "Why measure page weight as well as answer quality?",
                    "The target user has a weak connection. A correct answer behind a 3 MB bundle is not usable. I measure initial page weight, time to first answer and the size of the retrieved context.",
                ),
                (
                    "How did you handle translation without losing trust?",
                    "I keep the original source passage available beside the translated answer. That lets a learner or teacher check the source even when the translation is imperfect.",
                ),
            ],
            differentiators=[
                "A hard network budget, measured on a throttled connection.",
                "Citation support checked separately from answer fluency.",
                "A teacher-facing view that uses aggregate topics, not personal data.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-006",
        title="Agentic Payment Automation",
        summary=(
            "Build an AI agent that handles routine payment support: checkout "
            "help, subscription changes, refunds and dispute handling. It works "
            "only in payment-provider test mode, asks a human to approve risky "
            "actions such as large refunds, and writes an audit log for every "
            "step.\n\n"
            "Treat customer messages as untrusted input. Use idempotency keys "
            "for payment calls, enforce policy limits in code, and evaluate the "
            "agent on scripted scenarios. Report task success, policy "
            "violations and the share of risky actions escalated to a human.\n\n"
            "Responsible use: test mode only. Never use real money, real cards "
            "or real customer data."
        ),
        who_affected="Payments support teams, small merchants, and customers who need fast help with routine payment issues.",
        why_matters="Manual payment support is repetitive and error-prone, but an unguarded agent can move money or leak data.",
        field="aiml",
        domain="fintech",
        difficulty="intermediate",
        est_hours=120,
        tech_tags=["python", "llm", "tool-use", "fastapi", "stripe", "razorpay", "audit-log"],
        datasets=[
            {"name": "Stripe test-mode documentation", "url": "https://docs.stripe.com/testing"},
            {"name": "Razorpay test-mode documentation", "url": "https://razorpay.com/docs/api/"},
        ],
        approaches=[
            "Define a small set of payment tools with strict schemas and test-mode keys.",
            "Require human approval for refunds, disputes and anything above a policy limit.",
            "Log every tool call, decision and approval in an append-only audit trail.",
            "Evaluate on scripted scenarios including prompt-injection attempts and repeated requests.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Test mode only; never use real money or customer data.",
        original_text="Build a guarded payment-support agent that handles routine workflows in test mode, escalates risky actions and keeps a full audit log.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A scripted refund or subscription request runs in test mode, with an audit log and a human approval step.",
                [
                    "At least three payment actions run against test keys only.",
                    "A policy limit blocks or escalates high-risk actions.",
                    "Every tool call and approval is recorded with a timestamp.",
                    "A repeated request does not create a duplicate payment action.",
                ],
            ),
            impressive=(
                "The agent survives injected instructions, handles ambiguous requests and reports policy compliance across a scenario suite.",
                [
                    "Prompt-injection attempts are treated as untrusted text and never become tool calls.",
                    "The evaluation reports task success, policy violations and escalation accuracy.",
                    "A reviewer screen shows the proposed action, policy reason and audit trail.",
                    "Idempotency is tested with retries and duplicate customer messages.",
                ],
            ),
            roles=[
                ("AI engineer", "Shows tool use, guardrails, evaluation and safe failure modes for an agent with real consequences."),
                ("Backend engineer", "You designed idempotent payment calls, policy checks and an audit log."),
                ("Fintech engineer", "The project demonstrates test-mode discipline, sensitive-data handling and human approval."),
            ],
            bullets=[
                (
                    "Built a guarded payment-support agent that completed {X}% of {N} scenarios in test mode with zero policy violations and human approval on every high-risk action.",
                    "Built a guarded payment-support agent that completed 92% of 60 scripted scenarios in test mode with zero policy violations and human approval on every refund above the limit.",
                ),
                (
                    "Added idempotency and retry tests that prevented duplicate refunds under repeated requests.",
                    "Added idempotency keys and retry tests that prevented duplicate refunds when the same request arrived three times.",
                ),
                (
                    "Logged every tool call and approval in an append-only audit trail for review.",
                    "Logged every tool call, policy check and human approval in an append-only audit trail that a reviewer could replay.",
                ),
            ],
            interview=[
                (
                    "How do you stop prompt injection in a payment agent?",
                    "Customer text is data, never an instruction. Tool calls are chosen only from a fixed policy layer, and any message that tries to change the policy is refused. High-risk tools still require a human approval outside the model.",
                ),
                (
                    "Why use idempotency keys?",
                    "Networks retry. Without a key, a retried refund can run twice. The provider stores the key with the result, so a repeat request returns the same outcome instead of moving money again.",
                ),
                (
                    "What did you measure to call the agent safe?",
                    "Task success on scripted scenarios, policy violations, correct escalation of risky actions and duplicate prevention under retries. Safety is a test result, not a claim in the prompt.",
                ),
            ],
            differentiators=[
                "Policy enforcement outside the model, with human approval on risky actions.",
                "An auditable trail of every decision and tool call.",
                "Evaluation includes prompt injection and duplicate-request attacks.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-007",
        title="Social Post to Product Listing Converter",
        summary=(
            "Small sellers often describe products in a social post, not a "
            "catalogue. Build a converter that turns a post's text and images "
            "into a structured listing: title, description, category, "
            "attributes, price and variants.\n\n"
            "Use schema-constrained extraction and highlight low-confidence "
            "fields for the seller to confirm. Evaluate field-level accuracy "
            "against hand-labelled listings and measure listing time against "
            "manual entry.\n\n"
            "Responsible use: use synthetic, public or consented data only. Do "
            "not process anyone's personal information."
        ),
        who_affected="Small sellers, social-commerce operators, and catalogue teams turning informal posts into structured listings.",
        why_matters="Manual listing entry is slow and inconsistent, while silent extraction errors create bad prices and missing variants.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=85,
        tech_tags=["python", "llm", "json-schema", "ocr", "react", "fastapi", "human-in-the-loop"],
        datasets=[
            {"name": "Consented sample social posts and screenshots", "url": None},
            {"name": "Open Food Facts product attribute examples", "url": "https://world.openfoodfacts.org/data"},
        ],
        approaches=[
            "Define a fixed listing schema and extract only the fields the schema allows.",
            "Combine post text with OCR from the seller's images.",
            "Attach confidence to each field and route weak fields to a seller review screen.",
            "Measure field accuracy, edit rate and time saved against manual entry.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Do not scrape social platforms; use posts you have permission to process.",
        original_text="Build a converter that turns a seller's social post and images into a structured product listing with confidence and human review.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A pasted post plus one image produces a structured listing draft with editable fields.",
                [
                    "The extractor returns the fixed schema, not free-form text.",
                    "Low-confidence fields are visibly marked for review.",
                    "The seller can edit every field before saving.",
                    "Field-level accuracy is reported on a hand-labelled sample.",
                ],
            ),
            impressive=(
                "The converter measures which fields sellers edit and cuts listing time against manual entry.",
                [
                    "A review screen shows confidence, source text and the suggested value side by side.",
                    "Edit rate is tracked per field rather than as one overall score.",
                    "Listing time is compared with a manual baseline on the same posts.",
                    "The schema handles variants and missing values without inventing them.",
                ],
            ),
            roles=[
                ("AI application engineer", "Shows schema-constrained extraction, confidence handling and human-in-the-loop design."),
                ("Full-stack engineer", "You built the extraction pipeline, review UI and listing persistence."),
                ("Product engineer", "The project measures seller effort, not only model accuracy."),
            ],
            bullets=[
                (
                    "Built a social-post-to-listing converter extracting {N} fields with {X}% accuracy and cutting listing time from {A} to {B} minutes.",
                    "Built a social-post-to-listing converter extracting 12 fields with 89% accuracy and cutting listing time from 9 to 3 minutes.",
                ),
                (
                    "Added confidence-based review that reduced seller edits on high-confidence fields by {X}%.",
                    "Added confidence-based review that reduced seller edits on high-confidence fields by 42% while catching weak prices and sizes.",
                ),
                (
                    "Measured field-level accuracy and edit rate instead of reporting a single extraction score.",
                    "Measured field-level accuracy and edit rate on 80 consented posts instead of reporting a single extraction score.",
                ),
            ],
            interview=[
                (
                    "Why constrain the model with a schema?",
                    "A listing has a known shape. A schema prevents missing keys, invented attributes and unparseable output. It also makes each field independently reviewable and testable.",
                ),
                (
                    "How do you decide which fields need review?",
                    "I compare per-field confidence with the cost of a mistake. Price and quantity always need a check when confidence is low; a description can tolerate more uncertainty because the seller can edit it quickly.",
                ),
                (
                    "Why measure time saved as well as accuracy?",
                    "The product value is less seller effort. A highly accurate extractor that still makes the seller re-enter everything has not solved the problem.",
                ),
            ],
            differentiators=[
                "Per-field confidence and review, not one opaque extraction.",
                "Consent-first data collection instead of platform scraping.",
                "A measured reduction in listing time against manual entry.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-008",
        title="Fraud Ring Detector (Graph Analytics)",
        summary=(
            "Fraud rarely happens through one account. Build a graph of "
            "accounts, devices, phone numbers, addresses and transfers, then "
            "surface suspicious communities: many accounts on one device, "
            "circular money flow and sudden clusters of new accounts.\n\n"
            "Start with rules and community detection, then compare a graph "
            "neural network or node embeddings against that baseline. Evaluate "
            "precision and recall on planted rings in synthetic data, plus "
            "lift over the rule-only baseline and scoring time.\n\n"
            "Responsible use: flags are signals for human review, not proof of "
            "wrongdoing. Test only on synthetic or properly licensed data and "
            "do not process personal information."
        ),
        who_affected="Fraud analysts, payment platforms, and financial institutions investigating coordinated abuse.",
        why_matters="Ring-level fraud slips past account-level rules and creates large losses before anyone sees the pattern.",
        field="aiml",
        domain="fintech",
        difficulty="advanced",
        est_hours=130,
        tech_tags=["python", "networkx", "graph-neural-networks", "pytorch-geometric", "community-detection", "pandas"],
        datasets=[
            {"name": "PaySim synthetic mobile-money dataset", "url": "https://www.kaggle.com/datasets/ealaxi/paysim1"},
            {"name": "Synthetic fraud-ring generator you write", "url": None},
        ],
        approaches=[
            "Build a typed graph from accounts, devices, phones, addresses and transfers.",
            "Add rule-based and community-detection baselines for suspicious clusters.",
            "Train node embeddings or a graph neural network against planted ring labels.",
            "Report ring-level precision and recall, lift over rules and scoring time.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use synthetic or licensed data only.",
        original_text="Build a graph-based fraud-ring detector that finds coordinated accounts and compares graph learning with a rules baseline.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A synthetic graph with planted rings is scored, and a reviewer sees the top suspicious clusters with reasons.",
                [
                    "The graph includes accounts, devices and transfers with a documented schema.",
                    "A rules baseline finds at least some planted rings.",
                    "The UI ranks clusters and shows the shared entities behind each one.",
                    "Ring-level precision and recall are computed on synthetic labels.",
                ],
            ),
            impressive=(
                "Graph learning improves ring recall over rules, and the report separates easy from camouflaged rings.",
                [
                    "A graph model is compared with the rule baseline on the same planted rings.",
                    "The evaluation reports lift, not only raw recall.",
                    "A camouflage test adds legitimate shared devices and measures the false-positive cost.",
                    "Scoring time is reported for a graph with a stated number of accounts.",
                ],
            ),
            roles=[
                ("Machine learning engineer", "Shows graph construction, embeddings and honest evaluation on a class-imbalanced problem."),
                ("Data scientist", "You can compare graph learning with a rules baseline and explain where the gain comes from."),
                ("Fraud analytics engineer", "The project is framed around analyst review, synthetic data and ring-level evidence."),
            ],
            bullets=[
                (
                    "Built a graph-based fraud-ring detector that recovered {X}% of planted rings with {Y}% precision, a {Z} point recall lift over a rules baseline.",
                    "Built a graph-based fraud-ring detector that recovered 81% of planted rings with 74% precision, an 18 point recall lift over a rules baseline.",
                ),
                (
                    "Compared community detection with graph embeddings and documented where each method failed.",
                    "Compared community detection with graph embeddings and documented the camouflaged rings that only the learned model recovered.",
                ),
                (
                    "Scored a {N}-account graph in {X} seconds while keeping the evidence inspectable by an analyst.",
                    "Scored a 250,000-account graph in 34 seconds while keeping the shared-device and transfer evidence inspectable by an analyst.",
                ),
            ],
            interview=[
                (
                    "Why is ring-level evaluation different from account-level evaluation?",
                    "A detector can flag many accounts inside one ring and still miss most rings. Analysts care about recovering the group. I match predicted clusters to planted rings and report ring-level recall and precision.",
                ),
                (
                    "How do you handle legitimate shared devices?",
                    "Shared devices are common in families and small shops. I add realistic shared entities to the synthetic data and measure the false-positive cost instead of treating every shared device as fraud.",
                ),
                (
                    "Why compare with a rules baseline?",
                    "Rules are the system a team already trusts. A learned model has to beat them on the same data before it is worth the complexity. The lift is the useful claim.",
                ),
            ],
            differentiators=[
                "Ring-level evaluation with planted synthetic groups.",
                "A fair lift comparison against a rules baseline.",
                "Analyst-facing evidence for every flagged cluster.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-009",
        title="Lab Report Explainer",
        summary=(
            "A lab report is hard to read even when every value is correct. "
            "Build a tool that reads a photo or PDF, extracts each test with "
            "its value, unit and reference range, flags out-of-range values "
            "and explains them in plain language with questions to ask a "
            "doctor.\n\n"
            "It never diagnoses and it cites the source for each explanation. "
            "Evaluate extraction accuracy for test name, value, unit and range, "
            "recall for out-of-range flags, and the reading level of the "
            "explanations.\n\n"
            "Responsible use: educational tool only. It does not diagnose "
            "conditions or give medical advice. Use synthetic reports only."
        ),
        who_affected="Patients trying to understand lab results, caregivers, and clinics that need a clearer explanation layer.",
        why_matters="People often see numbers without context, which causes unnecessary fear or missed follow-up.",
        field="aiml",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=95,
        tech_tags=["python", "ocr", "llm", "pdfplumber", "fastapi", "react", "privacy"],
        datasets=[
            {"name": "Synthetic lab reports you generate", "url": None},
            {"name": "Open clinical reference ranges", "url": "https://www.who.int/"},
        ],
        approaches=[
            "Extract text and tables from synthetic reports with OCR and PDF parsing.",
            "Map each test to a value, unit and reference range with validation rules.",
            "Flag out-of-range values and generate a plain-language explanation with a source.",
            "Measure extraction accuracy, flag recall and reading level on held-out reports.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use synthetic reports only; never process real patient data.",
        original_text="Build a lab-report explainer that extracts test values, flags out-of-range results and explains them in plain language without diagnosing.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A synthetic report produces a table of tests, values, units and flags with a plain explanation.",
                [
                    "OCR or PDF parsing extracts the report table reliably enough for a synthetic sample.",
                    "Each test is matched to its unit and reference range.",
                    "Out-of-range values are flagged with a clear not-medical-advice notice.",
                    "Every explanation links to a cited source.",
                ],
            ),
            impressive=(
                "The tool measures extraction and flag quality and shows where it refuses to explain.",
                [
                    "Test name, value, unit and range accuracy are reported separately.",
                    "Out-of-range recall is measured on held-out synthetic reports.",
                    "The explanation step refuses when the test is unknown or the range is missing.",
                    "A readability score and a sample review by a non-expert are included.",
                ],
            ),
            roles=[
                ("AI application engineer", "Shows document extraction, retrieval and careful refusal in a high-risk domain."),
                ("Healthcare data engineer", "You can structure lab data, handle units and ranges, and measure extraction quality."),
                ("Full-stack engineer", "You built the upload, parsing, explanation and review experience end to end."),
            ],
            bullets=[
                (
                    "Built a lab-report explainer that extracted test values with {X}% accuracy and flagged out-of-range results with {Y}% recall on {N} synthetic reports.",
                    "Built a lab-report explainer that extracted test values with 94% accuracy and flagged out-of-range results with 91% recall on 120 synthetic reports.",
                ),
                (
                    "Added a refusal path for unknown tests and missing ranges instead of generating unsupported explanations.",
                    "Added a refusal path for unknown tests and missing ranges, preventing unsupported explanations on 18% of test rows.",
                ),
                (
                    "Measured reading level and cited a source for every explanation so the output was checkable.",
                    "Measured reading level at grade 8 and cited a source for every explanation so a patient could check the claim.",
                ),
            ],
            interview=[
                (
                    "Why not let the model diagnose?",
                    "The tool cannot see the patient, the symptoms or the full history. A diagnosis would be unsafe and outside the product's competence. The useful job is extraction, flagging and explaining what a value means with a source.",
                ),
                (
                    "How do you evaluate extraction?",
                    "I label test name, value, unit and range separately. A single accuracy number hides whether the OCR failed or the parser attached the wrong unit, so I report each field and inspect the failures.",
                ),
                (
                    "What happens when the report is unfamiliar?",
                    "The system refuses and asks the user to check with a clinician. A confident explanation for an unknown test is worse than an honest gap.",
                ),
            ],
            differentiators=[
                "A strict not-medical-advice boundary shown in the product.",
                "Field-level extraction metrics and a measured refusal path.",
                "Citations and reading level, not only model fluency.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-010",
        title="Deepfake Video Detector",
        summary=(
            "Build a detector for face-swap videos that combines frame-level "
            "artifact analysis with temporal inconsistency across frames. The "
            "important test is cross-dataset evaluation: train on one dataset "
            "and test on another to show how well the detector generalises.\n\n"
            "Report AUROC within a dataset and across datasets, accuracy drop "
            "under compression, and frames per second at inference. Visualise "
            "what the model focuses on so the result is inspectable.\n\n"
            "Responsible use: results are probabilistic, not proof. Do not use "
            "them to accuse a real person, and label synthetic output clearly."
        ),
        who_affected="Platform trust teams, journalists verifying video, and researchers studying synthetic media.",
        why_matters="Face-swap videos are cheap to make and can damage reputations before a human can verify them.",
        field="aiml",
        domain="cybersecurity",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["python", "pytorch", "opencv", "video-models", "computer-vision", "grad-cam"],
        datasets=[
            {"name": "FaceForensics++", "url": "https://github.com/ondyari/FaceForensics"},
            {"name": "Celeb-DF", "url": "https://github.com/yuezunli/celeb-deepfakeforensics"},
            {"name": "Deepfake Detection Challenge", "url": "https://ai.meta.com/datasets/dfdc/"},
        ],
        approaches=[
            "Extract faces and sample frames from real and manipulated videos.",
            "Combine frame-level artifact features with temporal inconsistency signals.",
            "Evaluate within one dataset and transfer to a second dataset.",
            "Add compression tests, visual explanations and inference-speed measurements.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Benchmark datasets need access agreements; check each.",
        original_text="Build a deepfake video detector that combines frame artifacts with temporal signals and measures cross-dataset generalisation.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A short video is classified as real or manipulated with a frame-level confidence chart.",
                [
                    "Faces are extracted consistently from the video.",
                    "The model reports one score per video and a frame-level view.",
                    "Within-dataset AUROC is measured on a held-out split.",
                    "The UI states clearly that the score is not proof.",
                ],
            ),
            impressive=(
                "The detector is tested across datasets and compression levels, with an honest generalisation gap.",
                [
                    "A second dataset is used only for testing, never training.",
                    "The report shows the AUROC drop across datasets and compression.",
                    "A Grad-CAM or temporal attention view shows what the model used.",
                    "Inference speed is reported in frames per second.",
                ],
            ),
            roles=[
                ("Computer vision engineer", "Shows video handling, artifact analysis and cross-dataset evaluation."),
                ("ML engineer", "You can measure generalisation honestly and explain model failure under distribution shift."),
                ("Trust & safety engineer", "The project keeps probabilistic evidence separate from accusations."),
            ],
            bullets=[
                (
                    "Built a deepfake detector reaching {A} AUROC in-dataset and {B} cross-dataset, and analysed the {X} point generalisation gap.",
                    "Built a deepfake detector reaching 0.96 AUROC in-dataset and 0.74 cross-dataset, and analysed the 22 point generalisation gap.",
                ),
                (
                    "Measured accuracy loss under compression instead of reporting only a clean benchmark score.",
                    "Measured a 12 point AUROC loss under heavy compression instead of reporting only the clean benchmark score.",
                ),
                (
                    "Added temporal and frame-level explanations so a reviewer could inspect the evidence.",
                    "Added temporal and frame-level explanations so a reviewer could inspect which frames drove the verdict.",
                ),
            ],
            interview=[
                (
                    "Why is cross-dataset testing essential here?",
                    "Deepfake datasets share generation methods, faces and compression. A model can learn dataset artifacts instead of manipulation cues. Testing on an unseen dataset exposes that shortcut.",
                ),
                (
                    "Why combine frame and temporal signals?",
                    "A single frame may look convincing, while flicker, inconsistent boundaries or identity drift appear across time. The temporal model catches a different failure mode from the frame classifier.",
                ),
                (
                    "How would you present a result responsibly?",
                    "As a probabilistic signal for human review, with the evidence and the error rates visible. It is not an accusation and not proof that a named person did anything.",
                ),
            ],
            differentiators=[
                "A genuine cross-dataset generalisation report.",
                "Compression and inference-speed tests, not just clean AUROC.",
                "Evidence visualisation for human review.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-011",
        title="Paper Form Digitizer with Human Review",
        summary=(
            "Paper forms still carry critical data in clinics, schools and "
            "government offices. Build a pipeline that detects fields, reads "
            "handwritten and printed values, validates dates, phone numbers "
            "and PIN codes, and sends low-confidence fields to a quick review "
            "screen before export.\n\n"
            "Track field-level accuracy before and after review, the share of "
            "fields auto-accepted, and seconds per form against manual entry.\n\n"
            "Responsible use: use synthetic, public or consented data only. Do "
            "not process anyone's personal information."
        ),
        who_affected="Back-office teams, clinic staff, and field offices digitising paper records.",
        why_matters="Manual data entry is slow and error-prone, but blind OCR creates silent mistakes in important records.",
        field="aiml",
        domain="governance",
        difficulty="intermediate",
        est_hours=100,
        tech_tags=["python", "ocr", "layout-parsing", "opencv", "fastapi", "react", "validation"],
        datasets=[
            {"name": "FUNSD form understanding dataset", "url": "https://guillaumejaume.github.io/FUNSD/"},
            {"name": "IAM handwriting database", "url": "https://fki.tic.heia-fr.ch/databases/iam-handwriting-database"},
        ],
        approaches=[
            "Detect form fields and associate each value with its label.",
            "Run OCR for printed and handwritten text, then apply format validators.",
            "Route low-confidence fields to a review screen with the original crop.",
            "Measure accuracy before and after review plus auto-accept rate.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use synthetic forms with fake data; never real personal records.",
        original_text="Build a paper-form digitizer that extracts fields, validates values and sends low-confidence fields through human review.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A scanned synthetic form becomes structured fields with low-confidence values marked for review.",
                [
                    "Field labels and values are extracted into a documented schema.",
                    "Dates, phone numbers and codes have basic validators.",
                    "Low-confidence fields show the original image crop.",
                    "Field accuracy is measured before and after review.",
                ],
            ),
            impressive=(
                "The review screen improves accuracy measurably and most fields are auto-accepted.",
                [
                    "Auto-accept rate and post-review accuracy are reported separately.",
                    "A reviewer can correct a field without losing the original crop or OCR text.",
                    "Export produces clean structured data with an audit of edits.",
                    "Time per form is compared with a manual-entry baseline.",
                ],
            ),
            roles=[
                ("Document AI engineer", "Shows OCR, layout understanding, validation and human-in-the-loop design."),
                ("Full-stack engineer", "You built the ingestion, review and export flow end to end."),
                ("Data engineer", "The project measures field-level quality and keeps an auditable correction trail."),
            ],
            bullets=[
                (
                    "Built a form digitizer reaching {X}% field accuracy after review, auto-accepting {Y}% of fields and cutting entry time to {Z} seconds per form.",
                    "Built a form digitizer reaching 97% field accuracy after review, auto-accepting 82% of fields and cutting entry time to 24 seconds per form.",
                ),
                (
                    "Added validation rules that caught malformed dates and codes before export.",
                    "Added validation rules that caught 94% of malformed dates and codes before export.",
                ),
                (
                    "Created a review screen that preserved every original crop and edit in an audit trail.",
                    "Created a review screen that preserved every original crop and edit in an audit trail for later verification.",
                ),
            ],
            interview=[
                (
                    "Why not trust the OCR output directly?",
                    "Handwriting and poor scans produce confident-looking errors. A review step is cheaper than correcting a database later, and it gives me a way to measure where the model is weak.",
                ),
                (
                    "How do you measure the value of human review?",
                    "I compare field accuracy before and after review, the share of fields auto-accepted and the time spent. A review step that improves accuracy but doubles time may not be worth it.",
                ),
                (
                    "How do you handle privacy?",
                    "I use synthetic forms with fake data and never send real records to a hosted model. The review screen shows only the minimum needed, and exports are explicit.",
                ),
            ],
            differentiators=[
                "A measurable review step, not an OCR demo.",
                "Validation rules that catch format errors before export.",
                "Synthetic-only data handling and an audit trail.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-012",
        title="Exoplanet Transit Detector",
        summary=(
            "Find possible exoplanets in telescope brightness data by looking "
            "for the small, regular dips caused by a planet crossing its star. "
            "Clean the light curves, search for periodic signals such as box "
            "least squares, then train a classifier to separate real planets "
            "from false positives.\n\n"
            "Report precision, recall, F1 and PR-AUC on held-out stars, the "
            "recovery rate of known confirmed planets, and the causes of false "
            "positives. Avoid leaking information between training and test "
            "stars."
        ),
        who_affected="Astronomy researchers, citizen-science projects, and students learning time-series analysis.",
        why_matters="Telescopes produce more light curves than humans can inspect, and real planets hide among eclipsing binaries and noise.",
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=105,
        tech_tags=["python", "lightkurve", "astropy", "time-series", "scikit-learn", "signal-processing"],
        datasets=[
            {"name": "NASA Exoplanet Archive", "url": "https://exoplanetarchive.ipac.caltech.edu/"},
            {"name": "MAST Kepler and TESS light curves", "url": "https://mast.stsci.edu/"},
            {"name": "lightkurve documentation", "url": "https://docs.lightkurve.org/"},
        ],
        approaches=[
            "Download and clean Kepler or TESS light curves, removing gaps and outliers.",
            "Search for periodic transit-like dips with box least squares.",
            "Train a classifier on candidate features with star-grouped splits.",
            "Report recovery, precision, false-positive causes and PR-AUC.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. NASA Kepler and TESS data are public.",
        original_text="Build an exoplanet transit detector that cleans light curves, searches for periodic dips and classifies real planets against false positives.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A light curve produces candidate transit periods and a ranked list of possible planets.",
                [
                    "The pipeline cleans a light curve and finds a periodic dip.",
                    "A classifier separates candidates from obvious false positives.",
                    "Held-out precision and recall are reported.",
                    "The UI shows the folded light curve behind each candidate.",
                ],
            ),
            impressive=(
                "The detector recovers known planets and explains which false positives are hardest.",
                [
                    "Known confirmed planets are used as a recovery check.",
                    "Splits are grouped by star to avoid leakage.",
                    "False positives are broken down into eclipsing binaries and noise.",
                    "PR-AUC and threshold choice are documented for an imbalanced target.",
                ],
            ),
            roles=[
                ("Machine learning engineer", "Shows time-series cleaning, signal search and class-imbalance evaluation."),
                ("Data scientist", "You can build a scientific pipeline and report recovery on known cases."),
                ("Science software engineer", "The project connects public astronomy data to an inspectable detection workflow."),
            ],
            bullets=[
                (
                    "Built an exoplanet transit detector that recovered {X}% of known planets with {Y} precision on {N} held-out stars.",
                    "Built an exoplanet transit detector that recovered 74% of known planets with 0.88 precision on 3,400 held-out stars.",
                ),
                (
                    "Removed star-level leakage and improved PR-AUC from {A} to {B}.",
                    "Removed star-level leakage from the split and improved PR-AUC from 0.61 to 0.79.",
                ),
                (
                    "Classified false positives by cause so the remaining candidates were easier to review.",
                    "Classified false positives into eclipsing binaries and noise so the remaining candidates were easier to review.",
                ),
            ],
            interview=[
                (
                    "Why group the train and test split by star?",
                    "Multiple light curves can come from the same star or system. A random split lets the model memorise the star and inflates the score. Grouping by star tests generalisation to new systems.",
                ),
                (
                    "Why use PR-AUC instead of only accuracy?",
                    "Confirmed planets are rare among all light curves, so accuracy is dominated by negatives. PR-AUC focuses on the candidate class and shows the precision-recall trade-off at different thresholds.",
                ),
                (
                    "What did you learn from the false positives?",
                    "Most remaining errors were eclipsing binaries with similar depths and periods. That is a useful finding: future work should add secondary-eclipse and centroid features.",
                ),
            ],
            differentiators=[
                "A known-planet recovery check, not only a held-out score.",
                "Star-grouped evaluation that removes leakage.",
                "False-positive analysis that points to the next modelling step.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-013",
        title="Orbital Debris Collision Risk Predictor",
        summary=(
            "Screen satellites and debris for close approaches using public "
            "orbital elements. Propagate orbits, compute the time and distance "
            "of closest approach, and rank objects by risk. Then train a model "
            "on conjunction data to predict which events become dangerous and "
            "compare it with a simple distance-based rule.\n\n"
            "Report recall of high-risk events at a fixed false-alarm rate, ROC "
            "or PR-AUC against the distance rule, and screening speed in object "
            "pairs per second.\n\n"
            "Responsible use: estimates can be wrong and are not a substitute "
            "for official alerts or safety systems."
        ),
        who_affected="Satellite operators, space agencies, and insurers assessing collision risk.",
        why_matters="A single collision can create debris that threatens many other satellites for decades.",
        field="aiml",
        domain="other",
        difficulty="advanced",
        est_hours=130,
        tech_tags=["python", "sgp4", "orbital-mechanics", "numpy", "scikit-learn", "pandas"],
        datasets=[
            {"name": "CelesTrak orbital element sets", "url": "https://celestrak.org/"},
            {"name": "ESA Kelvins collision-avoidance challenge", "url": "https://kelvins.esa.int/"},
        ],
        approaches=[
            "Parse orbital elements and propagate positions with SGP4 over a screening window.",
            "Compute close-approach time, distance and relative velocity for candidate pairs.",
            "Train a risk classifier on conjunction features and compare with a distance-only rule.",
            "Report recall at a fixed false-alarm rate plus screening throughput.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Orbital element sets and challenge data have their own terms.",
        original_text="Build an orbital conjunction screener and risk model that propagates public orbits, ranks close approaches and beats a distance-only rule.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A set of public orbits produces a ranked list of close approaches with time and minimum distance.",
                [
                    "Orbits are propagated from public elements with a stated time window.",
                    "Candidate pairs are screened and ranked by distance.",
                    "The UI shows the closest approach time and distance for each event.",
                    "Screening throughput is measured in pairs per second.",
                ],
            ),
            impressive=(
                "A risk model improves high-risk recall over a distance rule and the report shows the false-alarm cost.",
                [
                    "The model is compared with a distance-only rule at the same false-alarm rate.",
                    "PR-AUC and recall are reported for the high-risk class.",
                    "The screening pipeline prunes pairs before expensive propagation.",
                    "A note explains that outputs are risk estimates, not certainty.",
                ],
            ),
            roles=[
                ("Machine learning engineer", "Shows feature engineering, imbalanced classification and a strong baseline comparison."),
                ("Scientific software engineer", "You combined orbital propagation, candidate screening and measurable model evaluation."),
                ("Space systems engineer", "The project is framed around operator decisions, false alarms and throughput."),
            ],
            bullets=[
                (
                    "Built an orbital conjunction screener and risk model that caught {X}% of high-risk events at {Y}% false alarms and screened {Z} pairs per second.",
                    "Built an orbital conjunction screener and risk model that caught 87% of high-risk events at 5% false alarms and screened 42,000 pairs per second.",
                ),
                (
                    "Improved high-risk recall by {X} points over a distance-only rule at the same false-alarm rate.",
                    "Improved high-risk recall by 19 points over a distance-only rule at the same false-alarm rate.",
                ),
                (
                    "Pruned candidate pairs before propagation to make a full screening run finish in {X} minutes.",
                    "Pruned candidate pairs before propagation and cut a full screening run from 40 minutes to 6.",
                ),
            ],
            interview=[
                (
                    "Why not rank only by distance?",
                    "Distance ignores relative velocity, uncertainty and time to conjunction. Two objects can be far apart but closing fast, or close but moving apart. The model uses those features and is compared with the simple rule.",
                ),
                (
                    "How do you evaluate a rare high-risk event?",
                    "I fix a false-alarm budget the operator can tolerate, then measure recall at that budget. I also report PR-AUC so the whole trade-off is visible.",
                ),
                (
                    "What is the biggest limitation?",
                    "Public orbital elements are sparse and stale, and covariance information is limited. The output is a screening aid, not an authoritative collision warning.",
                ),
            ],
            differentiators=[
                "A distance-only baseline and a measured lift over it.",
                "Throughput and pruning, not only model accuracy.",
                "Clear language about uncertainty and official systems.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-014",
        title="Multi-Modal Agricultural Assistant",
        summary=(
            "Farmers often have a soil report, a field photo and a weather "
            "forecast, but no single place to make sense of them. Build an "
            "assistant that reads soil health reports with OCR, looks at "
            "satellite imagery and weather, and answers questions with "
            "retrieval over verified agricultural guidance.\n\n"
            "Every answer cites its source and the assistant says when it does "
            "not know. Test it against expert-written questions and report "
            "answer accuracy, citation support and OCR field accuracy.\n\n"
            "Responsible use: decision support, not advice. Check with a local "
            "agricultural officer before acting on outputs."
        ),
        who_affected="Smallholder farmers, agricultural extension officers, and cooperatives making input decisions.",
        why_matters="Confident but wrong advice can cost a season of income, so source grounding and uncertainty matter as much as fluency.",
        field="aiml",
        domain="agriculture",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["python", "ocr", "rag", "sentinel-2", "open-meteo", "fastapi", "llm"],
        datasets=[
            {"name": "Sentinel-2 imagery", "url": "https://sentinel.esa.int/web/sentinel/missions/sentinel-2"},
            {"name": "Open-Meteo forecasts", "url": "https://open-meteo.com/"},
            {"name": "Open agricultural guidance you have reuse rights for", "url": None},
        ],
        approaches=[
            "Extract soil-report fields with OCR and validate them against a schema.",
            "Retrieve verified guidance and cite the passage behind each answer.",
            "Combine report values, satellite indices and weather into a short context.",
            "Evaluate against expert questions and refuse when evidence is weak.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use verified guidance with open reuse terms.",
        original_text="Build a multimodal farming assistant that reads soil reports and satellite data and answers with citations or an honest refusal.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A soil report plus a question produces an answer with cited guidance and a clear uncertainty note.",
                [
                    "Soil report fields are extracted into a validated schema.",
                    "Answers retrieve at least one verified source passage.",
                    "The assistant refuses when the retrieved evidence is weak.",
                    "The UI labels every answer as decision support, not advice.",
                ],
            ),
            impressive=(
                "The assistant combines report, satellite and weather context and is measured on expert questions.",
                [
                    "Answers use soil, satellite and weather inputs without pretending they are ground truth.",
                    "Citation support is checked against the claim, not just the retrieval score.",
                    "Expert-written questions measure accuracy and refusal quality.",
                    "OCR field accuracy is reported separately from answer accuracy.",
                ],
            ),
            roles=[
                ("AI application engineer", "Shows OCR, retrieval, citations and refusal across several data sources."),
                ("AgriTech engineer", "You can connect farm data to guidance while respecting uncertainty and local expertise."),
                ("Full-stack engineer", "You built the ingestion, retrieval and farmer-facing answer flow."),
            ],
            bullets=[
                (
                    "Built a multimodal farming assistant answering {X}% of {N} expert questions correctly with {Y}% citation support.",
                    "Built a multimodal farming assistant answering 81% of 120 expert questions correctly with 90% citation support.",
                ),
                (
                    "Extracted soil-report fields with {X}% accuracy and used them as grounded context instead of free text.",
                    "Extracted 14 soil-report fields with 93% accuracy and used them as grounded context instead of free text.",
                ),
                (
                    "Added a refusal path that reduced unsupported advice on questions outside the verified sources.",
                    "Added a refusal path that reduced unsupported advice on out-of-scope questions from 27% to 6%.",
                ),
            ],
            interview=[
                (
                    "Why not let the language model answer from general knowledge?",
                    "Agricultural advice is local and seasonal. General knowledge can be outdated or wrong for a region. Retrieval from verified guidance gives a source, and refusal handles the gaps.",
                ),
                (
                    "How do you check a citation?",
                    "I compare the claim with the cited passage using a separate checker and a small human-labelled sample. A high retrieval score does not prove the passage supports the answer.",
                ),
                (
                    "What is the role of satellite and weather data?",
                    "They add context such as vegetation condition and upcoming rain, but they are estimates. I show them as inputs with dates and uncertainty, not as measured field truth.",
                ),
            ],
            differentiators=[
                "Citation support measured separately from answer fluency.",
                "A real refusal path for out-of-scope questions.",
                "Multiple data sources kept visible instead of blended into one score.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-015",
        title="Engineering Knowledge Copilot",
        summary=(
            "Engineering teams lose time searching specifications, standards "
            "and design documents. Build an assistant that answers with exact "
            "citations, drafts technical documentation from structured product "
            "data, and checks that each cited passage actually supports the "
            "answer.\n\n"
            "Report retrieval recall@k on a labelled question set, verified "
            "citation rate, answer accuracy and latency.\n\n"
            "Responsible use: a learning aid, not a replacement for source "
            "documents. Check answers against the cited sources."
        ),
        who_affected="Mechanical, electrical and systems engineers, technical writers, and new team members.",
        why_matters="A wrong specification answer can cause rework, safety issues or a failed design review.",
        field="aiml",
        domain="industry",
        difficulty="intermediate",
        est_hours=115,
        tech_tags=["python", "rag", "embeddings", "citation-checking", "fastapi", "react", "evaluation"],
        datasets=[
            {"name": "NASA Technical Reports Server", "url": "https://ntrs.nasa.gov/"},
            {"name": "Your own design documents and specifications", "url": None},
        ],
        approaches=[
            "Parse engineering documents into sections with stable source ids.",
            "Build hybrid retrieval and answer with exact passage citations.",
            "Check whether each citation supports the generated claim.",
            "Measure recall@k, citation support, accuracy and latency.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Use documents you have permission to process.",
        original_text="Build an engineering knowledge copilot that answers over specifications with exact citations and verifies that citations support the answer.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "An engineer asks a specification question and gets an answer with exact source passages.",
                [
                    "Documents are chunked with page and section ids.",
                    "Every answer includes at least one exact citation.",
                    "A labelled question set measures retrieval recall@k.",
                    "The UI links each citation back to the source passage.",
                ],
            ),
            impressive=(
                "The copilot verifies citation support and drafts documentation from structured data.",
                [
                    "A citation checker measures whether each passage supports the claim.",
                    "Recall@5 and answer accuracy are reported on a labelled set.",
                    "A documentation draft is generated from structured product data with source links.",
                    "Latency is measured and shown for retrieval and generation separately.",
                ],
            ),
            roles=[
                ("AI application engineer", "Shows retrieval-augmented generation, citation verification and evaluation."),
                ("Backend engineer", "You built document ingestion, retrieval, source ids and a measurable API."),
                ("Technical product engineer", "The project connects engineering documents to a workflow engineers already have."),
            ],
            bullets=[
                (
                    "Built an engineering knowledge copilot with {X}% recall@5 and {Y}% verified-citation rate across {N} documents.",
                    "Built an engineering knowledge copilot with 92% recall@5 and 88% verified-citation rate across 640 documents.",
                ),
                (
                    "Added a citation checker that caught unsupported passages before the answer reached an engineer.",
                    "Added a citation checker that caught 14% of unsupported passages before the answer reached an engineer.",
                ),
                (
                    "Cut document lookup time from {A} minutes to {B} seconds on a labelled question set.",
                    "Cut document lookup time from 11 minutes to 18 seconds on a 75-question set drawn from real design reviews.",
                ),
            ],
            interview=[
                (
                    "How is this different from a document chatbot?",
                    "It is evaluated. I measure retrieval recall, citation support and answer accuracy on labelled questions, and the UI exposes the exact passages. A chatbot that sounds plausible is not enough for engineering work.",
                ),
                (
                    "Why check citations separately?",
                    "Retrieval can return a relevant document that does not support the specific claim. A separate checker catches that mismatch, which is the main failure mode in technical answers.",
                ),
                (
                    "What would you improve next?",
                    "Table and diagram retrieval. Engineering documents often put the answer in a table, and text-only chunking loses the row and column context.",
                ),
            ],
            differentiators=[
                "Citation-support checking beyond retrieval similarity.",
                "A labelled evaluation set with recall@5 and accuracy.",
                "A documentation draft path built from structured data.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-016",
        title="Which AI Wrote This? (Model Attribution)",
        summary=(
            "As generated text becomes common, readers want to know which model "
            "produced a passage. Build features from writing style and token "
            "statistics, fine-tune a text classifier, then test it on models "
            "and prompts it has never seen.\n\n"
            "Report accuracy and F1 per source model on seen prompts, the same "
            "metrics on unseen prompts and models, and the calibration of "
            "confidence scores. Explain where attribution fails.\n\n"
            "Responsible use: attribution is probabilistic. Never treat it as "
            "proof of authorship or use it to penalise someone."
        ),
        who_affected="Platforms, editors, researchers and readers trying to understand the provenance of text.",
        why_matters="Attribution tools are easy to overtrust, and a wrong accusation can harm a real person.",
        field="aiml",
        domain="cybersecurity",
        difficulty="intermediate",
        est_hours=105,
        tech_tags=["python", "transformers", "stylometry", "scikit-learn", "calibration", "huggingface"],
        datasets=[
            {"name": "HC3 human versus ChatGPT corpus", "url": "https://huggingface.co/datasets/Hello-SimpleAI/HC3"},
            {"name": "M4 multi-model generated text", "url": "https://github.com/mbzuai-nlp/M4"},
            {"name": "MAGE machine-generated text benchmark", "url": "https://github.com/yafuly/MAGE"},
        ],
        approaches=[
            "Build stylometric and token-statistics features from text samples.",
            "Fine-tune a transformer classifier on seen models and prompts.",
            "Evaluate on unseen prompts and unseen models as a separate test.",
            "Calibrate confidence and report where attribution fails.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Check each corpus licence and do not use output as proof.",
        original_text="Build a text-source attribution model that identifies which language model wrote a passage and measures generalisation to unseen models and prompts.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A passage is classified by source model with a confidence score and a per-model probability view.",
                [
                    "The dataset has a clear model label and a held-out prompt split.",
                    "A baseline and a fine-tuned classifier are compared.",
                    "Accuracy and F1 are reported per model.",
                    "Confidence is shown to the user, not hidden.",
                ],
            ),
            impressive=(
                "The model is tested on unseen models and prompts, and calibration exposes when it should not be trusted.",
                [
                    "Unseen-model and unseen-prompt results are reported separately from in-distribution results.",
                    "A calibration curve shows the gap between confidence and accuracy.",
                    "Ablations show how much stylometric features add to the transformer.",
                    "The demo warns that attribution is not proof of authorship.",
                ],
            ),
            roles=[
                ("NLP engineer", "Shows fine-tuning, stylometric features and out-of-distribution evaluation."),
                ("ML engineer", "You can measure calibration and explain a model's limits instead of only its accuracy."),
                ("Trust & safety researcher", "The project treats attribution as probabilistic evidence with real consequences."),
            ],
            bullets=[
                (
                    "Built a text-source attribution model with {X}% accuracy on seen models and {Y}% on unseen models, quantifying the generalisation gap.",
                    "Built a text-source attribution model with 91% accuracy on seen models and 63% on unseen models, quantifying the 28 point generalisation gap.",
                ),
                (
                    "Calibrated confidence scores so low-confidence predictions were flagged instead of presented as certain.",
                    "Calibrated confidence scores and flagged the 22% of predictions that were too uncertain to use.",
                ),
                (
                    "Showed which stylistic features survived a change of prompt and which were dataset artifacts.",
                    "Showed which stylistic features survived a change of prompt and which were dataset-specific artifacts.",
                ),
            ],
            interview=[
                (
                    "Why is unseen-model accuracy the important number?",
                    "A classifier can learn the fingerprints of the models in its training set. New models appear constantly, so the useful claim is how it behaves on a model it has never seen.",
                ),
                (
                    "How do you calibrate the confidence?",
                    "I compare predicted confidence with observed accuracy on a held-out set and apply temperature scaling or isotonic calibration. Then I report the calibration curve, not just accuracy.",
                ),
                (
                    "Would you use this to accuse someone?",
                    "No. Attribution is probabilistic and can be wrong, especially after editing or translation. It can support an investigation, but it is not proof of authorship.",
                ),
            ],
            differentiators=[
                "A separate unseen-model evaluation.",
                "Calibration, not only a top-line accuracy score.",
                "Clear responsible-use language in the product.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-017",
        title="Molecule Structure Identification from Mass Spectra",
        summary=(
            "Given a tandem mass spectrum, predict the structure of a small "
            "molecule. Process the spectrum, predict a molecular fingerprint or "
            "substructures with a neural model, and rank candidate structures "
            "from a compound database.\n\n"
            "Report top-1, top-5 and top-10 identification accuracy, mean "
            "Tanimoto similarity of predicted fingerprints and runtime per "
            "spectrum. Keep the ranking inspectable so a chemist can review "
            "the evidence."
        ),
        who_affected="Analytical chemists, metabolomics researchers, and labs identifying unknown compounds.",
        why_matters="Manual structure elucidation is slow, and a wrong identification can send a whole study in the wrong direction.",
        field="aiml",
        domain="other",
        difficulty="advanced",
        est_hours=135,
        tech_tags=["python", "pytorch", "cheminformatics", "rdkit", "spectra", "ranking", "gnps"],
        datasets=[
            {"name": "MassBank spectral library", "url": "https://massbank.eu/MassBank/"},
            {"name": "MassBank of North America", "url": "https://mona.fiehnlab.ucdavis.edu/"},
            {"name": "GNPS public spectral libraries", "url": "https://gnps.ucsd.edu/"},
        ],
        approaches=[
            "Parse and normalise tandem mass spectra into a model-ready representation.",
            "Train a neural model to predict molecular fingerprints or substructures.",
            "Rank candidate molecules from a compound database by fingerprint similarity.",
            "Report top-k accuracy, Tanimoto similarity and runtime per spectrum.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Spectral libraries have different licences; check each.",
        original_text="Build a mass-spectrum structure identifier that predicts fingerprints and ranks candidate molecules, evaluated with top-k accuracy.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A spectrum produces a ranked candidate list with top-1 and top-5 accuracy reported.",
                [
                    "Spectra are parsed into a consistent peak representation.",
                    "A fingerprint model produces a similarity score for candidates.",
                    "Top-1 and top-5 accuracy are measured on a held-out library split.",
                    "The UI shows the spectrum and the ranked candidates.",
                ],
            ),
            impressive=(
                "The system improves top-10 recovery with a realistic candidate database and reports fingerprint quality.",
                [
                    "Candidates are ranked against a database large enough to be non-trivial.",
                    "Top-10 accuracy and mean Tanimoto similarity are reported.",
                    "Ablations show the effect of peak preprocessing and database size.",
                    "Runtime per spectrum is measured and documented.",
                ],
            ),
            roles=[
                ("ML engineer", "Shows scientific feature engineering, fingerprint prediction and ranking metrics."),
                ("Cheminformatics engineer", "You can combine RDKit, spectral data and candidate search in one pipeline."),
                ("Research software engineer", "The project keeps evidence and metrics inspectable for a domain expert."),
            ],
            bullets=[
                (
                    "Built a mass-spectrum structure identifier that ranks the correct molecule in the top 10 for {X}% of {N} test spectra.",
                    "Built a mass-spectrum structure identifier that ranks the correct molecule in the top 10 for 76% of 4,200 test spectra.",
                ),
                (
                    "Predicted molecular fingerprints with a mean Tanimoto similarity of {X} and used them to rank candidates.",
                    "Predicted molecular fingerprints with a mean Tanimoto similarity of 0.71 and used them to rank candidates.",
                ),
                (
                    "Scaled candidate ranking to {N} compounds with {X} ms per spectrum.",
                    "Scaled candidate ranking to 120,000 compounds with 41 ms per spectrum.",
                ),
            ],
            interview=[
                (
                    "Why predict fingerprints instead of the molecule directly?",
                    "A fingerprint is a stable intermediate representation. It supports similarity search and ranking, and it is easier to evaluate than generating a valid structure from scratch.",
                ),
                (
                    "Why report top-10 as well as top-1?",
                    "In real identification, a chemist reviews a shortlist. Top-1 hides whether the correct molecule is close. Top-10 matches the workflow and is a fairer measure of usefulness.",
                ),
                (
                    "What is the main data risk?",
                    "Library coverage. A molecule absent from the candidate database can never be ranked first. I report database size and discuss coverage as a limitation.",
                ),
            ],
            differentiators=[
                "A realistic candidate ranking task, not just fingerprint regression.",
                "Top-k metrics that match a chemist's shortlist workflow.",
                "Runtime and database-size reporting for a practical pipeline.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-018",
        title="Autonomous Engineering Problem Solver",
        summary=(
            "Build an agent that solves engineering problems in structural, "
            "electrical and mechanical settings. It reasons through "
            "constraints, calls calculation tools such as unit-aware "
            "calculators and simple solvers, then verifies its own answers.\n\n"
            "Evaluate on problems with known solutions and report the fraction "
            "solved correctly, unit and consistency errors caught by the "
            "verifier, and the failure categories.\n\n"
            "Responsible use: estimates can be wrong and are not a substitute "
            "for official engineering or safety decisions."
        ),
        who_affected="Engineering students, design teams, and engineers checking routine calculations.",
        why_matters="A fluent answer with a wrong unit or missed constraint can look correct and still cause a failed design.",
        field="aiml",
        domain="industry",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["python", "llm", "tool-use", "sympy", "pint", "pynite", "evaluation"],
        datasets=[
            {"name": "OpenStax engineering problems with known answers", "url": "https://openstax.org/"},
            {"name": "SymPy", "url": "https://www.sympy.org/"},
            {"name": "pint unit library", "url": "https://pint.readthedocs.io/"},
            {"name": "PyNite structural analysis", "url": "https://pynite.readthedocs.io/"},
            {"name": "ngspice circuit simulator", "url": "https://ngspice.sourceforge.io/"},
        ],
        approaches=[
            "Define tool schemas for units, symbolic maths, structures and circuits.",
            "Make the agent show its constraints and call tools instead of doing arithmetic in text.",
            "Add an automatic verifier for units, dimensional consistency and known checks.",
            "Evaluate on a set with known solutions and classify every failure.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Verify against authoritative solutions before trusting an answer.",
        original_text="Build an engineering problem-solving agent that uses calculation tools, checks units and self-verifies against known-solution problems.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A set of known problems is solved with tool calls and a visible verification step.",
                [
                    "The agent calls at least one calculation tool instead of doing arithmetic in prose.",
                    "Units are checked for each numeric answer.",
                    "Known-solution problems are scored automatically.",
                    "Failures are grouped into unit, constraint and reasoning errors.",
                ],
            ),
            impressive=(
                "The verifier catches its own errors and the failure analysis shows where the agent is unreliable.",
                [
                    "A verifier catches dimensional and consistency errors before the answer is shown.",
                    "The evaluation reports solve rate, verification pass rate and failure categories.",
                    "A tool-use trace lets a reviewer inspect every calculation.",
                    "At least two engineering domains are covered with domain-specific checks.",
                ],
            ),
            roles=[
                ("AI engineer", "Shows tool use, self-verification and evaluation on problems with objective answers."),
                ("Engineering software engineer", "You connected symbolic maths, units and domain solvers in one agent."),
                ("Backend engineer", "The project requires clear tool contracts, trace logging and safe failure handling."),
            ],
            bullets=[
                (
                    "Built an engineering problem-solving agent that solved {X}% of {N} known problems and caught {Y}% of its own errors through automated verification.",
                    "Built an engineering problem-solving agent that solved 78% of 140 known problems and caught 84% of its own unit and consistency errors.",
                ),
                (
                    "Added unit-aware verification that removed dimension errors from the final answers.",
                    "Added unit-aware verification that removed 31 dimension errors from the final answers across the test set.",
                ),
                (
                    "Classified failures into unit, constraint and reasoning categories so the next fix was obvious.",
                    "Classified failures into unit, constraint and reasoning categories so the next fix was obvious from the evaluation report.",
                ),
            ],
            interview=[
                (
                    "Why not let the model do the arithmetic?",
                    "Language models are fluent but unreliable calculators. A tool call gives a reproducible result, and a verifier can check units and constraints. The model's job is to choose the tool and interpret the result.",
                ),
                (
                    "What does the verifier check?",
                    "Dimensional consistency, expected units, plausible magnitudes and domain checks such as equilibrium or power balance. It catches a class of errors that a second model opinion would miss.",
                ),
                (
                    "How did you build the evaluation set?",
                    "I used textbook problems with published answers and wrote additional cases with known solutions. Each answer is compared automatically, and every failure is classified by hand.",
                ),
            ],
            differentiators=[
                "Automatic verification of the agent's own output.",
                "A failure taxonomy, not just a single solve rate.",
                "A visible tool-use trace for every answer.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-019",
        title="Neural Network Library from Scratch (Autograd)",
        summary=(
            "Build a tiny deep-learning library: an automatic-differentiation "
            "engine that records operations and computes gradients by "
            "backpropagation, plus layers, activations, losses and optimisers "
            "(SGD and Adam).\n\n"
            "Verify every gradient against numerical gradient checking, then "
            "train a small network on a real dataset and match an equivalent "
            "PyTorch model. Report maximum gradient-check error, test accuracy "
            "and training time per epoch."
        ),
        who_affected="Students learning deep learning, interview candidates, and engineers who want to understand frameworks.",
        why_matters="Most practitioners use frameworks as black boxes, which makes debugging gradients and training failures much harder.",
        field="aiml",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=110,
        tech_tags=["python", "numpy", "autograd", "pytorch", "neural-networks", "testing"],
        datasets=[
            {"name": "Fashion-MNIST", "url": "https://github.com/zalandoresearch/fashion-mnist"},
            {"name": "UCI machine learning repository", "url": "https://archive.ics.uci.edu/"},
        ],
        approaches=[
            "Implement tensor operations with a computation graph and reverse-mode gradients.",
            "Add layers, activations, losses, SGD and Adam on top of the engine.",
            "Verify gradients numerically before training anything large.",
            "Match an equivalent PyTorch model on accuracy and measure epoch time.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Any small public dataset is enough.",
        original_text="Implement a small deep-learning library with automatic differentiation, layers and optimizers, verified with gradient checks and compared with PyTorch.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A small network trains from scratch on a real dataset and gradients pass numerical checks.",
                [
                    "The autograd engine handles add, multiply, matrix multiply and common activations.",
                    "SGD trains a small classifier to a reported test accuracy.",
                    "Every implemented gradient has a numerical check.",
                    "A README explains the graph and the supported operations.",
                ],
            ),
            impressive=(
                "Adam and a second architecture match PyTorch within a stated tolerance, with performance measured.",
                [
                    "SGD and Adam are both implemented and tested.",
                    "The model matches an equivalent PyTorch model within a stated accuracy gap.",
                    "Gradient-check error and per-epoch training time are reported.",
                    "A small autograd visualisation shows the graph behind one backward pass.",
                ],
            ),
            roles=[
                ("ML engineer", "Shows backpropagation, computational graphs and optimisers from implementation experience."),
                ("Software engineer", "You built a small numerical library with tests, documentation and clear limits."),
                ("Interview candidate", "It gives a concrete story for gradient, chain-rule and optimizer questions."),
            ],
            bullets=[
                (
                    "Implemented a deep-learning library with automatic differentiation, verified by gradient checks to within {error} and matching PyTorch accuracy within {X} points on {dataset}.",
                    "Implemented a deep-learning library with automatic differentiation, verified by gradient checks to within 1e-6 and matching PyTorch accuracy within 0.4 points on Fashion-MNIST.",
                ),
                (
                    "Added SGD and Adam with tests for convergence and numerical stability.",
                    "Added SGD and Adam with convergence and numerical-stability tests on two small datasets.",
                ),
                (
                    "Documented the computation graph and measured training time per epoch against PyTorch.",
                    "Documented the computation graph and measured training time per epoch at 1.8x the equivalent PyTorch model.",
                ),
            ],
            interview=[
                (
                    "How does reverse-mode autodiff work?",
                    "Each operation records its inputs and a local backward function. During the backward pass, gradients flow from the output to the inputs by applying the chain rule in reverse order. The graph makes repeated operations and shared subgraphs explicit.",
                ),
                (
                    "Why run numerical gradient checks?",
                    "A wrong derivative can still train on a simple problem. A finite-difference check compares the analytic gradient with a small perturbation and catches sign, scale and broadcasting errors before they become mysterious training failures.",
                ),
                (
                    "What does matching PyTorch prove?",
                    "It shows the implementation is correct enough to reproduce a known result under the same data and architecture. It does not prove it is fast or complete, so I report the accuracy gap and training time.",
                ),
            ],
            differentiators=[
                "Numerical gradient checks for every operation.",
                "A direct accuracy and speed comparison with PyTorch.",
                "A visible computation graph, not only a working training loop.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-020",
        title="Mini GPT from Scratch",
        summary=(
            "Build a small GPT-style language model yourself: a character-level "
            "or byte-pair tokenizer, self-attention and transformer blocks, a "
            "training loop, and text generation with temperature and top-k "
            "sampling.\n\n"
            "Train on a small public-domain corpus, track loss and perplexity, "
            "and study how model size, context length and training time change "
            "the output. Report validation perplexity and generation speed.\n\n"
            "Responsible use: generated text can be wrong, biased or "
            "nonsensical. Label it as machine-generated and do not present it "
            "as fact."
        ),
        who_affected="Students learning transformers, NLP engineers, and interview candidates explaining attention.",
        why_matters="A working tiny model makes attention, tokenisation and sampling concrete instead of diagram-level knowledge.",
        field="aiml",
        domain="nlp-llm",
        difficulty="advanced",
        est_hours=130,
        tech_tags=["python", "pytorch", "transformers", "tokenization", "attention", "training"],
        datasets=[
            {"name": "Project Gutenberg public-domain texts", "url": "https://www.gutenberg.org/"},
            {"name": "Wikipedia database dumps", "url": "https://dumps.wikimedia.org/"},
        ],
        approaches=[
            "Implement a tokenizer and a small transformer with causal self-attention.",
            "Write a training loop with loss tracking and validation perplexity.",
            "Add temperature and top-k sampling for generation.",
            "Run ablations on model size, context length and training time.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Start tiny enough to train on a free GPU in under an hour.",
        original_text="Implement a small GPT-style transformer from scratch, train it on public-domain text and study perplexity and sampling.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A tiny transformer trains on a public-domain corpus and generates text with temperature and top-k controls.",
                [
                    "The tokenizer and causal attention are implemented from scratch.",
                    "Training loss and validation perplexity are logged.",
                    "Generation supports temperature and top-k sampling.",
                    "A README explains the architecture and the training budget.",
                ],
            ),
            impressive=(
                "Ablations show how size and context change perplexity, and generation speed is measured.",
                [
                    "At least two model sizes or context lengths are compared.",
                    "Validation perplexity and tokens per second are reported.",
                    "The report explains how sampling settings change repetition and diversity.",
                    "A small demo lets a reviewer type a prompt and adjust sampling.",
                ],
            ),
            roles=[
                ("NLP engineer", "Shows attention, tokenization, training dynamics and sampling from implementation experience."),
                ("ML engineer", "You can run controlled ablations and report honest perplexity and speed."),
                ("Research engineer", "The project turns transformer theory into a reproducible small experiment."),
            ],
            bullets=[
                (
                    "Implemented a {N}M-parameter GPT-style transformer from scratch, reaching {X} validation perplexity on {corpus} and generating at {Y} tokens per second.",
                    "Implemented a 6.4M-parameter GPT-style transformer from scratch, reaching 18.7 validation perplexity on a Gutenberg corpus and generating at 420 tokens per second.",
                ),
                (
                    "Compared context lengths and showed the point where extra context stopped improving perplexity.",
                    "Compared context lengths from 64 to 256 tokens and showed where extra context stopped improving validation perplexity.",
                ),
                (
                    "Documented how temperature and top-k changed repetition and diversity in generated text.",
                    "Documented how temperature and top-k changed repetition and diversity instead of presenting one cherry-picked sample.",
                ),
            ],
            interview=[
                (
                    "Why build a small GPT instead of fine-tuning a large one?",
                    "The goal is understanding. A tiny model makes tokenisation, attention, loss and sampling inspectable, and I can run ablations on a free GPU. Fine-tuning teaches a different skill.",
                ),
                (
                    "What does perplexity measure?",
                    "It measures how surprised the model is by the validation text. Lower is better, but it is not a direct measure of usefulness or truthfulness, so I pair it with sample inspection.",
                ),
                (
                    "Why does temperature change repetition?",
                    "Low temperature sharpens the distribution toward the most likely token, which can become repetitive. Higher temperature flattens it and increases diversity, but also increases nonsense.",
                ),
            ],
            differentiators=[
                "A from-scratch implementation, not a fine-tuning wrapper.",
                "Controlled ablations on size and context length.",
                "Sampling behaviour documented with evidence.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-021",
        title="Game-Playing AI: Minimax, Alpha-Beta and Monte Carlo Tree Search",
        summary=(
            "Build an AI that plays a board game such as Connect Four or "
            "Othello. Implement minimax with alpha-beta pruning and Monte Carlo "
            "Tree Search, then run a tournament between your agents and a "
            "random player.\n\n"
            "Measure win rates, positions searched per move, time per move and "
            "the effect of pruning on search size. Add a web page where people "
            "can play against different difficulty levels."
        ),
        who_affected="Students learning search and game AI, interview candidates, and anyone who wants a playable AI demo.",
        why_matters="Search, pruning and evaluation functions are core AI ideas that become intuitive when you can play against them.",
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=100,
        tech_tags=["python", "minimax", "alpha-beta", "monte-carlo-tree-search", "react", "game-ai"],
        datasets=[
            {"name": "Self-play games generated by your agents", "url": None},
        ],
        approaches=[
            "Implement the game state, legal moves and terminal scoring.",
            "Add minimax with alpha-beta pruning and a heuristic evaluation.",
            "Add Monte Carlo Tree Search and a tournament harness.",
            "Build a web board with difficulty levels and search statistics.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. No external dataset is needed; agents generate their own games.",
        original_text="Build minimax and Monte Carlo Tree Search agents for a board game, benchmark them in a tournament and expose a playable web UI.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A playable board supports a minimax agent and a random baseline, with win rate reported.",
                [
                    "The rules engine handles legal moves and terminal states correctly.",
                    "Minimax with alpha-beta beats a random player in a recorded tournament.",
                    "The UI shows the move chosen and the time taken.",
                    "Win rate and positions searched are logged.",
                ],
            ),
            impressive=(
                "MCTS competes with minimax and the report shows how search size and pruning affect strength.",
                [
                    "MCTS and minimax are compared across a fixed tournament.",
                    "Alpha-beta pruning reduces searched positions by a measured amount.",
                    "Difficulty levels change search depth or simulation budget.",
                    "A search visualisation shows the chosen line and pruned branches.",
                ],
            ),
            roles=[
                ("AI engineer", "Shows search algorithms, heuristics and empirical agent comparison."),
                ("Full-stack engineer", "You built the rules engine, agents and a playable browser interface."),
                ("Game developer", "The project combines game state, AI difficulty and interactive UI."),
            ],
            bullets=[
                (
                    "Built minimax and Monte Carlo Tree Search agents for {game} that win {X}% against a random baseline, with alpha-beta pruning reducing search by {Y}%.",
                    "Built minimax and Monte Carlo Tree Search agents for Connect Four that win 96% against a random baseline, with alpha-beta pruning reducing search by 71%.",
                ),
                (
                    "Ran a reproducible tournament that compared win rate, positions searched and time per move.",
                    "Ran a reproducible 1,000-game tournament that compared win rate, positions searched and time per move.",
                ),
                (
                    "Added a browser UI with difficulty levels and a search-tree view.",
                    "Added a browser UI with three difficulty levels and a search-tree view of the chosen and pruned lines.",
                ),
            ],
            interview=[
                (
                    "How does alpha-beta pruning help?",
                    "It skips branches that cannot change the final decision because a better alternative already exists. The move is the same as full minimax, but the search is smaller. I measure the reduction rather than assuming it.",
                ),
                (
                    "Why add Monte Carlo Tree Search?",
                    "MCTS handles large or uncertain search spaces differently: it samples playouts and balances exploration with exploitation. Comparing it with minimax shows the trade-off between heuristic knowledge and simulation.",
                ),
                (
                    "How do you make a fair agent comparison?",
                    "I fix the game, the time or simulation budget, the starting positions and the tournament schedule. Then I report win rate with confidence intervals instead of one lucky match.",
                ),
            ],
            differentiators=[
                "Two search families compared in a reproducible tournament.",
                "Pruning measured, not just claimed.",
                "A playable UI with visible search evidence.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-022",
        title="Traffic Signal Control with Reinforcement Learning",
        summary=(
            "Teach an agent to control traffic lights at an intersection so "
            "vehicles wait less. Start with a simple simulator or the open-source "
            "SUMO traffic simulator, then compare a fixed-timing controller, a "
            "rule-based controller and a reinforcement-learning agent.\n\n"
            "Begin with tabular Q-learning, then try a deep method if the state "
            "space needs it. Test all controllers when the traffic pattern "
            "changes. Report average waiting time, queue length, throughput and "
            "how much of the gain survives the shift.\n\n"
            "Responsible use: simulation only. Estimates can be wrong and are "
            "not a substitute for real traffic-safety systems."
        ),
        who_affected="City traffic engineers, transport researchers, and simulation teams studying congestion.",
        why_matters="Small changes in signal timing affect commute time, emissions and safety across an entire corridor.",
        field="aiml",
        domain="transport",
        difficulty="advanced",
        est_hours=135,
        tech_tags=["python", "reinforcement-learning", "sumo", "q-learning", "simulation", "pandas"],
        datasets=[
            {"name": "SUMO traffic simulator", "url": "https://eclipse.dev/sumo/"},
            {"name": "Open traffic-count data for demand patterns", "url": None},
        ],
        approaches=[
            "Model one intersection as a Markov decision process with a clear reward.",
            "Build fixed-timing and rule-based baselines before training an agent.",
            "Train tabular Q-learning, then compare a deep method if needed.",
            "Evaluate wait time, queue length and throughput under shifted demand.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Simulation only; never connect to live traffic infrastructure.",
        original_text="Train a reinforcement-learning traffic-signal controller in simulation and compare it with fixed and rule-based controllers under shifted demand.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A simulated intersection compares fixed timing with a Q-learning controller on waiting time.",
                [
                    "The environment has a documented state, action and reward.",
                    "A fixed-timing baseline is measured before training.",
                    "Q-learning reduces average waiting time on the training demand.",
                    "Queue length and throughput are reported alongside waiting time.",
                ],
            ),
            impressive=(
                "The agent keeps its gain under changed demand and is compared with a strong rule-based controller.",
                [
                    "A rule-based adaptive controller is included as a stronger baseline.",
                    "The evaluation includes demand patterns not seen during training.",
                    "Reward design choices are ablated and discussed.",
                    "A dashboard shows waiting time, queues and throughput over time.",
                ],
            ),
            roles=[
                ("Reinforcement learning engineer", "Shows MDP formulation, reward design and evaluation against strong baselines."),
                ("Transport modeller", "You can connect a simulator to a learning agent and interpret traffic metrics."),
                ("ML engineer", "The project demonstrates distribution-shift testing, not only training reward."),
            ],
            bullets=[
                (
                    "Trained a reinforcement-learning traffic-signal controller that cut average vehicle waiting time by {X}% versus fixed timing in simulation, and held {Y}% of that gain under shifted traffic.",
                    "Trained a reinforcement-learning traffic-signal controller that cut average vehicle waiting time by 23% versus fixed timing in SUMO, and held 68% of that gain under shifted traffic.",
                ),
                (
                    "Compared Q-learning with fixed and rule-based controllers on waiting time, queue length and throughput.",
                    "Compared Q-learning with fixed and rule-based controllers on waiting time, queue length and throughput across three demand scenarios.",
                ),
                (
                    "Ablated the reward function and showed which terms caused unstable or unfair signal behaviour.",
                    "Ablated the reward function and showed which terms caused unstable switching and long queues on side roads.",
                ),
            ],
            interview=[
                (
                    "How did you formulate the MDP?",
                    "The state includes queue lengths and current phase timing, the action selects the next phase, and the reward combines waiting time with a penalty for excessive switching. I kept the state small enough to inspect.",
                ),
                (
                    "Why compare with a rule-based controller?",
                    "A fixed timer is a weak baseline. A responsive rule-based controller is closer to what a city already uses, so beating it is a more credible result.",
                ),
                (
                    "What happens when traffic patterns change?",
                    "I test on demand patterns not seen in training. A controller that only works on the training pattern has memorised it, not learned a policy.",
                ),
            ],
            differentiators=[
                "Strong fixed and rule-based baselines.",
                "A distribution-shift evaluation.",
                "Reward ablations that explain behaviour, not just a reward curve.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-023",
        title="Molecular Property Prediction: Fingerprints vs Graph Neural Networks",
        summary=(
            "Predict chemical properties such as solubility or toxicity from a "
            "molecule's structure. Build a fingerprint plus random-forest "
            "baseline, then a graph neural network that treats atoms as nodes "
            "and bonds as edges.\n\n"
            "Compare them with a scaffold split, which tests on molecules with "
            "new core structures instead of random ones. Report RMSE or AUROC "
            "under both splits, the performance drop and prediction uncertainty.\n\n"
            "Responsible use: research and education only. Predictions are not "
            "a substitute for laboratory testing or a safety assessment."
        ),
        who_affected="Medicinal chemists, toxicology researchers, and drug-discovery teams prioritising compounds.",
        why_matters="Random splits make models look better than they are, which can send expensive experiments after false leads.",
        field="aiml",
        domain="healthcare",
        difficulty="advanced",
        est_hours=140,
        tech_tags=["python", "rdkit", "graph-neural-networks", "pytorch-geometric", "scikit-learn", "moleculenet"],
        datasets=[
            {"name": "MoleculeNet ESOL and Tox21", "url": "https://moleculenet.org/"},
            {"name": "RDKit cheminformatics toolkit", "url": "https://www.rdkit.org/"},
        ],
        approaches=[
            "Build a fingerprint plus random-forest baseline for each property.",
            "Train a graph neural network on atom and bond features.",
            "Evaluate with random and scaffold splits and compare the drop.",
            "Report calibration or uncertainty alongside the main metric.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Check the licence and intended use of each MoleculeNet dataset.",
        original_text="Compare fingerprint and graph-neural-network models for molecular property prediction under random and scaffold splits.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A fingerprint baseline and a GNN are trained on one property and evaluated on a scaffold split.",
                [
                    "The dataset is split by molecular scaffold, not randomly.",
                    "Both models report RMSE or AUROC on the same test set.",
                    "The performance drop from a random split is measured.",
                    "A note explains that predictions are not lab results.",
                ],
            ),
            impressive=(
                "Two properties are compared, calibration is reported and the report explains when the GNN is worth the complexity.",
                [
                    "Solubility and toxicity tasks use the correct metric for each target.",
                    "Random versus scaffold results are shown side by side.",
                    "Prediction uncertainty or calibration is reported.",
                    "The GNN is compared with the fingerprint baseline on training cost as well as accuracy.",
                ],
            ),
            roles=[
                ("ML engineer", "Shows molecular representations, graph models and why evaluation splits matter."),
                ("Cheminformatics engineer", "You can use RDKit and MoleculeNet to build a reproducible property pipeline."),
                ("Research engineer", "The project reports limitations and calibration instead of a single flattering score."),
            ],
            bullets=[
                (
                    "Built fingerprint and graph-neural-network models for molecular property prediction, showing a {X} point performance drop from random to scaffold splits and reaching {Y} on {dataset}.",
                    "Built fingerprint and graph-neural-network models for molecular property prediction, showing a 19 point performance drop from random to scaffold splits and reaching 0.79 AUROC on Tox21.",
                ),
                (
                    "Compared a random forest baseline with a GNN and documented when the extra complexity paid off.",
                    "Compared a random forest baseline with a GNN and documented the property and data size where the extra complexity paid off.",
                ),
                (
                    "Added calibration reporting so uncertain predictions were visible before experimental follow-up.",
                    "Added calibration reporting so uncertain predictions were visible before experimental follow-up.",
                ),
            ],
            interview=[
                (
                    "Why use a scaffold split?",
                    "Random splits put similar molecules in train and test, so the model can memorise a core structure. A scaffold split tests on new cores and better reflects discovering a new chemical series.",
                ),
                (
                    "When does a GNN beat fingerprints?",
                    "When the learned representation captures local structure that fingerprints miss, and when there is enough data. I report both accuracy and training cost, because a small gain may not justify the complexity.",
                ),
                (
                    "How do you report uncertainty?",
                    "I compare predicted confidence with observed error or use an ensemble spread. The goal is to show which predictions should be checked experimentally first.",
                ),
            ],
            differentiators=[
                "Random versus scaffold evaluation shown side by side.",
                "A strong fingerprint baseline, not only a GNN.",
                "Calibration or uncertainty included in the result.",
            ],
        ),
    ),
    dict(
        source_id="manabi-aiml-resume-024",
        title="Physics Law Discovery from Data",
        summary=(
            "Rediscover equations of motion from data. Simulate or record a "
            "pendulum, spring or predator-prey system, then use sparse "
            "regression such as SINDy to recover the governing differential "
            "equation.\n\n"
            "Test the equation by predicting the future and see how noise "
            "breaks discovery. Compare it with a neural network that fits the "
            "data well but gives no equation. Report coefficient error, "
            "prediction error over time and the noise level where discovery "
            "fails."
        ),
        who_affected="Physics students, computational scientists, and engineers modelling dynamical systems.",
        why_matters="A model that predicts without an equation cannot explain the system or extrapolate as reliably.",
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=105,
        tech_tags=["python", "pysindy", "numpy", "opencv", "system-identification", "physics"],
        datasets=[
            {"name": "PySINDy documentation and examples", "url": "https://pysindy.readthedocs.io/"},
            {"name": "OpenCV for video tracking", "url": "https://opencv.org/"},
        ],
        approaches=[
            "Generate or record trajectories for at least two dynamical systems.",
            "Use sparse regression to recover candidate governing equations.",
            "Test prediction over increasing horizons and sweep noise levels.",
            "Compare the recovered equation with a neural network fit.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML resume project. Simulated systems and your own video tracking are enough.",
        original_text="Recover governing equations from noisy dynamical-system data with sparse regression and compare interpretability with a neural network.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit=_kit(
            mvp=(
                "A simulated system produces a recovered equation that predicts the next interval with a measured error.",
                [
                    "At least one system is generated with a known true equation.",
                    "Sparse regression recovers a readable candidate equation.",
                    "Coefficient error and short-horizon prediction error are reported.",
                    "The UI or notebook shows the true and recovered trajectories.",
                ],
            ),
            impressive=(
                "Discovery is tested under noise across systems and compared with a neural baseline.",
                [
                    "At least two systems are tested, including one recorded from video.",
                    "A noise sweep shows the level where equation discovery fails.",
                    "A neural network is compared on fit and long-horizon extrapolation.",
                    "The report explains why the recovered equation is more useful than a black-box fit.",
                ],
            ),
            roles=[
                ("ML engineer", "Shows system identification, sparse regression and robustness to noise."),
                ("Scientific software engineer", "You can connect simulation, video tracking and equation discovery in one pipeline."),
                ("Research engineer", "The project measures interpretability and extrapolation instead of only training loss."),
            ],
            bullets=[
                (
                    "Recovered governing equations for {N} dynamical systems from noisy data with {X}% coefficient error, and measured the noise level at which discovery breaks down.",
                    "Recovered governing equations for 4 dynamical systems from noisy data with 6.2% coefficient error, and measured the noise level at which discovery breaks down.",
                ),
                (
                    "Compared SINDy with a neural network that fit well but extrapolated worse beyond the observed horizon.",
                    "Compared SINDy with a neural network that fit the training data well but extrapolated worse beyond the observed horizon.",
                ),
                (
                    "Tracked a physical pendulum from video and recovered its governing equation from real measurements.",
                    "Tracked a physical pendulum from video and recovered its governing equation from real measurements rather than only simulation.",
                ),
            ],
            interview=[
                (
                    "Why prefer a discovered equation to a neural network?",
                    "The equation is inspectable and can extrapolate outside the observed range when the assumptions hold. A network fit can be accurate inside the data and fail silently outside it.",
                ),
                (
                    "How does noise break SINDy?",
                    "Derivatives amplify noise. Sparse regression then selects the wrong terms or unstable coefficients. I smooth carefully, sweep noise levels and report the point where recovery fails.",
                ),
                (
                    "How did you validate the recovered equation?",
                    "I compare coefficients with the true simulated values and test prediction over increasing horizons. For a real recording, I compare the trajectory with held-out measurements.",
                ),
            ],
            differentiators=[
                "Recovered equations, not only predictions.",
                "A noise sweep with a documented failure point.",
                "A neural network comparison on extrapolation.",
            ],
        ),
    ),
]


for _problem in PROBLEMS:
    _detail = RESUME_DETAILS.get(_problem["source_id"])
    if _detail is None:
        continue
    _summary = _problem["summary"].rstrip()
    _notice = "\n\nResponsible use:"
    if _notice in _summary:
        _body, _tail = _summary.rsplit(_notice, 1)
        _problem["summary"] = (
            f"{_body.rstrip()}\n\n{_detail['description'].rstrip()}"
            f"{_notice}{_tail}"
        )
    else:
        _problem["summary"] = f"{_summary}\n\n{_detail['description'].rstrip()}"
    _problem["build_guide"] = _detail["build_guide"]


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
