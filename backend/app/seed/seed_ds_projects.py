"""Seed 30 Data Science & Data Analytics project ideas (10 beginner, 10 intermediate, 10 advanced)."""

from app.seed.runner import seed_problems


PROBLEMS = [
    # ── Beginner ──
    dict(
        source_id="manabi-ds-beginner-001",
        title="Public Health Data Explorer",
        summary="Analyze public health datasets to identify disease trends, regional differences, demographic patterns, and changes over time.",
        who_affected="Public health officials, researchers, and communities monitoring disease burden.",
        why_matters="Understanding disease trends helps allocate healthcare resources and design targeted interventions.",
        field="data-science",
        domain="healthcare",
        difficulty="beginner",
        est_hours=40,
        tech_tags=["python", "pandas", "matplotlib", "seaborn", "eda"],
        datasets=[{"name": "Public health dataset", "url": None}],
        approaches=[
            "Load and clean public health datasets.",
            "Perform exploratory data analysis on disease incidence by region and demographic.",
            "Visualize trends over time using line and bar charts.",
            "Identify hotspots and vulnerable population segments.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze public health datasets to identify disease trends, regional differences, demographic patterns, and changes over time.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-002",
        title="Student Academic Performance Analytics",
        summary="Investigate how attendance, study hours, assessment scores, and other factors relate to academic performance.",
        who_affected="Educators, students, and academic advisors.",
        why_matters="Understanding performance drivers enables targeted support and better learning outcomes.",
        field="data-science",
        domain="education",
        difficulty="beginner",
        est_hours=38,
        tech_tags=["python", "pandas", "correlation", "eda", "matplotlib"],
        datasets=[{"name": "Student performance dataset", "url": None}],
        approaches=[
            "Clean and merge student demographic, attendance, and score data.",
            "Compute correlations between study hours, attendance, and grades.",
            "Visualize score distributions by demographic group.",
            "Identify factors most strongly associated with high and low performance.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Investigate how attendance, study hours, assessment scores, and other factors relate to academic performance.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-003",
        title="Retail Sales & Revenue Intelligence Dashboard",
        summary="Analyze sales, revenue, profit margins, product performance, and seasonal trends to identify business opportunities.",
        who_affected="Retail managers, business owners, and sales analysts.",
        why_matters="Sales intelligence reveals which products and seasons drive profit, guiding inventory and promotion decisions.",
        field="data-science",
        domain="industry",
        difficulty="beginner",
        est_hours=42,
        tech_tags=["sql", "python", "dashboard", "kpis", "visualization"],
        datasets=[{"name": "Retail sales transactions", "url": None}],
        approaches=[
            "Query sales data by product, region, and time period.",
            "Compute KPIs: total revenue, profit margin, average order value.",
            "Identify top and bottom performing products and categories.",
            "Build a dashboard visualizing seasonal sales trends.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze sales, revenue, profit margins, product performance, and seasonal trends to identify business opportunities.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-004",
        title="Road Accident Data Analysis",
        summary="Identify accident hotspots, high-risk time periods, vehicle-related patterns, and regional accident trends.",
        who_affected="Transport authorities, urban planners, and road safety advocates.",
        why_matters="Accident hotspot analysis informs safer road design and targeted enforcement.",
        field="data-science",
        domain="transport",
        difficulty="beginner",
        est_hours=44,
        tech_tags=["python", "geospatial", "folium", "eda", "visualization"],
        datasets=[{"name": "Road accident records", "url": None}],
        approaches=[
            "Load accident records with location, time, and vehicle fields.",
            "Map accident hotspots using geospatial visualization.",
            "Analyze accidents by time of day, day of week, and season.",
            "Compare accident rates across vehicle types and regions.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Identify accident hotspots, high-risk time periods, vehicle-related patterns, and regional accident trends.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-005",
        title="Personal Finance & Spending Analytics",
        summary="Analyze income, expenses, recurring payments, savings patterns, and category-wise spending behavior.",
        who_affected="Individuals and households managing personal budgets.",
        why_matters="Spending visibility helps people reduce waste, save more, and reach financial goals.",
        field="data-science",
        domain="fintech",
        difficulty="beginner",
        est_hours=36,
        tech_tags=["python", "pandas", "data-aggregation", "time-based-analysis", "matplotlib"],
        datasets=[{"name": "Personal transaction data", "url": None}],
        approaches=[
            "Categorize transactions into spending buckets (food, transport, housing, etc.).",
            "Aggregate monthly income vs. expenses and compute savings rate.",
            "Identify recurring subscriptions and large discretionary spends.",
            "Visualize spending trends by category over time.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze income, expenses, recurring payments, savings patterns, and category-wise spending behavior.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-006",
        title="Air Pollution & Environmental Trends Analysis",
        summary="Study pollution levels across locations and seasons to identify environmental patterns and possible contributing factors.",
        who_affected="Environmental agencies, city residents, and public health officials.",
        why_matters="Pollution trend analysis supports air quality improvement policies and public health advisories.",
        field="data-science",
        domain="climate",
        difficulty="beginner",
        est_hours=40,
        tech_tags=["python", "time-series", "correlation", "visualization", "pandas"],
        datasets=[{"name": "Air quality monitoring data", "url": None}],
        approaches=[
            "Collect pollutant readings (PM2.5, PM10, NO2, SO2) by station and time.",
            "Analyze seasonal and daily pollution cycles.",
            "Correlate pollution with weather and traffic factors.",
            "Visualize pollution maps and trend lines.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Study pollution levels across locations and seasons to identify environmental patterns and possible contributing factors.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-007",
        title="E-Commerce Customer Behavior Analysis",
        summary="Explore browsing, purchasing, cart abandonment, and product preferences to understand customer behavior.",
        who_affected="E-commerce businesses, product managers, and marketers.",
        why_matters="Understanding drop-off points and preferences helps improve conversion and customer experience.",
        field="data-science",
        domain="social-impact",
        difficulty="beginner",
        est_hours=42,
        tech_tags=["sql", "funnel-analysis", "segmentation", "python", "eda"],
        datasets=[{"name": "E-commerce event logs", "url": None}],
        approaches=[
            "Extract page views, add-to-cart, and purchase events from logs.",
            "Build a funnel from browse to purchase and measure conversion at each step.",
            "Segment customers by purchase frequency and average order value.",
            "Analyze cart abandonment rates by product category.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Explore browsing, purchasing, cart abandonment, and product preferences to understand customer behavior.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-008",
        title="Public Transport Performance Analytics",
        summary="Analyze delays, route efficiency, passenger demand, and peak-hour traffic to identify transportation bottlenecks.",
        who_affected="Transit agencies, commuters, and city planners.",
        why_matters="Performance insights guide schedule improvements and capacity planning.",
        field="data-science",
        domain="transport",
        difficulty="beginner",
        est_hours=40,
        tech_tags=["python", "time-based-aggregation", "geospatial-visualization", "pandas"],
        datasets=[{"name": "Transit schedule and delay data", "url": None}],
        approaches=[
            "Aggregate on-time performance by route and time of day.",
            "Map passenger demand peaks across the network.",
            "Identify routes with the highest delay frequencies.",
            "Visualize bottleneck locations on a transit map.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze delays, route efficiency, passenger demand, and peak-hour traffic to identify transportation bottlenecks.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-009",
        title="Sports Performance & Statistics Explorer",
        summary="Analyze player performance, team statistics, consistency, and match trends to identify meaningful performance patterns.",
        who_affected="Coaches, analysts, athletes, and sports fans.",
        why_matters="Performance analytics informs training focus, lineup decisions, and scouting.",
        field="data-science",
        domain="social-impact",
        difficulty="beginner",
        est_hours=38,
        tech_tags=["python", "statistical-analysis", "comparative-visualization", "pandas"],
        datasets=[{"name": "Sports match and player statistics", "url": None}],
        approaches=[
            "Collect match-level player and team statistics.",
            "Compare performance metrics across players and teams.",
            "Analyze consistency using variance and rolling averages.",
            "Visualize head-to-head and season trends.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze player performance, team statistics, consistency, and match trends to identify meaningful performance patterns.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-beginner-010",
        title="Job Market & Skills Demand Analytics",
        summary="Analyze job postings to discover in-demand skills, salary ranges, experience requirements, and hiring trends.",
        who_affected="Job seekers, career coaches, and workforce planners.",
        why_matters="Skills demand data helps learners prioritize training and employers set competitive offers.",
        field="data-science",
        domain="governance",
        difficulty="beginner",
        est_hours=44,
        tech_tags=["web-data-collection", "text-analysis", "sql", "dashboard", "python"],
        datasets=[{"name": "Job posting listings", "url": None}],
        approaches=[
            "Scrape or import job postings with title, skills, salary, and experience fields.",
            "Extract and normalize skill keywords from descriptions.",
            "Rank skills by frequency and analyze salary bands by role.",
            "Visualize hiring trends by industry and location.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze job postings to discover in-demand skills, salary ranges, experience requirements, and hiring trends.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    # ── Intermediate ──
    dict(
        source_id="manabi-ds-intermediate-001",
        title="Customer Churn & Retention Intelligence",
        summary="Analyze customer activity, identify churn patterns, measure retention, and discover the behaviors associated with customer loss.",
        who_affected="Subscription businesses, product teams, and customer success managers.",
        why_matters="Retaining customers is cheaper than acquiring new ones. Churn analysis reveals at-risk segments early.",
        field="data-science",
        domain="social-impact",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["python", "cohort-analysis", "survival-analysis", "customer-segmentation", "sql"],
        datasets=[{"name": "Customer subscription and activity logs", "url": None}],
        approaches=[
            "Build customer cohorts by signup month and track retention over time.",
            "Identify behavioral markers preceding churn (inactivity, support tickets).",
            "Segment customers by tenure, value, and risk level.",
            "Estimate survival curves and compute churn probability by segment.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze customer activity, identify churn patterns, measure retention, and discover the behaviors associated with customer loss.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-002",
        title="Product Analytics & User Journey Intelligence",
        summary="Analyze user events to understand conversion funnels, feature adoption, drop-off points, and user engagement.",
        who_affected="Product managers, designers, and growth teams.",
        why_matters="Funnel and journey analysis pinpoints where users get stuck and which features drive value.",
        field="data-science",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=84,
        tech_tags=["python", "event-analytics", "funnel-analysis", "retention-metrics", "mixpanel-style"],
        datasets=[{"name": "Product event stream", "url": None}],
        approaches=[
            "Instrument and collect user interaction events.",
            "Map conversion funnels and measure step-by-step drop-off.",
            "Track feature adoption by user segment over time.",
            "Compare engaged vs. churned user journeys.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze user events to understand conversion funnels, feature adoption, drop-off points, and user engagement.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-003",
        title="Supply Chain Bottleneck & Efficiency Analysis",
        summary="Investigate delivery delays, inventory movements, supplier performance, and operational inefficiencies across a supply chain.",
        who_affected="Supply chain managers, logistics coordinators, and operations teams.",
        why_matters="Bottleneck identification reduces lead times, inventory costs, and stockouts.",
        field="data-science",
        domain="industry",
        difficulty="intermediate",
        est_hours=82,
        tech_tags=["sql", "operational-analytics", "optimization", "python", "delivery-analysis"],
        datasets=[{"name": "Supply chain shipment records", "url": None}],
        approaches=[
            "Join order, shipment, and inventory tables by SKU and date.",
            "Compute lead times by supplier and route.",
            "Flag shipments exceeding agreed delivery windows.",
            "Identify suppliers and routes contributing most to delays.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Investigate delivery delays, inventory movements, supplier performance, and operational inefficiencies across a supply chain.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-004",
        title="Marketing Campaign Attribution & ROI Analysis",
        summary="Measure campaign performance across channels and investigate how different marketing interactions contribute to conversions.",
        who_affected="Marketing teams, growth marketers, and media planners.",
        why_matters="Attribution clarifies which channels deserve budget, improving marketing ROI.",
        field="data-science",
        domain="social-impact",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["python", "attribution-modeling", "roi-analysis", "statistical-methods", "sql"],
        datasets=[{"name": "Marketing touchpoint and conversion data", "url": None}],
        approaches=[
            "Collect ad impressions, clicks, and conversions by channel.",
            "Apply first-touch, last-touch, and linear attribution models.",
            "Compute ROI per channel and campaign.",
            "Compare attribution models to shift budget efficiently.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Measure campaign performance across channels and investigate how different marketing interactions contribute to conversions.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-005",
        title="Real Estate Market Intelligence Platform",
        summary="Analyze property prices, rental trends, location characteristics, and market movements to identify undervalued areas.",
        who_affected="Homebuyers, investors, and real estate agents.",
        why_matters="Market intelligence helps buyers and investors find value and avoid overpaying.",
        field="data-science",
        domain="fintech",
        difficulty="intermediate",
        est_hours=86,
        tech_tags=["python", "geospatial-analytics", "regression", "market-analysis", "folium"],
        datasets=[{"name": "Property listings and sales data", "url": None}],
        approaches=[
            "Collect property listings with price, location, size, and features.",
            "Map price per square foot by neighborhood.",
            "Build a regression model to estimate fair market value.",
            "Identify areas where actual prices deviate from model predictions.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze property prices, rental trends, location characteristics, and market movements to identify undervalued areas.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-006",
        title="A/B Testing & Experimentation Analysis Platform",
        summary="Evaluate experiments using statistical tests, confidence intervals, effect sizes, and segment-level comparisons.",
        who_affected="Product teams, data scientists, and conversion rate optimizers.",
        why_matters="Rigorous experiment analysis prevents false positives and supports confident product decisions.",
        field="data-science",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=78,
        tech_tags=["python", "hypothesis-testing", "experimental-design", "statistical-inference", "scipy"],
        datasets=[{"name": "A/B test experiment logs", "url": None}],
        approaches=[
            "Randomize users into treatment and control groups.",
            "Compute lift, confidence intervals, and p-values for primary metrics.",
            "Analyze results by user segment (new vs. returning, device type).",
            "Check for multiple comparisons and peeking biases.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Evaluate experiments using statistical tests, confidence intervals, effect sizes, and segment-level comparisons.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-007",
        title="Customer Lifetime Value & Revenue Analysis",
        summary="Estimate customer lifetime value, compare customer segments, and identify the factors that drive long-term revenue.",
        who_affected="Finance teams, marketers, and business strategists.",
        why_matters="CLV informs customer acquisition budgets and retention prioritization.",
        field="data-science",
        domain="fintech",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["python", "clv-modeling", "cohort-analysis", "probability-distributions", "sql"],
        datasets=[{"name": "Customer transaction history", "url": None}],
        approaches=[
            "Compute recency, frequency, and monetary (RFM) metrics per customer.",
            "Model CLV using probabilistic or regression approaches.",
            "Segment customers by CLV and acquisition cost.",
            "Identify behavioral drivers of high-value customers.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Estimate customer lifetime value, compare customer segments, and identify the factors that drive long-term revenue.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-008",
        title="Financial Market Risk & Portfolio Analytics",
        summary="Analyze asset returns, volatility, correlation, drawdowns, and portfolio risk under different market conditions.",
        who_affected="Investors, portfolio managers, and risk analysts.",
        why_matters="Risk analytics helps investors size positions and avoid excessive drawdowns.",
        field="data-science",
        domain="fintech",
        difficulty="intermediate",
        est_hours=82,
        tech_tags=["python", "time-series-analysis", "statistical-risk-measures", "pandas", "numpy"],
        datasets=[{"name": "Historical asset price data", "url": None}],
        approaches=[
            "Download historical prices for a basket of assets.",
            "Compute daily returns, volatility, and rolling Sharpe ratios.",
            "Analyze correlation and drawdowns across market regimes.",
            "Build an efficient frontier for sample portfolios.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze asset returns, volatility, correlation, drawdowns, and portfolio risk under different market conditions.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-009",
        title="Healthcare Resource Utilization Analytics",
        summary="Analyze hospital admissions, bed occupancy, treatment duration, and resource utilization to identify operational inefficiencies.",
        who_affected="Hospital administrators, operations managers, and health policymakers.",
        why_matters="Utilization analysis reduces wait times, optimizes staffing, and lowers care costs.",
        field="data-science",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=80,
        tech_tags=["python", "healthcare-analytics", "time-series-analysis", "kpi-design", "sql"],
        datasets=[{"name": "Hospital admission and occupancy records", "url": None}],
        approaches=[
            "Extract admissions, discharges, and bed occupancy by department.",
            "Compute average length of stay and bed turnover rates.",
            "Identify peak occupancy periods and boarding delays.",
            "Compare utilization across departments and shifts.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze hospital admissions, bed occupancy, treatment duration, and resource utilization to identify operational inefficiencies.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-intermediate-010",
        title="Data Quality & Anomaly Investigation Platform",
        summary="Detect missing values, inconsistent records, unexpected distributions, duplicate entries, and unusual changes in business datasets.",
        who_affected="Data engineers, analysts, and business intelligence teams.",
        why_matters="Poor data quality leads to wrong decisions. Proactive anomaly detection protects downstream analytics.",
        field="data-science",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=76,
        tech_tags=["python", "data-profiling", "statistical-anomaly-detection", "data-validation", "pandas"],
        datasets=[{"name": "Business operational datasets", "url": None}],
        approaches=[
            "Profile datasets for completeness, uniqueness, and validity.",
            "Detect duplicates and inconsistent categorical values.",
            "Flag statistical outliers and distribution shifts using z-scores and IQR.",
            "Build dashboards tracking data quality trends over time.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Detect missing values, inconsistent records, unexpected distributions, duplicate entries, and unusual changes in business datasets.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    # ── Advanced ──
    dict(
        source_id="manabi-ds-advanced-001",
        title="Causal Impact & Policy Evaluation Platform",
        summary="Evaluate whether a policy, intervention, or business change actually caused an observed outcome rather than merely correlating with it.",
        who_affected="Policymakers, program evaluators, and business strategy teams.",
        why_matters="Correlation does not imply causation. Causal impact analysis prevents wrong conclusions from observational data.",
        field="data-science",
        domain="governance",
        difficulty="advanced",
        est_hours=200,
        tech_tags=["python", "causal-inference", "difference-in-differences", "propensity-score-matching", "statsmodels"],
        datasets=[{"name": "Policy intervention and outcome data", "url": None}],
        approaches=[
            "Construct treatment and control groups using propensity score matching.",
            "Apply difference-in-differences to estimate causal effects.",
            "Conduct sensitivity analyses for unobserved confounding.",
            "Report effect sizes with confidence intervals.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Evaluate whether a policy, intervention, or business change actually caused an observed outcome rather than merely correlating with it.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-002",
        title="Large-Scale Clickstream & Behavioral Analytics Engine",
        summary="Process large volumes of user interaction events to discover behavioral patterns, navigation sequences, and engagement trends.",
        who_affected="Product analysts, data engineers, and digital platform teams.",
        why_matters="Clickstream at scale reveals how users truly navigate products, beyond sampled surveys.",
        field="data-science",
        domain="developer-tools",
        difficulty="advanced",
        est_hours=220,
        tech_tags=["python", "distributed-data-processing", "event-analytics", "sql", "spark-style"],
        datasets=[{"name": "Large-scale web clickstream logs", "url": None}],
        approaches=[
            "Ingest and store billions of clickstream events in a columnar store.",
            "Sessionize events and extract navigation paths.",
            "Identify common sequences leading to conversion or drop-off.",
            "Aggregate engagement trends by cohort and device.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Process large volumes of user interaction events to discover behavioral patterns, navigation sequences, and engagement trends.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-003",
        title="Real-Time Business Intelligence & Streaming Analytics System",
        summary="Ingest live business events and generate real-time metrics, anomaly alerts, and operational dashboards.",
        who_affected="Operations teams, executives, and monitoring analysts.",
        why_matters="Real-time metrics enable immediate response to incidents and opportunities.",
        field="data-science",
        domain="developer-tools",
        difficulty="advanced",
        est_hours=210,
        tech_tags=["python", "stream-processing", "kafka", "flink", "analytical-databases"],
        datasets=[{"name": "Simulated live business event stream", "url": None}],
        approaches=[
            "Ingest events via Kafka or similar message bus.",
            "Compute sliding-window metrics (revenue, active users, error rates).",
            "Detect anomalies using statistical process control on streams.",
            "Stream results to a real-time dashboard and alerting system.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Ingest live business events and generate real-time metrics, anomaly alerts, and operational dashboards.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-004",
        title="Demand Forecasting & Inventory Optimization System",
        summary="Forecast demand across multiple products and locations while considering uncertainty, lead times, storage constraints, and stockout costs.",
        who_affected="Retailers, warehouse operators, and supply chain planners.",
        why_matters="Probabilistic forecasting balances stockout risk against holding costs.",
        field="data-science",
        domain="industry",
        difficulty="advanced",
        est_hours=200,
        tech_tags=["python", "probabilistic-forecasting", "optimization", "time-series-analysis", "scikit-learn"],
        datasets=[{"name": "Multi-location sales and inventory data", "url": None}],
        approaches=[
            "Build probabilistic demand forecasts (quantile regression, Bayesian models).",
            "Model lead time variability and storage constraints.",
            "Optimize reorder points and safety stock by SKU-location.",
            "Simulate stockout costs and service level tradeoffs.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Forecast demand across multiple products and locations while considering uncertainty, lead times, storage constraints, and stockout costs.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-005",
        title="Economic Indicator & Macroeconomic Intelligence Platform",
        summary="Combine inflation, employment, interest rates, GDP, and other indicators to investigate economic relationships and emerging trends.",
        who_affected="Economists, policymakers, and financial analysts.",
        why_matters="Macroeconomic analysis supports monetary and fiscal policy decisions.",
        field="data-science",
        domain="fintech",
        difficulty="advanced",
        est_hours=190,
        tech_tags=["python", "econometrics", "multivariate-time-series", "statistical-modeling", "statsmodels"],
        datasets=[{"name": "Macroeconomic indicator dataset", "url": None}],
        approaches=[
            "Assemble monthly/quarterly macro indicators from public sources.",
            "Test for stationarity and cointegration across series.",
            "Build VAR or ARIMAX models to forecast key indicators.",
            "Analyze impulse responses to policy shocks.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Combine inflation, employment, interest rates, GDP, and other indicators to investigate economic relationships and emerging trends.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-006",
        title="Data-Driven Fraud Network Investigation System",
        summary="Analyze transaction relationships and interconnected entities to uncover suspicious networks, coordinated activity, and fraud patterns.",
        who_affected="Fraud investigators, compliance teams, and financial institutions.",
        why_matters="Fraud often involves coordinated actors. Network analysis reveals rings that individual transaction review misses.",
        field="data-science",
        domain="cybersecurity",
        difficulty="advanced",
        est_hours=200,
        tech_tags=["python", "graph-analytics", "network-science", "anomaly-detection", "networkx"],
        datasets=[{"name": "Transaction and entity relationship data", "url": None}],
        approaches=[
            "Model transactions as a bipartite graph of accounts and counterparties.",
            "Compute centrality, community detection, and motif metrics.",
            "Flag densely connected subgraphs with unusual velocity.",
            "Prioritize networks for investigator review.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Analyze transaction relationships and interconnected entities to uncover suspicious networks, coordinated activity, and fraud patterns.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-007",
        title="Data Observability & Pipeline Reliability Platform",
        summary=(
            "Data breaks quietly. A feed stops updating, a column gets renamed "
            "upstream, a sales spike is actually a reporting bug - and nobody "
            "finds out until a dashboard looks wrong to a decision maker. This "
            "project is the watchdog against that silence: a platform that "
            "checks data constantly, notices when normal turns abnormal, and "
            "says precisely what broke, where, and who is downstream.\n\n"
            "You build it in layers. First the reader: a scheduler that pulls "
            "table metadata and samples after each pipeline run - last refresh "
            "time, row count, NULL rates, schema shape. Then the checks: "
            "freshness against a staleness threshold, completeness against "
            "expected volumes per time window, and validity against column "
            "types. Each run's results get stored, not just shown, so history "
            "is queryable and the trend lines are real.\n\n"
            "Then the interesting layer: baselines. The platform records what "
            "normal looks like per column and per weekday - Tuesday dips are "
            "normal, Tuesday zeros are not - and flags distribution shifts "
            "using simple statistics before they turn into broken dashboards. "
            "When a check fails, an alert lands in one channel with the failing "
            "table, the check, the failing value, and the list of downstream "
            "things that consume this table.\n\n"
            "On top sits a run history UI: which pipelines passed today, which "
            "are stale, which checks fire repeatedly, and which changed "
            "behavior this week. The whole loop imitates what senior data teams "
            "run in production, which is exactly what makes it worth a resume."
        ),
        who_affected="Data engineers, analytics engineers, and platform teams.",
        why_matters="Silent data pipeline failures corrupt dashboards and decisions. Observability catches issues before stakeholders notice.",
        field="data-science",
        domain="developer-tools",
        difficulty="advanced",
        est_hours=190,
        tech_tags=["python", "data-engineering", "statistical-monitoring", "lineage", "great-expectations-style"],
        datasets=[{"name": "Pipeline metadata and data quality logs", "url": None}],
        approaches=[
            "Track table freshness, row counts, and NULL rates per pipeline run.",
            "Detect schema changes (added/dropped columns, type changes).",
            "Monitor distribution shifts using statistical tests on column values.",
            "Alert on SLA breaches and data quality regressions.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Monitor analytical pipelines for freshness, schema changes, distribution shifts, data quality regressions, and unexpected metric changes.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="resume",
        resume_kit={
            "scope_levels": [
                {
                    "level": "Good enough (MVP)",
                    "text": (
                        "One pipeline wired to one dashboard that says whether "
                        "yesterday's data is trustworthy: freshness, row counts, "
                        "NULL rates, and an alert that fires when a check fails."
                    ),
                    "checks": [
                        "Freshness check per table with a configurable staleness threshold.",
                        "Row count and NULL rate checks stored per run, so you can graph them.",
                        "Alerts land in one channel and name the failing table and check.",
                        "A run history page showing when pipelines last passed or failed.",
                    ],
                },
                {
                    "level": "Impressive",
                    "text": (
                        "The monitor knows what normal looks like. It flags "
                        "distribution shifts and schema changes before "
                        "stakeholders email you, and it says what breaks "
                        "downstream when a table goes bad."
                    ),
                    "checks": [
                        "Distribution checks on key columns: baseline mean/std or a two-sample test.",
                        "Schema-change detection that logs added, dropped, or retyped columns.",
                        "Impact view: which dashboards or models eat this table, so a red check names its blast radius.",
                        "Anomaly detection on the monitored metrics themselves, not just the raw data.",
                        "A rerun or backfill hook so the fix is one click after the alert.",
                    ],
                },
            ],
            "target_roles": [
                {
                    "role": "Data engineer",
                    "how_it_helps": (
                        "This is a data engineer's actual job: monitoring, "
                        "schemas, SLAs. You can talk check design, alert "
                        "routing, and incident handling from real experience."
                    ),
                },
                {
                    "role": "Analytics engineer",
                    "how_it_helps": (
                        "You built the trust layer for dashboards: freshness "
                        "and quality checks that gate bad data before it hits "
                        "metrics teams quote in meetings."
                    ),
                },
                {
                    "role": "ML / MLOps engineer",
                    "how_it_helps": (
                        "Data drift monitoring is half of model health. Point "
                        "at your distribution-shift checks and explain how "
                        "retraining triggers connect to them."
                    ),
                },
                {
                    "role": "Backend engineer",
                    "how_it_helps": (
                        "The platform side is real backend work: a scheduler, "
                        "idempotent run recording, alert delivery, and an API "
                        "over run history."
                    ),
                },
                {
                    "role": "DevOps / SRE",
                    "how_it_helps": (
                        "Observability thinking applied to data: thresholds, "
                        "alert fatigue, runbooks, and post-incident review. "
                        "The concepts transfer from servers to pipelines."
                    ),
                },
            ],
            "resume_bullets": [
                {
                    "bullet": (
                        "Built a data observability platform monitoring {N} "
                        "pipelines and cut time-to-detect for bad data from "
                        "{days} to {minutes}."
                    ),
                    "example": (
                        "Built a data observability platform monitoring 6 "
                        "pipelines; time-to-detect for stale or broken feeds "
                        "dropped from 2 days to under 10 minutes."
                    ),
                },
                {
                    "bullet": (
                        "Cut false-positive data alerts by {X}% using per-column, "
                        "per-weekday baselines instead of global thresholds."
                    ),
                    "example": (
                        "Cut false-positive alerts 60% by baselining each "
                        "column against its own weekday pattern; a Tuesday "
                        "sales dip no longer pages anyone."
                    ),
                },
                {
                    "bullet": (
                        "Detected {M} breaking schema changes across {N} tables "
                        "before they broke downstream dashboards."
                    ),
                    "example": (
                        "Caught 9 breaking schema changes in 3 months before "
                        "any dashboard failed; each alert listed the merged "
                        "columns and the affected reports."
                    ),
                },
            ],
            "interview_points": [
                {
                    "question": "How do you decide what counts as 'bad data'?",
                    "answer": (
                        "Split it into types you can actually check: freshness "
                        "(are timestamps recent), completeness (row counts per "
                        "window, NULL rates), validity (schema and dtypes), and "
                        "distribution (stats drifting from baseline). Each type "
                        "has different thresholds and different failure modes - "
                        "saying that taxonomy out loud is the answer."
                    ),
                },
                {
                    "question": "How do you avoid alert fatigue?",
                    "answer": (
                        "Baseline per table and per weekday, deduplicate "
                        "cascading failures (one upstream break floods twenty "
                        "downstream checks), and rate-limit repeat alerts. Ship "
                        "few checks that are always worth acting on."
                    ),
                },
                {
                    "question": "What happens when an anomaly is a real business change, not a bug?",
                    "answer": (
                        "Annotate it: promotions, migrations, new markets landed "
                        "as events next to the metrics. When you can't annotate, "
                        "the alert body links related recent events and a human "
                        "triages. The monitor's job is fewer, clearer alerts - "
                        "not zero-touch truth."
                    ),
                },
                {
                    "question": "Which test do you use for distribution shift, and why?",
                    "answer": (
                        "Start simple: compare a fresh window's mean, std, and "
                        "quantiles to a trailing baseline. Move to two-sample "
                        "tests (KS for numeric, chi-square for categorical) on "
                        "high-value columns. The tradeoff to discuss is "
                        "sensitivity versus noise - a test nobody reads is worse "
                        "than a test that's coarse."
                    ),
                },
                {
                    "question": "Why build this when Great Expectations and dbt tests exist?",
                    "answer": (
                        "They cover a lot; nobody needs a worse rewrite. Building "
                        "one teaches why those tools are shaped the way they are "
                        "- check routing, baselines, lineage. In interviews the "
                        "value is explaining those design decisions, not "
                        "claiming novelty."
                    ),
                },
                {
                    "question": "How do you keep the checks cheap to run?",
                    "answer": (
                        "Sample large tables, check aggregates instead of rows, "
                        "test incremental windows only, and hang checks off the "
                        "pipeline scheduler so nothing scans a warehouse twice. "
                        "Cost per check is a design constraint, not an afterthought."
                    ),
                },
            ],
            "differentiators": [
                "Write the runbook: what on-call does when each check fires. A repo with a runbook reads like production experience, not course work.",
                "Store per-column history so thresholds come from data instead of guesses, and say so in the README - self-tuning baselines are rare in student projects.",
                "Add lineage-lite: a small map of which table feeds which dashboard, and have each failed check name its downstream victims.",
                "Log every alert as true positive or false positive and graph your alerting precision over weeks. It turns 'I built a monitor' into 'I tuned and owned a monitor'.",
                "Ship a docker-compose demo with a fake flaky pipeline, so a reviewer watches alerts fire without wiring up a real warehouse.",
            ],
        },
        build_guide=[
            {
                "title": "Pick one pipeline and record its metadata",
                "summary": (
                    "Observability starts with capture, not checking. One "
                    "pipeline, fully instrumented, beats five barely "
                    "monitored ones."
                ),
                "steps": [
                    "Choose a pipeline you can actually observe: a CSV feed into storage, a scheduled SQL job, or a public dataset refresh. Fake flaky failures into it later by appending a bad file.",
                    "After every run, capture the shape: last refresh timestamp, row count, NULL rate per column, and the schema (column names plus types). Store each run as one append-only row.",
                    "Design the storage first: runs keyed by pipeline id, table, and started_at. You will graph and diff these rows later, so no aggregation yet - raw results only.",
                    "Hook the capture into scheduler events if the pipeline has one (or a cron wrapper); capture must fire even when the run fails.",
                ],
            },
            {
                "title": "Ship the first checks and one alert channel",
                "summary": (
                    "Three boring checks, one loud channel. The goal is "
                    "trustworthy signal, not clever detections."
                ),
                "steps": [
                    "Freshness: compare the table's last refresh time against a configurable staleness threshold per table.",
                    "Completeness: row counts per time window against expected ranges, plus NULL rates per column against tolerance.",
                    "Validity: column presence and type enforcement - a dropped or retyped column is automatically a failure.",
                    "Wire all failures to one channel (email or a webhook) and keep the alert body honest: failing table, check name, expected versus actual, and a run link.",
                ],
            },
            {
                "title": "Build the run history UI",
                "summary": (
                    "History turns checks into a product. This is the part "
                    "interviewers can see and click, so make it fast and "
                    "readable."
                ),
                "steps": [
                    "One page answering three questions: what passed today, what is stale, what failed last night.",
                    "Per-pipeline view: check timelines graphed from the stored rows - row count over runs, NULL rate over runs.",
                    "Every alert links to this view; a check that fails should be explainable in one click, not by re-querying the warehouse.",
                    "Add a manual 'snooze check' button that records who snoozed and until when - audit even the mute action.",
                ],
            },
            {
                "title": "Baselines and distribution shifts",
                "summary": (
                    "This layer is what separates a toy from honest "
                    "monitoring: comparing today against what normal looks "
                    "like, learned from data."
                ),
                "steps": [
                    "For each monitored column, build a trailing baseline: mean, std, and quantiles per column per weekday - Tuesday dips are normal, Tuesday zeros are not.",
                    "Flag distribution shifts and surface them as alerts: a fresh window's stats outside baseline bands, or a two-sample test (KS for numeric, chi-square for categorical) on key columns.",
                    "Tune on real history and count false positives; a threshold nobody reads is worse than a coarse one.",
                    "Deduplicate cascades: one upstream failure floods downstream checks. Group alerts by root table so one incident sends one alert.",
                ],
            },
            {
                "title": "Impact, backfill, and the demo story",
                "summary": (
                    "Make the platform finish the incident loop: what breaks "
                    "downstream, how to fix, and a reviewer able to watch it "
                    "all fire without touching a real warehouse."
                ),
                "steps": [
                    "Add lineage-lite: a small config file mapping which table feeds which dashboard or model, and have failed checks name their downstream victims in the alert.",
                    "Add a rerun or backfill hook for one-click remediation after an alert, logged like any other action.",
                    "Log every alert as true positive or false positive and graph alerting precision over time - it proves you tuned it, not just built it.",
                    "Package a docker-compose demo with the fake flaky pipeline so alerts fire in minutes; write the runbook README explaining what on-call does per check.",
                ],
            },
        ],
    ),
    dict(
        source_id="manabi-ds-advanced-008",
        title="Urban Mobility & Traffic Optimization Analytics",
        summary="Combine traffic, public transport, road network, and mobility data to identify congestion patterns and evaluate infrastructure improvements.",
        who_affected="City transportation departments, urban planners, and commuters.",
        why_matters="Mobility analytics guides infrastructure investment and congestion pricing.",
        field="data-science",
        domain="transport",
        difficulty="advanced",
        est_hours=200,
        tech_tags=["python", "geospatial-analytics", "simulation", "optimization", "postgis"],
        datasets=[{"name": "Traffic counts, transit ridership, road network", "url": None}],
        approaches=[
            "Fuse GPS probe data, traffic counts, and transit ridership.",
            "Identify recurring congestion hotspots and bottleneck corridors.",
            "Simulate the impact of lane changes or new transit lines.",
            "Evaluate before/after metrics for infrastructure projects.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Combine traffic, public transport, road network, and mobility data to identify congestion patterns and evaluate infrastructure improvements.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-009",
        title="Experimentation Intelligence & Decision Platform",
        summary="Manage multiple experiments, detect statistical pitfalls, measure heterogeneous treatment effects, and support evidence-based product decisions.",
        who_affected="Experimentation teams, product leaders, and data scientists.",
        why_matters="Running many experiments increases false discovery risk. A decision platform enforces statistical rigor.",
        field="data-science",
        domain="developer-tools",
        difficulty="advanced",
        est_hours=210,
        tech_tags=["python", "causal-inference", "bayesian-statistics", "sequential-testing", "pymc-style"],
        datasets=[{"name": "Multi-experiment telemetry data", "url": None}],
        approaches=[
            "Build an experiment registry with power analysis and sample sizing.",
            "Apply sequential testing with alpha spending controls.",
            "Estimate heterogeneous treatment effects using causal forests or Bayesian hierarchies.",
            "Surface winner/loser/flat decisions with confidence statements.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Manage multiple experiments, detect statistical pitfalls, measure heterogeneous treatment effects, and support evidence-based product decisions.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
    dict(
        source_id="manabi-ds-advanced-010",
        title="Enterprise Data-to-Decision Intelligence System",
        summary="Unify data from sales, finance, operations, and customer systems to discover cross-department relationships and quantify the impact of potential business decisions.",
        who_affected="Executives, strategy teams, and business intelligence leaders.",
        why_matters="Siloed data hides cross-functional insights. A decision intelligence layer quantifies decision impact before execution.",
        field="data-science",
        domain="social-impact",
        difficulty="advanced",
        est_hours=220,
        tech_tags=["python", "data-warehousing", "semantic-layers", "advanced-analytics", "decision-modeling"],
        datasets=[{"name": "Integrated enterprise dataset sample", "url": None}],
        approaches=[
            "Build an ELT pipeline unifying sales, finance, operations, and CRM data.",
            "Model cross-department relationships in a semantic layer.",
            "Quantify decision impact using scenario and what-if modeling.",
            "Expose findings through an executive decision dashboard.",
        ],
        source_name="MANABI Curated",
        source_note="Curated data science project idea.",
        original_text="Unify data from sales, finance, operations, and customer systems to discover cross-department relationships and quantify the impact of potential business decisions.",
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
    ),
]


if __name__ == "__main__":
    seed_problems(PROBLEMS)
