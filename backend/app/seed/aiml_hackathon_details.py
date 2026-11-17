"""Hackathon-only AI/ML briefs and short problem statements.

The 28-project list comes from ``aiml_project.md``. Seventeen projects already
exist as resume briefs, so the seed composer reuses those facts and adds a
hackathon team plan and pitch kit. The eleven projects in ``NEW_PROJECTS`` only
exist on the hackathon track and are documented here.
"""


NEW_PROJECTS = {
    8: dict(
        title="Waste Sorting Assistant (India-Aware)",
        summary=(
            "Classify a photo of waste into plastic, paper, glass, metal or "
            "organic, then map it to a local wet, dry or recyclable rule. Say "
            "not sure when confidence is low."
        ),
        who_affected=(
            "Households, waste workers, school sustainability clubs and "
            "municipal teams trying to improve segregation at source."
        ),
        why_matters=(
            "Mixed waste contaminates recyclables and makes collection more "
            "expensive. A clear bin decision at the moment of disposal is more "
            "useful than a poster nobody reads."
        ),
        field="aiml",
        domain="climate",
        difficulty="beginner",
        est_hours=40,
        tech_tags=[
            "python",
            "pytorch",
            "transfer-learning",
            "computer-vision",
            "streamlit",
            "confidence",
        ],
        datasets=[
            {"name": "TrashNet", "url": "https://github.com/garythung/trashnet"},
            {"name": "TACO waste dataset", "url": "https://github.com/pedropro/TACO"},
        ],
        approaches=[
            "Map source classes to local wet, dry and recyclable bins instead of stopping at material labels.",
            "Fine-tune a small image model on a balanced subset and compare it with a frozen-feature baseline.",
            "Use a confidence threshold and a not-sure response for blurry, mixed or unfamiliar waste.",
            "Report a confusion matrix and the mistakes that would contaminate a recycling stream.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Check TrashNet and TACO licences before use.",
        original_text=(
            "Classify waste photos into local bin categories, show confidence "
            "and refuse to guess when the image is ambiguous."
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
                "title": "Define bins and collect a balanced sample",
                "summary": "A local bin mapping is the product decision; the model only supports it.",
                "steps": [
                    "Write the exact local rules for wet, dry and recyclable waste, including tricky items such as laminated paper and food-soiled plastic.",
                    "Map TrashNet or TACO classes to those bins and drop classes that cannot be mapped honestly.",
                    "Balance the sample and add a small set of your own photos from clean and cluttered backgrounds.",
                    "Create a not-sure fixture with mixed waste, blur and an object outside the training classes.",
                ],
            },
            {
                "title": "Train a small image classifier",
                "summary": "Start with a frozen backbone, then unfreeze only if the error analysis demands it.",
                "steps": [
                    "Train a frozen-feature classifier as the baseline and record per-class precision and recall.",
                    "Fine-tune the last block on the same split and compare the confusion matrix, not only accuracy.",
                    "Add light augmentation for rotation, brightness and background clutter.",
                    "Save the class mapping, threshold and model version together as one artifact.",
                ],
            },
            {
                "title": "Add confidence and mixed-waste handling",
                "summary": "A confident wrong bin is worse than an honest not-sure.",
                "steps": [
                    "Calibrate confidence on a held-out set and choose a threshold from the cost of contaminating a recycling stream.",
                    "Add a not-sure response for low confidence, multiple detected items or an unfamiliar object.",
                    "Show the top two likely bins and a short reason so the user can decide.",
                    "Test the refusal path on blurred, dark and mixed-waste photos.",
                ],
            },
            {
                "title": "Build the phone-friendly demo",
                "summary": "The decision should be readable in one glance beside the bin.",
                "steps": [
                    "Build an upload or camera flow with one large bin decision, a confidence bar and the not-sure state.",
                    "Show the local rule that produced the answer so the user can challenge it.",
                    "Add a short feedback control for wrong or mixed items without collecting personal data.",
                    "Test the page on a narrow screen and a slow connection.",
                ],
            },
            {
                "title": "Evaluate and tell the failure story",
                "summary": "The confusion matrix is more persuasive than a single accuracy number.",
                "steps": [
                    "Report the confusion matrix, per-class recall and the not-sure rate on the held-out set.",
                    "Show the top confusions such as paper versus cardboard or plastic film versus glass.",
                    "Explain how class imbalance and background clutter affected the result.",
                    "Record a demo with one clear item, one mixed item and one honest refusal.",
                ],
            },
        ],
    ),
    10: dict(
        title="Fall & Activity Recognition from Phone Sensors",
        summary=(
            "Use accelerometer and gyroscope data to recognise walking, running, "
            "sitting and falling, then alert a caregiver after a likely fall "
            "while avoiding false alarms from dropping the phone."
        ),
        who_affected=(
            "Older adults living alone, caregivers and wearable developers "
            "exploring low-cost safety alerts."
        ),
        why_matters=(
            "A fall can leave someone unable to call for help. A phone already "
            "has the sensors needed for a useful alert, but false alarms make "
            "the system easy to ignore."
        ),
        field="aiml",
        domain="healthcare",
        difficulty="intermediate",
        est_hours=60,
        tech_tags=[
            "python",
            "scikit-learn",
            "time-series",
            "sensors",
            "deep-learning",
            "mobile",
        ],
        datasets=[
            {"name": "UCI HAR dataset", "url": "https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones"},
            {"name": "SisFall dataset", "url": "https://www.kaggle.com/datasets/arashnic/sisfall-dataset"},
            {"name": "MobiAct dataset", "url": "https://www.mobiact.cz/"},
        ],
        approaches=[
            "Window the sensor stream with overlap and label activities and falls separately.",
            "Engineer time and frequency features, then compare a classic model with a small neural network.",
            "Add a post-fall stillness check so a dropped phone does not trigger an alert.",
            "Measure false alarms per hour and fall recall on held-out subjects.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Use public or consented sensor data only; this is not a safety system.",
        original_text=(
            "Recognise activities and falls from phone sensors, reduce false "
            "alarms with a stillness check and show a caregiver alert."
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
                "title": "Define windows and collect a safe sample",
                "summary": "Fall data is sensitive; start with public or consented recordings only.",
                "steps": [
                    "Choose a sampling rate, window length and overlap that fit a phone and a short alert delay.",
                    "Use a public dataset and record a few consented simulated activities such as sitting, walking and a controlled drop onto a soft surface.",
                    "Keep subject ids so train and test do not share the same person.",
                    "Define the alert rule and the fallback when sensor data is missing.",
                ],
            },
            {
                "title": "Build the classic baseline",
                "summary": "A simple model with good features is often enough for this problem.",
                "steps": [
                    "Extract mean, variance, energy, frequency and orientation-change features per window.",
                    "Train a random forest or gradient-boosting model and report per-class recall.",
                    "Inspect false positives from sitting down quickly, jumping and dropping the phone.",
                    "Save the feature order and window settings with the model.",
                ],
            },
            {
                "title": "Add a small neural model and false-alarm logic",
                "summary": "The sequence around a fall matters more than one isolated peak.",
                "steps": [
                    "Train a small 1D convolutional or recurrent model on the raw windows with the same subject split.",
                    "Compare fall recall and false alarms per hour against the classic baseline.",
                    "Add a stillness and orientation check after the impact to separate a fall from a drop.",
                    "Test deliberate false-alarm cases and document the trade-off.",
                ],
            },
            {
                "title": "Build the caregiver alert flow",
                "summary": "The demo must show what happens after a positive prediction.",
                "steps": [
                    "Simulate a sensor stream in the browser or a small phone page and show the current activity.",
                    "Display a short countdown before sending an alert so the user can cancel a false alarm.",
                    "Show the evidence behind the alert such as impact, stillness and orientation change.",
                    "Add a clear notice that the app is educational and not a substitute for emergency or medical systems.",
                ],
            },
            {
                "title": "Evaluate on people, not rows",
                "summary": "A random window split overstates performance because adjacent windows leak.",
                "steps": [
                    "Report fall recall, activity accuracy and false alarms per hour with a subject-grouped split.",
                    "Show the confusion between sitting quickly, lying down and a real fall.",
                    "Explain how phone placement and sensor quality change the result.",
                    "Record a demo with one true fall sequence and one cancelled false alarm.",
                ],
            },
        ],
    ),
    12: dict(
        title="Satellite Air Quality Downscaling",
        summary=(
            "Turn coarse satellite air-quality maps into finer local estimates "
            "by combining satellite measurements with ground stations, weather, "
            "roads, land use and elevation. Validate by hiding whole stations "
            "and present results with uncertainty."
        ),
        who_affected=(
            "City health teams, environmental researchers and residents in "
            "areas with too few ground monitors."
        ),
        why_matters=(
            "Pollution varies street by street, but monitors are sparse. A "
            "credible fine-grid estimate can support warnings and planning if "
            "its uncertainty is visible."
        ),
        field="aiml",
        domain="climate",
        difficulty="advanced",
        est_hours=90,
        tech_tags=[
            "python",
            "geopandas",
            "rasterio",
            "scikit-learn",
            "xgboost",
            "remote-sensing",
        ],
        datasets=[
            {"name": "OpenAQ ground stations", "url": "https://openaq.org/"},
            {"name": "NASA MAIAC aerosol products", "url": "https://ladsweb.modaps.eosdis.nasa.gov/"},
            {"name": "Copernicus Sentinel-5P", "url": "https://dataspace.copernicus.eu/"},
        ],
        approaches=[
            "Join satellite, station, weather, road and land-use layers on a common grid and time window.",
            "Build a station-mean or nearest-satellite baseline before training a downscaling model.",
            "Validate with leave-one-station-out splits so nearby station leakage cannot inflate the score.",
            "Report error, uncertainty bands and where the estimate should not be trusted.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Check each satellite and station data licence.",
        original_text=(
            "Downscale coarse satellite air-quality data with ground stations "
            "and spatial features, validate by station and show uncertainty."
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
                "title": "Pick one pollutant, region and time window",
                "summary": "A narrow scope makes the spatial validation believable.",
                "steps": [
                    "Choose one pollutant such as PM2.5 and a region with enough ground stations and satellite coverage.",
                    "Define the target grid resolution and the time window used for every layer.",
                    "Download station measurements, satellite products and weather fields, and record their native resolution.",
                    "Inspect missing values and write the rule for a grid cell with no usable satellite observation.",
                ],
            },
            {
                "title": "Build the spatial feature table",
                "summary": "Every feature must be available at prediction time, not only after the fact.",
                "steps": [
                    "Aggregate satellite values to the target grid and match them to the nearest station within a time window.",
                    "Add weather, elevation, road density and land-use features on the same grid.",
                    "Create a baseline that uses the nearest station mean or satellite value without a learned model.",
                    "Remove features that leak the station measurement or its immediate neighbours.",
                ],
            },
            {
                "title": "Train a downscaling model",
                "summary": "A tree-based model is a strong first choice for mixed spatial features.",
                "steps": [
                    "Train a gradient-boosting regressor with leave-one-station-out cross-validation.",
                    "Compare it with the baseline on MAE, RMSE and spatial correlation.",
                    "Inspect the worst stations and whether their errors come from distance, terrain or missing satellite data.",
                    "Add a simple uncertainty estimate such as ensemble spread or quantile predictions.",
                ],
            },
            {
                "title": "Build the map and uncertainty view",
                "summary": "A fine map without uncertainty invites false confidence.",
                "steps": [
                    "Render the predicted grid with a colour scale and the ground stations as points.",
                    "Add an uncertainty layer and a warning for cells with weak satellite coverage.",
                    "Show the station-level error for the selected region so a viewer can judge the map.",
                    "Add a timestamp and source list beside the map.",
                ],
            },
            {
                "title": "Validate and state the limits",
                "summary": "The station split is the result; the map is only the presentation.",
                "steps": [
                    "Report leave-one-station-out MAE, RMSE and the baseline comparison.",
                    "Check for geographic and seasonal bias in the residuals.",
                    "Explain why the estimate is not a regulatory monitor and where it should not be used.",
                    "Record a demo that switches between the coarse satellite view and the downscaled estimate.",
                ],
            },
        ],
    ),
    15: dict(
        title="SAR Image Colorization",
        summary=(
            "Translate radar satellite images into optical-style colour images "
            "so terrain is easier to interpret. Train on paired radar and optical "
            "data, measure SSIM and PSNR plus a downstream land-cover check, and "
            "label every output as an interpretation aid rather than ground truth."
        ),
        who_affected=(
            "Remote-sensing analysts, disaster-response teams and students "
            "learning image-to-image translation."
        ),
        why_matters=(
            "Radar sees through cloud and at night, but it is hard for non-"
            "specialists to read. A clear synthetic colour view can speed up "
            "interpretation if its uncertainty is labelled."
        ),
        field="aiml",
        domain="climate",
        difficulty="advanced",
        est_hours=85,
        tech_tags=[
            "python",
            "pytorch",
            "gan",
            "remote-sensing",
            "image-translation",
            "sentinel",
        ],
        datasets=[
            {"name": "SEN12MS paired radar and optical data", "url": "https://mediatum.ub.tum.de/1474000"},
            {"name": "SEN1-2 paired Sentinel imagery", "url": "https://github.com/ImperialCollegeLondon/SEN1-2"},
        ],
        approaches=[
            "Build paired Sentinel-1 radar and Sentinel-2 optical chips with a documented date gap.",
            "Train a pix2pix-style baseline and compare it with a simpler colourisation heuristic.",
            "Evaluate SSIM, PSNR and a downstream land-cover classifier on the generated images.",
            "Show the original radar beside the generated colour image and label it synthetic.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Generated colours can be wrong; check every dataset licence.",
        original_text=(
            "Translate paired Sentinel-1 radar images into optical-style colour "
            "views, evaluate image quality and a downstream task, and label the output as synthetic."
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
                "title": "Build paired chips and a simple baseline",
                "summary": "The pairing date gap and geolocation decide whether the task is meaningful.",
                "steps": [
                    "Download a small region of paired Sentinel-1 and Sentinel-2 imagery and record acquisition dates.",
                    "Crop aligned chips at a fixed size and remove pairs with heavy cloud, missing data or a large date gap.",
                    "Build a simple baseline such as a false-colour or histogram-matching translation.",
                    "Create train, validation and spatial test regions so nearby chips cannot leak.",
                ],
            },
            {
                "title": "Train an image-to-image model",
                "summary": "A small pix2pix model is enough to prove the idea on a laptop or free GPU.",
                "steps": [
                    "Train a conditional GAN or U-Net translation model with a reconstruction and adversarial loss.",
                    "Monitor validation SSIM and PSNR and inspect generated chips for blur and invented objects.",
                    "Add a baseline comparison on the same spatial test region.",
                    "Save the checkpoint, normalisation and chip metadata.",
                ],
            },
            {
                "title": "Evaluate beyond pretty pictures",
                "summary": "A downstream task tests whether the generated image preserves useful structure.",
                "steps": [
                    "Report SSIM and PSNR on held-out chips for the model and baseline.",
                    "Train a small land-cover classifier on real optical chips, then test it on generated chips.",
                    "Compare downstream accuracy with the classifier run on a simple baseline image.",
                    "Inspect cases where the generated colours are plausible but wrong.",
                ],
            },
            {
                "title": "Build the interpretation viewer",
                "summary": "The original radar and the synthetic colour view must stay together.",
                "steps": [
                    "Build a side-by-side viewer with radar, generated colour and optional optical reference.",
                    "Add a prominent generated-image label and a short explanation of what colour means.",
                    "Show the date gap and the model version for the selected chip.",
                    "Add a case where the model hallucinates a feature and explain why it happens.",
                ],
            },
            {
                "title": "Document the limits and demo",
                "summary": "The project is about interpretation, not replacing real optical data.",
                "steps": [
                    "Write a model card with paired-data limits, cloud filtering, spatial split and failure modes.",
                    "Explain that generated colour is not ground truth and should not be used alone for decisions.",
                    "Add tests for a missing optical pair, a cloudy chip and an out-of-region image.",
                    "Record a demo with one good translation and one obvious failure.",
                ],
            },
        ],
    ),
    16: dict(
        title="Satellite Frame Interpolation",
        summary=(
            "Generate in-between frames for satellite image sequences so cloud "
            "movement and other time-dependent data look smooth. Compare a "
            "pretrained interpolation model with optical-flow blending and label "
            "every generated frame as synthetic."
        ),
        who_affected=(
            "Weather communicators, remote-sensing analysts and students "
            "learning video interpolation."
        ),
        why_matters=(
            "Weather satellites do not capture every moment. A smooth sequence "
            "can make motion easier to explain, but an invented frame must never "
            "be mistaken for an observation."
        ),
        field="aiml",
        domain="climate",
        difficulty="intermediate",
        est_hours=60,
        tech_tags=[
            "python",
            "pytorch",
            "optical-flow",
            "video",
            "remote-sensing",
            "evaluation",
        ],
        datasets=[
            {"name": "NOAA GOES imagery", "url": "https://www.goes.noaa.gov/"},
            {"name": "JMA Himawari imagery", "url": "https://www.data.jma.go.jp/mscweb/en/himawari89/"},
            {"name": "Vimeo-90K benchmark", "url": "http://toflow.csail.mit.edu/"},
        ],
        approaches=[
            "Build short satellite frame triplets with a held-out middle frame for evaluation.",
            "Implement an optical-flow blending baseline before using a pretrained model.",
            "Measure PSNR and SSIM on held-out frames and inspect cloud motion errors.",
            "Present generated frames with a synthetic label and a comparison to the real frame.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Interpolated frames are synthetic, not observations.",
        original_text=(
            "Interpolate satellite frames with optical flow and a pretrained "
            "model, evaluate held-out frames and label generated frames as synthetic."
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
                "title": "Build a satellite triplet dataset",
                "summary": "The held-out middle frame is the whole evaluation.",
                "steps": [
                    "Download a small weather-satellite sequence and align frames to a common crop and timestamp spacing.",
                    "Create triplets of frame A, middle frame B and frame C, using B only for testing.",
                    "Remove sequences with missing frames, large jumps or heavy artefacts.",
                    "Split by time and region so similar cloud patterns do not leak.",
                ],
            },
            {
                "title": "Build the optical-flow baseline",
                "summary": "A simpler baseline shows whether the learned model earns its complexity.",
                "steps": [
                    "Estimate flow between A and C and blend them to approximate B.",
                    "Handle occlusion and large motion with a documented fallback.",
                    "Measure PSNR and SSIM on the held-out middle frames.",
                    "Inspect where blending produces ghosting or double edges.",
                ],
            },
            {
                "title": "Run a pretrained interpolation model",
                "summary": "Use a small checkpoint and keep the comparison fair.",
                "steps": [
                    "Run a pretrained frame-interpolation model on the same triplets and resolution.",
                    "Measure PSNR and SSIM against the real middle frame and compare with the flow baseline.",
                    "Inspect cloud edges, small features and regions with rapid motion.",
                    "Record inference time per frame on the available hardware.",
                ],
            },
            {
                "title": "Build the labelled viewer",
                "summary": "The user must always know which frame is real.",
                "steps": [
                    "Build a player that shows the original frames and marks interpolated frames in a different colour.",
                    "Add a toggle to compare the generated middle frame with the real held-out frame.",
                    "Show PSNR, SSIM and the model name beside the clip.",
                    "Add a prominent synthetic-frame notice and a link to the data source.",
                ],
            },
            {
                "title": "Analyse failure and document",
                "summary": "Interpolation fails in ways a smooth animation can hide.",
                "steps": [
                    "Report metrics for the model and baseline and show the worst cloud-motion cases.",
                    "Explain that a generated frame is not an observation and must not be used as data.",
                    "Add tests for missing frames, uneven timing and a sequence with almost no motion.",
                    "Record a demo with a good interpolation and a visible ghosting failure.",
                ],
            },
        ],
    ),
    19: dict(
        title="Hyperlocal Weather Prediction & Risk Alerts",
        summary=(
            "Predict short-term local rain or heat risk from satellite and Earth-"
            "observation data. Beat a persistence baseline, score events with hit "
            "rate and false-alarm rate, and turn the output into a simple "
            "location-based alert."
        ),
        who_affected=(
            "Residents, farmers, event organisers and local authorities who need "
            "a short heads-up rather than a long-range forecast."
        ),
        why_matters=(
            "A timely local alert can prevent travel trouble and heat exposure, "
            "but an unreliable alarm quickly loses trust."
        ),
        field="aiml",
        domain="climate",
        difficulty="advanced",
        est_hours=90,
        tech_tags=[
            "python",
            "xarray",
            "pytorch",
            "remote-sensing",
            "time-series",
            "weather",
        ],
        datasets=[
            {"name": "NASA GPM IMERG rainfall", "url": "https://gpm.nasa.gov/data/imerg"},
            {"name": "Copernicus ERA5 reanalysis", "url": "https://cds.climate.copernicus.eu/"},
            {"name": "Open-Meteo API", "url": "https://open-meteo.com/"},
        ],
        approaches=[
            "Choose one hazard, region and forecast horizon before touching the data.",
            "Build a persistence baseline from the latest observation.",
            "Combine recent satellite imagery with weather and terrain features.",
            "Evaluate with event-based hit rate and false-alarm rate, then show an alert.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Estimates are not official alerts or safety advice.",
        original_text=(
            "Predict short-term local rain or heat risk, beat a persistence "
            "baseline with satellite and weather features and show a location alert."
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
                "title": "Scope one hazard and one region",
                "summary": "A narrow forecast target is finishable; a general weather model is not.",
                "steps": [
                    "Choose rain in the next three hours or heat risk for the next day in one region.",
                    "Define the event threshold and the alert threshold with a reason.",
                    "Download a time-aligned sample of satellite, weather and terrain data.",
                    "Hold out a later period and a nearby region for honest testing.",
                ],
            },
            {
                "title": "Build the persistence baseline",
                "summary": "Most short-term forecasts are hard to beat; start from that truth.",
                "steps": [
                    "Predict the next period from the latest observation or a simple seasonal average.",
                    "Compute hit rate, false-alarm rate and a simple error metric on the held-out period.",
                    "Inspect which events the baseline misses and whether they are sudden or gradual.",
                    "Keep the baseline in every later comparison.",
                ],
            },
            {
                "title": "Train a spatiotemporal model",
                "summary": "A small sequence model is enough for a hackathon-scale region.",
                "steps": [
                    "Build features from recent satellite frames, temperature, humidity, wind and terrain.",
                    "Train a gradient-boosting or small sequence model on the training period.",
                    "Compare hit rate and false-alarm rate with persistence on the held-out period.",
                    "Calibrate the alert threshold against a stated false-alarm budget.",
                ],
            },
            {
                "title": "Build the location alert",
                "summary": "The alert must show its time window, confidence and source.",
                "steps": [
                    "Build a simple map or location search with a current risk card.",
                    "Show the forecast horizon, event probability, confidence and data timestamp.",
                    "Add an alert preview with a clear not-an-official-warning notice.",
                    "Include a short explanation of the weather pattern behind the alert.",
                ],
            },
            {
                "title": "Test event behaviour and document",
                "summary": "A model can look good on average and still miss the events people care about.",
                "steps": [
                    "Report hit rate, false-alarm rate and missed-event examples for both models.",
                    "Test a sudden event, a gradual event and a no-event period.",
                    "Explain the limits of satellite latency and the selected region.",
                    "Record a demo that shows one correct alert, one false alarm and the data timestamp.",
                ],
            },
        ],
    ),
    21: dict(
        title="Crop Advisor with Satellite and Weather Data",
        summary=(
            "Recommend suitable crops for a location using soil, rainfall, "
            "temperature and satellite vegetation indices, explain each "
            "suggestion, show uncertainty and test on regions not seen in training."
        ),
        who_affected=(
            "Smallholder farmers, extension officers and cooperatives choosing "
            "what to plant for the coming season."
        ),
        why_matters=(
            "A crop choice affects a whole season of income. A generic "
            "recommendation that ignores local soil and climate can be worse "
            "than no recommendation."
        ),
        field="aiml",
        domain="agriculture",
        difficulty="intermediate",
        est_hours=65,
        tech_tags=[
            "python",
            "scikit-learn",
            "geopandas",
            "remote-sensing",
            "weather",
            "explainability",
        ],
        datasets=[
            {"name": "NASA POWER agroclimate data", "url": "https://power.larc.nasa.gov/"},
            {"name": "Sentinel-2 vegetation indices", "url": "https://dataspace.copernicus.eu/"},
            {"name": "ICRISAT district data", "url": "https://data.icrisat.org/"},
            {"name": "Government soil health records", "url": "https://soilhealth.dac.gov.in/"},
        ],
        approaches=[
            "Join soil, rainfall, temperature and vegetation features at district or farm level.",
            "Train a crop classifier with a region-grouped split, not a random row split.",
            "Explain each recommendation with the crops and features it is closest to.",
            "Report uncertainty and test on regions and seasons not seen during training.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Decision support, not agricultural advice; check every data licence.",
        original_text=(
            "Recommend crops from soil, weather and satellite features with "
            "explanations, uncertainty and region-held-out validation."
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
                "title": "Define a region and a crop label",
                "summary": "Existing crop records are not automatically a recommendation target.",
                "steps": [
                    "Choose a region and a set of crops with enough labelled district records.",
                    "Join soil, rainfall, temperature and vegetation features on a common district or farm key.",
                    "Record the season and year so the model cannot learn a future leak.",
                    "Hold out entire districts and one season for testing.",
                ],
            },
            {
                "title": "Build a baseline and a learned model",
                "summary": "A majority-crop baseline sets the bar for a useful recommendation.",
                "steps": [
                    "Build a baseline that always recommends the most common crop for the region.",
                    "Train a random forest or gradient-boosting classifier on the same features.",
                    "Report accuracy, macro F1 and per-crop recall on the district-held-out set.",
                    "Compare the model with the baseline and inspect regions where it collapses.",
                ],
            },
            {
                "title": "Add explanations and uncertainty",
                "summary": "A recommendation without a reason is hard for an extension officer to trust.",
                "steps": [
                    "Explain a suggestion with the strongest soil, rainfall and temperature factors.",
                    "Show the top two crop options and a confidence or uncertainty estimate.",
                    "Add a refusal or low-confidence state when the location is outside the training region.",
                    "Test the explanation on a known district and check it against agronomist guidance.",
                ],
            },
            {
                "title": "Build the advisor screen",
                "summary": "The screen should make local context visible, not only a crop name.",
                "steps": [
                    "Build a district or map-based form that shows the input soil, weather and vegetation values.",
                    "Display the top crops, confidence and a plain-language reason for each.",
                    "Add a clear decision-support notice and a recommendation to consult a local officer.",
                    "Show the training region and a warning for an unseen location.",
                ],
            },
            {
                "title": "Validate outside the training region",
                "summary": "Region-held-out performance is the honest test of usefulness.",
                "steps": [
                    "Report results for held-out districts and a held-out season.",
                    "Inspect failures caused by unusual soil, irrigation or market preferences.",
                    "Document how the recommendation could reinforce existing crop patterns.",
                    "Record a demo with one confident recommendation and one low-confidence refusal.",
                ],
            },
        ],
    ),
    31: dict(
        title="Scam Message Detector with Explanations",
        summary=(
            "Classify messages as normal or scam, including fake KYC, OTP, "
            "lottery, job and UPI collect patterns, and highlight the words and "
            "structures behind each verdict. Measure precision and recall and "
            "explain the cost of blocking a real message."
        ),
        who_affected=(
            "Mobile users, community help desks and trust-and-safety teams "
            "trying to explain why a message looks suspicious."
        ),
        why_matters=(
            "Scam messages are cheap to send and often imitate a trusted bank or "
            "delivery service. A warning with a reason is easier to act on than "
            "a bare label."
        ),
        field="aiml",
        domain="cybersecurity",
        difficulty="beginner",
        est_hours=40,
        tech_tags=[
            "python",
            "scikit-learn",
            "tf-idf",
            "transformers",
            "explainability",
            "streamlit",
        ],
        datasets=[
            {"name": "UCI SMS Spam Collection", "url": "https://archive.ics.uci.edu/dataset/228/sms+spam+collection"},
            {"name": "Hand-written Indian scam templates", "url": None},
        ],
        approaches=[
            "Combine a public SMS spam set with hand-written, synthetic Indian scam templates.",
            "Train a TF-IDF logistic-regression baseline before trying a small transformer.",
            "Explain verdicts with highlighted words or n-grams and a short reason.",
            "Report precision, recall and the false-positive cost at a chosen threshold.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Use synthetic or public messages only; flags are not proof.",
        original_text=(
            "Detect scam messages, explain the words behind each flag and "
            "measure precision and recall with the cost of false positives."
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
                "title": "Build a safe labelled message set",
                "summary": "Use synthetic scam examples and never collect real people's messages.",
                "steps": [
                    "Download the public SMS spam collection and record its licence.",
                    "Write synthetic Indian scam templates for KYC, OTP, lottery, job and UPI collect cases.",
                    "Create a validation set that includes legitimate bank and delivery messages to test false positives.",
                    "Remove phone numbers, names and links from the sample before training.",
                ],
            },
            {
                "title": "Train an explainable baseline",
                "summary": "TF-IDF plus logistic regression is fast, transparent and hard to beat on small data.",
                "steps": [
                    "Clean text while preserving the cues that matter such as urgency, links and payment requests.",
                    "Train a TF-IDF logistic-regression classifier and report precision, recall and F1 at a chosen threshold.",
                    "Highlight the top positive words or n-grams for a few scam and legitimate messages.",
                    "Inspect false positives and add legitimate examples rather than hiding them.",
                ],
            },
            {
                "title": "Compare a small pretrained model",
                "summary": "A transformer may improve recall, but the explanation must remain useful.",
                "steps": [
                    "Fine-tune or use a small pretrained text model on the same split.",
                    "Compare precision, recall and false positives with the baseline, especially on short messages.",
                    "Use an explanation method such as token attribution and check whether it highlights plausible cues.",
                    "Choose the model based on the cost of blocking a real message, not only accuracy.",
                ],
            },
            {
                "title": "Build the warning interface",
                "summary": "The user needs a reason and a safe next action.",
                "steps": [
                    "Build a paste-a-message screen with a verdict, confidence and highlighted evidence.",
                    "Add a clear reason line such as asks for OTP, creates urgency or contains a shortened link.",
                    "Show a safe next step such as verify through the official app and never share a code.",
                    "Add a human-review note and explain that a flag is not proof of wrongdoing.",
                ],
            },
            {
                "title": "Evaluate and explain the trade-off",
                "summary": "Blocking a real bank message can be more harmful than missing one spam message.",
                "steps": [
                    "Report precision, recall and the false-positive rate on the validation set.",
                    "Show examples of missed scams and blocked legitimate messages.",
                    "Explain how the threshold would change for a warning feature versus automatic blocking.",
                    "Record a demo with one scam, one legitimate message and one uncertain case.",
                ],
            },
        ],
    ),
    33: dict(
        title="Plant Disease Detector: Lab Accuracy vs Field Accuracy",
        summary=(
            "Fine-tune a small image model on leaf disease data, then test it on "
            "real field photos to show the accuracy drop when backgrounds, "
            "lighting and camera quality change. Add an unsure state instead of "
            "guessing."
        ),
        who_affected=(
            "Farmers, agricultural extension workers and students learning how "
            "lab benchmarks fail in the field."
        ),
        why_matters=(
            "A model that scores well on clean lab images can fail on a real "
            "leaf photo. Showing that gap honestly is more useful than another "
            "inflated benchmark."
        ),
        field="aiml",
        domain="agriculture",
        difficulty="beginner",
        est_hours=45,
        tech_tags=[
            "python",
            "pytorch",
            "transfer-learning",
            "computer-vision",
            "distribution-shift",
            "streamlit",
        ],
        datasets=[
            {"name": "PlantVillage", "url": "https://github.com/spMohanty/PlantVillage-Dataset"},
            {"name": "PlantDoc", "url": "https://github.com/pratikkayal/PlantDoc-Dataset"},
        ],
        approaches=[
            "Train on controlled PlantVillage images and keep PlantDoc field images for an honest test.",
            "Compare a frozen-feature baseline with fine-tuning of the last block.",
            "Add augmentation and measure whether it closes part of the field gap.",
            "Use confidence thresholds and an unsure response for low-quality or unfamiliar leaves.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Decision support, not advice; check PlantVillage and PlantDoc licences.",
        original_text=(
            "Train a leaf-disease classifier on lab images, test it on field "
            "photos, measure the accuracy gap and add an unsure state."
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
                "title": "Separate lab and field data",
                "summary": "The field set must stay untouched until the final evaluation.",
                "steps": [
                    "Download PlantVillage and PlantDoc and record their licences and class mappings.",
                    "Map common diseases across the two datasets and drop classes with no fair match.",
                    "Use PlantVillage for training and validation, and PlantDoc only for the field test.",
                    "Create a small unsure set with blur, multiple leaves and a non-leaf object.",
                ],
            },
            {
                "title": "Train a controlled baseline",
                "summary": "Start with the easiest model and the cleanest split.",
                "steps": [
                    "Train a frozen-feature classifier on PlantVillage and record validation accuracy.",
                    "Fine-tune the last block and compare per-class recall, not only top-line accuracy.",
                    "Save the class mapping, image size and model version.",
                    "Inspect validation errors for label noise and duplicated images.",
                ],
            },
            {
                "title": "Measure the field gap",
                "summary": "The drop is the headline result, not a reason to hide the model.",
                "steps": [
                    "Evaluate the same model on PlantDoc without training on it.",
                    "Report lab accuracy, field accuracy and the per-class collapse.",
                    "Inspect field photos that fail because of background, lighting, occlusion or camera blur.",
                    "Add augmentation and retrain once to show whether the gap narrows.",
                ],
            },
            {
                "title": "Add uncertainty and build the app",
                "summary": "A field photo often does not contain enough evidence for a confident answer.",
                "steps": [
                    "Calibrate confidence and choose a threshold that prioritises avoiding confident wrong answers.",
                    "Add an unsure response with a prompt to take a clearer photo or ask an expert.",
                    "Build a simple upload screen with the leaf image, predicted disease and top alternatives.",
                    "Show the lab-versus-field result beside the prediction so the user understands the limit.",
                ],
            },
            {
                "title": "Tell the honest evaluation story",
                "summary": "The project is strongest when the field failure is visible.",
                "steps": [
                    "Report the full lab-to-field accuracy drop and the confusion changes.",
                    "Show one correct field prediction, one wrong field prediction and one unsure case.",
                    "Explain why a lab benchmark is not a field deployment result.",
                    "Write the demo script and include the agricultural decision-support notice.",
                ],
            },
        ],
    ),
    44: dict(
        title="Bird Call Identifier (Bioacoustics)",
        summary=(
            "Identify bird species from recordings by converting audio to "
            "spectrograms, fine-tuning a pretrained audio model and handling "
            "background noise plus recordings with several birds. Return a ranked "
            "species list with confidence."
        ),
        who_affected=(
            "Birdwatchers, ecology students, conservation volunteers and "
            "researchers processing field recordings."
        ),
        why_matters=(
            "Manual review of long field recordings is slow. A ranked shortlist "
            "can help experts focus, but uncertain predictions must not be "
            "treated as verified sightings."
        ),
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=60,
        tech_tags=[
            "python",
            "pytorch",
            "audio",
            "spectrograms",
            "transfer-learning",
            "multi-label",
        ],
        datasets=[
            {"name": "Xeno-canto recordings", "url": "https://xeno-canto.org/"},
            {"name": "BirdCLEF datasets", "url": "https://www.kaggle.com/competitions/birdclef-2024"},
        ],
        approaches=[
            "Convert clips to mel spectrograms and split by recording or recordist.",
            "Fine-tune a small pretrained audio model and compare it with a spectrogram CNN baseline.",
            "Treat noisy or multi-bird clips as multi-label cases rather than forcing one answer.",
            "Report top-1 and top-5 accuracy plus confidence calibration.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Check each recording licence; predictions need expert verification.",
        original_text=(
            "Identify bird species from audio, handle noise and multi-bird "
            "clips and return a ranked list with confidence."
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
                "title": "Collect audio and define the label scope",
                "summary": "A small, well-labelled species set is better than a huge noisy one.",
                "steps": [
                    "Choose 10-20 species with enough recordings and clear licence terms.",
                    "Download clips through the Xeno-canto API or a BirdCLEF subset and record the licence per clip.",
                    "Split by recording and recordist so the same bird does not appear in train and test.",
                    "Create a background-noise class and a multi-bird validation sample.",
                ],
            },
            {
                "title": "Build spectrograms and a baseline",
                "summary": "The time-frequency representation is the core feature.",
                "steps": [
                    "Convert clips to mel spectrograms with a fixed duration and normalisation.",
                    "Train a small CNN baseline and report top-1 and top-5 accuracy.",
                    "Inspect errors from rain, wind, insects and distant calls.",
                    "Save the audio preprocessing settings with the model.",
                ],
            },
            {
                "title": "Fine-tune a pretrained audio model",
                "summary": "Transfer learning helps when the species set is small.",
                "steps": [
                    "Fine-tune a pretrained audio or spectrogram model on the same split.",
                    "Compare top-1, top-5 and calibration with the CNN baseline.",
                    "Evaluate multi-label clips and report which species are confused.",
                    "Measure inference time for a short clip.",
                ],
            },
            {
                "title": "Build the ranked identification view",
                "summary": "The shortlist and confidence are more useful than a single label.",
                "steps": [
                    "Build an upload screen that shows the spectrogram and a ranked species list.",
                    "Show confidence, the top three alternatives and a low-confidence warning.",
                    "Keep a prominent note that predictions are estimates and need expert verification.",
                    "Add a sample multi-bird clip where the model returns more than one plausible species.",
                ],
            },
            {
                "title": "Evaluate noise and document",
                "summary": "Field audio is the real test, not a clean benchmark.",
                "steps": [
                    "Report accuracy on clean, noisy and multi-bird subsets separately.",
                    "Inspect top confusions and whether they are visually similar species or recording artefacts.",
                    "Document the species scope, licence trail and verification requirement.",
                    "Record a demo with one clear call, one noisy clip and one uncertain result.",
                ],
            },
        ],
    ),
    45: dict(
        title="Galaxy Morphology Classifier with Uncertainty",
        summary=(
            "Classify galaxy shapes such as spiral, elliptical, merging and edge-"
            "on from telescope images using crowd-sourced labels. Train on vote "
            "fractions instead of single labels, report uncertainty and flag "
            "galaxies where the model and the crowd disagree."
        ),
        who_affected=(
            "Astronomy researchers, citizen-science volunteers and students "
            "working with large image catalogues."
        ),
        why_matters=(
            "Volunteers often disagree on ambiguous galaxies. Treating one vote "
            "as truth hides that uncertainty and makes the model look more "
            "certain than the evidence allows."
        ),
        field="aiml",
        domain="other",
        difficulty="intermediate",
        est_hours=65,
        tech_tags=[
            "python",
            "pytorch",
            "astronomy",
            "soft-labels",
            "uncertainty",
            "transfer-learning",
        ],
        datasets=[
            {"name": "Galaxy Zoo data releases", "url": "https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/"},
            {"name": "Sloan Digital Sky Survey images", "url": "https://www.sdss.org/"},
        ],
        approaches=[
            "Build a labelled sample from Galaxy Zoo vote fractions and SDSS images.",
            "Train a small image model with a soft-label loss rather than majority labels only.",
            "Estimate uncertainty and compare it with volunteer disagreement.",
            "Flag high-disagreement galaxies and model-crowd disagreements for expert review.",
        ],
        source_name="MANABI Curated",
        source_note="Curated AI/ML hackathon brief. Check Galaxy Zoo and SDSS terms before use.",
        original_text=(
            "Classify galaxy morphology from crowd vote fractions, estimate "
            "uncertainty and flag cases that need expert review."
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
                "title": "Build images with soft labels",
                "summary": "The vote fraction is the label; do not throw that information away.",
                "steps": [
                    "Download Galaxy Zoo labels and matching SDSS images for a small, balanced sample.",
                    "Keep the vote fractions for each morphology class and the total vote count.",
                    "Remove galaxies with very few votes or missing images.",
                    "Split by galaxy id and record the class mapping.",
                ],
            },
            {
                "title": "Train a soft-label baseline",
                "summary": "A simple CNN can learn vote fractions with a suitable loss.",
                "steps": [
                    "Train a small pretrained CNN with a soft cross-entropy or KL loss against the vote fractions.",
                    "Compare it with a hard-label model trained on the majority class.",
                    "Report top-1 agreement and a proper scoring metric such as log loss or Brier score.",
                    "Inspect examples where the model is confident but the crowd is divided.",
                ],
            },
            {
                "title": "Add uncertainty and disagreement flags",
                "summary": "Uncertainty is the product differentiator here.",
                "steps": [
                    "Estimate predictive uncertainty with an ensemble or a calibrated softmax.",
                    "Compare predicted uncertainty with the entropy of the crowd vote fractions.",
                    "Flag galaxies where the model and crowd disagree or both are uncertain.",
                    "Add a simple threshold for expert review rather than hiding the ambiguous cases.",
                ],
            },
            {
                "title": "Build the review gallery",
                "summary": "A reviewer needs the image, the vote distribution and the model's view together.",
                "steps": [
                    "Build a gallery with the galaxy image, crowd fractions, model probabilities and uncertainty.",
                    "Add filters for high confidence, high disagreement and review candidates.",
                    "Let a reviewer mark a case as agree, disagree or needs-expert without overwriting the crowd label.",
                    "Show a clear note that the model is an aid, not a replacement for visual inspection.",
                ],
            },
            {
                "title": "Evaluate and document the labels",
                "summary": "Crowd labels are not ground truth; the report should say so.",
                "steps": [
                    "Report agreement, log loss and calibration on the held-out galaxies.",
                    "Show examples where the vote fraction is more informative than the majority label.",
                    "Explain the limits of volunteer labels, image resolution and class definitions.",
                    "Record a demo with a clear spiral, a merging galaxy and an uncertain review case.",
                ],
            },
        ],
    ),
}


STATEMENTS = {
    1: (
        "Build a detector for fake reviews that combines suspicious wording "
        "with reviewer behaviour such as posting bursts and one-product "
        "histories. Show a product trust score, the reasons behind each flag "
        "and any reviewer cluster that posts together.\n\n"
        "Flags are signals for human review, not proof of wrongdoing. Use "
        "synthetic or properly licensed data."
    ),
    2: (
        "Build an anomaly detector that learns what a good product looks like "
        "from images and highlights scratches, cracks or missing parts. Compare "
        "a simple autoencoder with a stronger method and show a heatmap for "
        "every prediction.\n\n"
        "Report image-level and pixel-level AUROC, the false-alarm rate at a "
        "fixed defect recall, and inference time per image."
    ),
    3: (
        "Build an OCR pipeline that reads product packaging photos and extracts "
        "weight, volume and quantity into a consistent schema. Normalise units "
        "and say cannot tell when the value is not visible instead of guessing.\n\n"
        "Report field-level exact-match accuracy, numeric error and the correct-"
        "abstention rate."
    ),
    5: (
        "Build a low-bandwidth tutor that answers from openly licensed course "
        "material and cites the source behind every answer. Add a translation "
        "step, a refusal path when retrieval is weak and a teacher view of "
        "struggle topics.\n\n"
        "Measure answer accuracy, citation support, page weight and response "
        "time on a throttled connection."
    ),
    6: (
        "Build a guarded payment-support agent that handles routine help in test "
        "mode, escalates refunds and disputes to a person and logs every tool "
        "call. Treat customer text as untrusted and use idempotency keys for "
        "every payment action.\n\n"
        "Test mode only. Never use real money, real cards or real customer data."
    ),
    7: (
        "Build a converter that turns a consented social post and its images "
        "into a structured product listing with title, category, price, "
        "quantity and variants. Mark low-confidence fields for seller review "
        "beside the original evidence.\n\n"
        "Use synthetic, public or consented data only. Measure field accuracy "
        "and listing time against manual entry."
    ),
    8: (
        "Build a waste-photo classifier that maps an item to a local wet, dry "
        "or recyclable bin and says not sure when the image is ambiguous. "
        "Fine-tune a small image model and study which mistakes would "
        "contaminate recycling.\n\n"
        "Show a confusion matrix, per-bin recall and the not-sure rate."
    ),
    9: (
        "Build a graph of accounts, devices, phones, addresses and transfers, "
        "then surface suspicious communities such as many accounts on one device "
        "or circular money flow. Compare rules and community detection with a "
        "graph model.\n\n"
        "Flags are signals for human review, not proof. Use synthetic or "
        "properly licensed data and report ring-level precision and recall."
    ),
    10: (
        "Build a phone-sensor model that recognises walking, running, sitting "
        "and falling, then alerts a caregiver after a likely fall. Add a "
        "stillness check so a dropped phone does not trigger an alarm.\n\n"
        "Estimates can be wrong and are not a safety system. Use public or "
        "consented data only and report false alarms per hour."
    ),
    11: (
        "Build a lab-report explainer that extracts test values, units and "
        "reference ranges, flags out-of-range results and explains them in plain "
        "language with sources. It never diagnoses and it refuses when a test "
        "or range is unknown.\n\n"
        "Educational tool only. Use synthetic reports and tell users to talk to "
        "a qualified doctor."
    ),
    12: (
        "Downscale coarse satellite air-quality maps into finer local estimates "
        "using ground stations, weather, roads, land use and elevation. Validate "
        "by hiding whole stations and show uncertainty on the map.\n\n"
        "Predictions are estimates, not official measurements or health advice."
    ),
    13: (
        "Build a deepfake video detector that combines frame artifacts with "
        "temporal inconsistency. Train on one dataset, test on another and show "
        "the generalisation gap plus the evidence the model used.\n\n"
        "Results are probabilistic, not proof. Do not use them to accuse a real "
        "person."
    ),
    14: (
        "Build a paper-form digitizer that extracts fields, validates dates and "
        "codes and sends low-confidence values to a quick review screen. Keep "
        "the original crop beside every corrected field.\n\n"
        "Use synthetic forms with fake data only. Measure field accuracy before "
        "and after review and time per form."
    ),
    15: (
        "Translate radar satellite images into optical-style colour images to "
        "make terrain easier to read. Compare a simple baseline with an image-to-"
        "image model and evaluate SSIM, PSNR plus a downstream land-cover task.\n\n"
        "Generated colours can be wrong. Label every output as an interpretation "
        "aid, not ground truth."
    ),
    16: (
        "Generate in-between frames for satellite sequences so cloud motion "
        "looks smoother. Compare optical-flow blending with a pretrained model "
        "on held-out middle frames and show a labelled viewer.\n\n"
        "Interpolated frames are synthetic, not observations. Label them "
        "clearly and report PSNR and SSIM."
    ),
    18: (
        "Build an exoplanet transit detector that cleans light curves, searches "
        "for periodic dips and classifies candidates against false positives. "
        "Validate with star-grouped splits and a known-planet recovery check.\n\n"
        "Report precision, recall, F1 and PR-AUC, and explain the main false-"
        "positive causes."
    ),
    19: (
        "Predict short-term local rain or heat risk from satellite and weather "
        "data, beat a persistence baseline and show a location-based alert with "
        "its time window and confidence.\n\n"
        "Estimates can be wrong and are not a substitute for official alerts or "
        "safety systems."
    ),
    20: (
        "Screen public orbital elements for close approaches, rank events by "
        "risk and compare a learned risk model with a distance-only rule. Show "
        "the closest-approach time, distance and relative velocity.\n\n"
        "Estimates can be wrong and are not official collision warnings. Report "
        "recall at a fixed false-alarm rate and screening throughput."
    ),
    21: (
        "Recommend crops from soil, rainfall, temperature and satellite "
        "vegetation data, explain each suggestion and test on regions not seen "
        "in training.\n\n"
        "Decision support, not advice. Show uncertainty and tell users to check "
        "with a local agricultural officer."
    ),
    23: (
        "Build a farming assistant that reads a soil report, adds satellite and "
        "weather context and answers questions from verified guidance with "
        "citations. Refuse when the evidence is weak.\n\n"
        "Decision support, not advice. Present satellite and weather inputs as "
        "estimates and keep local experts in the loop."
    ),
    24: (
        "Build an engineering copilot that answers specification questions with "
        "exact citations, checks whether each passage supports the claim and "
        "drafts documentation from structured data.\n\n"
        "A learning aid, not a replacement for source documents. Report recall, "
        "verified-citation rate and latency."
    ),
    29: (
        "Build an engineering problem-solving agent that calls unit-aware "
        "calculation and domain tools, shows its constraints and verifies its "
        "own answer before replying.\n\n"
        "Estimates can be wrong and are not a substitute for official "
        "engineering or safety decisions. Report solve rate and failure types."
    ),
    31: (
        "Build a scam-message detector for fake KYC, OTP, lottery, job and UPI "
        "collect messages. Highlight the words and patterns behind each verdict "
        "and measure the cost of blocking a real message.\n\n"
        "Flags are signals for human review, not proof. Use synthetic or "
        "properly licensed messages only."
    ),
    33: (
        "Train a leaf-disease classifier on clean lab images, then test it on "
        "real field photos and show the accuracy drop. Add augmentation and an "
        "unsure state instead of forcing a guess.\n\n"
        "Decision support, not advice. The field gap is the result; report it "
        "honestly."
    ),
    40: (
        "Build a playable board-game AI with minimax, alpha-beta pruning and "
        "Monte Carlo Tree Search. Run a tournament against a random player and "
        "show win rate, positions searched and time per move.\n\n"
        "Add difficulty levels and a search view that marks the chosen line and "
        "pruned branches."
    ),
    41: (
        "Train a reinforcement-learning traffic-signal controller in simulation "
        "and compare it with fixed-timing and rule-based controllers. Test it "
        "on demand patterns it has not seen.\n\n"
        "Simulation only. Report waiting time, queue length, throughput and how "
        "much of the gain survives the shift."
    ),
    44: (
        "Identify bird species from recordings by turning audio into "
        "spectrograms and fine-tuning a pretrained model. Handle noisy and "
        "multi-bird clips and return a ranked list with confidence.\n\n"
        "Predictions are estimates and need expert verification. Check each "
        "recording's licence."
    ),
    45: (
        "Classify galaxy shapes from telescope images using crowd vote "
        "fractions instead of single labels. Report uncertainty and flag "
        "galaxies where the model and volunteers disagree.\n\n"
        "Show the vote distribution and model probabilities together, and keep "
        "a clear expert-review path."
    ),
}
