"""Learning-only briefs and concepts for the Web Dev learning pack.

Most learning projects already exist as resume or hackathon briefs. This module
adds the twelve projects that only appear on the learning track, then records
the concepts every learning brief should teach.
"""

LEARNING_ONLY = {
    16: dict(
        title="Expense Splitter with Debt Simplification",
        summary=(
            "Build a small web app that tracks shared costs for trips, flats or events. "
            "People add an expense, choose who paid and who shares it, and the app keeps "
            "each person's balance. At the end it shows the smallest set of payments that "
            "settles everyone.\n\n"
            "The learning value is the money model. Store amounts as integers in the "
            "smallest currency unit, keep every split as its own record, and test the "
            "settlement algorithm against hand-worked examples. Add a payment link only "
            "as a convenience, not as a real payment integration."
        ),
        who_affected=(
            "Roommates, trip groups and friends who share costs and lose track of who "
            "owes whom."
        ),
        why_matters=(
            "Shared expenses often end in messy spreadsheets and awkward reminders. A "
            "clear balance and a short settlement plan make it easy to pay and move on."
        ),
        field="web-dev",
        domain="fintech",
        difficulty="beginner",
        est_hours=24,
        tech_tags=["typescript", "react", "sqlite", "vitest", "payments"],
        datasets=[{"name": "Sample group expenses", "url": None}],
        approaches=[
            "Model groups, members, expenses, payers and per-person shares as separate records.",
            "Store every amount as an integer in the smallest currency unit and round only when showing totals.",
            "Calculate each member's net balance, then reduce the number of transfers with a min-cash-flow pass.",
            "Show the working balance beside the settlement plan so users can check the result.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Log shared expenses, split them equally or by custom amounts, and minimise "
            "the number of payments needed to settle everyone with a min-cash-flow "
            "algorithm. Include a payment link for settling up."
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
                "title": "Model money before you build screens",
                "summary": "Most expense apps fail on rounding, not on layout.",
                "steps": [
                    "Write down a group, a member, an expense, a payer and a share as separate ideas.",
                    "Choose integer minor units for money and write the rounding rule before coding.",
                    "Draw the balance formula for one expense with three people.",
                    "List explicit non-goals such as live bank payments and foreign exchange.",
                ],
            },
            {
                "title": "Create groups and expenses",
                "summary": "Get the plain data entry path correct first.",
                "steps": [
                    "Build a group page with members and a simple invite code.",
                    "Add an expense form for amount, payer, date, note and participants.",
                    "Support equal splits first, then exact amounts and percentage splits.",
                    "Validate that split shares always add up to the full expense.",
                ],
            },
            {
                "title": "Calculate balances and settle up",
                "summary": "The algorithm is the part worth explaining.",
                "steps": [
                    "Compute each member's paid total and owed total from the stored shares.",
                    "Turn those totals into a net balance list with positive and negative sides.",
                    "Implement a greedy min-cash-flow pass that matches the largest debtor with the largest creditor.",
                    "Check the settlement against at least three hand-worked examples, including a three-way cycle.",
                ],
            },
            {
                "title": "Make the balances easy to trust",
                "summary": "A number without a trail looks like a guess.",
                "steps": [
                    "Show every member's paid, owed and net amount on one screen.",
                    "Add an expense history that explains how each balance changed.",
                    "Show the settlement plan as a short list of payments with a copy action.",
                    "Handle deleted expenses and edited shares without leaving stale balances.",
                ],
            },
            {
                "title": "Test edge cases and ship a demo",
                "summary": "Small money bugs become trust bugs.",
                "steps": [
                    "Test one-person groups, zero-cost expenses, repeated payers and uneven splits.",
                    "Add a property-style test that every settlement returns all balances to zero.",
                    "Seed a demo trip with a deliberate cycle so the simplification is visible.",
                    "Deploy the app and write down the data reset command for the next demo.",
                ],
            },
        ],
    ),
    17: dict(
        title="Personal Portfolio Website",
        summary=(
            "Build a fast, accessible portfolio with your bio, skills and a small set of "
            "project write-ups. Keep the content in Markdown or JSON so the site is easy "
            "to update. Add a contact form, a project index and a dark mode that respects "
            "the user's system setting.\n\n"
            "The project is not the template. The learning comes from measuring it: set "
            "Lighthouse targets, check keyboard navigation, test on a narrow screen and "
            "fix what fails. A portfolio with real numbers and a short case study is more "
            "convincing than a gallery of screenshots."
        ),
        who_affected=(
            "Students, career switchers and early-career developers who need a clear place "
            "to show their work."
        ),
        why_matters=(
            "A portfolio gives a reviewer a fast way to understand what you built and how "
            "you think. A slow or inaccessible site sends the wrong signal."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=30,
        tech_tags=["html", "css", "typescript", "vite", "accessibility", "lighthouse"],
        datasets=[],
        approaches=[
            "Define the pages and content model before choosing a framework.",
            "Write semantic HTML, then add a small responsive style system with tokens.",
            "Keep project case studies short: problem, what you built, your part and the result.",
            "Measure performance and accessibility, then fix the largest issues rather than chasing a perfect score.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Build a fast, accessible, deployed portfolio with your bio, skills and "
            "projects. Set measurable targets for Lighthouse scores, keyboard "
            "accessibility, responsive layout, content from Markdown or JSON, a contact "
            "form and dark mode."
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
                "title": "Decide what the portfolio is for",
                "summary": "A portfolio is a short argument, not an archive.",
                "steps": [
                    "Write the one sentence you want a reviewer to remember.",
                    "Pick three projects that support that sentence and drop the rest.",
                    "Choose a content shape for each project: problem, build, role, result.",
                    "Set measurable targets for mobile layout, keyboard access and page weight.",
                ],
            },
            {
                "title": "Build the content and structure",
                "summary": "Content first keeps the design honest.",
                "steps": [
                    "Store bio and project entries in Markdown or JSON and load them at build time.",
                    "Create the home, project index and project detail pages.",
                    "Write the project copy in plain language and remove generic skill lists.",
                    "Add a contact form with a clear success and error state.",
                ],
            },
            {
                "title": "Style it for real screens",
                "summary": "The layout should work on a phone before it looks clever on a desktop.",
                "steps": [
                    "Define spacing, type and colour tokens in one place.",
                    "Build the mobile layout first, then add wider breakpoints.",
                    "Add a dark theme that follows the system setting and can be overridden.",
                    "Check focus states, link contrast and tap target sizes as you go.",
                ],
            },
            {
                "title": "Measure accessibility and speed",
                "summary": "Use the reports as a to-do list, not a scoreboard.",
                "steps": [
                    "Run Lighthouse on a production build and record the three weakest checks.",
                    "Navigate the whole site with only a keyboard and fix any trap or skipped control.",
                    "Compress images and remove unused scripts until the first view is fast on a slow connection.",
                    "Test with a screen reader for headings, landmarks and form labels.",
                ],
            },
            {
                "title": "Deploy and keep it current",
                "summary": "A portfolio needs a simple update path or it goes stale.",
                "steps": [
                    "Deploy with a static host and set a custom domain if you have one.",
                    "Add basic analytics or server logs that do not track personal data.",
                    "Write a short README that explains how to add a project.",
                    "Add one new case study after the next project you finish.",
                ],
            },
        ],
    ),
    18: dict(
        title="Developer News Aggregator",
        summary=(
            "Build a daily digest that reads posts from open sources such as RSS feeds, "
            "the Hacker News API and Dev.to. Normalize each item, remove duplicates, group "
            "stories by topic and let the reader save items for later.\n\n"
            "The useful learning is in the pipeline. Fetch on a schedule, cache responses, "
            "handle rate limits and bad feeds, and keep the digest readable when one source "
            "is down. Do not scrape a source that forbids it."
        ),
        who_affected=(
            "Developers who want one short, filtered reading list instead of checking "
            "several sites every morning."
        ),
        why_matters=(
            "Important posts are mixed with noise and repeated links. A small personal "
            "digest saves time and makes the sources behind each item clear."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=30,
        tech_tags=["typescript", "react", "rss", "hacker-news-api", "sqlite", "caching"],
        datasets=[{"name": "Sample RSS and API responses", "url": None}],
        approaches=[
            "Write one adapter per source and normalize every item into the same shape.",
            "Deduplicate by canonical URL, title and a normalized text fingerprint.",
            "Group items by topic with simple tag rules before trying any model.",
            "Cache source responses and show the last refresh time for each feed.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Fetch posts from open sources such as RSS feeds, the Hacker News API and "
            "Dev.to, remove duplicates, group them by topic and show a daily digest with "
            "filters and a saved-items list."
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
                "title": "Pick sources and define one item shape",
                "summary": "Every source has its own quirks. Hide them behind one record.",
                "steps": [
                    "Choose three open sources and read their usage rules.",
                    "Define an item with title, url, source, published time, summary and tags.",
                    "Write a small adapter for each source and keep network code out of the UI.",
                    "Record a fixture for each adapter so tests do not need the live service.",
                ],
            },
            {
                "title": "Build the fetch and cache path",
                "summary": "A digest should still render when one source fails.",
                "steps": [
                    "Fetch each source on a schedule and store the raw response with a timestamp.",
                    "Add timeouts, retries with backoff and a per-source error state.",
                    "Cache normalized items in SQLite or another local store.",
                    "Show the last successful refresh and the failing source on the page.",
                ],
            },
            {
                "title": "Deduplicate and group",
                "summary": "The same story often arrives from three feeds.",
                "steps": [
                    "Normalize URLs by removing tracking parameters and trailing slashes.",
                    "Compare titles with a simple text fingerprint before grouping.",
                    "Assign topics with a small rule list and let the user correct them.",
                    "Keep one canonical item with links to every source that carried it.",
                ],
            },
            {
                "title": "Build the digest and saved list",
                "summary": "The reading experience matters more than the number of sources.",
                "steps": [
                    "Build a daily view sorted by publish time with a source label on every item.",
                    "Add topic and source filters plus a short search field.",
                    "Let the user save an item and keep saved items after a reload.",
                    "Add an empty state for slow news days and a clear source error state.",
                ],
            },
            {
                "title": "Test the pipeline end to end",
                "summary": "The hard cases are duplicates, bad dates and dead feeds.",
                "steps": [
                    "Test a duplicate story from two sources and confirm one card appears.",
                    "Test a malformed feed, a timeout and a rate-limit response.",
                    "Check that saved items do not disappear when a fetch fails.",
                    "Write a short README that lists every source and its licence or terms.",
                ],
            },
        ],
    ),
    20: dict(
        title="Concert Buddy Finder (Chrome Extension)",
        summary=(
            "Build a Chrome extension that detects the artist or track you are listening "
            "to and shows opted-in people with similar taste. Use public listening data "
            "from a service such as ListenBrainz or Last.fm, not scraped playlists. Keep "
            "the first version to one browser and one data source.\n\n"
            "Matching strangers needs care. Make every profile opt-in, hide precise "
            "location, and add block and report actions before the matching feature. "
            "Explain what the extension reads and when it sends anything to a server."
        ),
        who_affected=(
            "Music fans who want to find people with similar taste without posting their "
            "whole listening history in public."
        ),
        why_matters=(
            "Music is an easy way to start a conversation, but most recommendation apps "
            "push public profiles and location. A small opt-in tool can make the same "
            "connection with less exposure."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=35,
        tech_tags=["typescript", "chrome-extension", "listenbrainz", "lastfm", "privacy"],
        datasets=[{"name": "Sample public listening data", "url": None}],
        approaches=[
            "Build a manifest v3 extension with a popup, a background worker and minimal content scripts.",
            "Read the current track from one permitted source and map it to a stable artist and track id.",
            "Match users on shared artists and listening recency instead of exact playlists.",
            "Make profiles opt-in and add block, report and delete controls before any match is shown.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "A Chrome extension that detects the artist or song you are listening to and "
            "shows opted-in users with similar taste, using open listening data such as "
            "ListenBrainz or Last.fm instead of scraping anyone's playlists."
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
                "title": "Design the extension boundary",
                "summary": "A browser extension gets more access than a normal page. Keep it small.",
                "steps": [
                    "List the exact browser permission each feature needs and drop the rest.",
                    "Draw the popup, background worker and server responsibilities on one page.",
                    "Choose one listening data source and read its terms and rate limits.",
                    "Write a privacy note that says what is read, stored and shared.",
                ],
            },
            {
                "title": "Read the current track",
                "summary": "The extension should fail quietly when it cannot identify a track.",
                "steps": [
                    "Use the smallest permitted content script or API to detect the current artist and track.",
                    "Normalize the artist and title, then look up a stable id from the chosen data source.",
                    "Cache a mapping so repeated lookups do not hit the API every time.",
                    "Show a clear unknown-track state instead of a wrong match.",
                ],
            },
            {
                "title": "Build opt-in matching",
                "summary": "A match is only acceptable when both people chose to appear.",
                "steps": [
                    "Create an opt-in profile with a display name, a short bio and no precise location.",
                    "Score similarity from shared artists and recent listening, then explain the shared artists.",
                    "Add block, report and delete-profile actions before showing a person's card.",
                    "Rate-limit profile views and never expose a user who has not opted in.",
                ],
            },
            {
                "title": "Package and test the extension",
                "summary": "Extensions break when permissions or worker lifecycles change.",
                "steps": [
                    "Load the unpacked extension in Chrome and test the full path from track detection to a match.",
                    "Test the no-login, no-track and blocked-user states.",
                    "Check that the background worker restarts without losing the session.",
                    "Write install and privacy notes for the store listing.",
                ],
            },
            {
                "title": "Run a small honest trial",
                "summary": "Ask a few people to use it before adding more sources.",
                "steps": [
                    "Invite five to ten people and watch where the opt-in flow confuses them.",
                    "Record the most common failed track lookup and fix that source first.",
                    "Remove any feature that needs data you cannot explain or justify.",
                    "Decide whether the project is ready for a public listing or should stay a local demo.",
                ],
            },
        ],
    ),
    21: dict(
        title="Playlist Remix Finder",
        summary=(
            "Build a tool that takes a list of songs and finds remixes, edits, live "
            "versions and alternate recordings for each one. Use open music metadata such "
            "as MusicBrainz, show why each result matched, and export the final list as "
            "text or an M3U file.\n\n"
            "Music metadata is messy. Different releases use different titles, and one "
            "song can have many versions. Normalize titles, keep the original query beside "
            "every result, and let the user reject a bad match. Cache lookups so the tool "
            "stays inside the service limits."
        ),
        who_affected=(
            "Listeners and DJs who want alternate versions of a playlist without hunting "
            "through several music sites."
        ),
        why_matters=(
            "Alternate versions are hard to find because titles and releases vary. A "
            "transparent matcher saves time and helps people discover versions they would "
            "otherwise miss."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=25,
        tech_tags=["typescript", "react", "musicbrainz", "api", "caching", "m3u"],
        datasets=[{"name": "Sample playlist and MusicBrainz responses", "url": None}],
        approaches=[
            "Parse pasted text into artist and track pairs and show uncertain lines before searching.",
            "Query MusicBrainz for recordings and releases, then group results by relationship and title.",
            "Score each candidate with title similarity, artist match and version keywords.",
            "Cache lookups and let the user accept or reject every proposed match.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Paste a list of songs and find remixes, edits and alternate versions of each, "
            "using open music metadata such as MusicBrainz, then export the result as a "
            "shareable list or an M3U file."
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
                "title": "Parse the input without guessing",
                "summary": "Bad input creates bad matches, so show the parse result first.",
                "steps": [
                    "Choose a simple input format such as one song per line or a pasted numbered list.",
                    "Split artist and title with a small set of rules and flag ambiguous lines.",
                    "Let the user correct a line before any lookup starts.",
                    "Show a preview of the parsed list with counts.",
                ],
            },
            {
                "title": "Query the music metadata",
                "summary": "One API call should return enough context to explain a match.",
                "steps": [
                    "Read the MusicBrainz usage rules and set a descriptive user agent.",
                    "Search for a recording, then fetch releases and relationships for the best candidates.",
                    "Store the raw response and a timestamp so repeat searches are fast.",
                    "Handle no-result, rate-limit and timeout responses with different messages.",
                ],
            },
            {
                "title": "Match and rank versions",
                "summary": "A remix result is useful only if the user can see why it matched.",
                "steps": [
                    "Normalize case, punctuation, featured artists and common version words.",
                    "Score a candidate on title similarity, artist match and explicit version type.",
                    "Group candidates by version family and label each one as remix, edit, live or alternate.",
                    "Show the original query beside every result and allow a manual override.",
                ],
            },
            {
                "title": "Build the review and export flow",
                "summary": "The user should leave with a list they chose, not a list the tool guessed.",
                "steps": [
                    "Add accept, reject and replace actions for each proposed match.",
                    "Show a final playlist with source links and release details.",
                    "Export a plain text list and a valid M3U file.",
                    "Keep the reviewed list after a reload until the user clears it.",
                ],
            },
            {
                "title": "Test coverage and limits",
                "summary": "Music databases are large, inconsistent and rate-limited.",
                "steps": [
                    "Test titles with remix tags, featured artists, punctuation and non-Latin scripts.",
                    "Test a track with no alternate versions and a track with too many.",
                    "Verify that cached results do not change when the network is offline.",
                    "Measure lookup time and add throttling before the demo.",
                ],
            },
        ],
    ),
    25: dict(
        title="HTTP Server From Scratch",
        summary=(
            "Write an HTTP/1.1 server on raw sockets. Accept connections, parse request "
            "lines and headers, serve static files, route a few paths and keep connections "
            "alive. Add a small test suite that checks correct responses and malformed "
            "requests.\n\n"
            "The goal is to understand the protocol every web app depends on. Do not use a "
            "framework for the core path. Read the request as bytes, find the header "
            "boundary, parse fields safely and write a response with the right status, "
            "headers and body length."
        ),
        who_affected=(
            "Developers who use web frameworks every day but have never handled a request "
            "at the socket level."
        ),
        why_matters=(
            "Protocol knowledge makes debugging, performance work and framework behaviour "
            "much less mysterious. A small server makes the request and response cycle "
            "concrete."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="intermediate",
        est_hours=50,
        tech_tags=["python", "sockets", "tcp", "http", "pytest"],
        datasets=[{"name": "Sample static site and request fixtures", "url": None}],
        approaches=[
            "Start with a TCP listener that reads a request until the header terminator.",
            "Parse the method, target, version and headers with strict limits and clear errors.",
            "Serve static files with safe path resolution, content type and content length.",
            "Add routes and keep-alive, then test with a real client and malformed input.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Write an HTTP/1.1 server on raw sockets that parses requests, serves static "
            "files, supports routing and keep-alive connections, and passes a "
            "conformance-style test suite."
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
                "title": "Open a socket and read bytes",
                "summary": "The first working version only needs to accept one connection.",
                "steps": [
                    "Create a TCP listener on a local port and accept one connection.",
                    "Read incoming bytes into a fixed-size buffer until the header terminator appears.",
                    "Print the raw request so you can see line endings and byte boundaries.",
                    "Close the connection cleanly after the response.",
                ],
            },
            {
                "title": "Parse the request",
                "summary": "A parser must reject bad input without crashing.",
                "steps": [
                    "Split the request line into method, target and version.",
                    "Parse header names and values case-insensitively and reject duplicate invalid lines.",
                    "Set maximum header count and size so one client cannot exhaust memory.",
                    "Return a clear 400 response for malformed input.",
                ],
            },
            {
                "title": "Write a correct response",
                "summary": "Status, headers and body length must agree.",
                "steps": [
                    "Build a response helper that always writes status, headers and the correct Content-Length.",
                    "Serve a few static files with safe path resolution and sensible content types.",
                    "Add HEAD support and return 404 or 405 where appropriate.",
                    "Test with curl and a browser before adding more features.",
                ],
            },
            {
                "title": "Add routes and keep-alive",
                "summary": "Connection reuse exposes state bugs that one-shot requests hide.",
                "steps": [
                    "Add a small route table for at least one JSON endpoint.",
                    "Support Connection: keep-alive and handle several requests on one socket.",
                    "Set timeouts so idle clients do not hold a worker forever.",
                    "Test pipelined and sequential requests on the same connection.",
                ],
            },
            {
                "title": "Run a conformance-style test suite",
                "summary": "The tests are the proof that the server behaves like HTTP.",
                "steps": [
                    "Test normal GET, HEAD, 404 and 405 responses.",
                    "Test malformed request lines, oversized headers and unsupported methods.",
                    "Test keep-alive, connection close and slow partial requests.",
                    "Run the suite against a real client and document what is intentionally unsupported.",
                ],
            },
        ],
    ),
    36: dict(
        title="Build Your Own Static Site Generator with Live Reload",
        summary=(
            "Turn a folder of Markdown files into a complete website. Write your own small "
            "Markdown parser for headings, lists, links and code blocks, read front matter, "
            "apply layouts and generate tag, index and RSS pages.\n\n"
            "Add a development server that watches files and reloads the browser when one "
            "changes. Start with a clean build from an empty output folder. Then make the "
            "next build incremental so the project stays pleasant as the content grows."
        ),
        who_affected=(
            "Developers and writers who want to understand how static site generators turn "
            "files into pages."
        ),
        why_matters=(
            "Most sites start with content in files. Building the pipeline yourself makes "
            "routing, templates, feeds and live reload easy to reason about."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=30,
        tech_tags=["typescript", "node", "markdown", "websocket", "rss"],
        datasets=[{"name": "Sample Markdown content folder", "url": None}],
        approaches=[
            "Read Markdown files, split front matter and parse headings, lists, links and code blocks.",
            "Render content through a layout and write pages to a clean output directory.",
            "Generate index and tag pages from metadata, plus a valid RSS feed.",
            "Watch the content folder and reload the browser after each successful rebuild.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Turn a folder of Markdown files into a complete website: write your own "
            "Markdown parser, read front-matter metadata, apply templates and layouts, "
            "generate tag and index pages and an RSS feed, and run a dev server that "
            "rebuilds and reloads the browser when files change."
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
                "title": "Define the content folder and output",
                "summary": "A small fixed layout keeps the first build understandable.",
                "steps": [
                    "Create a content folder, a layouts folder and an output folder.",
                    "Choose front matter fields such as title, date, tags and description.",
                    "Write two sample posts and the page you expect each one to produce.",
                    "Add a clean command that removes the output folder before a build.",
                ],
            },
            {
                "title": "Write the Markdown parser",
                "summary": "Start with the syntax your content actually uses.",
                "steps": [
                    "Parse paragraphs, headings, unordered lists, links and fenced code blocks.",
                    "Escape raw HTML and test text that contains angle brackets or asterisks.",
                    "Return a small syntax tree instead of concatenating HTML strings.",
                    "Render the tree and compare the output with a known Markdown example.",
                ],
            },
            {
                "title": "Add front matter and layouts",
                "summary": "Content and presentation should meet in one clear step.",
                "steps": [
                    "Parse the front matter block and validate required fields.",
                    "Load a base layout and insert the rendered content and page metadata.",
                    "Generate one page per Markdown file at a predictable URL.",
                    "Fail the build with a readable error when a required field is missing.",
                ],
            },
            {
                "title": "Generate index, tags and RSS",
                "summary": "A site needs navigation as well as individual pages.",
                "steps": [
                    "Build an index page sorted by date with title, description and link.",
                    "Collect tags and generate one tag page per tag.",
                    "Generate a valid RSS feed with absolute links and publication dates.",
                    "Add previous and next links between posts.",
                ],
            },
            {
                "title": "Watch files and reload the browser",
                "summary": "Live reload is mostly a small server and a clear rebuild status.",
                "steps": [
                    "Start a local static server after each successful build.",
                    "Watch the content and layout folders for changes.",
                    "Notify connected browsers to reload only after a successful rebuild.",
                    "Keep the last good output when a build fails and show the error in the terminal.",
                ],
            },
        ],
    ),
    37: dict(
        title="Typing Racer with a Ghost of Your Best Run",
        summary=(
            "A typing test that shows words per minute and accuracy while you type, "
            "then saves your best run to localStorage. On the next attempt a ghost "
            "cursor replays that best run at the same speed, so you race your own "
            "previous self instead of a random score.\n\n"
            "The interesting part is the record and replay. Store each keystroke with a "
            "timestamp, then replay the timestamps on a timer to move the ghost. Keep "
            "the cursor and the text in the same coordinate space so they line up on "
            "any screen size, and draw a small chart of speed over the run."
        ),
        who_affected=(
            "People learning to type faster and beginners who want a low-pressure way to "
            "practise typing code."
        ),
        why_matters=(
            "A single speed number says little about where you slow down. Racing a "
            "recorded run shows the exact moment you fell behind, and beating your own "
            "ghost is a clear, fair measure of progress."
        ),
        field="web-dev",
        domain="education",
        difficulty="beginner",
        est_hours=10,
        tech_tags=["typescript", "react", "canvas", "localstorage", "vitest"],
        datasets=[
            {
                "name": "Public-domain books from Project Gutenberg",
                "url": "https://www.gutenberg.org/",
            },
            {"name": "Code snippets from your own projects", "url": None},
        ],
        approaches=[
            "Record every keystroke with a timestamp and the state of the text at that moment.",
            "Replay a saved run with a timer that reads the recorded gaps instead of the original clock.",
            "Keep the text renderer and the cursor on the same grid so the ghost lines up at every width.",
            "Chart words per minute over the run so a slow stretch is visible, not just the final score.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Build a typing test that shows words per minute and accuracy, saves your "
            "best run, and replays it as a ghost cursor you race against. Stretch goal: "
            "use any code snippet as practice text."
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
                "title": "Type a sentence and count it",
                "summary": "Get one clean measurement working before adding the ghost.",
                "steps": [
                    "Render a fixed prompt and highlight the character the user should type next.",
                    "Count correct and incorrect keystrokes and ignore modifier keys.",
                    "Compute words per minute from correct characters and elapsed seconds.",
                    "End the run on the last character and show speed plus accuracy.",
                ],
            },
            {
                "title": "Record a run as data",
                "summary": "A run is a list of timed events, so save it that way.",
                "steps": [
                    "Store each keystroke as position, expected character, actual character and time.",
                    "Start the timer on the first keystroke, not on page load.",
                    "Save the best run by words per minute keyed to the prompt text.",
                    "Handle a wrong character by marking it and letting the user backspace.",
                ],
            },
            {
                "title": "Replay the ghost",
                "summary": "The ghost is the same recording played back on a timer.",
                "steps": [
                    "Write a replay function that advances through saved timestamps against the clock.",
                    "Move the ghost cursor to the recorded position for the current time.",
                    "Compare positions to show who is ahead and by how many characters.",
                    "Stop the ghost when the recording ends and keep it visible at the finish.",
                ],
            },
            {
                "title": "Draw the speed chart",
                "summary": "A small chart shows where the run went well or badly.",
                "steps": [
                    "Bucket the run into five-second windows and compute speed per window.",
                    "Draw the bars or line on a canvas with a labelled axis.",
                    "Mark mistakes as dots on the same timeline.",
                    "Show the previous best line so the current run has something to compare against.",
                ],
            },
            {
                "title": "Test, adapt and extend",
                "summary": "Timing logic breaks quietly, so check it with fake clocks.",
                "steps": [
                    "Test the words per minute and accuracy functions with hand-worked examples.",
                    "Test replay with a fake timer so the test does not wait in real time.",
                    "Check the layout at a narrow width and with a long prompt.",
                    "Load a code snippet from your own repo as the practice text.",
                ],
            },
        ],
    ),
    38: dict(
        title="Live Sky Window",
        summary=(
            "Pick a city and the page background becomes the sky right now: sunrise "
            "colours near dawn, plain blue at midday, stars and a moon at night. Show "
            "the current weather in a small panel and the moon phase as a drawn shape.\n\n"
            "Most of the work is time and state. Ask for the city, load coordinates and "
            "weather from an API, work out sunrise and sunset for that place, then pick "
            "the gradient from the sun's height. Handle loading, a wrong city name and a "
            "failed request without leaving the page blank."
        ),
        who_affected=(
            "People who want a calm, informative start page and anyone learning to work "
            "with time zones and weather APIs."
        ),
        why_matters=(
            "Weather and daylight are the most familiar data there is, and they are hard "
            "to fake: time zones, sunrise times and API limits all force you to handle "
            "real edge cases."
        ),
        field="web-dev",
        domain="climate",
        difficulty="beginner",
        est_hours=12,
        tech_tags=["typescript", "react", "open-meteo", "suncalc", "css"],
        datasets=[
            {"name": "Open-Meteo weather API", "url": "https://open-meteo.com/"},
            {
                "name": "SunCalc sun and moon positions",
                "url": "https://github.com/mourner/suncalc",
            },
        ],
        approaches=[
            "Use the city geocoding endpoint to turn a name into coordinates, then fetch weather for those coordinates.",
            "Compute sun and moon positions locally from coordinates and time instead of asking the API.",
            "Choose the background gradient from the sun's height above the horizon, with distinct dawn, day, dusk and night bands.",
            "Show loading, empty and error states in the same panel so the page never looks broken.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Pick a city and show the real sky right now as the page background: sunrise "
            "colours, daytime blue, night stars, the moon phase and current weather. Use "
            "Open-Meteo for weather and SunCalc for sun and moon positions."
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
                "title": "City to coordinates",
                "summary": "Everything else depends on a latitude and longitude.",
                "steps": [
                    "Add a search box and call the geocoding endpoint with the typed name.",
                    "Show a short list of matches so the user picks the right city.",
                    "Store the chosen city, coordinates and time zone in local state.",
                    "Show a clear message when nothing matches the search.",
                ],
            },
            {
                "title": "Fetch and cache the weather",
                "summary": "One request per city, with honest loading and error states.",
                "steps": [
                    "Request current temperature, cloud cover and weather code for the coordinates.",
                    "Show a skeleton while the request runs and a retry button when it fails.",
                    "Cache the result with a timestamp so a reload does not hit the API again.",
                    "Map the weather code to a short label and an icon.",
                ],
            },
            {
                "title": "Work out the sun and moon",
                "summary": "Sunrise, sunset and the moon phase are local maths.",
                "steps": [
                    "Compute sunrise, sunset and the sun's height for the current time.",
                    "Compute moon illumination and phase angle for the same moment.",
                    "Format times in the city's own time zone, not the browser's.",
                    "Test with a fixed date and a known city and compare against a published table.",
                ],
            },
            {
                "title": "Paint the sky",
                "summary": "The gradient comes from the sun, not from a random palette.",
                "steps": [
                    "Define colour stops for night, dawn, day and dusk.",
                    "Blend between stops using the sun's height so the change is smooth.",
                    "Add stars at night with a fixed seeded pattern and dim them in daylight.",
                    "Draw the moon as a shape with the correct phase and keep text readable over every gradient.",
                ],
            },
            {
                "title": "Polish and respect the API",
                "summary": "Small details decide whether the page feels alive.",
                "steps": [
                    "Refresh the sky every few minutes and on tab focus.",
                    "Respect API usage terms and show the data source in a footer note.",
                    "Respect a reduced-motion setting for any animation.",
                    "Animate the sun across the day as a stretch goal.",
                ],
            },
        ],
    ),
    39: dict(
        title="Identicon Avatar Generator",
        summary=(
            "Turn any username into a square pixel avatar with a vertical line of "
            "symmetry, the way GitHub creates its default pictures. Hash the name, use "
            "the hash to fill one half of the grid, then mirror it. The same name always "
            "gives the same picture, on any browser.\n\n"
            "The learning is in the hashing and the drawing. Use the Web Crypto API to "
            "get a stable digest, turn bytes into a fixed-size grid, and draw it with "
            "SVG or canvas. Add a download button so the avatar can be used elsewhere."
        ),
        who_affected=(
            "Developers who need placeholder avatars and anyone curious about how "
            "deterministic images are made."
        ),
        why_matters=(
            "Many products need an image per user before anyone uploads a photo. A "
            "deterministic avatar avoids storage and looks intentional."
        ),
        field="web-dev",
        domain="developer-tools",
        difficulty="beginner",
        est_hours=8,
        tech_tags=["typescript", "react", "web-crypto", "canvas", "svg"],
        datasets=[{"name": "Any list of usernames", "url": None}],
        approaches=[
            "Hash the trimmed, lowercased name with SHA-256 and treat the bytes as the pattern source.",
            "Fill only the left half of a grid and mirror it, so the result is symmetric by construction.",
            "Draw the grid once with SVG rectangles or canvas squares and keep the size configurable.",
            "Export the drawing as a PNG or SVG file without sending anything to a server.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Turn any username into a unique symmetric pixel avatar, the way GitHub's "
            "default avatars work. The same name always gives the same picture. Add "
            "colour palettes and a downloadable PNG or SVG."
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
                "title": "Hash the name",
                "summary": "A stable hash is the whole trick.",
                "steps": [
                    "Normalise the input by trimming spaces and lowercasing it.",
                    "Compute a SHA-256 digest with the Web Crypto API and keep the bytes.",
                    "Write a small helper that reads a bit or a byte from the digest by index.",
                    "Confirm the same name gives the same digest across browsers.",
                ],
            },
            {
                "title": "Pick the pattern",
                "summary": "Mirroring half a grid keeps the avatar readable at small sizes.",
                "steps": [
                    "Choose a grid size such as five columns and five rows.",
                    "Fill the left half from hash bits and mirror the columns.",
                    "Add a margin rule so the shape does not touch the edge.",
                    "Check a few names to make sure the results look different from each other.",
                ],
            },
            {
                "title": "Draw it",
                "summary": "SVG is easier to download, canvas is easier to animate.",
                "steps": [
                    "Draw filled squares for set bits and leave the rest transparent.",
                    "Pick the foreground and background colours from the same hash.",
                    "Keep the drawing in one component that takes a name and a size.",
                    "Render at 16, 64 and 256 pixels and check the shape stays readable.",
                ],
            },
            {
                "title": "Export the file",
                "summary": "A download button turns a demo into something usable.",
                "steps": [
                    "Serialise the SVG or read the canvas pixels into a blob.",
                    "Trigger a download with a filename based on the username.",
                    "Test that the downloaded file opens as an image.",
                    "Show the code snippet used elsewhere, such as an image tag with a data URL.",
                ],
            },
            {
                "title": "Handle the awkward cases",
                "summary": "Empty and unusual names should not break the page.",
                "steps": [
                    "Decide what an empty name shows and test it.",
                    "Test very long names and names with emoji or spaces.",
                    "Check that nothing is sent to a server and note that in the page copy.",
                    "Add a palette choice as a stretch goal and keep the default stable.",
                ],
            },
        ],
    ),
    40: dict(
        title="Color-Blindness Simulator",
        summary=(
            "Upload an image or paste a small palette, then see the same colours through "
            "the eyes of people with deuteranopia, protanopia, tritanopia and monochrome "
            "vision. The page shows the original beside the simulation and reports the "
            "colour difference between them.\n\n"
            "The work is pixel maths. Read the image into a canvas, apply a colour matrix "
            "to every pixel, and draw the result back. Add a checker that says whether two "
            "chosen colours look the same under each simulation, and be honest in the copy "
            "that these are approximations."
        ),
        who_affected=(
            "Designers and developers checking their palettes, plus anyone who wants to "
            "see how a chart or screenshot reads with colour-vision deficiency."
        ),
        why_matters=(
            "Around one in twelve men sees colours differently. A quick check while a "
            "palette is still a draft is far cheaper than fixing an unreadable chart later."
        ),
        field="web-dev",
        domain="social-impact",
        difficulty="beginner",
        est_hours=10,
        tech_tags=["typescript", "canvas", "web-crypto", "accessibility", "vitest"],
        datasets=[
            {
                "name": "Colour-vision simulation matrices",
                "url": "https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html",
            },
            {"name": "Your own screenshots and palettes", "url": None},
        ],
        approaches=[
            "Draw the uploaded image to a canvas at its natural size and read the pixels once.",
            "Multiply the pixel values by a matrix per type of colour blindness, then clamp and write back.",
            "Show original and simulated versions side by side so the change is easy to judge.",
            "State clearly that simulations are approximations and link to the source of the matrices.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Upload an image or a colour palette and see how it looks to people with "
            "different types of colour-blindness. Add a checker that says whether two "
            "colours will be confusable, and make clear that simulations are approximations."
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
                "title": "Get pixels into a canvas",
                "summary": "One clear path from file to pixel array.",
                "steps": [
                    "Accept an image from a file picker and reject files that are not images.",
                    "Draw the image to a canvas at a size that keeps the page responsive.",
                    "Read the pixel data with getImageData and keep one copy as the source.",
                    "Show the original so the user can confirm the upload worked.",
                ],
            },
            {
                "title": "Apply a colour matrix",
                "summary": "The simulation is a fixed matrix applied to red, green and blue.",
                "steps": [
                    "Write a function that takes pixel data and a 3x3 matrix and returns new data.",
                    "Keep the original data untouched and write the result to a second canvas.",
                    "Clamp values to 0 to 255 after the multiplication.",
                    "Test one known colour through each matrix and check the output by hand.",
                ],
            },
            {
                "title": "Switch between types",
                "summary": "The interface should make comparison quick.",
                "steps": [
                    "Add a control for the simulation type and redraw on change.",
                    "Label each option in plain words instead of only Latin names.",
                    "Keep the layout stable when switching so nothing jumps.",
                    "Add a side-by-side view of original and simulation.",
                ],
            },
            {
                "title": "Check a palette",
                "summary": "Two colours can look different and still be confusable.",
                "steps": [
                    "Let the user enter two colours as swatches or hex values.",
                    "Run both through each simulation and measure the distance between the results.",
                    "Flag a pair when the difference falls under a stated threshold.",
                    "Explain the threshold and warn that it is a guide, not a pass or fail test.",
                ],
            },
            {
                "title": "Keep it honest and local",
                "summary": "The page should not overclaim, and the image should stay on the device.",
                "steps": [
                    "Add copy that the simulation is an approximation, not a medical test.",
                    "Keep all processing in the browser and say so.",
                    "Handle very large images by downscaling before reading pixels.",
                    "Test the page with keyboard only and with an image that has fine detail.",
                ],
            },
        ],
    ),
    41: dict(
        title="ASCII Art Camera",
        summary=(
            "Open the webcam and turn the video into live text art: each block of pixels "
            "becomes a character chosen by its brightness. Add a download button to save "
            "the current frame as an image, and a character-set switch so the art changes "
            "look.\n\n"
            "The learning is the render loop. Read the frame, downscale it to a grid, map "
            "brightness to a character, and draw only as often as the screen needs. Nothing "
            "leaves the browser, and the page says so."
        ),
        who_affected=(
            "Beginners who want a first camera project and anyone curious about how much "
            "of a picture survives when you keep only brightness."
        ),
        why_matters=(
            "It is a small, fun way to learn camera permissions, frame timing and the cost "
            "of touching every pixel too often."
        ),
        field="web-dev",
        domain="computer-vision",
        difficulty="beginner",
        est_hours=12,
        tech_tags=["typescript", "canvas", "mediastream", "requestanimationframe", "css"],
        datasets=[{"name": "Your own webcam feed", "url": None}],
        approaches=[
            "Ask for the camera with getUserMedia, stop all tracks when the page unmounts and handle a refused permission.",
            "Draw the video to a small offscreen canvas so the pixel count stays cheap.",
            "Map average brightness per cell to an ordered character list and draw the text into a pre block or canvas.",
            "Use requestAnimationFrame with a frame cap so the loop does not run faster than needed.",
        ],
        source_name="MANABI Curated",
        source_note="Curated web development learning project.",
        original_text=(
            "Turn your webcam feed into live ASCII art, with brightness mapped to "
            "characters. Add a button to download a frame as an image. Everything should "
            "stay on the device, and the camera needs permission and HTTPS."
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
                "title": "Open the camera",
                "summary": "Permission and cleanup are part of the feature.",
                "steps": [
                    "Request video only, with a clear button instead of asking on page load.",
                    "Show a readable message when permission is refused or no camera exists.",
                    "Attach the stream to a hidden video element and wait for metadata.",
                    "Stop every track when the user turns the camera off or navigates away.",
                ],
            },
            {
                "title": "Build the render loop",
                "summary": "Decide the frame rate before drawing anything.",
                "steps": [
                    "Write a loop with requestAnimationFrame that skips frames to a set target rate.",
                    "Copy the current video frame into a small offscreen canvas.",
                    "Read the pixel data once per frame and keep the array for mapping.",
                    "Pause the loop when the tab is hidden and resume on return.",
                ],
            },
            {
                "title": "Map brightness to characters",
                "summary": "Each cell becomes one character, so cell size is a design choice.",
                "steps": [
                    "Split the frame into a grid and average the brightness of each cell.",
                    "Order a character set from dark to light and pick an index from the brightness.",
                    "Draw the characters with a monospace font and line height that matches cell size.",
                    "Try a few character sets and pick two that look clearly different.",
                ],
            },
            {
                "title": "Add export and looks",
                "summary": "A saved frame makes the project easy to share.",
                "steps": [
                    "Draw the current frame to a canvas with the chosen background and text colour.",
                    "Export it as a PNG through a blob download.",
                    "Add a colour mode that uses the cell's average colour instead of one ink colour.",
                    "Add a simple dark theme for a different look.",
                ],
            },
            {
                "title": "Check performance and privacy",
                "summary": "Text art is easy to make slow and easy to make leaky.",
                "steps": [
                    "Measure frame time and reduce the grid size if it drops below the target.",
                    "Cap the grid size on large screens so the character count stays sane.",
                    "Confirm nothing is uploaded and state it on the page.",
                    "Test on a laptop with the camera off, denied and unplugged.",
                ],
            },
        ],
    ),
}


LEARNING_CONCEPTS = {
    1: [
        "How service workers cache an app shell and handle offline navigation.",
        "Storing structured drafts and photo blobs in IndexedDB.",
        "Building a sync queue with retries and idempotency keys.",
        "Detecting and resolving conflicting edits instead of overwriting data.",
        "Designing clear offline, syncing, failed and conflict states.",
    ],
    2: [
        "Matching reports by location and text similarity.",
        "Designing a workflow with categories, departments and service deadlines.",
        "Keeping a public status page accurate without exposing private details.",
        "Writing queries that group related records without losing the original reports.",
        "Handling duplicate merges and splits with an audit trail.",
    ],
    3: [
        "Modeling offers and wants as a directed skill graph.",
        "Finding reciprocal pairs and bounded three-way cycles.",
        "Scheduling across time zones and availability windows.",
        "Using request states to prevent spam and repeated matches.",
        "Adding block, report and rating flows to a matching product.",
    ],
    4: [
        "Reading GitHub search results and staying inside API rate limits.",
        "Turning activity, response time and contribution guides into an explainable score.",
        "Caching API responses and handling partial failures.",
        "Designing filters for language, topic and issue age.",
        "Understanding what makes an open-source issue beginner-friendly.",
    ],
    7: [
        "Modeling volunteers, shifts, donors, pledges and beneficiaries.",
        "Enforcing role-based access in both the API and the UI.",
        "Sending reminders from a small queue with a visible delivery log.",
        "Building a report from records that staff actually maintain.",
        "Keeping sensitive beneficiary data out of public views.",
    ],
    9: [
        "Loading GTFS stops, routes, trips and service calendars.",
        "Running a timetable-aware search such as RAPTOR or Connection Scan.",
        "Handling time zones, overnight trips and service dates.",
        "Comparing fastest arrival with fewest transfers as separate goals.",
        "Drawing an itinerary with legs, walking transfers and waiting time.",
    ],
    12: [
        "Modeling product scores when source data is incomplete.",
        "Explaining a sustainability score and its provenance.",
        "Estimating a cart footprint with clear assumptions.",
        "Comparing alternatives without hiding uncertainty.",
        "Designing a catalogue that admits when a label is missing.",
    ],
    13: [
        "Working with map tile layers and time series imagery.",
        "Building a time slider and side-by-side comparison.",
        "Reading basic remote-sensing layers without overclaiming.",
        "Crediting data sources and respecting their terms.",
        "Explaining change in plain language beside the map.",
    ],
    14: [
        "Modeling an application and approval workflow as explicit states.",
        "Enforcing student, reviewer and admin permissions.",
        "Keeping an append-only audit trail for every decision.",
        "Handling document uploads safely and privately.",
        "Exporting disbursement reports without exposing personal data.",
    ],
    15: [
        "Reading browser location with user consent and clear limits.",
        "Detecting route deviation and long stops from location updates.",
        "Scheduling check-ins and alerts with a safe fallback.",
        "Expiring shared trips and deleting location history.",
        "Explaining what the browser can and cannot track in the background.",
    ],
    16: [
        "Modeling shared expenses with integer money values.",
        "Computing net balances from payers and shares.",
        "Reducing transfers with a min-cash-flow algorithm.",
        "Testing rounding and uneven split edge cases.",
        "Presenting a settlement plan that users can verify.",
    ],
    17: [
        "Writing semantic HTML and a small responsive layout.",
        "Meeting keyboard and screen-reader basics.",
        "Measuring performance with Lighthouse on a production build.",
        "Modeling portfolio content in Markdown or JSON.",
        "Deploying a static site and keeping updates simple.",
    ],
    18: [
        "Normalizing items from RSS feeds and JSON APIs.",
        "Deduplicating stories by URL and title fingerprints.",
        "Scheduling fetches and caching responses.",
        "Grouping topics with transparent rules.",
        "Building a digest that survives a failing source.",
    ],
    19: [
        "Keeping shared state consistent over WebSockets.",
        "Handling message order, reconnect and missed updates.",
        "Rate-limiting actions and enforcing cooldowns.",
        "Storing a history that can be replayed.",
        "Moderating user-generated pixels with an audit path.",
    ],
    20: [
        "Structuring a Chrome extension with a popup, worker and minimal permissions.",
        "Reading and normalizing listening data from a public source.",
        "Scoring taste similarity and explaining shared artists.",
        "Designing opt-in, block and report flows for strangers.",
        "Packaging an extension and testing its lifecycle.",
    ],
    21: [
        "Querying MusicBrainz and respecting rate limits.",
        "Normalizing messy artist and track titles.",
        "Ranking remixes, edits and live versions with an explanation.",
        "Letting users review and override proposed matches.",
        "Exporting a playlist as text and a valid M3U file.",
    ],
    22: [
        "Measuring motion energy with frame differencing.",
        "Using the Web Audio API to change music in real time.",
        "Rendering visuals on canvas or WebGL without dropping frames.",
        "Keeping camera processing local and avoiding face analysis.",
        "Explaining what the app measured and why it reacted.",
    ],
    23: [
        "Designing a multi-tenant data model with tenant isolation.",
        "Letting each shop manage products and branding.",
        "Generating shareable storefront links and QR codes.",
        "Building an order enquiry flow without real payments.",
        "Testing subscription states in a sandbox.",
    ],
    24: [
        "Designing a small, typed public API.",
        "Writing tests for edge cases and type-level behaviour.",
        "Producing ESM and CommonJS builds from one source.",
        "Automating CI, documentation and versioned releases.",
        "Choosing a semver bump from the actual change.",
    ],
    25: [
        "Handling TCP connections and byte buffers.",
        "Parsing HTTP request lines, headers and bodies safely.",
        "Writing correct status codes, headers and Content-Length.",
        "Implementing static files, routing and keep-alive.",
        "Testing malformed requests and slow clients.",
    ],
    26: [
        "Modeling a persistent job queue and worker pool.",
        "Implementing retries with backoff and a dead-letter queue.",
        "Scheduling delayed jobs without duplicate execution.",
        "Adding metrics, logs and a dashboard for queue health.",
        "Load-testing while workers fail and recover.",
    ],
    27: [
        "Propagating satellite orbits with SGP4.",
        "Computing observer geometry and pass visibility.",
        "Drawing a ground track on a globe and a sky chart.",
        "Caching orbital elements and handling stale data.",
        "Explaining why a high pass may still be invisible.",
    ],
    28: [
        "Calculating Hohmann and bi-elliptic transfer burns.",
        "Integrating motion with an RK4 solver.",
        "Moving heavy simulation work into Web Workers.",
        "Comparing simulation output with real ephemeris data.",
        "Showing assumptions and numerical error beside the animation.",
    ],
    29: [
        "Parsing SMILES and resolving compound names.",
        "Rendering a molecule in 3D in the browser.",
        "Computing Lipinski properties locally.",
        "Explaining each drug-likeness rule in plain language.",
        "Loading a large chemistry bundle lazily.",
    ],
    30: [
        "Implementing Needleman-Wunsch and Smith-Waterman.",
        "Tracing back an alignment from a scoring matrix.",
        "Changing gap and substitution scores to see the effect.",
        "Finding open reading frames and translating codons.",
        "Fetching sequences from public biology APIs.",
    ],
    31: [
        "Modeling a population as a contact network.",
        "Simulating transmission and interventions over time.",
        "Comparing a network model with a simple SIR curve.",
        "Running the simulation in a Web Worker.",
        "Stating assumptions and uncertainty in an educational model.",
    ],
    32: [
        "Solving the time-dependent Schrodinger equation numerically.",
        "Choosing a stable grid and time step.",
        "Using WebAssembly or the GPU for real-time updates.",
        "Checking transmission against an analytic barrier result.",
        "Visualizing reflection, tunneling and interference.",
    ],
    33: [
        "Reading the USGS earthquake feed and caching results.",
        "Estimating the Gutenberg-Richter b-value.",
        "Estimating magnitude of completeness and uncertainty.",
        "Warning when a catalogue is too small or incomplete.",
        "Linking a map view with a statistical chart.",
    ],
    34: [
        "Creating elements and a virtual DOM tree.",
        "Diffing trees and reconciling keyed children.",
        "Implementing function components and hooks.",
        "Wiring a small event system.",
        "Benchmarking against real React with honest numbers.",
    ],
    35: [
        "Storing blobs, trees and commits as content-addressed objects.",
        "Building an index, commits, refs and branches.",
        "Reading a commit graph and drawing it.",
        "Implementing checkout and diff.",
        "Resolving a three-way merge with conflict markers.",
    ],
    36: [
        "Parsing Markdown into a small syntax tree.",
        "Reading front matter and rendering layouts.",
        "Generating index, tag and RSS pages.",
        "Watching files and reloading the browser.",
        "Keeping builds fast as content grows.",
    ],
    37: [
        "Recording keystrokes with timestamps and replaying them on a timer.",
        "Measuring words per minute and accuracy from raw events.",
        "Saving and loading a personal best from localStorage.",
        "Keeping a cursor and text grid aligned at different widths.",
        "Charting progress over time instead of only a final score.",
    ],
    38: [
        "Turning a place name into coordinates with a geocoding API.",
        "Handling loading, empty and failed requests in the same panel.",
        "Computing sunrise, sunset and the moon phase from coordinates and time.",
        "Showing times in the chosen city's time zone.",
        "Driving a CSS gradient from live data instead of a fixed palette.",
    ],
    39: [
        "Hashing with the Web Crypto API and getting a stable digest.",
        "Turning hash bytes into a fixed-size pixel grid.",
        "Building symmetry by mirroring half the pattern.",
        "Drawing the same idea with SVG and with canvas.",
        "Exporting a generated image as a downloadable file.",
    ],
    40: [
        "Reading and writing pixels through a canvas.",
        "Applying a colour matrix to red, green and blue values.",
        "Comparing colours with a distance measure instead of by eye.",
        "Explaining why simulation is an approximation.",
        "Treating accessibility checks as part of normal design work.",
    ],
    41: [
        "Requesting camera access and stopping tracks when done.",
        "Running a render loop with requestAnimationFrame.",
        "Mapping brightness to characters in a fixed grid.",
        "Timing frames and capping the work per second.",
        "Keeping camera data on the device and saying so.",
    ],
}


DIFFICULTIES = {
    1: "advanced",
    2: "intermediate",
    3: "intermediate",
    4: "intermediate",
    7: "intermediate",
    9: "advanced",
    12: "intermediate",
    13: "intermediate",
    14: "intermediate",
    15: "intermediate",
    16: "beginner",
    17: "beginner",
    18: "beginner",
    19: "intermediate",
    20: "intermediate",
    21: "beginner",
    22: "advanced",
    23: "intermediate",
    24: "intermediate",
    25: "intermediate",
    26: "advanced",
    27: "intermediate",
    28: "advanced",
    29: "intermediate",
    30: "intermediate",
    31: "intermediate",
    32: "advanced",
    33: "intermediate",
    34: "advanced",
    35: "intermediate",
    36: "beginner",
    37: "beginner",
    38: "beginner",
    39: "beginner",
    40: "beginner",
    41: "beginner",
}


TITLES = {
    1: "Offline-First Field Data Collection PWA with Conflict-Free Sync",
    2: "Civic Issue Tracker with Duplicate Detection",
    3: "Skill Exchange Matching Platform",
    4: "Open-Source Contribution Finder",
    7: "Nonprofit Volunteer & Donor Management Hub",
    9: "Public Transit Journey Planner (GTFS)",
    12: "Green Shopping Platform with Environmental Scores",
    13: "Earth Change Explorer",
    14: "Paperless Scholarship Disbursement System",
    15: "Journey Safety Share",
    16: "Expense Splitter with Debt Simplification",
    17: "Personal Portfolio Website",
    18: "Developer News Aggregator",
    19: "Real-Time Collaborative Pixel Canvas",
    20: "Concert Buddy Finder (Chrome Extension)",
    21: "Playlist Remix Finder",
    22: "Crowd-Reactive Music Visualizer",
    23: "Storefront Builder for Local Shops",
    24: "Typed NPM Utility Library",
    25: "HTTP Server From Scratch",
    26: "Distributed Task Queue",
    27: "Satellite Pass Predictor & Live Sky Tracker",
    28: "Mission Trajectory Playground",
    29: "Molecule Explorer & Drug-Likeness Checker",
    30: "Sequence Alignment & Gene Finder Lab",
    31: "Epidemic Spread Simulator on Contact Networks",
    32: "Quantum Tunneling Lab",
    33: "Seismic Activity Explorer & b-Value Analyzer",
    34: "Build Your Own React",
    35: "Build Your Own Git",
    36: "Build Your Own Static Site Generator with Live Reload",
    37: "Typing Racer with a Ghost of Your Best Run",
    38: "Live Sky Window",
    39: "Identicon Avatar Generator",
    40: "Color-Blindness Simulator",
    41: "ASCII Art Camera",
}
