"""Seed the catalog with 10 curated Beginner Web Development project ideas.

These are *curated suggestions*, not official problem statements from any
organisation. Each row is inserted with origin="manual" and status="published".

The script is idempotent: re-running it skips rows whose
(source_name, source_id) already exist, so it is safe to run more than once.

Usage (from the backend directory):
    .venv/Scripts/python scripts/seed_beginner_web_projects.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.db import session_scope
from app.models import Problem

SOURCE_NAME = "MANABI Curated"


def _project(
    source_id: str,
    title: str,
    summary: str,
    who_affected: str,
    why_matters: str,
    domain: str,
    est_hours: int,
    tech_tags: list[str],
    datasets: list[dict],
    approaches: list[str],
    original_text: str,
) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "summary": summary,
        "who_affected": who_affected,
        "why_matters": why_matters,
        "field": "web-dev",
        "domain": domain,
        "difficulty": "beginner",
        "est_hours": est_hours,
        "tech_tags": tech_tags,
        "datasets": datasets,
        "approaches": approaches,
        "source_name": SOURCE_NAME,
        "source_url": None,
        "source_note": (
            "Curated beginner project idea. Not an official problem statement "
            "from any organisation, company, or hackathon."
        ),
        "original_text": original_text,
        "ai_fields": [],  # Manually curated; nothing here was AI-generated.
        "created_by": None,
    }


PROJECTS = [
    _project(
        source_id="manabi-web-beginner-001",
        title="Smart Document Expiry Tracker",
        summary=(
            "A personal dashboard that stores documents with expiry dates, "
            "flags upcoming and expired items, and shows how many days remain "
            "before each expires."
        ),
        who_affected=(
            "Individuals managing driving licences, insurance policies, "
            "subscriptions, certificates, and other time-sensitive documents."
        ),
        why_matters=(
            "Missing an expiry date can mean fines, lapsed cover, or avoidable "
            "inconvenience. A single place to track renewals helps people act "
            "before a document expires."
        ),
        domain="social-impact",
        est_hours=28,
        tech_tags=["html", "css", "javascript", "localstorage", "date-handling"],
        datasets=[{"name": "Sample document categories", "url": None}],
        approaches=[
            "Store documents as an array of objects in browser localStorage.",
            "Compute days remaining by comparing each expiry date with today.",
            "Render documents in valid / expiring-soon / expired groups.",
            "Colour-code each card by urgency.",
            "Validate that the expiry date is well-formed before saving.",
        ],
        original_text=(
            "# Smart Document Expiry Tracker\n\n"
            "## Problem statement\n"
            "People often forget when important documents such as driving "
            "licences, insurance policies, subscriptions, and certificates "
            "expire. The result can be lapsed cover, fines, or avoidable "
            "inconvenience. Reminders are scattered across calendars, emails, "
            "and paper folders.\n\n"
            "## Proposed solution\n"
            "A beginner-friendly, single-page web app that lets a user register "
            "documents, assign each one a category and expiry date, and see at a "
            "glance which documents are upcoming, expired, or valid, with the "
            "number of days remaining shown for every item.\n\n"
            "## Target audience\n"
            "Students, renters, vehicle owners, and anyone who keeps track of "
            "personal or household documents.\n\n"
            "## Real-world use case\n"
            "A user adds their driving licence (expires in 45 days), car "
            "insurance (expires in 12 days), and a gym subscription (already "
            "expired). The dashboard highlights the expired subscription in red, "
            "the insurance in amber, and the licence in green, so the user "
            "renews insurance first.\n\n"
            "## Core features (MVP)\n"
            "- Add a document with name, category, and expiry date\n"
            "- Categorise documents (identity, insurance, subscription, "
            "certificate, other)\n"
            "- List documents grouped by status: valid, expiring soon, expired\n"
            "- Show remaining days before expiry for each document\n"
            "- Colour-coded visual status indicators\n"
            "- Persist data in browser localStorage so it survives refresh\n\n"
            "## Optional features (post-MVP)\n"
            "- Edit and delete documents\n"
            "- Mark a document as renewed (resets the expiry date)\n"
            "- Browser notification on the day of expiry\n"
            "- Export the document list to CSV\n\n"
            "## Stretch goals\n"
            "- Photo or scan attachment for each document\n"
            "- Recurring renewal reminders (for example, every 12 months)\n"
            "- Multiple user accounts with login\n\n"
            "## Suggested technology stack\n"
            "HTML, CSS, vanilla JavaScript, browser localStorage\n\n"
            "## Required skills\n"
            "DOM manipulation, form handling, date arithmetic, array filtering, "
            "localStorage API, responsive layout\n\n"
            "## Expected deliverables\n"
            "A working single-page app that runs entirely in the browser, with "
            "sample documents preloaded so it is useful without any setup.\n\n"
            "## Estimated development duration\n"
            "25–30 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "CRUD operations on an in-memory collection, date comparison and "
            "formatting, conditional rendering and styling, client-side "
            "persistence, input validation\n\n"
            "## Technical challenges\n"
            "- Comparing dates correctly across time-zone and daylight-saving "
            "boundaries\n"
            "- Keeping the UI in sync when items are added, edited, or expire\n\n"
            "## Suggested implementation approach\n"
            "Start with a hard-coded array of sample documents. Add a form to "
            "create new ones, render them in three status groups, compute days "
            "remaining with `Date` arithmetic, and persist to localStorage on "
            "every change. Only add notifications or export after the core list "
            "works.\n\n"
            "## Possible future improvements\n"
            "Email reminders, document tags, dark mode, search by document name\n\n"
            "## Limitations\n"
            "Runs in one browser only. Data is not synced across devices. "
            "Notifications depend on browser permission and the tab being open. "
            "This is a personal tracking tool, not a legal reminder service."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-002",
        title="Accessibility-Friendly Website Checker",
        summary=(
            "A client-side tool that checks a sample web page for common "
            "accessibility issues (colour contrast, missing image alt text, "
            "and heading order) and produces a plain-language report."
        ),
        who_affected=(
            "Web developers, students, and site owners who want to make pages "
            "easier to use for people with visual, cognitive, or motor "
            "impairments."
        ),
        why_matters=(
            "Poor contrast, missing alt text, and illogical headings create "
            "real barriers for people using screen readers or keyboard "
            "navigation. Catching these early helps developers build more "
            "inclusive sites."
        ),
        domain="social-impact",
        est_hours=32,
        tech_tags=["html", "css", "javascript", "dom", "accessibility", "wcag"],
        datasets=[{"name": "WCAG 2.1 contrast guidelines", "url": None}],
        approaches=[
            "Paste or load HTML markup into a sandbox container on the page.",
            "Query all images and flag those without alt text.",
            "Compute colour contrast ratios for text/background pairs.",
            "Walk the heading tree and flag skipped heading levels.",
            "Render a grouped pass/fail report with plain-language explanations.",
        ],
        original_text=(
            "# Accessibility-Friendly Website Checker\n\n"
            "## Problem statement\n"
            "Many websites have poor colour contrast, missing image descriptions, "
            "and difficult-to-read text. These issues create barriers for people "
            "who use screen readers, keyboard navigation, or need high-contrast "
            "content, and they often go unnoticed by the people building the "
            "sites.\n\n"
            "## Proposed solution\n"
            "A client-side checker where a user pastes HTML markup (or loads a "
            "built-in sample page) and receives a plain-language accessibility "
            "report: colour-contrast failures, images missing alt text, and "
            "heading-order problems.\n\n"
            "## Target audience\n"
            "Frontend learners, freelancers, and small site owners testing their "
            "own pages.\n\n"
            "## Real-world use case\n"
            "A student finishes a portfolio page and runs it through the checker "
            "before submitting. The tool flags two images without alt text and a "
            "heading that skips from h1 to h3, so the student fixes them first.\n\n"
            "## Core features (MVP)\n"
            "- Paste HTML markup into an editor on the page\n"
            "- Check colour contrast between foreground and background text\n"
            "- Identify images missing alt text\n"
            "- Check whether headings follow a logical order (h1 → h2 → h3)\n"
            "- Generate a simple pass/fail accessibility report\n"
            "- Show the original markup alongside the highlighted results\n\n"
            "## Optional features (post-MVP)\n"
            "- Suggest concrete fixes for each flagged issue\n"
            "- Check multiple pages in one session\n"
            "- Export the report as text\n\n"
            "## Stretch goals\n"
            "- Integrate an established accessibility rules engine\n"
            "- Audit keyboard navigation and ARIA attributes\n"
            "- Check colour-blindness simulation\n\n"
            "## Suggested technology stack\n"
            "HTML, CSS, vanilla JavaScript, DOM APIs\n\n"
            "## Required skills\n"
            "DOM traversal, HTML semantics, form validation, string parsing, "
            "accessibility fundamentals (WCAG)\n\n"
            "## Expected deliverables\n"
            "A working checker that accepts HTML, runs the three core checks, "
            "and displays a clear report, with a built-in sample page so it is "
            "usable without pasting anything.\n\n"
            "## Estimated development duration\n"
            "30–35 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "DOM traversal and manipulation, HTML document semantics, form "
            "validation, accessibility principles and WCAG contrast rules, "
            "rendering results in the DOM\n\n"
            "## Technical challenges\n"
            "- Computing contrast ratios correctly for arbitrary colours\n"
            "- Detecting skipped heading levels in nested markup\n"
            "- Keeping the sandboxed preview isolated from the page itself\n\n"
            "## Suggested implementation approach\n"
            "Build the three checks as pure functions over a DOM tree, wire up a "
            "textarea + preview iframe, and render the report below. Start with "
            "the built-in sample page; add URL input only as an extension.\n\n"
            "## Possible future improvements\n"
            "Fix suggestions, PDF export, multi-page audits, ARIA audit\n\n"
            "## Important implementation notes\n"
            "Client-side JavaScript cannot fetch an arbitrary URL because of "
            "browser CORS restrictions. Start with a local HTML checker (pasted "
            "markup or a built-in sample page); treat live URL scanning as an "
            "extension that would need a backend proxy.\n\n"
            "## Limitations\n"
            "Rule-based and educational only, not a substitute for a manual "
            "accessibility audit or a guarantee of legal compliance. Cannot scan "
            "external URLs directly due to CORS."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-003",
        title="Local Lost & Found Portal",
        summary=(
            "A community bulletin board where anyone can post lost or found "
            "items, attach photos, and browse or search listings by category and "
            "location."
        ),
        who_affected=(
            "Students and local residents who misplace belongings, and people "
            "who find items and want to return them."
        ),
        why_matters=(
            "Lost-item information is scattered across chat groups and physical "
            "notice boards, so reunions are slow and often never happen. One "
            "searchable portal makes it easier to return belongings."
        ),
        domain="social-impact",
        est_hours=38,
        tech_tags=["react", "javascript", "css", "localstorage", "crud", "search"],
        datasets=[{"name": "Sample lost-and-found listings", "url": None}],
        approaches=[
            "Maintain an array of item listings in React state.",
            "Each listing has title, description, category, location, contact, "
            "photo URL, and lost/found status.",
            "Render listings as cards with a search bar and category/location "
            "filters.",
            "Filter and search in memory as the user types.",
            "Persist listings to localStorage on add or update.",
        ],
        original_text=(
            "# Local Lost & Found Portal\n\n"
            "## Problem statement\n"
            "Students and local community members often struggle to find lost "
            "belongings because information is scattered across WhatsApp groups, "
            "Discord servers, and physical notice boards. A finder may have an "
            "item but no way to reach its owner.\n\n"
            "## Proposed solution\n"
            "A simple community portal where anyone can post a lost or found "
            "listing with a photo, category, location, and contact information. "
            "Others can browse, filter by category or location, and search by "
            "keyword.\n\n"
            "## Target audience\n"
            "Students, residents, and community members in a locality or campus.\n\n"
            "## Real-world use case\n"
            "A student loses their identity card in the cafeteria and posts a "
            "lost listing. Another student finds the card, sees the listing, and "
            "contacts them through the posted contact information.\n\n"
            "## Core features (MVP)\n"
            "- Post a lost or found item with title, description, category, "
            "location, contact information, and photo URL\n"
            "- Mark each listing as lost or found\n"
            "- Browse all listings as cards\n"
            "- Filter by category (electronics, documents, keys, bags, other) "
            "and by location\n"
            "- Search listings by keyword\n"
            "- Persist listings in browser localStorage\n\n"
            "## Optional features (post-MVP)\n"
            "- Mark a listing as resolved/returned\n"
            "- User accounts so posters can edit their own listings\n"
            "- Report or moderate inappropriate listings\n"
            "- Notification when a match is found\n\n"
            "## Stretch goals\n"
            "- Map view of where items were lost or found\n"
            "- Image file upload (requires a storage backend)\n"
            "- Real-time messaging between finder and owner\n\n"
            "## Suggested technology stack\n"
            "React, CSS, vanilla JavaScript, browser localStorage (Firebase is "
            "an optional enhancement for multi-device sync)\n\n"
            "## Required skills\n"
            "Component state, forms, image handling, search and filtering, "
            "conditional rendering, responsive layout\n\n"
            "## Expected deliverables\n"
            "A working portal where users can post, browse, filter, and search "
            "lost-and-found listings, preloaded with a few sample listings.\n\n"
            "## Estimated development duration\n"
            "35–40 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "CRUD over client-side state, form handling, image handling, "
            "search/filter logic, lifting state, localStorage persistence\n\n"
            "## Technical challenges\n"
            "- Keeping the filtered list in sync with the search input and\n"
            "  active filters\n"
            "- Handling image URLs gracefully when an image fails to load\n\n"
            "## Suggested implementation approach\n"
            "Store listings in React state, render them as cards, add a search "
            "bar and two filter selects that narrow the list in memory, and "
            "persist to localStorage whenever a listing is added or marked "
            "resolved.\n\n"
            "## Possible future improvements\n"
            "User profiles, moderation queue, map view, real-time chat\n\n"
            "## Limitations\n"
            "MVP stores photos as URLs only (no file storage). Data lives in one "
            "browser and is not synced across devices. Contact information is "
            "shown publicly, so users should share only what they are "
            "comfortable sharing."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-004",
        title="Student Resource Exchange",
        summary=(
            "A place for students to upload and share study resources (notes, "
            "lab manuals, reference books), organised by subject and semester, "
            "with search, ratings, and a way to report broken resources."
        ),
        who_affected=(
            "Students looking for course materials, and students who want to "
            "share resources they have created or collected."
        ),
        why_matters=(
            "Useful notes and manuals are often locked in personal drives or "
            "chat groups. A shared exchange makes course materials easier to "
            "discover and helps students prepare for exams and labs."
        ),
        domain="education",
        est_hours=38,
        tech_tags=["react", "javascript", "css", "localstorage", "crud", "search"],
        datasets=[{"name": "Sample study resources", "url": None}],
        approaches=[
            "Store resources as objects with title, link, subject, semester, "
            "description, and rating.",
            "Render a filterable grid by subject and semester.",
            "Add a search bar that matches title, subject, and description.",
            "Allow thumbs-up ratings and a report flag per resource.",
            "Persist resources to localStorage.",
        ],
        original_text=(
            "# Student Resource Exchange\n\n"
            "## Problem statement\n"
            "Students often have difficulty finding useful notes, lab manuals, "
            "reference books, and study resources shared by other students. "
            "Materials tend to be scattered across personal drives, chat groups, "
            "and old emails, so discovering them takes longer than it should.\n\n"
            "## Proposed solution\n"
            "A student-run exchange where anyone can upload or link a study "
            "resource, tag it by subject and semester, and others can search, "
            "filter, rate helpfulness, and report broken or inappropriate "
            "resources.\n\n"
            "## Target audience\n"
            "College and school students.\n\n"
            "## Real-world use case\n"
            "A student needs last semester's organic chemistry lab manual. They "
            "search the exchange, find a PDF shared by a peer, download it, and "
            "mark it as helpful.\n\n"
            "## Core features (MVP)\n"
            "- Upload or link a study resource with title, file or link, "
            "subject, semester, and description\n"
            "- Organise resources by subject and semester\n"
            "- Search and filter uploaded materials by keyword\n"
            "- Add a helpfulness rating (thumbs up)\n"
            "- Allow users to report broken or inappropriate resources\n"
            "- Persist resources in browser localStorage\n\n"
            "## Optional features (post-MVP)\n"
            "- User profiles and upload history\n"
            "- Download/view counts per resource\n"
            "- Comments on resources\n"
            "- Resource tags (notes, lab manual, reference book, previous-year "
            "paper)\n\n"
            "## Stretch goals\n"
            "- Actual file storage (requires a backend)\n"
            "- Search by course code\n"
            "- Resource requests (students can ask for a specific material)\n\n"
            "## Suggested technology stack\n"
            "React, CSS, vanilla JavaScript, browser localStorage (Firebase is "
            "an optional enhancement for file storage)\n\n"
            "## Required skills\n"
            "File/link handling, CRUD, search, categorisation, ratings, basic "
            "moderation\n\n"
            "## Expected deliverables\n"
            "A working exchange where students can post resources, browse by "
            "subject/semester, search, rate, and report, preloaded with sample "
            "resources.\n\n"
            "## Estimated development duration\n"
            "35–40 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "File and link handling, CRUD operations, search and filtering, "
            "categorisation, rating mechanics, content-report flow\n\n"
            "## Technical challenges\n"
            "- Validating that a submitted link looks like a real URL\n"
            "- Keeping search results responsive as the dataset grows\n\n"
            "## Suggested implementation approach\n"
            "Store resources in React state, render filterable cards, add a "
            "keyword search across title/subject/description, and persist to "
            "localStorage. Keep the MVP link-based rather than building file "
            "upload.\n\n"
            "## Possible future improvements\n"
            "User profiles, comments, download counts, file storage\n\n"
            "## Limitations\n"
            "MVP stores links rather than files (no file server). Content "
            "moderation is report-based and manual. Not a substitute for "
            "official course materials provided by instructors."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-005",
        title="Household Waste Sorting Guide",
        summary=(
            "A searchable directory of common household items that tells users "
            "which waste bin each item belongs in, plus disposal and recycling "
            "tips."
        ),
        who_affected=(
            "Households, students in shared accommodation, and anyone unsure "
            "how to dispose of batteries, plastic bottles, electronics, or "
            "packaging."
        ),
        why_matters=(
            "Putting the wrong item in the wrong bin contaminates recycling and "
            "sends reusable material to landfill. A quick lookup helps people "
            "dispose of waste correctly."
        ),
        domain="climate",
        est_hours=24,
        tech_tags=["html", "css", "javascript", "json", "search"],
        datasets=[{"name": "Sample household waste directory", "url": None}],
        approaches=[
            "Build a JSON array of common waste items with category, disposal "
            "instructions, and recycling tips.",
            "Render the directory as searchable cards.",
            "Filter results as the user types a keyword.",
            "Highlight the matching category and show disposal steps.",
            "Group items by waste category for browsing.",
        ],
        original_text=(
            "# Household Waste Sorting Guide\n\n"
            "## Problem statement\n"
            "People frequently do not know how to dispose of different types of "
            "waste correctly. For example, whether batteries, plastic bottles, "
            "or cardboard go in the recycling bin, the general waste bin, or a "
            "special drop-off point.\n\n"
            "## Proposed solution\n"
            "A searchable directory where a user looks up an item (batteries, "
            "plastic bottles, cardboard, electronics, etc.) and sees its waste "
            "category, disposal instructions, and recycling tips.\n\n"
            "## Target audience\n"
            "Households, students in shared accommodation, and environmentally "
            "conscious residents.\n\n"
            "## Real-world use case\n"
            "A user searches for \"battery\" and learns it is hazardous waste "
            "that belongs at a drop-off point, not in the regular bin.\n\n"
            "## Core features (MVP)\n"
            "- Search for an item such as batteries, plastic bottles, or "
            "cardboard\n"
            "- Show its waste category (recyclable, hazardous, organic, "
            "general, electronic)\n"
            "- Display disposal instructions\n"
            "- Display recycling tips\n"
            "- Searchable directory of common household waste items\n"
            "- Responsive layout that works on phone and desktop\n\n"
            "## Optional features (post-MVP)\n"
            "- Let users suggest or add custom items\n"
            "- Favourite or bookmark items\n"
            "- Local drop-off locations\n"
            "- Print-friendly view\n\n"
            "## Stretch goals\n"
            "- Barcode or photo lookup\n"
            "- Location-based drop-off finder\n"
            "- Gamified sorting quiz\n\n"
            "## Suggested technology stack\n"
            "HTML, CSS, vanilla JavaScript, JSON data\n\n"
            "## Required skills\n"
            "Search, conditional rendering, JSON data handling, responsive UI, "
            "filtering\n\n"
            "## Expected deliverables\n"
            "A working, mobile-friendly waste-lookup tool preloaded with a "
            "curated directory of common household items.\n\n"
            "## Estimated development duration\n"
            "20–25 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Working with JSON data, client-side search and filtering, "
            "conditional rendering based on category, responsive layouts\n\n"
            "## Technical challenges\n"
            "- Matching synonyms (for example, \"pop bottle\" and \"plastic "
            "bottle\") to the same entry\n"
            "- Keeping the UI fast as the directory grows\n\n"
            "## Suggested implementation approach\n"
            "Build a JSON array of waste items, render them as cards, add a "
            "search bar that filters the list as the user types, and show "
            "category + disposal instructions + recycling tips for each match.\n\n"
            "## Possible future improvements\n"
            "Custom item suggestions, drop-off locations, print view\n\n"
            "## Limitations\n"
            "Disposal rules vary by city and country, so the dataset is "
            "illustrative and must be localised before real use. This is not "
            "official waste-management guidance."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-006",
        title="Shared Expense Splitter",
        summary=(
            "A tool for friends or housemates to log shared expenses, split "
            "them equally or by custom amounts, and see who owes whom."
        ),
        who_affected=(
            "Friends sharing trips, meals, or accommodation, and housemates "
            "splitting rent and utilities."
        ),
        why_matters=(
            "Tracking who paid for what gets confusing quickly, especially in "
            "groups. A simple balance sheet prevents awkwardness and makes "
            "settling up straightforward."
        ),
        domain="fintech",
        est_hours=32,
        tech_tags=["react", "javascript", "localstorage", "state-management", "calculations"],
        datasets=[{"name": "Sample group and expenses", "url": None}],
        approaches=[
            "Model a group as members plus an array of expenses.",
            "Each expense records the payer, amount, and split (equal or custom "
            "per member).",
            "Compute each member's balance as paid minus share.",
            "Render a settlement table showing who pays whom and how much.",
            "Persist the group to localStorage.",
        ],
        original_text=(
            "# Shared Expense Splitter\n\n"
            "## Problem statement\n"
            "Friends sharing accommodation, trips, or meals often struggle to "
            "track who paid and who owes whom. Receipts and mental maths lead to "
            "disagreements when it is time to settle up.\n\n"
            "## Proposed solution\n"
            "A simple group expense tracker where users create a group, add "
            "members, log expenses with a payer, and split each expense equally "
            "or by custom amounts. The app calculates individual balances and "
            "shows who should pay whom.\n\n"
            "## Target audience\n"
            "Students, friends, housemates, and travel groups.\n\n"
            "## Real-world use case\n"
            "Three friends on a trip log meals and transport. The app shows each "
            "person's balance and a settlement summary: who should pay whom and "
            "how much, so everyone settles fairly at the end.\n\n"
            "## Core features (MVP)\n"
            "- Create a group\n"
            "- Add members to a group\n"
            "- Add expenses (payer, amount, date, note)\n"
            "- Split expenses equally or by custom amounts\n"
            "- Calculate individual balances\n"
            "- Show who owes whom (settlement summary)\n"
            "- Persist data in browser localStorage\n\n"
            "## Optional features (post-MVP)\n"
            "- Multiple groups\n"
            "- Edit or delete expenses\n"
            "- Mark expenses as settled\n"
            "- Expense history\n\n"
            "## Stretch goals\n"
            "- Recurring expenses (rent, utilities)\n"
            "- Receipt photos\n"
            "- Export a settlement summary\n"
            "- Currency selection\n\n"
            "## Suggested technology stack\n"
            "React, vanilla JavaScript, browser localStorage\n\n"
            "## Required skills\n"
            "Arrays and objects, arithmetic, forms, state management, derived "
            "data (balances from expenses)\n\n"
            "## Expected deliverables\n"
            "A working expense splitter where a group can log expenses, split "
            "them, and see a clear who-owes-whom summary, preloaded with a "
            "sample group.\n\n"
            "## Estimated development duration\n"
            "30–35 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Modelling data with arrays and objects, derived-state calculations, "
            "form handling, client-side persistence\n\n"
            "## Technical challenges\n"
            "- Handling custom splits that must add up to the total\n"
            "- Displaying a sensible settlement summary (minimising payments)\n\n"
            "## Suggested implementation approach\n"
            "Model a group as members plus expenses. Compute each balance as "
            "paid minus share. Render a table of who pays whom. Persist to "
            "localStorage on every change.\n\n"
            "## Possible future improvements\n"
            "Multiple groups, settlements, receipts, export\n\n"
            "## Limitations\n"
            "Single device/browser in the MVP; no authentication. Balances are "
            "lost if localStorage is cleared. Not an accounting or tax tool."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-007",
        title="Public Service & Government Scheme Finder",
        summary=(
            "A searchable directory of public services and government welfare "
            "schemes, with eligibility requirements, documents needed, and links "
            "to official application pages."
        ),
        who_affected=(
            "Citizens, students, and families who want to know which government "
            "services or welfare schemes they may be eligible for."
        ),
        why_matters=(
            "Eligible people often miss out on schemes simply because they do "
            "not know they exist or what documents are needed. A plain-language "
            "directory lowers that barrier."
        ),
        domain="governance",
        est_hours=28,
        tech_tags=["html", "css", "javascript", "json", "search"],
        datasets=[
            {"name": "Curated public schemes directory (sample region)", "url": None}
        ],
        approaches=[
            "Curate a JSON list of schemes with name, category, intended "
            "audience, eligibility, documents, and official URL.",
            "Render as cards with a search bar and category/audience filters.",
            "Match search against scheme name, category, and description.",
            "Show source name and last-updated date prominently on every card "
            "and the detail view.",
            "Link out to official application pages only.",
        ],
        original_text=(
            "# Public Service & Government Scheme Finder\n\n"
            "## Problem statement\n"
            "People often do not know which government services or public "
            "welfare schemes they are eligible to access. Information is spread "
            "across many department websites, and eligibility rules are written "
            "in formal language, so eligible people miss out.\n\n"
            "## Proposed solution\n"
            "A plain-language directory of public schemes and services. Users "
            "can browse, filter by category and intended audience, search by "
            "keyword, and see eligibility requirements, documents needed, and a "
            "link to the official application website for each scheme.\n\n"
            "## Target audience\n"
            "Citizens, students, low-income families, seniors, and anyone "
            "seeking public welfare support.\n\n"
            "## Real-world use case\n"
            "A user searches for \"student scholarship\" and sees the schemes "
            "they may qualify for, the required documents (for example, ID and "
            "income certificate), and the official application link for each.\n\n"
            "## Core features (MVP)\n"
            "- List available public schemes and services\n"
            "- Filter by category and intended audience\n"
            "- Search using keywords\n"
            "- Display eligibility requirements and documents needed\n"
            "- Link to official application websites\n"
            "- Show the source and last-updated date so users know how fresh the "
            "information is\n\n"
            "## Optional features (post-MVP)\n"
            "- Bookmark or favourite schemes\n"
            "- Share a scheme link\n"
            "- Simple eligibility quiz\n"
            "- Print-friendly scheme sheet\n\n"
            "## Stretch goals\n"
            "- Location-based schemes (state or city)\n"
            "- Application status tracker\n"
            "- Scheme deadline reminders\n\n"
            "## Suggested technology stack\n"
            "HTML, CSS, vanilla JavaScript, JSON data\n\n"
            "## Required skills\n"
            "Search, filtering, data organisation, external links, source "
            "transparency\n\n"
            "## Expected deliverables\n"
            "A working directory of schemes preloaded with a curated dataset for "
            "one region, clearly labelled with source and last-updated date.\n\n"
            "## Estimated development duration\n"
            "25–30 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Working with structured JSON data, client-side search and "
            "filtering, rendering data as cards, safe external linking\n\n"
            "## Technical challenges\n"
            "- Keeping search relevant across scheme name, category, and "
            "description\n"
            "- Presenting eligibility rules in plain language without "
            "oversimplifying\n\n"
            "## Suggested implementation approach\n"
            "Curate a JSON list of schemes, render cards, add search and "
            "category/audience filters, and display source + last-updated date "
            "on every card.\n\n"
            "## Possible future improvements\n"
            "Bookmarks, eligibility quiz, location-based filtering\n\n"
            "## Limitations and assumptions\n"
            "Scheme details change over time, so the source and last-updated "
            "date must be displayed and the data periodically reviewed. This is "
            "not legal advice. Users should always verify on the official "
            "website. The MVP uses a manually curated dataset for one region, "
            "not live government data."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-008",
        title="Small Business Digital Catalogue",
        summary=(
            "A simple product catalogue for small local businesses to showcase "
            "items with images, descriptions, prices, and a WhatsApp enquiry "
            "link, without a full e-commerce store."
        ),
        who_affected=(
            "Small local shop owners, artisans, and home-based businesses "
            "wanting an online presence."
        ),
        why_matters=(
            "Many small businesses cannot afford or do not need a full online "
            "shop. A lightweight catalogue lets customers browse products and "
            "enquire by WhatsApp."
        ),
        domain="social-impact",
        est_hours=28,
        tech_tags=["react", "javascript", "css", "localstorage", "search"],
        datasets=[{"name": "Sample product catalogue", "url": None}],
        approaches=[
            "Store products as objects with name, image URL, description, "
            "price, and category.",
            "Render a responsive product grid.",
            "Add category filter pills and a name search bar.",
            "Build a WhatsApp deep link with a pre-filled enquiry message per "
            "product.",
            "Persist products to localStorage.",
        ],
        original_text=(
            "# Small Business Digital Catalogue\n\n"
            "## Problem statement\n"
            "Small local businesses often lack a simple way to showcase their "
            "products online without building and maintaining a full e-commerce "
            "store with payments, inventory, and shipping.\n\n"
            "## Proposed solution\n"
            "A lightweight digital catalogue where a business adds products with "
            "images, descriptions, and prices. Customers can browse, filter by "
            "category, search by name, and send a WhatsApp enquiry for any "
            "product.\n\n"
            "## Target audience\n"
            "Small shop owners, artisans, bakeries, and home-based businesses.\n\n"
            "## Real-world use case\n"
            "A bakery lists cakes with photos and prices. A customer browses, "
            "filters by \"cakes\", and sends a WhatsApp message to place an "
            "order.\n\n"
            "## Core features (MVP)\n"
            "- Create a product catalogue\n"
            "- Add products with images, descriptions, and prices\n"
            "- Filter products by category\n"
            "- Search products by name\n"
            "- Provide a WhatsApp enquiry link for each product\n"
            "- Persist the catalogue in browser localStorage\n\n"
            "## Optional features (post-MVP)\n"
            "- Product details page\n"
            "- Stock status (in stock / out of stock)\n"
            "- Featured items\n"
            "- Business contact information\n\n"
            "## Stretch goals\n"
            "- Online ordering enquiry form\n"
            "- Image upload (requires storage backend)\n"
            "- Multi-language support\n\n"
            "## Suggested technology stack\n"
            "React, CSS, JSON or browser localStorage (Firebase is an optional "
            "enhancement)\n\n"
            "## Required skills\n"
            "Dynamic rendering, responsive layouts, search, data management, "
            "deep links\n\n"
            "## Expected deliverables\n"
            "A working, mobile-friendly catalogue preloaded with sample "
            "products, where customers can browse and WhatsApp to enquire.\n\n"
            "## Estimated development duration\n"
            "25–30 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Dynamic rendering from data, responsive product grids, search and "
            "filtering, WhatsApp deep links, client-side persistence\n\n"
            "## Technical challenges\n"
            "- Handling products without images gracefully\n"
            "- Keeping search and category filter combined correctly\n\n"
            "## Suggested implementation approach\n"
            "Store products in React state, render a responsive grid, add "
            "category filter pills and a name search bar, and generate a "
            "WhatsApp deep link with a pre-filled message for each product. "
            "Persist to localStorage.\n\n"
            "## Possible future improvements\n"
            "Product details page, stock status, image upload\n\n"
            "## Limitations\n"
            "Enquiry-only in the MVP. No payment or checkout. Images are stored "
            "as URLs. Data lives in one browser. The WhatsApp link depends on "
            "the customer having WhatsApp installed."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-009",
        title="Public Transport Route & Fare Guide",
        summary=(
            "A manually curated guide to local bus routes, stops, and fares for "
            "one city, with source-to-destination search and links to official "
            "transport information."
        ),
        who_affected=(
            "New residents, students, and visitors trying to learn local bus "
            "routes, stops, and fares."
        ),
        why_matters=(
            "Transit information is hard to navigate for newcomers. A simple, "
            "curated route guide helps people plan journeys without needing a "
            "live data feed."
        ),
        domain="transport",
        est_hours=32,
        tech_tags=["react", "javascript", "json", "geospatial", "leaflet"],
        datasets=[
            {"name": "Curated bus routes for one city (sample)", "url": None}
        ],
        approaches=[
            "Curate a JSON list of routes with ordered stops and fare.",
            "Implement a source-to-destination search that finds routes "
            "containing both stops.",
            "Render the stop sequence for a selected route.",
            "Show fare and a link to the official transport authority.",
            "Optionally add a Leaflet map showing stops along the route.",
        ],
        original_text=(
            "# Public Transport Route & Fare Guide\n\n"
            "## Problem statement\n"
            "People who are new to a city often struggle to understand local bus "
            "routes, stops, and fares. Route maps and timetables can be "
            "overwhelming, and there is no simple place to ask \"which bus goes "
            "from A to B?\"\n\n"
            "## Proposed solution\n"
            "A beginner-friendly guide listing bus routes, stops along each "
            "route, and fares. Users can search by source and destination to "
            "find matching routes, and follow links to official transport "
            "information.\n\n"
            "## Target audience\n"
            "New residents, students, visitors, and occasional riders in one "
            "city.\n\n"
            "## Real-world use case\n"
            "A student searches \"university to central station\" and sees the "
            "bus route, the stops along the way, and the fare.\n\n"
            "## Core features (MVP)\n"
            "- List available bus routes\n"
            "- Search routes using source and destination\n"
            "- Display stops along a route\n"
            "- Show available fare information\n"
            "- Provide links to official transport information\n"
            "- Use a manually curated dataset for one city\n\n"
            "## Optional features (post-MVP)\n"
            "- Fare by zone or route\n"
            "- Static route map (for example, Leaflet)\n"
            "- Favourite routes\n"
            "- Accessibility information per route\n\n"
            "## Stretch goals\n"
            "- Live bus positions (requires a transit API)\n"
            "- Multi-modal journey planning\n"
            "- Real-time service alerts\n\n"
            "## Suggested technology stack\n"
            "React, vanilla JavaScript, JSON data, Leaflet (optional map)\n\n"
            "## Required skills\n"
            "Data structures, search, filtering, map basics\n\n"
            "## Expected deliverables\n"
            "A working route guide preloaded with a curated dataset for one "
            "city, where users can search source-to-destination and see stops "
            "and fares.\n\n"
            "## Estimated development duration\n"
            "30–35 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Working with route data structures, source-to-destination search, "
            "filtering, basic map rendering\n\n"
            "## Technical challenges\n"
            "- Matching a source and destination to routes that contain both\n"
            "- Displaying stops in the correct order along a route\n\n"
            "## Suggested implementation approach\n"
            "Curate a JSON list of routes with ordered stops and fare. Build a "
            "search that finds routes containing both the source and destination "
            "stops, then render the stop sequence and fare.\n\n"
            "## Possible future improvements\n"
            "Route map, favourites, service alerts\n\n"
            "## Limitations\n"
            "The dataset is manually curated and goes out of date, so the source "
            "and last-updated date must be displayed. There is no live transit "
            "integration in the MVP; start with one city rather than attempting "
            "live data."
        ),
    ),
    _project(
        source_id="manabi-web-beginner-010",
        title="Privacy Policy Simplifier",
        summary=(
            "A rule-based tool that pastes a privacy policy and highlights "
            "mentions of data collection, cookies, and third-party sharing, "
            "producing a plain-language summary."
        ),
        who_affected=(
            "Website users who accept privacy policies without reading them, "
            "and students learning how privacy disclosures work."
        ),
        why_matters=(
            "Privacy policies are long and written in legal language. "
            "Highlighting the key clauses helps people understand what is "
            "collected and shared, without needing a law degree."
        ),
        domain="cybersecurity",
        est_hours=24,
        tech_tags=["html", "css", "javascript", "regex", "text-processing"],
        datasets=[{"name": "Sample privacy policy text", "url": None}],
        approaches=[
            "Accept pasted privacy-policy text in an editor.",
            "Define keyword and phrase rules for each section (data collection, "
            "cookies, third-party sharing, children's data, retention).",
            "Use regular expressions to find and highlight matches in the text.",
            "Summarise which sections were detected and how often.",
            "Show the original text alongside the highlighted version.",
        ],
        original_text=(
            "# Privacy Policy Simplifier\n\n"
            "## Problem statement\n"
            "Most people accept website privacy policies without understanding "
            "what information is collected or how it is used. Policies are long, "
            "written in legal language, and the important clauses are hard to "
            "find.\n\n"
            "## Proposed solution\n"
            "A rule-based educational tool where a user pastes a privacy policy "
            "and the tool highlights mentions of data collection, cookies, "
            "third-party sharing, and related clauses using predefined keyword "
            "rules, then produces a plain-language summary of the detected "
            "sections.\n\n"
            "## Target audience\n"
            "General web users, students, and privacy-curious individuals.\n\n"
            "## Real-world use case\n"
            "A user pastes a website's privacy policy. The tool highlights \"we "
            "collect your email address\" and \"we share data with partners\" "
            "and produces a short summary of the detected sections.\n\n"
            "## Core features (MVP)\n"
            "- Paste a privacy policy into a text editor\n"
            "- Highlight important sections using predefined keyword rules\n"
            "- Identify mentions of data collection, cookies, and "
            "third-party sharing\n"
            "- Display a simple summary of identified sections\n"
            "- Show the original text alongside the highlighted content\n\n"
            "## Optional features (post-MVP)\n"
            "- Upload a .txt file\n"
            "- Export the summary\n"
            "- Custom keyword rules\n"
            "- Plain-language rewrite suggestions\n\n"
            "## Stretch goals\n"
            "- Support multiple languages\n"
            "- PDF upload\n"
            "- Saved policies\n\n"
            "## Suggested technology stack\n"
            "HTML, CSS, vanilla JavaScript, regular expressions\n\n"
            "## Required skills\n"
            "String manipulation, text processing, DOM manipulation, regular "
            "expressions\n\n"
            "## Expected deliverables\n"
            "A working simplifier that highlights key clauses in a pasted "
            "privacy policy and produces a short summary, with a sample policy "
            "preloaded.\n\n"
            "## Estimated development duration\n"
            "20–25 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "String manipulation, text processing, DOM manipulation, regular "
            "expressions, rule-based detection\n\n"
            "## Technical challenges\n"
            "- Writing keyword rules that catch the right clauses without too "
            "much noise\n"
            "- Highlighting matches inside the original text while preserving "
            "layout\n\n"
            "## Suggested implementation approach\n"
            "Accept pasted text, run a set of regex rules over it, wrap matches "
            "in highlighted spans, count detections per category, and render a "
            "summary next to the highlighted text.\n\n"
            "## Possible future improvements\n"
            "File upload, export, custom rules, rewrite suggestions\n\n"
            "## Limitations\n"
            "This is a rule-based educational tool, not a legal assessment or a "
            "guarantee of policy completeness. Keyword matching may miss clauses "
            "or over-flag text. Users should not rely on it for legal decisions."
        ),
    ),
]
def main() -> int:
    inserted = skipped = 0
    with session_scope() as db:
        for data in PROJECTS:
            existing = db.scalar(
                select(Problem).where(
                    Problem.source_name == data["source_name"],
                    Problem.source_id == data["source_id"],
                )
            )
            if existing is not None:
                skipped += 1
                continue
            db.add(Problem(**data))
            inserted += 1
    print(
        f"Beginner web projects - inserted: {inserted}, skipped: {skipped}, "
        f"total: {len(PROJECTS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
