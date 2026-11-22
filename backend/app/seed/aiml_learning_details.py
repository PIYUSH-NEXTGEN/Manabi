"""Learning-only AI/ML briefs, difficulties and concepts.

Thirty learning projects also exist on the resume or hackathon tracks. This
module only defines the sixteen learning-only projects, then records the
difficulty, title and concepts for the full forty-six project learning pack.
"""

_AI_FIELDS = [
    "field",
    "domain",
    "difficulty",
    "est_hours",
    "who_affected",
    "why_matters",
    "tech_tags",
]

LEARNING_ONLY = {
    17: dict(
        title="Dataset Origin Detective",
        summary=(
            "Given an unfamiliar dataset, work out which process most likely produced it: "
            "a mixture of clusters, a linear or nonlinear relationship, a random walk, a "
            "seasonal time series or plain noise. Generate labelled synthetic datasets, "
            "extract statistical features, train a classifier and test how it handles noisy "
            "and mixed cases.\n\n"
            "The point is to make data inspection disciplined. Keep a table of which features "
            "separate which processes, show where the classifier confuses a random walk with "
            "a trend, and explain why the diagnosis changes which model or validation split "
            "you should use."
        ),
        who_affected=(
            "Analysts, students and engineers who inherit datasets without documentation and "
            "need a defensible first look before modelling."
        ),
        why_matters=(
            "Method choice follows the data-generating process. A systematic diagnosis stops "
            "people from applying a seasonal model to noise or a linear model to a threshold "
            "effect."
        ),
        field="aiml",
        domain="ml",
        difficulty="advanced",
        est_hours=45,
        tech_tags=["python", "numpy", "pandas", "scikit-learn", "statsmodels", "matplotlib"],
        datasets=[
            {"name": "Synthetic datasets generated with scikit-learn and statsmodels", "url": None}
        ],
        approaches=[
            "Define a closed list of candidate processes before choosing any features.",
            "Generate many labelled datasets per process with varied noise and sample sizes.",
            "Extract simple statistical features and inspect their class separation.",
            "Stress-test on mixed datasets, then report where the diagnosis is unreliable.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Given an unknown dataset, identify which kind of process most likely produced it: "
            "a mixture of clusters, a linear or nonlinear relationship, a random walk, a "
            "seasonal time series, uniform noise and so on. Generate labelled synthetic "
            "datasets, extract statistical features, train a classifier, and test how well it "
            "handles noisy and mixed cases."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Define the processes worth detecting",
                "summary": "A vague target makes the classifier impossible to evaluate.",
                "steps": [
                    "List each process and write its generating rule in one sentence.",
                    "Include a mixture of clusters, a linear relationship, a nonlinear relationship, a random walk, a seasonal series and uniform noise.",
                    "Decide which confusions are acceptable, such as trend versus random walk.",
                    "Write the diagnosis you would give a user for each process.",
                ],
            },
            {
                "title": "Generate labelled synthetic datasets",
                "summary": "Control the truth so every score has a clear meaning.",
                "steps": [
                    "Set sample size, noise level and random seed for every generated dataset.",
                    "Create several variants per process instead of one fixed example.",
                    "Hold out whole generating configurations to test generalisation.",
                    "Record the generator settings beside each label for later error analysis.",
                ],
            },
            {
                "title": "Extract and inspect statistical features",
                "summary": "Start with features you can explain.",
                "steps": [
                    "Compute simple summaries such as mean, variance, skew and autocorrelation.",
                    "Add trend, seasonality and nearest-neighbour structure measures.",
                    "Plot feature distributions by process before training any classifier.",
                    "Remove features that leak the generator seed or sample size.",
                ],
            },
            {
                "title": "Train and stress-test the classifier",
                "summary": "Accuracy on clean synthetic data is only the start.",
                "steps": [
                    "Train a simple baseline and a tree-based classifier with a fixed split.",
                    "Report the confusion matrix between processes, not just overall accuracy.",
                    "Add noise, missing values and mixed-process datasets and rerun the test.",
                    "Find the smallest changes that cause confident wrong predictions.",
                ],
            },
            {
                "title": "Report a diagnosis with limits",
                "summary": "The useful output is evidence, not a single label.",
                "steps": [
                    "Show the top supporting features for each prediction.",
                    "State which processes the detector cannot separate reliably.",
                    "Explain how the diagnosis affects model and validation choices.",
                    "Publish the generator code and the exact evaluation protocol.",
                ],
            },
        ],
    ),
    22: dict(
        title="Climate-Linked Health Risk Analyzer",
        summary=(
            "Study how heat, air pollution and other climate factors relate to aggregated "
            "health outcomes. Build a supervised model that predicts whether recorded health "
            "events fall into a climate-sensitive category, then compare a simple baseline with "
            "a boosted model and explain which factors matter most.\n\n"
            "The responsible version uses aggregated public data only. Check geographic and "
            "demographic bias, state clearly that correlation is not causation, and present the "
            "output as an educational signal rather than medical advice."
        ),
        who_affected=(
            "Public-health students, analysts and local planners exploring how heat and air "
            "quality coincide with health-service demand."
        ),
        why_matters=(
            "Climate signals can inform planning, but careless analysis can imply causation or "
            "stigmatise a neighbourhood. Aggregate data and explicit bias checks keep the work "
            "honest."
        ),
        field="aiml",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=50,
        tech_tags=["python", "pandas", "scikit-learn", "xarray", "matplotlib", "openaq"],
        datasets=[
            {"name": "ERA5 climate reanalysis", "url": "https://cds.climate.copernicus.eu/"},
            {"name": "OpenAQ air-quality observations", "url": "https://openaq.org/"},
            {"name": "Aggregated public health statistics", "url": None},
        ],
        approaches=[
            "Use aggregated health counts and keep every join at a region-and-period level.",
            "Align climate and health records by place and time before building features.",
            "Compare a transparent baseline with a boosted model and inspect the difference.",
            "Check errors and feature importance across regions and demographic groups.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Study how heat, air pollution and other climate factors relate to health outcomes. "
            "Build a supervised model that predicts whether recorded health events fall into a "
            "climate-sensitive category. Compare simple and boosted models, check for geographic "
            "and demographic bias, and explain which factors matter most."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Scope the question and the data",
                "summary": "Choose one outcome and one climate signal before joining anything.",
                "steps": [
                    "Pick a climate-sensitive outcome that exists in aggregated public data.",
                    "Write the region, time period and unit of analysis before collecting files.",
                    "List the climate and air-quality variables that could plausibly matter.",
                    "Reject any dataset that contains personal records or small unstable cells.",
                ],
            },
            {
                "title": "Build a defensible joined table",
                "summary": "Bad joins create relationships that do not exist.",
                "steps": [
                    "Normalize timestamps and map both sources to the same region identifiers.",
                    "Aggregate to the chosen period and document how missing values were handled.",
                    "Add lagged heat and pollution features only when the delay is plausible.",
                    "Save a data dictionary and a small sample of matched records.",
                ],
            },
            {
                "title": "Model a baseline and a stronger model",
                "summary": "A simple model tells you whether complexity is earning its place.",
                "steps": [
                    "Split by time or region so the test set is not a random row from the same event.",
                    "Train a regularized linear baseline with a small feature set.",
                    "Train a boosted tree model and tune only a few parameters.",
                    "Compare calibration and error rates across regions and groups.",
                ],
            },
            {
                "title": "Investigate bias and explanation",
                "summary": "Correlation is not causation, and model importance is not proof.",
                "steps": [
                    "Report error rates for each region and demographic group available in aggregate data.",
                    "Use permutation importance and simpler partial-effect plots to explain the model.",
                    "Check whether a feature is a proxy for reporting quality or access to care.",
                    "Write the causal limitation beside every interpretation.",
                ],
            },
            {
                "title": "Publish an educational analysis",
                "summary": "Make the limits as visible as the result.",
                "steps": [
                    "Summarize the main relationship with uncertainty and sample sizes.",
                    "Show where the model is weak or the data are sparse.",
                    "Add the health and privacy notices in plain language.",
                    "Release the aggregation and evaluation script, not the raw personal data.",
                ],
            },
        ],
    ),
    26: dict(
        title="House Price Prediction with Explanations",
        summary=(
            "Predict residential prices from location, area, quality and room counts. Start "
            "with a linear baseline, engineer a small set of defensible features, then compare "
            "ensemble and gradient-boosting models. Present each estimate as a range with the "
            "factors that moved it.\n\n"
            "Add prediction intervals, check errors across neighbourhoods and avoid treating the "
            "output as a professional valuation. The explanation and bias check matter as much "
            "as the score. Predictions are estimates with uncertainty, not professional advice."
        ),
        who_affected=(
            "First-time buyers, students and analysts who want to understand what drives a "
            "property estimate instead of accepting a single opaque number."
        ),
        why_matters=(
            "Housing is a large financial decision. A range with reasons and a visible "
            "neighbourhood bias check is more useful than an overconfident point estimate."
        ),
        field="aiml",
        domain="other",
        difficulty="beginner",
        est_hours=24,
        tech_tags=["python", "pandas", "scikit-learn", "matplotlib", "seaborn", "shap"],
        datasets=[
            {"name": "Ames Housing dataset", "url": "https://www.openml.org/d/42165"},
            {
                "name": "Indian city housing dataset with a clear licence",
                "url": None,
            },
        ],
        approaches=[
            "Explore missingness and outliers before engineering price features.",
            "Start with a linear model on a small, interpretable feature set.",
            "Compare tree ensembles and gradient boosting with the same split.",
            "Add prediction intervals and per-row explanations before reporting results.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Predict residential property prices from location, area, quality and room counts. "
            "Compare a linear baseline with ensemble and gradient-boosting models, engineer "
            "features carefully, then add prediction intervals and feature explanations so the "
            "answer is a range with reasons, not one number."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Understand the housing table",
                "summary": "Price datasets hide missingness and rare categories.",
                "steps": [
                    "Profile every column and write down its meaning, unit and missingness.",
                    "Plot the target and remove impossible prices with a documented rule.",
                    "Separate numeric, ordinal and categorical features.",
                    "Hold out a test set before trying any model.",
                ],
            },
            {
                "title": "Build a linear baseline",
                "summary": "A clear baseline exposes whether complexity helps.",
                "steps": [
                    "Impute missing values with a documented, simple strategy.",
                    "Encode categories with a method you can explain.",
                    "Fit a regularized linear model and inspect the largest coefficients.",
                    "Measure MAE and RMSE on the held-out set.",
                ],
            },
            {
                "title": "Compare tree-based models",
                "summary": "Use the same split and report the trade-offs.",
                "steps": [
                    "Train a random forest and a gradient-boosting model with modest tuning.",
                    "Compare error, training time and stability across folds.",
                    "Check errors by price band and neighbourhood.",
                    "Keep the simplest model that wins by a meaningful margin.",
                ],
            },
            {
                "title": "Turn predictions into ranges and reasons",
                "summary": "A point estimate hides the uncertainty users need.",
                "steps": [
                    "Estimate prediction intervals with quantile models or residual calibration.",
                    "Add per-row feature contributions and translate them into plain language.",
                    "Show the estimate as a range with the largest positive and negative drivers.",
                    "Flag rows outside the training range instead of guessing.",
                ],
            },
            {
                "title": "Check bias and report honestly",
                "summary": "Neighbourhood-level errors affect real decisions.",
                "steps": [
                    "Report error by neighbourhood and property type where sample size allows.",
                    "Test whether a proxy feature causes large group-level gaps.",
                    "Write the valuation and uncertainty notice on the results page.",
                    "Publish the split, metrics and known failure cases with the demo.",
                ],
            },
        ],
    ),
    27: dict(
        title="Athlete Testing vs Match Performance",
        summary=(
            "Explore how physical test results such as speed, strength and agility relate to "
            "real match performance, then build models that show which attributes matter for "
            "each position. Keep the target and the features at the same player and match level "
            "so the analysis answers a clear question.\n\n"
            "Small samples make it easy to overfit and overinterpret. Use cross-validation by "
            "player, report uncertainty and avoid concluding causation from correlation."
        ),
        who_affected=(
            "Sports analytics students, coaches and fans who want to separate useful physical "
            "signals from noisy small-sample stories."
        ),
        why_matters=(
            "Player evaluation can affect selection and careers. Careful validation and honest "
            "correlation language keep a learning project from becoming a misleading scouting "
            "tool."
        ),
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=35,
        tech_tags=["python", "pandas", "scikit-learn", "matplotlib", "seaborn", "statsmodels"],
        datasets=[
            {"name": "nflverse open data", "url": "https://nflverse.nflverse.com/"},
            {"name": "Cricsheet ball-by-ball data", "url": "https://cricsheet.org/"},
        ],
        approaches=[
            "Define one performance target and the player population before joining tables.",
            "Aggregate match data to the player-season level to reduce noise.",
            "Group folds by player so the same person never appears in train and test.",
            "Compare position-specific models with a pooled baseline.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Explore how physical test results (speed, strength, agility) relate to real match "
            "performance and build models that show which attributes matter for each position. "
            "Handle small samples carefully, use cross-validation by player, and avoid concluding "
            "causation from correlation."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Define a measurable performance target",
                "summary": "A vague target produces a model nobody can interpret.",
                "steps": [
                    "Choose a target such as matches played, minutes or a position-specific score.",
                    "Write the population, seasons and minimum games required.",
                    "List physical tests that are recorded before or independent of the target.",
                    "State the causal question you are not answering.",
                ],
            },
            {
                "title": "Join tests to match performance",
                "summary": "Player identity and season keys are the main failure points.",
                "steps": [
                    "Normalize player identifiers across test and match sources.",
                    "Aggregate match records to the player-season level.",
                    "Check how many players survive every join and report the loss.",
                    "Create a data dictionary for units and test dates.",
                ],
            },
            {
                "title": "Model with player-aware validation",
                "summary": "Random row splits leak the same athlete into both sides.",
                "steps": [
                    "Build a mean baseline and a simple linear model.",
                    "Add tree-based models only after the baseline is stable.",
                    "Use GroupKFold by player and report fold-to-fold variation.",
                    "Compare pooled and position-specific models.",
                ],
            },
            {
                "title": "Interpret signals without overclaiming",
                "summary": "The model ranks associations; it does not prove training effects.",
                "steps": [
                    "Report coefficients or importances with uncertainty intervals.",
                    "Show the strongest associations separately for each position.",
                    "Check whether results change after removing injured or low-minute players.",
                    "Write a plain-language correlation warning beside the chart.",
                ],
            },
            {
                "title": "Share a reproducible analysis",
                "summary": "A small-sample result needs a visible protocol.",
                "steps": [
                    "Publish the cohort rules, fold assignment and metric definition.",
                    "Add a notebook or script that rebuilds every table.",
                    "List the smallest sample groups and suppress unstable conclusions.",
                    "Close with what a larger or better dataset would change.",
                ],
            },
        ],
    ),
    30: dict(
        title="Gradient Descent Playground: Regression from Scratch",
        summary=(
            "Implement linear and logistic regression with gradient descent in NumPy, using no "
            "ML libraries. Build an interactive view with a loss curve and a decision boundary "
            "that updates each step, then compare every result with scikit-learn and explain the "
            "differences.\n\n"
            "Change the learning rate, feature scaling and regularization to see what breaks and "
            "why. The goal is to understand training rather than to beat a library."
        ),
        who_affected=(
            "Students and career switchers who can call a model but cannot yet explain what "
            "happens inside the training loop."
        ),
        why_matters=(
            "Debugging a real model requires knowing how loss, gradients, scaling and learning "
            "rate interact. Building the loop once makes every later framework less mysterious."
        ),
        field="aiml",
        domain="education",
        difficulty="beginner",
        est_hours=20,
        tech_tags=["python", "numpy", "matplotlib", "jupyter", "scikit-learn"],
        datasets=[
            {"name": "UCI small tabular dataset", "url": "https://archive.ics.uci.edu/"}
        ],
        approaches=[
            "Write the prediction and loss functions before the optimizer.",
            "Derive and implement gradients, then check them numerically.",
            "Standardize features and show what happens when scaling is removed.",
            "Compare coefficients, loss curves and accuracy with scikit-learn.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Implement linear and logistic regression with gradient descent in NumPy, using no "
            "ML libraries. Build an interactive visual (loss curve, and a decision boundary that "
            "updates each step) in a notebook or small web page, then compare with scikit-learn "
            "and explain every difference. Change the learning rate, feature scaling and "
            "regularization to see what breaks and why."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Derive the training loop on paper",
                "summary": "Write the maths before the code.",
                "steps": [
                    "Write the linear prediction and mean-squared-error loss.",
                    "Derive the gradient for each weight and the bias.",
                    "Write the logistic loss and its gradient.",
                    "Decide the stopping rule and what you will log each step.",
                ],
            },
            {
                "title": "Implement NumPy regression",
                "summary": "Keep one clear path from data to update.",
                "steps": [
                    "Implement prediction, loss and gradient as separate functions.",
                    "Add batch gradient descent with a configurable learning rate.",
                    "Check gradients against finite differences.",
                    "Fit a small synthetic line and verify the loss decreases.",
                ],
            },
            {
                "title": "Visualize and break the training",
                "summary": "The failures teach more than the successful run.",
                "steps": [
                    "Plot loss per step for several learning rates.",
                    "Remove feature scaling and record divergence or slow convergence.",
                    "Add L2 regularization and observe coefficient shrinkage.",
                    "Animate the logistic decision boundary during training.",
                ],
            },
            {
                "title": "Compare with scikit-learn",
                "summary": "Explain differences instead of hiding them.",
                "steps": [
                    "Fit the equivalent linear and logistic models in scikit-learn.",
                    "Compare coefficients and predictions with your implementation.",
                    "Account for solver, regularization and convergence differences.",
                    "Document at least one case where the two disagree and why.",
                ],
            },
            {
                "title": "Package the playground",
                "summary": "A short guided notebook is easier to learn from than a library.",
                "steps": [
                    "Add controls for learning rate, scaling and regularization.",
                    "Write short exercises that ask the learner to predict the outcome.",
                    "Include the gradient-check and comparison results.",
                    "Finish with a one-page explanation of every observed failure mode.",
                ],
            },
        ],
    ),
    32: dict(
        title="Hinglish Sentiment Analyzer",
        summary=(
            "Classify the sentiment of mixed Hindi-English text such as 'movie bakwas thi but "
            "songs mast the'. Handle spelling variants of transliterated words, compare a "
            "bag-of-words baseline with a pretrained multilingual model, and analyse where each "
            "approach fails.\n\n"
            "Error analysis is the main deliverable. Group mistakes by sarcasm, slang, spelling "
            "variation and mixed-script input so the limits are visible rather than hidden "
            "inside one accuracy score."
        ),
        who_affected=(
            "Students and developers building sentiment tools for Indian social media, reviews "
            "or support messages where English-only models miss the meaning."
        ),
        why_matters=(
            "Code-mixed text is common, but most tutorials use clean monolingual examples. "
            "Working with Hinglish exposes tokenization and evaluation problems that generalise "
            "to many real products."
        ),
        field="aiml",
        domain="nlp-llm",
        difficulty="beginner",
        est_hours=24,
        tech_tags=["python", "pandas", "scikit-learn", "transformers", "pytorch", "matplotlib"],
        datasets=[
            {
                "name": "SemEval-2020 Task 9 Hinglish sentiment data",
                "url": "https://competitions.codalab.org/competitions/20654",
            },
            {"name": "Small self-labelled Hinglish set", "url": None},
        ],
        approaches=[
            "Profile spelling variants and script mixing before preprocessing.",
            "Start with TF-IDF character and word features plus a linear classifier.",
            "Compare with a multilingual transformer on the same split.",
            "Build an error taxonomy and report examples for each category.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Classify the sentiment of mixed Hindi-English text (Hinglish) such as 'movie bakwas "
            "thi but songs mast the'. Handle spelling variants of transliterated words, compare "
            "a bag-of-words baseline with a pretrained multilingual model, and analyse where each "
            "fails (sarcasm, slang, inconsistent spelling)."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Understand the code-mixed data",
                "summary": "Tokenization assumptions break quickly on Hinglish.",
                "steps": [
                    "Inspect label balance, text length and script mixing.",
                    "Collect common spelling variants for the same Hindi word.",
                    "Identify sarcasm and mixed-sentiment examples in the training set.",
                    "Create a small held-out set you label yourself.",
                ],
            },
            {
                "title": "Build a transparent baseline",
                "summary": "A simple model gives you something to diagnose.",
                "steps": [
                    "Train TF-IDF word features with logistic regression.",
                    "Add character n-grams for transliteration variants.",
                    "Report per-class precision, recall and F1.",
                    "List the most influential n-grams for each class.",
                ],
            },
            {
                "title": "Try a multilingual model",
                "summary": "Use the same split so the comparison is fair.",
                "steps": [
                    "Fine-tune or prompt a pretrained multilingual sentiment model.",
                    "Keep the baseline split and label mapping unchanged.",
                    "Compare accuracy and per-class errors with the baseline.",
                    "Record compute cost and inference latency.",
                ],
            },
            {
                "title": "Analyse errors by category",
                "summary": "The failure groups are more useful than one score.",
                "steps": [
                    "Tag errors as sarcasm, slang, spelling, mixed script or label ambiguity.",
                    "Count each category for both models.",
                    "Pick representative examples and explain the cause.",
                    "Test targeted fixes on the categories they are meant to help.",
                ],
            },
            {
                "title": "Report what the model cannot do",
                "summary": "A sentiment demo needs a visible scope.",
                "steps": [
                    "State the domains and languages represented in training data.",
                    "Show examples that should be sent to human review.",
                    "Publish the split, label rules and error taxonomy.",
                    "Avoid presenting a benchmark score as general Hinglish understanding.",
                ],
            },
        ],
    ),
    34: dict(
        title="Forecasting Basics: Beat the Naive Baseline",
        summary=(
            "Pick a real daily series for your city, such as air quality, temperature or "
            "electricity demand, and learn to forecast it honestly. Split the data by time, "
            "build naive and seasonal-naive baselines, then try moving averages, exponential "
            "smoothing and one machine-learning model.\n\n"
            "Compare MAE for every method and explain when a fancier model actually beats a "
            "simple baseline. Predictions are estimates with uncertainty, not professional "
            "advice."
        ),
        who_affected=(
            "Students and analysts who want a first honest forecasting project using public "
            "city-level data."
        ),
        why_matters=(
            "Most impressive-looking forecasts are just persistence with extra steps. Learning "
            "to beat a baseline prevents wasted complexity and misleading claims."
        ),
        field="aiml",
        domain="climate",
        difficulty="beginner",
        est_hours=20,
        tech_tags=["python", "pandas", "statsmodels", "scikit-learn", "matplotlib"],
        datasets=[
            {"name": "OpenAQ historical air quality", "url": "https://openaq.org/"},
            {
                "name": "Open-Meteo historical weather",
                "url": "https://open-meteo.com/en/docs/historical-weather-api",
            },
        ],
        approaches=[
            "Plot the series and mark gaps before choosing a forecast horizon.",
            "Use a time-ordered split and never shuffle observations.",
            "Build naive and seasonal-naive baselines first.",
            "Compare every model on the same horizon and error metric.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Pick a real daily series for your city (air quality, temperature or electricity "
            "demand) and learn to forecast honestly. Split the data by time, build naive and "
            "seasonal-naive baselines, then try moving averages, exponential smoothing and one "
            "machine-learning model, and compare MAE for each. The lesson is when a fancier "
            "model actually beats a simple baseline."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Inspect the series and define the task",
                "summary": "The horizon and metric decide everything that follows.",
                "steps": [
                    "Plot the full series and mark missing periods or sensor changes.",
                    "Choose a forecast horizon such as the next day or next seven days.",
                    "Write the MAE definition and the units users will see.",
                    "Reserve the final period as a test set before modelling.",
                ],
            },
            {
                "title": "Build honest baselines",
                "summary": "Persistence is a real competitor.",
                "steps": [
                    "Implement a naive forecast that repeats the last observed value.",
                    "Implement a seasonal-naive forecast using the same weekday or season.",
                    "Score both baselines on the held-out period.",
                    "Write down why the series might defeat each baseline.",
                ],
            },
            {
                "title": "Add smoothing and a learned model",
                "summary": "Complexity must earn its place on the same test.",
                "steps": [
                    "Try moving averages and exponential smoothing with a small parameter search.",
                    "Create lag and calendar features for one machine-learning model.",
                    "Use walk-forward validation instead of a random split.",
                    "Compare every method with the baseline MAE.",
                ],
            },
            {
                "title": "Analyse errors and uncertainty",
                "summary": "A forecast without error context is hard to trust.",
                "steps": [
                    "Plot errors over time and look for regime changes.",
                    "Report error by season, weekday and pollution or weather event.",
                    "Add a simple prediction interval from residual errors.",
                    "Explain which method wins and on which periods.",
                ],
            },
            {
                "title": "Publish the forecast notebook",
                "summary": "The baseline lesson is the main result.",
                "steps": [
                    "Show the split, horizon and metric in one place.",
                    "Include the baseline table even if a complex model wins.",
                    "Display the forecast as an estimate with uncertainty.",
                    "Add a short note on data source terms and sensor reliability.",
                ],
            },
        ],
    ),
    35: dict(
        title="Recommender from Scratch: Content-Based vs Collaborative",
        summary=(
            "Build a movie or book recommender two ways: content-based, using similar "
            "descriptions, and collaborative filtering, using similar users. Compare them with "
            "precision@k on held-out ratings and explain every recommendation in one line.\n\n"
            "Study the cold-start problem with new users and new items. The comparison matters "
            "more than the leaderboard: each method fails in a different situation."
        ),
        who_affected=(
            "Students learning recommendation systems and developers who need a transparent "
            "baseline before reaching for a library."
        ),
        why_matters=(
            "Recommenders shape what people discover. Building both families from scratch makes "
            "their biases and cold-start limits visible."
        ),
        field="aiml",
        domain="ml",
        difficulty="beginner",
        est_hours=24,
        tech_tags=["python", "pandas", "numpy", "scikit-learn", "scipy", "matplotlib"],
        datasets=[
            {
                "name": "MovieLens latest small dataset",
                "url": "https://grouplens.org/datasets/movielens/",
            }
        ],
        approaches=[
            "Build a user-item matrix and hold out ratings per user.",
            "Score content similarity from item text or genres.",
            "Score collaborative similarity from co-rated items.",
            "Evaluate both with precision@k and a cold-start simulation.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Build a movie or book recommender two ways, content-based (similar descriptions) "
            "and collaborative filtering (similar users), and compare them with precision@k on "
            "held-out ratings. Study the cold-start problem with new users and add a one-line "
            "explanation for each recommendation."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Shape the ratings problem",
                "summary": "Hold out future preferences, not random interactions.",
                "steps": [
                    "Load ratings and item metadata into a clean table.",
                    "Hold out a fixed number of recent ratings per user.",
                    "Define what counts as a relevant recommendation for precision@k.",
                    "Record the sparsity and popularity distribution.",
                ],
            },
            {
                "title": "Build content-based recommendations",
                "summary": "Similar descriptions are useful when ratings are sparse.",
                "steps": [
                    "Turn genres or descriptions into a simple feature matrix.",
                    "Compute item-to-item similarity.",
                    "Score unseen items for each user and return the top k.",
                    "Add one line explaining which similar items drove the result.",
                ],
            },
            {
                "title": "Build collaborative filtering",
                "summary": "Similar users carry information descriptions cannot.",
                "steps": [
                    "Build the user-item rating matrix with missing values handled explicitly.",
                    "Compute user or item similarity on co-rated entries.",
                    "Score unseen items and rank them for each user.",
                    "Explain the recommendation through the nearest users or items.",
                ],
            },
            {
                "title": "Evaluate and study cold start",
                "summary": "A new user has no ratings and changes the game.",
                "steps": [
                    "Compare both methods with precision@k on the held-out ratings.",
                    "Simulate a new user and a new item with no interactions.",
                    "Measure how each method behaves before and after a few ratings.",
                    "Identify the popularity bias in the collaborative results.",
                ],
            },
            {
                "title": "Report the trade-offs",
                "summary": "The best method depends on the situation.",
                "steps": [
                    "Show a side-by-side table of quality, coverage and cold-start behaviour.",
                    "Include example recommendations with their explanations.",
                    "State when a hybrid would be the sensible next step.",
                    "Publish the split and evaluation code for reproducibility.",
                ],
            },
        ],
    ),
    36: dict(
        title="Messy Data Doctor",
        summary=(
            "Upload a CSV and get an automatic data-quality report: missing values, duplicates, "
            "outliers, wrong data types, inconsistent spellings in category columns and columns "
            "that leak the target. Suggest fixes, apply them with an undo log, and show "
            "before-and-after summaries.\n\n"
            "Use synthetic, public or consented data only. The project is a lesson in why data "
            "quality decides model quality, so every suggested fix should be inspectable and "
            "reversible."
        ),
        who_affected=(
            "Students, analysts and small teams who receive spreadsheets from many sources and "
            "need a repeatable first-pass quality check."
        ),
        why_matters=(
            "Most modelling failures start in the table. A visible report and reversible "
            "cleaning steps make bad data easier to discuss before it reaches a model."
        ),
        field="aiml",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=28,
        tech_tags=["python", "pandas", "streamlit", "pytest", "plotly"],
        datasets=[
            {"name": "Messy public table from an open-data portal", "url": None}
        ],
        approaches=[
            "Profile the table before changing any value.",
            "Separate detection rules from the actions that repair data.",
            "Store every change in an undo log with a before and after value.",
            "Show before-and-after summaries beside the cleaning controls.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Upload a CSV and get an automatic data-quality report: missing values, duplicates, "
            "outliers, wrong data types, inconsistent spellings in category columns, and columns "
            "that leak the target. Suggest fixes, apply them with an undo log, and show "
            "before-and-after summaries."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Define the quality checks",
                "summary": "A report is only useful if each check is specific.",
                "steps": [
                    "List the checks for missingness, duplicates, types, outliers and categories.",
                    "Write the exact rule that triggers each warning.",
                    "Define how to detect a possible target-leakage column.",
                    "Separate errors from warnings so users can prioritise.",
                ],
            },
            {
                "title": "Profile an uploaded table",
                "summary": "Read the file without silently changing it.",
                "steps": [
                    "Parse the CSV with explicit encoding and type handling.",
                    "Compute column summaries and missingness counts.",
                    "Detect duplicate rows and near-duplicate category spellings.",
                    "Render the report in a small local web app.",
                ],
            },
            {
                "title": "Suggest reversible fixes",
                "summary": "Cleaning should never be a one-way door.",
                "steps": [
                    "Generate a proposed action for each warning.",
                    "Apply one action at a time and record the affected rows.",
                    "Store old and new values in an undo log.",
                    "Allow the user to revert any action and recompute the report.",
                ],
            },
            {
                "title": "Show before and after",
                "summary": "The user must be able to judge the change.",
                "steps": [
                    "Display summary statistics before and after each fix.",
                    "Highlight the rows that changed.",
                    "Warn when a fix removes a large share of the data.",
                    "Export the cleaned table and the change log together.",
                ],
            },
            {
                "title": "Test with deliberately messy files",
                "summary": "Synthetic tables let you test every rule safely.",
                "steps": [
                    "Create fixtures for each quality problem.",
                    "Test that detection fires only when it should.",
                    "Test that undo restores the original table exactly.",
                    "Add the privacy notice and reject files containing personal data in the demo.",
                ],
            },
        ],
    ),
    38: dict(
        title="Decision Trees & Random Forests from Scratch",
        summary=(
            "Implement a CART decision tree with Gini and entropy splits, depth limits and "
            "pruning, then add bagging and random feature selection to build a random forest. "
            "Use only plain Python or NumPy for the model.\n\n"
            "Compare accuracy and speed with scikit-learn, and add feature importance plus a "
            "printable rule view so the model can explain itself. The point is to understand "
            "overfitting and why many weak trees work together."
        ),
        who_affected=(
            "Students and developers who use tree ensembles but want to understand the split, "
            "pruning and bagging steps inside them."
        ),
        why_matters=(
            "Trees are common in high-stakes tabular work. Knowing how they overfit and why "
            "ensembling helps makes model review much more useful."
        ),
        field="aiml",
        domain="education",
        difficulty="intermediate",
        est_hours=40,
        tech_tags=["python", "numpy", "scikit-learn", "pytest", "matplotlib"],
        datasets=[
            {
                "name": "UCI Iris, Wine and Breast Cancer Wisconsin datasets",
                "url": "https://archive.ics.uci.edu/",
            }
        ],
        approaches=[
            "Write impurity and split search tests before building the full tree.",
            "Implement depth limits and pruning as separate, testable rules.",
            "Add bootstrap sampling and random feature subsets for the forest.",
            "Compare with scikit-learn and export a human-readable rule tree.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Implement a decision tree (CART) with Gini and entropy splits, depth limits and "
            "pruning, then bagging and random feature selection to make a random forest, using "
            "only plain Python or NumPy. Compare with scikit-learn on accuracy and speed, and "
            "add feature importance and a printable rule view so the model can explain itself."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Implement impurity and split search",
                "summary": "The split rule is the core of the tree.",
                "steps": [
                    "Implement Gini impurity and entropy with unit tests on hand-worked examples.",
                    "Enumerate candidate thresholds for one numeric feature.",
                    "Score each split by weighted child impurity.",
                    "Choose the best split and record why ties are broken deterministically.",
                ],
            },
            {
                "title": "Grow and prune a tree",
                "summary": "A tree can fit noise perfectly if you let it.",
                "steps": [
                    "Build recursive nodes with a maximum depth and minimum leaf size.",
                    "Add a stopping rule for pure or tiny leaves.",
                    "Implement a simple pruning pass and compare validation scores.",
                    "Print the learned rules as nested if statements.",
                ],
            },
            {
                "title": "Build a random forest",
                "summary": "Many weak, decorrelated trees beat one deep tree.",
                "steps": [
                    "Sample rows with replacement for each tree.",
                    "Sample a random subset of features at every split.",
                    "Aggregate predictions across trees.",
                    "Measure the effect of tree count and feature subset size.",
                ],
            },
            {
                "title": "Compare with scikit-learn",
                "summary": "Match its protocol before comparing scores.",
                "steps": [
                    "Use the same train and test split for both implementations.",
                    "Compare accuracy, training time and prediction time.",
                    "Add permutation or impurity-based feature importance.",
                    "Explain any gap through differences in stopping or split rules.",
                ],
            },
            {
                "title": "Teach the result",
                "summary": "A readable rule view makes the model inspectable.",
                "steps": [
                    "Show one shallow tree as printable rules.",
                    "Include a chart of accuracy versus depth to show overfitting.",
                    "Add a short explanation of bagging and feature randomness.",
                    "Publish the tests and a reproducible benchmark script.",
                ],
            },
        ],
    ),
    46: dict(
        title="Matchbox Machine: Teach Tic-Tac-Toe with Beads",
        summary=(
            "Rebuild Donald Michie's 1961 matchbox machine in plain Python. Every board "
            "position gets a small box that holds one bead per legal move. To play, shake "
            "the box for the current position and take out a random bead: that bead is "
            "your move. After the game, add beads to the boxes that produced winning moves "
            "and remove beads from the boxes that lost. You never write down a strategy; "
            "the bead counts become the strategy.\n\n"
            "The first version plays badly. Play 1,000 games against a random opponent, plot "
            "the win and draw rate every 50 games, and watch the curve climb. Then open a "
            "few boxes and compare their beads with the moves a perfect player would make. "
            "Where the machine still loses, you can usually spot the extra beads that keep "
            "it on that move, which is a clearer picture of reinforcement learning than any "
            "diagram."
        ),
        who_affected=(
            "Students who want to see a machine learn from wins and losses alone, with no "
            "maths library, no model file and no training loop beyond a few dozen lines."
        ),
        why_matters=(
            "Reinforcement learning is usually taught inside a deep-learning framework, which "
            "hides the basic idea. Here the whole learning rule is one function, and every "
            "decision the program makes can be traced back to a bead count you can read."
        ),
        field="aiml",
        domain="ml",
        difficulty="beginner",
        est_hours=10,
        tech_tags=["python", "matplotlib", "pytest"],
        datasets=[
            {
                "name": (
                    "None. The program learns from games it plays against itself or against "
                    "a random player."
                ),
                "url": None,
            }
        ],
        approaches=[
            "Encode each board position as a short string so boxes can be stored in a dictionary.",
            "Start against a random opponent, before adding anything clever, to keep a baseline.",
            "Apply the bead update after every game and log the win rate as you go.",
            "Open single boxes to explain, in words, why the machine picked one move over another.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Recreate Donald Michie's 1961 matchbox machine in Python. Each board position "
            "holds a set of beads (moves). A move is picked at random, and beads are added "
            "after a win and removed after a loss, so the program slowly learns to play. "
            "Plot its win rate over 1,000 games and watch it improve."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Build the board and the rules",
                "summary": "Get a correct, testable tic-tac-toe engine before any learning.",
                "steps": [
                    "Write the board as nine cells and a function that lists the legal moves.",
                    "Add win detection for rows, columns and both diagonals, with a test per case.",
                    "Add a player that always picks a legal move at random, so you have an opponent.",
                    "Print the board in the terminal so you can follow a game by hand.",
                ],
            },
            {
                "title": "Make the boxes and hold the beads",
                "summary": "The bead counts are the entire memory of the machine.",
                "steps": [
                    "Key each box by the board position plus whose turn it is.",
                    "Start every legal move with the same number of beads, for example four.",
                    "Write a function that draws one bead at random and updates the box.",
                    "Save and load the box contents in a JSON file so training is not lost.",
                ],
            },
            {
                "title": "Play games and update the beads",
                "summary": "One game should teach the machine something every time.",
                "steps": [
                    "Record the box and move used at each turn of a game.",
                    "After a win, add a bead to each move on the winning path.",
                    "After a loss, remove one bead at random from the losing path.",
                    "Refill an empty box with the starting count so the machine never gets stuck.",
                ],
            },
            {
                "title": "Plot the learning curve",
                "summary": "A chart over many games is the only fair claim of progress.",
                "steps": [
                    "Write win, draw and loss counts for every 50 games to a CSV file.",
                    "Plot wins and draws against games played and smooth the line.",
                    "Run the same setup against itself and compare the shape of the curve.",
                    "Note the games it still loses and check whether those boxes look odd.",
                ],
            },
            {
                "title": "Compare with a perfect player",
                "summary": "A machine that stops losing is the real result.",
                "steps": [
                    "Add a small minimax player that never loses.",
                    "Check that the learned machine draws often instead of dropping games.",
                    "Open five boxes and read the bead counts that shape its first move.",
                    "Write a README that explains the update rule in plain words.",
                ],
            },
        ],
    ),
    47: dict(
        title="Doodle Recognizer: Guess the Sketch",
        summary=(
            "Draw with a mouse or a finger on a web canvas and have a model name what you "
            "drew, using ten categories such as cat, house, bicycle, tree, pizza and "
            "umbrella. Google's Quick, Draw! data ships thousands of finished sketches per "
            "category as stroke lists, so you can spend your time on the model instead of on "
            "collecting images.\n\n"
            "Start with a simple baseline, then train something a little stronger and compare "
            "the two. The most useful output is the confusion matrix. The model confuses a house "
            "with a tree, or a clock with a pizza, for reasons you can see in the drawings, and "
            "fixing one of those confusions teaches you more than adding two points of accuracy."
        ),
        who_affected=(
            "Beginners who want a first image project that ends in something a friend can "
            "open in a browser and try with their own doodle."
        ),
        why_matters=(
            "Image classification is easier to learn when you can draw your own test case and "
            "watch the model get it wrong. Training splits, class balance and error analysis "
            "stop being abstract words once your own sketch is in the test set."
        ),
        field="aiml",
        domain="computer-vision",
        difficulty="beginner",
        est_hours=12,
        tech_tags=["python", "numpy", "scikit-learn", "pillow", "streamlit"],
        datasets=[
            {
                "name": "Quick, Draw! dataset (Creative Commons, check the terms)",
                "url": "https://github.com/googlecreativelab/quickdraw-dataset",
            }
        ],
        approaches=[
            "Download the simplified stroke files for ten categories only, so the data fits on a laptop.",
            "Draw each stroke list onto a fixed-size greyscale image that any model can read.",
            "Measure a simple baseline first, then compare one stronger model against it.",
            "Read the confusion matrix and describe the mistakes in words, not just numbers.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Draw on a web canvas and the model guesses what you drew, using 10 categories "
            "such as cat, house and bicycle. Then find out which doodles it confuses."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Pick ten categories and look at them",
                "summary": "Choose classes you can tell apart, then check that people can too.",
                "steps": [
                    "Pick ten categories and note how each one is usually drawn.",
                    "Download a few thousand sketches per category, not the whole dataset.",
                    "Render fifty random sketches and look at them before writing any code.",
                    "Drop a category that turns out to overlap heavily with another one.",
                ],
            },
            {
                "title": "Turn strokes into images",
                "summary": "One clear input format keeps the model simple.",
                "steps": [
                    "Scale every stroke list into a 64 by 64 box without changing its shape.",
                    "Draw the strokes as a line image and save it as a greyscale picture.",
                    "Check a sample by eye to confirm the scaling is not clipping corners.",
                    "Split the data into train, validation and test sets before training.",
                ],
            },
            {
                "title": "Beat a baseline",
                "summary": "A simple model gives every later score a meaning.",
                "steps": [
                    "Train the simplest model you can think of and record its accuracy.",
                    "Train one stronger model with the same split and the same categories.",
                    "Compare accuracy and training time side by side.",
                    "Only then start tuning, one setting at a time and with a reason.",
                ],
            },
            {
                "title": "Read the confusion matrix",
                "summary": "The wrong answers carry the lesson.",
                "steps": [
                    "Print the full confusion matrix for the test set.",
                    "Find the three most common mistakes and look at real examples of each.",
                    "Write one sentence per mistake explaining the likely cause.",
                    "Fix one cause, retrain, and report whether that cell improved.",
                ],
            },
            {
                "title": "Put a canvas in front of it",
                "summary": "A live demo shows the honest failure rate.",
                "steps": [
                    "Add a small web page with a drawing canvas and a clear button.",
                    "Send the drawn strokes through the same image conversion the model was trained on.",
                    "Show the top three guesses with their confidence.",
                    "Ask a few people to try it and note the doodles it mishandles.",
                ],
            },
        ],
    ),
    48: dict(
        title="Is It Legendary? A Pokemon Stats Classifier",
        summary=(
            "Predict whether a Pokemon is legendary from its stats and types alone. The data "
            "comes from PokeAPI and fits in a single file, so the whole project is about the "
            "modelling rather than the data plumbing.\n\n"
            "Legendary Pokemon are a small share of the list, which makes this a neat first "
            "look at imbalanced classes. A model that always answers no looks accurate and is "
            "useless, so you have to pick a better measure and explain why. Finish by drawing "
            "the decision tree as a picture and reading out the rules it found: a handful of "
            "stats usually do all the work."
        ),
        who_affected=(
            "Beginners who like games and want a classification project where the data is "
            "small enough to understand row by row."
        ),
        why_matters=(
            "Most real classifiers face rare positive cases: fraud, faults, disease. A toy "
            "problem with rare legendaries makes the same trap visible in an afternoon."
        ),
        field="aiml",
        domain="ml",
        difficulty="beginner",
        est_hours=8,
        tech_tags=["python", "pandas", "scikit-learn", "requests", "matplotlib"],
        datasets=[
            {
                "name": "PokeAPI (free, cache the responses and follow its fair-use rules)",
                "url": "https://pokeapi.co/",
            }
        ],
        approaches=[
            "Download each Pokemon once, cache it on disk, then work offline from a CSV.",
            "Check the class balance before choosing any measure of success.",
            "Compare a baseline that always says no with a real classifier.",
            "Draw the tree and translate its branches into plain sentences.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Predict whether a Pokemon is legendary from its stats and types. Draw the "
            "decision tree and read what it learned."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Collect and cache the data",
                "summary": "Small data problems still deserve a tidy pipeline.",
                "steps": [
                    "Fetch the Pokemon list, then each record, and save the raw JSON to disk.",
                    "Follow the API's fair-use rules: one request at a time, with a short pause.",
                    "Flatten the useful fields into a table and save it as a CSV.",
                    "Re-run the script offline from the cache so later runs cost nothing.",
                ],
            },
            {
                "title": "Look at the class balance",
                "summary": "A rare class changes which number matters.",
                "steps": [
                    "Count legendary and non-legendary rows and write the ratio down.",
                    "Train a model that always answers no and record its accuracy.",
                    "Explain in your notes why that score is not useful here.",
                    "Choose measures such as precision, recall and F1 for a rare class.",
                ],
            },
            {
                "title": "Train and read a tree",
                "summary": "A shallow tree is a set of rules you can argue with.",
                "steps": [
                    "Split the data into train and test sets and keep the split fixed.",
                    "Train a decision tree with a small depth limit so it stays readable.",
                    "Plot the tree and read each rule out loud in plain English.",
                    "Check whether the rules make sense against what you know about the games.",
                ],
            },
            {
                "title": "Handle the rare class properly",
                "summary": "Same data, different weighting, different trade-off.",
                "steps": [
                    "Retrain with class weights and compare precision and recall.",
                    "Look at which legendaries the model misses most often.",
                    "Try a second model family and say which errors you would rather have.",
                    "Report every number on the test set only, never on the training set.",
                ],
            },
            {
                "title": "Write the findings",
                "summary": "A short honest write-up beats a big accuracy claim.",
                "steps": [
                    "State the class ratio and the baseline score in the first paragraph.",
                    "Show the tree picture and name the two or three stats that matter.",
                    "List the Pokemon the model gets most wrong and guess why.",
                    "Mention that stats alone cannot capture how a game actually plays.",
                ],
            },
        ],
    ),
    49: dict(
        title="Which Chess Player Are You? Clustering Playing Styles",
        summary=(
            "Group chess players by how they play rather than by how well they play. From "
            "Lichess open games you can build simple features per player: average game length, "
            "how often the game ends in a capture, preferred openings, early queen moves and "
            "time per move. Run k-means on those features and see whether the clusters look "
            "like real styles: aggressive attackers, solid grinders, endgame specialists.\n\n"
            "The hard part is not the clustering, it is deciding whether the groups mean "
            "anything. Use the silhouette score, rename the clusters by hand, and check whether "
            "one cluster is only beginners. Then put your own games through the same pipeline "
            "and see which group they land in, along with the players it sits closest to."
        ),
        who_affected=(
            "Students who play chess and want a first unsupervised project with data they "
            "already care about."
        ),
        why_matters=(
            "Clustering always returns groups, even on random numbers. Learning to test whether "
            "the groups are real is the skill that carries over to every analysis job."
        ),
        field="aiml",
        domain="ml",
        difficulty="beginner",
        est_hours=10,
        tech_tags=["python", "pandas", "scikit-learn", "python-chess", "matplotlib"],
        datasets=[
            {
                "name": "Lichess open database (CC0, one monthly file is plenty)",
                "url": "https://database.lichess.org/",
            }
        ],
        approaches=[
            "Use one month of games, or your own export, and keep only players with enough games.",
            "Turn each game into per-player numbers before averaging them by player.",
            "Scale the features and try several cluster counts instead of trusting the first answer.",
            "Judge the result with a silhouette score and a human look at sample players.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Group players into styles (aggressive, solid, endgame specialist) using stats "
            "like game length, openings and captures per game, then see which cluster your "
            "own games land in."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Load a month of games",
                "summary": "Big files are fine if you never load them whole.",
                "steps": [
                    "Download one monthly archive and read it one game at a time.",
                    "Keep only finished games with a rating on both sides.",
                    "Store a small clean table instead of the raw moves for every game.",
                    "Note how many games you dropped and why.",
                ],
            },
            {
                "title": "Build features that describe style",
                "summary": "Clustering is only as meaningful as its features.",
                "steps": [
                    "Compute per game: number of moves, captures, checks and game length in seconds.",
                    "Count how often each player's opening appears in the sample.",
                    "Average the game numbers per player, keeping players with ten games or more.",
                    "Write one sentence per feature explaining what it should capture.",
                ],
            },
            {
                "title": "Cluster and test the result",
                "summary": "Try more than one answer before believing any of them.",
                "steps": [
                    "Scale the features so a long game does not dominate everything.",
                    "Run k-means for three to six clusters and record the silhouette score.",
                    "Check whether one cluster is simply low-rated players.",
                    "Plot the clusters on two features you can actually explain.",
                ],
            },
            {
                "title": "Name the styles from examples",
                "summary": "A label only counts if you can point at players behind it.",
                "steps": [
                    "Print ten random players from each cluster with their averages.",
                    "Look up two of them and see whether the label fits.",
                    "Rename each cluster in plain words, or merge the ones that look the same.",
                    "Show the most common opening in each cluster.",
                ],
            },
            {
                "title": "Place your own games",
                "summary": "The personal test exposes how thin the features are.",
                "steps": [
                    "Export your own games and compute the same features.",
                    "Assign yourself to a cluster and say whether the label feels right.",
                    "Compare your distance to the cluster centre with a typical player's.",
                    "Write down what the features cannot see, such as tactical accuracy.",
                ],
            },
        ],
    ),
    50: dict(
        title="Analyse Your Own Life: A Small Personal Dashboard",
        summary=(
            "Track four numbers for three or four weeks: sleep hours, study hours, steps and "
            "mood from 1 to 5. Then ask the ordinary questions. Do I sleep better on days I "
            "move more? Do late nights drag my mood down two days later? A spreadsheet and a "
            "notebook are enough; the project is about asking carefully, not about tools.\n\n"
            "With 28 days of data, almost every pattern can be luck. That is the lesson. Build "
            "the charts, run a simple regression, and then state plainly how much you cannot "
            "conclude. Keep the data on your own machine, use no names and no health records, "
            "and say clearly what a bigger sample would need to show."
        ),
        who_affected=(
            "Anyone who wants to practise data analysis but does not have a dataset they care "
            "about yet."
        ),
        why_matters=(
            "Small personal samples are where bad reasoning starts, because the first chart "
            "always looks convincing. Practising the careful version on your own numbers is "
            "cheaper than learning it on someone else's data later."
        ),
        field="aiml",
        domain="social-impact",
        difficulty="beginner",
        est_hours=6,
        tech_tags=["python", "pandas", "matplotlib", "jupyter", "scipy"],
        datasets=[
            {
                "name": "Your own daily numbers, kept local and private",
                "url": None,
            }
        ],
        approaches=[
            "Decide what to record and at what time of day, then keep the sheet boring and regular.",
            "Plot each variable against time before computing anything between variables.",
            "Use lagged days to test whether a change comes before or after another change.",
            "Report uncertainty openly, with the sample size next to every claim.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Track a few things for 3 to 4 weeks in a spreadsheet (sleep hours, study hours, "
            "steps, mood from 1 to 5), then explore which patterns show up. Do you sleep better "
            "after exercise? Do late nights lower your mood?"
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Choose a few things and log them",
                "summary": "Consistency matters more than the size of the sheet.",
                "steps": [
                    "Pick four numbers you can record in under a minute each day.",
                    "Fix the time of day for each entry so the numbers mean the same thing.",
                    "Note missing days honestly instead of filling them in later.",
                    "Keep the file local and store no names, locations or health details.",
                ],
            },
            {
                "title": "Look at each variable alone",
                "summary": "Before pairing variables, learn each one's shape.",
                "steps": [
                    "Plot each variable against the day number.",
                    "Mark obvious events such as travel, exams or illness on the timeline.",
                    "Note the range and any days that look like entry mistakes.",
                    "Check whether a trend exists before reading anything into a pairing.",
                ],
            },
            {
                "title": "Compare pairs and lags",
                "summary": "Timing decides how a relationship should be read.",
                "steps": [
                    "Scatter one variable against another and count your points.",
                    "Test same-day, next-day and two-day-later pairings.",
                    "Compute a simple correlation with its confidence interval.",
                    "List other explanations for the same pattern, such as weekends or study load.",
                ],
            },
            {
                "title": "Fit something simple and be honest",
                "summary": "A regression on 28 points is a starting estimate, not a finding.",
                "steps": [
                    "Fit a straight line for one clear question and plot the line over the points.",
                    "Report the slope with its interval, not just a single number.",
                    "Say out loud that correlation is not causation for every claim you keep.",
                    "Calculate how many days a stronger claim would need.",
                ],
            },
            {
                "title": "Make the dashboard useful",
                "summary": "A small set of charts should answer the questions you actually had.",
                "steps": [
                    "Build one page with four small charts and the sample size on each.",
                    "Add a short note under every chart saying what it cannot show.",
                    "Keep the file private and add it to your ignore list before sharing anything.",
                    "Write a closing page of what you would track next time.",
                ],
            },
        ],
    ),
    51: dict(
        title="Music Genre Detective: Guess the Genre from a Clip",
        summary=(
            "Predict a track's genre from a 30-second clip. The audio never goes into the "
            "model directly: you turn each clip into numbers such as MFCCs, tempo and spectral "
            "contrast, then classify the features. The Free Music Archive's small set gives you "
            "eight balanced genres, which is close to the classic teaching example.\n\n"
            "Compare a nearest-neighbour model with logistic regression and look closely at "
            "where they disagree. Rock and metal get mixed up, and so do pop and electronic, "
            "for reasons you can hear once you know them. The project ends where it should: "
            "with a chart of the mistakes and a short explanation of why the features cannot "
            "separate those pairs."
        ),
        who_affected=(
            "Students who want to work with sound but do not want to train a large model on a "
            "laptop."
        ),
        why_matters=(
            "Audio features are a good lesson in representation: the same clip becomes easy or "
            "hard to classify depending on how you describe it. That idea returns in every "
            "field, from text to images."
        ),
        field="aiml",
        domain="ml",
        difficulty="beginner",
        est_hours=14,
        tech_tags=["python", "librosa", "numpy", "scikit-learn", "matplotlib"],
        datasets=[
            {
                "name": (
                    "Free Music Archive small dataset (each track has its own Creative Commons "
                    "licence, check before sharing clips)"
                ),
                "url": "https://github.com/mdeff/fma",
            }
        ],
        approaches=[
            "Slice each track into fixed clips and keep the genre label with every slice.",
            "Extract a small, explainable set of audio features per clip.",
            "Train two simple models with the same split and compare their errors.",
            "Group the confusion by genre pair and explain each pair with what the features measure.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML learning project.",
        original_text=(
            "Predict a track's genre from 30-second clips by turning audio into features such "
            "as MFCCs, then look at why rock and metal, or pop and electronic, get mixed up."
        ),
        ai_fields=_AI_FIELDS,
        build_guide=[
            {
                "title": "Get the clips and their labels",
                "summary": "A clean label table is half the project.",
                "steps": [
                    "Download the small audio set and its metadata table.",
                    "Read the licence notes and keep the clips for personal study only.",
                    "Cut each track into 30-second pieces and drop the ones that are mostly silence.",
                    "Check that every genre has a similar number of clips.",
                ],
            },
            {
                "title": "Turn sound into numbers",
                "summary": "You cannot classify a waveform; you classify a summary of it.",
                "steps": [
                    "Load each clip at a fixed sample rate and check the duration.",
                    "Compute MFCCs, tempo, spectral contrast and a few zero-crossing statistics.",
                    "Average each feature over the clip and store one row per clip.",
                    "Listen to two clips with very different feature values and confirm the numbers match your ears.",
                ],
            },
            {
                "title": "Train two simple models",
                "summary": "Two cheap models show more than one tuned model.",
                "steps": [
                    "Scale the features and make a single fixed train and test split.",
                    "Train a nearest-neighbour classifier as the baseline.",
                    "Train logistic regression on the same features and split.",
                    "Record accuracy and per-genre precision and recall for both.",
                ],
            },
            {
                "title": "Study the confusion",
                "summary": "The mixed-up genres tell you what the features miss.",
                "steps": [
                    "Print the confusion matrix for both models side by side.",
                    "Name the three most confused genre pairs.",
                    "Listen to two misclassified clips per pair and describe the overlap.",
                    "Explain which feature fails to separate them and why.",
                ],
            },
            {
                "title": "Build a genre meter",
                "summary": "A probability view makes the uncertainty visible.",
                "steps": [
                    "Add a small script that takes one clip and prints genre probabilities.",
                    "Show the top three genres instead of only the best guess.",
                    "Try a clip you recorded yourself and check the confidence.",
                    "Write a short note on which genres this approach should never be trusted with.",
                ],
            },
        ],
    ),
}

LEARNING_CONCEPTS = {
    1: [
        "Text features for suspicious wording",
        "Imbalanced classification",
        "Graph features from reviewer behaviour",
        "Explainable trust scores",
    ],
    4: [
        "Multimodal features from text and images",
        "Gradient boosting for price prediction",
        "MAE and SMAPE for skewed targets",
        "Feature attribution",
    ],
    7: [
        "Schema-constrained extraction",
        "Confidence handling",
        "Human-in-the-loop review",
        "Structured output validation",
    ],
    8: [
        "Transfer learning",
        "Confusion matrices",
        "Confidence thresholds",
        "Reading model mistakes",
    ],
    9: [
        "Graph construction",
        "Community detection",
        "Evaluating against a baseline",
        "Suspicious-group analysis",
    ],
    10: [
        "Time-series windowing",
        "Feature engineering for motion",
        "Handling false alarms",
        "Activity-class evaluation",
    ],
    12: [
        "Spatial features",
        "Leave-one-station-out validation",
        "Communicating uncertainty",
        "Satellite and ground-truth joins",
    ],
    13: [
        "Video frame sampling",
        "Artifact features",
        "Cross-dataset generalisation",
        "Precision and recall on deepfakes",
    ],
    14: [
        "OCR",
        "Validation rules",
        "Human-review workflows",
        "Field-level confidence",
    ],
    15: [
        "Image-to-image translation",
        "Paired data",
        "Evaluating generated images",
        "Remote-sensing preprocessing",
    ],
    16: [
        "Optical flow",
        "Interpolation models",
        "Perceptual quality metrics",
        "Synthetic-frame labelling",
    ],
    17: [
        "Statistical features",
        "Synthetic data generation",
        "Noise robustness",
        "Process classification",
    ],
    18: [
        "Light-curve cleaning",
        "Periodic signal search",
        "Class-imbalance handling",
        "False-positive diagnosis",
    ],
    19: [
        "Spatiotemporal data",
        "Persistence baselines",
        "Event-based scoring",
        "Hazard scoping",
    ],
    20: [
        "Orbit propagation",
        "Conjunction screening",
        "Risk classification",
        "Comparing against a distance rule",
    ],
    21: [
        "Satellite, weather and soil features",
        "Regional validation",
        "Uncertainty display",
        "Crop recommendation baselines",
    ],
    22: [
        "Feature engineering across data sources",
        "Bias checks",
        "Correlation versus causation",
        "Aggregate-data analysis",
    ],
    23: [
        "OCR",
        "Retrieval with citations",
        "Handling 'I don't know'",
        "Expert-question evaluation",
    ],
    24: [
        "Retrieval-augmented generation",
        "Citation checking",
        "Retriever evaluation",
        "Answer latency",
    ],
    25: [
        "Fine-tuning a text classifier",
        "Stylometric features",
        "Out-of-distribution testing",
        "Confidence calibration",
    ],
    26: [
        "Regression",
        "Feature engineering",
        "Prediction intervals",
        "Bias checks across neighbourhoods",
    ],
    27: [
        "Small-sample modelling",
        "Cross-validation by player",
        "Interpreting correlations",
        "Position-specific features",
    ],
    28: [
        "Spectrum processing",
        "Fingerprint prediction",
        "Ranking candidates",
        "Tanimoto similarity",
    ],
    29: [
        "Tool use",
        "Self-verification",
        "Building an evaluation set",
        "Unit-aware calculation",
    ],
    30: [
        "Loss functions",
        "Gradients and learning rate",
        "Feature scaling",
        "Comparing with scikit-learn",
    ],
    31: [
        "Text classification",
        "Precision versus recall trade-offs",
        "Explaining a model",
        "Handling class imbalance",
    ],
    32: [
        "Code-mixed text",
        "Tokenization problems",
        "Error analysis",
        "Multilingual baselines",
    ],
    33: [
        "Transfer learning",
        "Distribution shift",
        "Honest evaluation",
        "Confidence thresholds and abstention",
    ],
    34: [
        "Time-based train and test splits",
        "Naive and seasonal baselines",
        "Forecast error metrics",
        "When complex models fail",
    ],
    35: [
        "Similarity measures",
        "Train and test splits for recommenders",
        "Cold-start problem",
        "Precision@k",
    ],
    36: [
        "Data profiling",
        "Cleaning rules with pandas",
        "Undo logs",
        "Target leakage detection",
    ],
    37: [
        "Backpropagation",
        "Computational graphs",
        "Optimizers",
        "Gradient checking",
    ],
    38: [
        "Recursion",
        "Impurity measures",
        "Overfitting and pruning",
        "Ensemble methods",
    ],
    39: [
        "Attention",
        "Tokenization",
        "Training dynamics",
        "Sampling strategies",
    ],
    40: [
        "Search trees",
        "Pruning",
        "Heuristic evaluation",
        "Exploration versus exploitation",
    ],
    41: [
        "Markov decision processes",
        "Reward design",
        "Policy evaluation",
        "Strong baselines",
    ],
    42: [
        "Molecular representations",
        "Graph neural networks",
        "Evaluation splits",
        "Fingerprint baselines",
    ],
    43: [
        "System identification",
        "Sparsity",
        "Noise sensitivity",
        "Interpretable extrapolation",
    ],
    44: [
        "Audio features and spectrograms",
        "Noisy labels",
        "Multi-label classification",
        "Bioacoustics evaluation",
    ],
    45: [
        "Transfer learning on astronomy images",
        "Soft labels",
        "Measuring uncertainty",
        "Morphology class imbalance",
    ],
    46: [
        "Reinforcement learning with no library",
        "Rewards, penalties and exploration",
        "Learning from games against a random player",
        "Reading a learning curve",
    ],
    47: [
        "Image classification from stroke drawings",
        "Train, validation and test splits",
        "Confusion matrices",
        "Comparing a simple and a stronger model",
    ],
    48: [
        "Classification with rare positive cases",
        "Why accuracy misleads on imbalanced data",
        "Precision, recall and F1",
        "Reading a decision tree as rules",
    ],
    49: [
        "Feature engineering from game records",
        "k-means clustering",
        "Judging clusters with the silhouette score",
        "Naming clusters from real examples",
    ],
    50: [
        "Exploratory data analysis on a small sample",
        "Lag plots and timing",
        "Correlation versus causation",
        "Honest uncertainty in a write-up",
    ],
    51: [
        "Audio features such as MFCCs",
        "Nearest neighbours versus logistic regression",
        "Reading errors by genre pair",
        "Why a representation makes a task easy or hard",
    ],
}

DIFFICULTIES = {
    1: "intermediate",
    4: "intermediate",
    7: "intermediate",
    8: "beginner",
    9: "advanced",
    10: "intermediate",
    12: "advanced",
    13: "advanced",
    14: "intermediate",
    15: "advanced",
    16: "intermediate",
    17: "advanced",
    18: "intermediate",
    19: "advanced",
    20: "advanced",
    21: "intermediate",
    22: "intermediate",
    23: "advanced",
    24: "intermediate",
    25: "intermediate",
    26: "beginner",
    27: "intermediate",
    28: "advanced",
    29: "advanced",
    30: "beginner",
    31: "beginner",
    32: "beginner",
    33: "beginner",
    34: "beginner",
    35: "beginner",
    36: "beginner",
    37: "intermediate",
    38: "intermediate",
    39: "advanced",
    40: "intermediate",
    41: "advanced",
    42: "advanced",
    43: "intermediate",
    44: "intermediate",
    45: "intermediate",
    46: "beginner",
    47: "beginner",
    48: "beginner",
    49: "beginner",
    50: "beginner",
    51: "beginner",
}

TITLES = {
    1: "Review & Rating Manipulation Detector",
    4: "Smart Product Pricing",
    7: "Social Post to Product Listing Converter",
    8: "Waste Sorting Assistant (India-Aware)",
    9: "Fraud Ring Detector (Graph Analytics)",
    10: "Fall & Activity Recognition from Phone Sensors",
    12: "Satellite Air Quality Downscaling",
    13: "Deepfake Video Detector",
    14: "Paper Form Digitizer with Human Review",
    15: "SAR Image Colorization",
    16: "Satellite Frame Interpolation",
    17: "Dataset Origin Detective",
    18: "Exoplanet Transit Detector",
    19: "Hyperlocal Weather Prediction & Risk Alerts",
    20: "Orbital Debris Collision Risk Predictor",
    21: "Crop Advisor with Satellite and Weather Data",
    22: "Climate-Linked Health Risk Analyzer",
    23: "Multi-Modal Agricultural Assistant",
    24: "Engineering Knowledge Copilot",
    25: "Which AI Wrote This? (Model Attribution)",
    26: "House Price Prediction with Explanations",
    27: "Athlete Testing vs Match Performance",
    28: "Molecule Structure Identification from Mass Spectra",
    29: "Autonomous Engineering Problem Solver",
    30: "Gradient Descent Playground: Regression from Scratch",
    31: "Scam Message Detector with Explanations",
    32: "Hinglish Sentiment Analyzer",
    33: "Plant Disease Detector: Lab Accuracy vs Field Accuracy",
    34: "Forecasting Basics: Beat the Naive Baseline",
    35: "Recommender from Scratch: Content-Based vs Collaborative",
    36: "Messy Data Doctor",
    37: "Neural Network Library from Scratch (Autograd)",
    38: "Decision Trees & Random Forests from Scratch",
    39: "Mini GPT from Scratch",
    40: "Game-Playing AI: Minimax, Alpha-Beta and Monte Carlo Tree Search",
    41: "Traffic Signal Control with Reinforcement Learning",
    42: "Molecular Property Prediction: Fingerprints vs Graph Neural Networks",
    43: "Physics Law Discovery from Data",
    44: "Bird Call Identifier (Bioacoustics)",
    45: "Galaxy Morphology Classifier with Uncertainty",
    46: "Matchbox Machine: Teach Tic-Tac-Toe with Beads",
    47: "Doodle Recognizer: Guess the Sketch",
    48: "Is It Legendary? A Pokemon Stats Classifier",
    49: "Which Chess Player Are You? Clustering Playing Styles",
    50: "Analyse Your Own Life: A Small Personal Dashboard",
    51: "Music Genre Detective: Guess the Genre from a Clip",
}
