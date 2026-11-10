"""Seed the catalog with 10 curated Intermediate Web Development project ideas.

These are *curated suggestions*, not official problem statements from any
organisation. Each row is inserted with origin="manual" and status="published".

The script is idempotent: re-running it skips rows whose
(source_name, source_id) already exist, so it is safe to run more than once.

Usage (from the backend directory):
    .venv/Scripts/python scripts/seed_intermediate_web_projects.py
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
    team_plan: dict | None = None,
    pitch_guide: dict | None = None,
) -> dict:
    entry = {
        "source_id": source_id,
        "title": title,
        "summary": summary,
        "who_affected": who_affected,
        "why_matters": why_matters,
        "field": "web-dev",
        "domain": domain,
        "difficulty": "intermediate",
        "est_hours": est_hours,
        "tech_tags": tech_tags,
        "datasets": datasets,
        "approaches": approaches,
        "source_name": SOURCE_NAME,
        "source_url": None,
        "source_note": (
            "Curated intermediate project idea. Not an official problem "
            "statement from any organisation, company, or hackathon."
        ),
        "original_text": original_text,
        "ai_fields": [],  # Manually curated; nothing here was AI-generated.
        "created_by": None,
        "goal": "hackathon",
    }
    if team_plan is not None:
        entry["team_plan"] = team_plan
    if pitch_guide is not None:
        entry["pitch_guide"] = pitch_guide
    return entry


PROJECTS = [
    _project(
        source_id="manabi-web-intermediate-001",
        title="Community Skill Exchange Platform",
        summary=(
            "A peer-to-peer platform where users offer skills they can teach "
            "and request skills they want to learn, matching people for "
            "barter-style exchanges instead of paid courses."
        ),
        who_affected=(
            "Learners who cannot afford formal courses, skilled people who want "
            "to teach, and hobbyists or professionals trading knowledge."
        ),
        why_matters=(
            "Formal courses are expensive and often inaccessible. Peer-to-peer "
            "skill exchange lowers cost, builds community, and directly matches "
            "teaching supply with learning demand."
        ),
        domain="social-impact",
        est_hours=60,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "authentication",
            "matching",
            "scheduling",
        ],
        datasets=[{"name": "Sample users and skills", "url": None}],
        approaches=[
            "User registration with profiles listing teachable skills and "
            "desired skills.",
            "A matching algorithm that pairs users whose offered skills overlap "
            "with another user's requested skills.",
            "Exchange requests with accept/reject flow and a scheduling calendar.",
            "User ratings and reviews after each completed exchange.",
            "Persist users, skills, requests, and ratings in a relational "
            "database with proper foreign keys.",
        ],
        original_text=(
            "# Community Skill Exchange Platform\n\n"
            "## Problem statement\n"
            "People often have skills they are willing to teach but no easy way "
            "to find learners, while learners who want skills cannot always "
            "afford courses or find a willing teacher. Knowledge exchange is "
            "fragmented across informal chats and word of mouth.\n\n"
            "## Proposed solution\n"
            "A web platform where every user lists skills they can teach and "
            "skills they want to learn. A matching engine pairs complementary "
            "users, who then send exchange requests, schedule sessions, and "
            "rate each other afterward — all without money changing hands.\n\n"
            "## Target audience\n"
            "Students, freelancers, hobbyists, and professionals looking to "
            "learn or teach practical skills affordably.\n\n"
            "## Real-world use case\n"
            "A user offers guitar lessons and wants to learn web design. The "
            "platform matches them with a designer who wants to learn guitar. "
            "They schedule two weekly sessions, teach each other, and leave "
            "ratings.\n\n"
            "## Core features (MVP)\n"
            "- User sign-up, login, and profile with teachable and desired skills\n"
            "- Skill-based matching between users\n"
            "- Send, accept, or reject exchange requests\n"
            "- Schedule exchange sessions on a shared calendar\n"
            "- Rate and review partners after an exchange\n"
            "- Browse suggested matches and incoming requests\n\n"
            "## Optional features (post-MVP)\n"
            "- Skill categories and difficulty levels\n"
            "- Video call integration\n"
            "- Badges for top teachers and active learners\n"
            "- Email reminders before scheduled sessions\n\n"
            "## Stretch goals\n"
            "- Group skill swaps\n"
            "- Verified skill badges\n"
            "- Mobile app\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, JSON Web Tokens for auth\n\n"
            "## Required skills\n"
            "Authentication, relational database design, matching algorithms, "
            "scheduling logic, ratings and reviews\n\n"
            "## Estimated development duration\n"
            "55–65 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "User authentication, relational data modelling, matching logic, "
            "date/time scheduling, review aggregation\n\n"
            "## Technical challenges\n"
            "- Designing a matching query that is performant as the user base grows\n"
            "- Preventing duplicate or spam exchange requests\n"
            "- Keeping scheduled sessions consistent across time zones\n\n"
            "## Suggested implementation approach\n"
            "Start with user profiles and a skills table. Build a SQL-based "
            "match query that finds users offering skills another user wants. "
            "Add request and scheduling tables, then ratings.\n\n"
            "## Possible future improvements\n"
            "- Skill categories, video calls, badges\n"
            "- Session notes and progress tracking\n\n"
            "## Limitations\n"
            "MVP is text-based scheduling; no built-in video. Matches depend on "
            "users keeping their skill lists accurate."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-002",
        title="Real-Time Collaborative Workspace",
        summary=(
            "A shared document editor where multiple users can edit the same "
            "document simultaneously, see live cursor positions, and browse "
            "document version history."
        ),
        who_affected=(
            "Remote teams, students working on group projects, and anyone "
            "co-authoring documents who needs live coordination."
        ),
        why_matters=(
            "Emailing document copies back and forth creates version conflicts "
            "and coordination overhead. A real-time workspace lets collaborators "
            "edit together and see each other's presence instantly."
        ),
        domain="developer-tools",
        est_hours=80,
        tech_tags=[
            "react",
            "websockets",
            "nodejs",
            "postgresql",
            "crdt",
            "real-time",
        ],
        datasets=[{"name": "Sample shared documents", "url": None}],
        approaches=[
            "WebSocket connections for live synchronization between clients.",
            "Operational transformation or CRDTs to merge concurrent edits "
            "without data loss.",
            "Presence indicators showing which users are online and where their "
            "cursors are.",
            "An append-only version history so users can view and restore past "
            "document states.",
            "Authentication and per-document access control.",
        ],
        original_text=(
            "# Real-Time Collaborative Workspace\n\n"
            "## Problem statement\n"
            "Teams co-authoring documents usually pass files around by email or "
            "chat, which produces conflicting copies and makes it hard to know "
            "who is editing what at any moment.\n\n"
            "## Proposed solution\n"
            "A shared workspace where multiple users open the same document and "
            "see each other's edits, cursors, and selections in real time. "
            "Changes are merged automatically, and every version is saved so "
            "users can roll back.\n\n"
            "## Target audience\n"
            "Remote teams, educators, student project groups, and technical "
            "writers.\n\n"
            "## Real-world use case\n"
            "Three teammates open a project proposal. As one edits the budget "
            "section, another rewrites the timeline. Both see cursors move and "
            "changes appear instantly without overwriting each other.\n\n"
            "## Core features (MVP)\n"
            "- Create, name, and open shared documents\n"
            "- Simultaneous text editing with live synchronization\n"
            "- User presence indicators and cursor positions\n"
            "- Document version history with restore points\n"
            "- User login and document access control\n\n"
            "## Optional features (post-MVP)\n"
            "- Comments and threaded discussions on document sections\n"
            "- Export to PDF or Markdown\n"
            "- @mentions to notify collaborators\n"
            "- Offline editing with sync on reconnect\n\n"
            "## Stretch goals\n"
            "- Rich text (bold, lists, images)\n"
            "- Multiple rooms or workspaces\n"
            "- Public share links\n\n"
            "## Suggested technology stack\n"
            "React, Node.js, WebSockets (Socket.io or ws), PostgreSQL, Yjs or "
            "similar CRDT library\n\n"
            "## Required skills\n"
            "WebSockets, real-time synchronization, conflict handling, "
            "authentication, version storage\n\n"
            "## Estimated development duration\n"
            "70–90 hours (solo)\n\n"
            "## Suggested team size\n"
            "2\n\n"
            "## Concepts the developer will learn\n"
            "WebSocket protocols, operational transformation/CRDTs, presence "
            "tracking, optimistic UI, append-only versioning\n\n"
            "## Technical challenges\n"
            "- Merging concurrent edits without losing data\n"
            "- Handling network disconnects and reconnection gracefully\n"
            "- Keeping cursor positions accurate across clients\n\n"
            "## Suggested implementation approach\n"
            "Set up a WebSocket server that broadcasts document operations. Use "
            "a CRDT or operational-transformation library to merge edits "
            "deterministically. Store each document version as an immutable "
            "record in PostgreSQL.\n\n"
            "## Possible future improvements\n"
            "- Rich text, comments, public links\n"
            "- Conflict-resolution UI for rare edge cases\n\n"
            "## Limitations\n"
            "Real-time collaboration over WebSockets requires a persistent "
            "server connection; the MVP does not support fully offline editing."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-003",
        title="Smart Appointment & Queue Management System",
        summary=(
            "An online appointment booking system for clinics, salons, and "
            "service centres, with live queue position tracking, cancellation, "
            "and rescheduling."
        ),
        who_affected=(
            "Small businesses managing appointments manually and customers "
            "tired of long, unpredictable waits."
        ),
        why_matters=(
            "Manual appointment books lead to scheduling conflicts, no-shows, "
            "and long waiting times. Online booking with live queue tracking "
            "improves efficiency and customer experience."
        ),
        domain="healthcare",
        est_hours=70,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "scheduling",
            "notifications",
            "transactions",
        ],
        datasets=[{"name": "Sample clinics and appointment slots", "url": None}],
        approaches=[
            "Business owners define services, staff, and available time slots.",
            "Customers book appointments online and receive confirmation.",
            "A live queue shows each customer's current position and estimated "
            "wait time.",
            "Customers can cancel or reschedule appointments, freeing slots for "
            "others.",
            "Database transactions prevent double-booking the same slot.",
        ],
        original_text=(
            "# Smart Appointment & Queue Management System\n\n"
            "## Problem statement\n"
            "Clinics, salons, and small service centres often manage "
            "appointments on paper or spreadsheets. This causes double-booking, "
            "long queues, and no way for customers to know their wait time.\n\n"
            "## Proposed solution\n"
            "A web system where businesses list services and available staff "
            "slots. Customers book online, see their live queue position, and "
            "can cancel or reschedule. Staff manage the queue and mark patients "
            "as served.\n\n"
            "## Target audience\n"
            "Clinics, salons, gyms, repair shops, and other appointment-based "
            "small businesses.\n\n"
            "## Real-world use case\n"
            "A patient books a dentist appointment for 2:00 PM. On arrival, "
            "they see they are third in the live queue with a 20-minute wait. "
            "If delayed, they reschedule from their phone and the slot opens "
            "for someone else.\n\n"
            "## Core features (MVP)\n"
            "- Business setup: services, staff, working hours\n"
            "- Online appointment booking by customers\n"
            "- Live queue position and estimated wait time\n"
            "- Cancel or reschedule existing appointments\n"
            "- Staff dashboard to mark arrivals and completions\n"
            "- Database transactions to prevent double-booking\n\n"
            "## Optional features (post-MVP)\n"
            "- SMS or email appointment reminders\n"
            "- Waitlist for fully booked slots\n"
            "- Recurring appointments\n"
            "- Business analytics (no-show rate, peak hours)\n\n"
            "## Stretch goals\n"
            "- Online payment at booking\n"
            "- Multi-location support\n"
            "- Mobile check-in kiosk mode\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL\n\n"
            "## Required skills\n"
            "Scheduling logic, database transactions, notifications, role-based "
            "access\n\n"
            "## Estimated development duration\n"
            "60–80 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "Time-slot modelling, transactional booking, queue state, customer "
            "notifications\n\n"
            "## Technical challenges\n"
            "- Preventing race conditions when two customers book the same slot\n"
            "- Calculating accurate wait times as appointments run late\n"
            "- Handling cancellations mid-queue without gaps\n\n"
            "## Suggested implementation approach\n"
            "Model services, staff, and slots as database rows. Use a "
            "transaction when booking to lock and mark a slot taken. Build a "
            "queue view ordered by appointment time that updates as staff mark "
            "customers served.\n\n"
            "## Possible future improvements\n"
            "- Reminders, waitlist, analytics\n"
            "- Online payments, multi-location\n\n"
            "## Limitations\n"
            "MVP assumes one business location. Wait times are estimates based "
            "on scheduled duration, not real-time service speed."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-004",
        title="Public Issue Reporting & Tracking Platform",
        summary=(
            "A civic platform where residents report local problems such as "
            "damaged roads, broken streetlights, or garbage accumulation with "
            "photos and locations, then track whether anything is being done."
        ),
        who_affected=(
            "Residents reporting neighbourhood issues and municipal staff or "
            "administrators assigning and resolving them."
        ),
        why_matters=(
            "Reports often disappear into email or phone calls with no status "
            "for the reporter. A tracked platform creates accountability and "
            "visibility into issue resolution."
        ),
        domain="governance",
        est_hours=65,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "file-upload",
            "geolocation",
            "role-based-access",
        ],
        datasets=[{"name": "Sample reported issues", "url": None}],
        approaches=[
            "Residents submit reports with title, description, photo, and "
            "location (map pin or address).",
            "Each report gets a status (received, in-progress, resolved, "
            "rejected) and a public tracking reference.",
            "An admin dashboard lets staff assign reports to teams and update "
            "status.",
            "Role-based access separates reporters, staff, and administrators.",
            "File uploads for photos are stored securely and linked to reports.",
        ],
        original_text=(
            "# Public Issue Reporting & Tracking Platform\n\n"
            "## Problem statement\n"
            "Residents who report potholes, broken streetlights, or overflowing "
            "bins usually call a phone number or send an email and never hear "
            "whether the issue was fixed. There is no public record or status.\n\n"
            "## Proposed solution\n"
            "A web portal where anyone files a report with a photo and map "
            "location. Every report receives a status and tracking code so the "
            "reporter can check progress. An admin dashboard lets officials "
            "assign, update, and close reports.\n\n"
            "## Target audience\n"
            "City residents and municipal or housing-association staff.\n\n"
            "## Real-world use case\n"
            "A resident photographs a broken streetlight and pins its location. "
            "The report receives status \"received\" and tracking ID INC-104. "
            "A works crew assigns it to themselves, marks it \"in-progress\", "
            "and later \"resolved\". The resident sees the update online.\n\n"
            "## Core features (MVP)\n"
            "- Submit reports with title, description, photo, and location\n"
            "- Public status tracking by report ID\n"
            "- Admin dashboard to assign and update report status\n"
            "- Role-based access: reporter, staff, administrator\n"
            "- Secure photo upload linked to each report\n\n"
            "## Optional features (post-MVP)\n"
            "- Email notifications on status changes\n"
            "- Map view of all reported issues\n"
            "- Public comments or upvotes on issues\n"
            "- Escalation for overdue reports\n\n"
            "## Stretch goals\n"
            "- Mobile app with camera integration\n"
            "- Integration with municipal work-order systems\n"
            "- Analytics dashboard for issue trends\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, file storage (local or S3)\n\n"
            "## Required skills\n"
            "Role-based access control, geolocation, file uploads, workflow "
            "management, status transitions\n\n"
            "## Estimated development duration\n"
            "55–75 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "RBAC, file handling, map coordinates, state-machine workflows, "
            "public tracking references\n\n"
            "## Technical challenges\n"
            "- Securing photo uploads and serving them only to authorized users\n"
            "- Validating map locations and handling imprecise addresses\n"
            "- Defining valid status transitions so reports cannot skip steps\n\n"
            "## Suggested implementation approach\n"
            "Create a reports table with status enum and location fields. Add "
            "photo uploads stored on disk or object storage. Build an admin "
            "route protected by RBAC that transitions statuses.\n\n"
            "## Possible future improvements\n"
            "- Notifications, map view, upvotes\n"
            "- Mobile app, analytics, system integration\n\n"
            "## Limitations\n"
            "MVP stores photos as files/URLs; no AI triage. Status updates are "
            "manual by staff, not automatic."
        ),
        team_plan={
            "note": (
                "3 people, one weekend (24-36 focused hours). Roles overlap on "
                "purpose - when something catches fire, everyone helps."
            ),
            "roles": [
                {
                    "role": "API and database",
                    "covers": (
                        "Reports table, status history, photo storage, and "
                        "authentication. Owns every endpoint the other two call."
                    ),
                },
                {
                    "role": "Web app",
                    "covers": (
                        "The report form (photo + map pin), the public tracking "
                        "page, and the staff dashboard."
                    ),
                },
                {
                    "role": "Demo and fixes",
                    "covers": (
                        "Seed data, slides, screenshots, and end-to-end testing "
                        "of the demo path. Joins whoever is most behind."
                    ),
                },
            ],
            "milestones": [
                "Hour 8: a report can be created and stored with a photo and location.",
                "Hour 16: staff can change a status and the public page shows it.",
                "Hour 24: all three roles log in; the full demo path is usable.",
                "Hour 30: demo script frozen - only bug fixes after this point.",
            ],
        },
        pitch_guide={
            "one_liner": (
                "Every civic complaint becomes a numbered, trackable ticket, so "
                "residents stop wondering what happened to their report."
            ),
            "beats": [
                {
                    "heading": "Hook",
                    "text": (
                        "Ask the judges: have you ever reported a pothole and "
                        "never heard back? That silence is what we fix."
                    ),
                },
                {
                    "heading": "The problem",
                    "text": (
                        "Complaints come in by phone and email. A clerk notes "
                        "them somewhere that is not a system. Two weeks later, "
                        "nobody can say who is handling what, or whether it "
                        "was fixed."
                    ),
                },
                {
                    "heading": "Who feels it",
                    "text": (
                        "Residents repeat the same phone call and stop trusting "
                        "the office. Staff retype paper complaints and answer "
                        "'any update?' calls they have no way to check."
                    ),
                },
                {
                    "heading": "Our solution",
                    "text": (
                        "File a report with a photo and a map pin. It gets a "
                        "tracking number and a status: received, in-progress, "
                        "resolved, rejected. Staff get one dashboard to assign "
                        "and close reports. The resident needs nothing more "
                        "than a browser."
                    ),
                },
                {
                    "heading": "Live demo",
                    "text": (
                        "File a streetlight report, open a second tab as staff, "
                        "move the status, then show the resident's tab updating. "
                        "If the venue network dies: screenshots and locally "
                        "seeded data, no apology needed."
                    ),
                },
                {
                    "heading": "What's next",
                    "text": (
                        "Auto-assign reports by ward, deadline escalations, and "
                        "an open export of resolved issues for the public data "
                        "portal."
                    ),
                },
            ],
            "judge_questions": [
                {
                    "question": "Why would a municipality actually adopt this?",
                    "answer": (
                        "It replaces a phone-and-paper log with a tracked ticket "
                        "at zero cost to try. Staff need a browser and one "
                        "dashboard - onboarding is one screen, which we kept "
                        "small on purpose because adoption is the real risk."
                    ),
                },
                {
                    "question": "How do you stop duplicate reports for the same issue?",
                    "answer": (
                        "MVP shows 'similar reports nearby' on submit, matched by "
                        "category and area. We didn't silently merge - exact "
                        "dedupe is a hard problem and hiding reports is worse "
                        "than showing them."
                    ),
                },
                {
                    "question": "Is this just a CRUD app?",
                    "answer": (
                        "Deliberately, yes. The value is the workflow: status "
                        "transitions that cannot skip steps, assignment, and a "
                        "public tracking trail. Boring, well-run tech is what "
                        "a municipal office can actually maintain."
                    ),
                },
                {
                    "question": "Anyone can upload files - how is that safe?",
                    "answer": (
                        "Uploads are checked for type and size, stored under "
                        "generated names, and a report's photos are only served "
                        "with the report. Roles are enforced in the API, not by "
                        "hiding buttons in the UI."
                    ),
                },
                {
                    "question": "What does your demo not handle?",
                    "answer": (
                        "Bulk imports of past complaints, automatic triage, and "
                        "offline submissions. We cut those to make the core "
                        "loop solid, because that is the part that has to work."
                    ),
                },
                {
                    "question": "How do you know resolution complaints will drop?",
                    "answer": (
                        "The claim we can defend today: every report now has a "
                        "status and a timestamp, so 'where is my case' is answerable. "
                        "Measuring the trust effect needs pilot data - that is "
                        "exactly what the escalation and reports features are "
                        "for next."
                    ),
                },
            ],
        },
    ),
    _project(
        source_id="manabi-web-intermediate-005",
        title="API Monitoring & Status Dashboard",
        summary=(
            "A centralized dashboard where developers register API endpoints "
            "and monitor availability, response times, and downtime, with "
            "alerts and incident logs."
        ),
        who_affected=(
            "Developers and DevOps teams operating multiple APIs who need a "
            "single view of service health."
        ),
        why_matters=(
            "When APIs go down, teams often find out from users instead of "
            "monitoring. Continuous checks with alerts reduce mean time to "
            "detect and resolve incidents."
        ),
        domain="developer-tools",
        est_hours=60,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "cron",
            "time-series",
            "monitoring",
        ],
        datasets=[{"name": "Sample monitored endpoints", "url": None}],
        approaches=[
            "Users register API endpoints (URL, method, expected status).",
            "A background job polls each endpoint on a schedule and records "
            "status code and response time.",
            "Time-series storage of uptime and response-time history.",
            "Downtime alerts (email or in-app) when an endpoint fails checks.",
            "An incident log listing past outages and duration.",
        ],
        original_text=(
            "# API Monitoring & Status Dashboard\n\n"
            "## Problem statement\n"
            "Developers running several APIs lack a single place to see whether "
            "each is up, how fast it responds, and when it last went down. "
            "Outages are often discovered through user complaints.\n\n"
            "## Proposed solution\n"
            "A dashboard where users register API endpoints. A scheduled "
            "background job polls each one, stores availability and response "
            "time, and triggers alerts on failure. A status page and incident "
            "log show current and past health.\n\n"
            "## Target audience\n"
            "Backend developers, DevOps engineers, and API product teams.\n\n"
            "## Real-world use case\n"
            "A developer registers their payment API. Every five minutes the "
            "monitor pings it. When response time spikes above two seconds, an "
            "alert fires. The dashboard shows the outage window and recovery.\n\n"
            "## Core features (MVP)\n"
            "- Register, edit, and delete monitored API endpoints\n"
            "- Scheduled polling with status code and response-time recording\n"
            "- Uptime and response-time history charts\n"
            "- Downtime alerts when consecutive checks fail\n"
            "- Incident log with outage start, end, and duration\n\n"
            "## Optional features (post-MVP)\n"
            "- SMS or Slack alerts\n"
            "- Public status pages per service\n"
            "- SSL certificate expiry monitoring\n"
            "- Multiple check locations\n\n"
            "## Stretch goals\n"
            "- Synthetic transaction checks (login flows)\n"
            "- Alert escalation policies\n"
            "- API for the monitor itself\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, node-cron or similar\n\n"
            "## Required skills\n"
            "Background jobs, scheduled requests, time-series data, monitoring, "
            "alerting\n\n"
            "## Estimated development duration\n"
            "50–70 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Cron scheduling, time-series storage, health-check probing, "
            "alerting, charting time-series data\n\n"
            "## Technical challenges\n"
            "- Avoiding duplicate alerts for a single prolonged outage\n"
            "- Storing and querying time-series data efficiently in PostgreSQL\n"
            "- Handling slow or hanging endpoints without blocking the scheduler\n\n"
            "## Suggested implementation approach\n"
            "Create an endpoints table and a results table (timestamp, status "
            "code, response time). Run a cron job that hits each endpoint, "
            "inserts a result, and raises an alert after N consecutive "
            "failures. Chart results over time.\n\n"
            "## Possible future improvements\n"
            "- Slack/SMS alerts, public status pages, SSL monitoring\n"
            "- Synthetic checks, escalation policies\n\n"
            "## Limitations\n"
            "MVP polls from a single server location. Alerts are in-app or "
            "email only in the basic version."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-006",
        title="Freelance Project & Milestone Management Platform",
        summary=(
            "A platform where clients and freelancers coordinate projects, "
            "track milestones, submit deliverables, and manage feedback and "
            "revisions in one place."
        ),
        who_affected=(
            "Freelancers juggling multiple clients and clients who want a "
            "single source of truth for project progress and revisions."
        ),
        why_matters=(
            "Deliverables, feedback, and revisions scattered across email and "
            "chat cause missed deadlines and scope creep. A structured platform "
            "keeps project history and accountability in one place."
        ),
        domain="social-impact",
        est_hours=75,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "authorization",
            "workflow",
            "file-upload",
        ],
        datasets=[{"name": "Sample freelance projects", "url": None}],
        approaches=[
            "Clients create projects and invite freelancers; freelancers create "
            "profiles with skills and rates.",
            "Projects are broken into milestones with due dates and deliverables.",
            "Freelancers submit files for each milestone; clients review and "
            "request revisions or approve.",
            "Role-based authorization: clients own projects, freelancers submit "
            "work, both see activity history.",
            "An activity log records submissions, approvals, and revision "
            "requests per milestone.",
        ],
        original_text=(
            "# Freelance Project & Milestone Management Platform\n\n"
            "## Problem statement\n"
            "Freelancers and clients coordinate over email, chat, and shared "
            "folders, so deliverables, feedback, and revision rounds get lost. "
            "There is no single record of what was agreed or when it is due.\n\n"
            "## Proposed solution\n"
            "A platform where clients post projects, define milestones with due "
            "dates, and freelancers submit deliverables per milestone. Clients "
            "approve or request revisions, and every action is logged.\n\n"
            "## Target audience\n"
            "Freelancers (designers, writers, developers) and their clients.\n\n"
            "## Real-world use case\n"
            "A client hires a designer for a website with three milestones: "
            "wireframes, mockups, final files. The designer submits each, the "
            "client requests one revision on mockups, then approves. Payment "
            "milestone status is clear to both.\n\n"
            "## Core features (MVP)\n"
            "- Client and freelancer workspaces\n"
            "- Project creation with milestones and due dates\n"
            "- Deliverable file submissions per milestone\n"
            "- Client review: approve or request revision with comments\n"
            "- Activity history per project and milestone\n"
            "- Role-based authorization for clients and freelancers\n\n"
            "## Optional features (post-MVP)\n"
            "- Invoicing tied to milestone approval\n"
            "- Time tracking per milestone\n"
            "- Dispute flagging for escalation\n"
            "- Contract templates\n\n"
            "## Stretch goals\n"
            "- Escrow payment integration\n"
            "- Milestone templates for common project types\n"
            "- Freelancer ratings and portfolio\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, file storage\n\n"
            "## Required skills\n"
            "Role-based authorization, relational data modelling, workflow "
            "design, file handling\n\n"
            "## Estimated development duration\n"
            "65–85 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "RBAC, milestone state machines, deliverable lifecycle, activity "
            "logging, access control\n\n"
            "## Technical challenges\n"
            "- Ensuring freelancers can only submit to their own assigned milestones\n"
            "- Managing revision cycles without losing prior deliverables\n"
            "- Keeping activity history immutable and auditable\n\n"
            "## Suggested implementation approach\n"
            "Model projects, milestones, submissions, and reviews as related "
            "tables. Enforce authorization in route handlers. Store submitted "
            "files and link each revision to its milestone.\n\n"
            "## Possible future improvements\n"
            "- Invoicing, time tracking, disputes\n"
            "- Escrow payments, freelancer ratings\n\n"
            "## Limitations\n"
            "MVP does not include payments. File storage is basic; virus "
            "scanning and previews are out of scope."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-007",
        title="Subscription & Recurring Payment Tracker",
        summary=(
            "A personal finance tool that tracks recurring subscriptions and "
            "billing dates, with monthly/yearly spending analytics and upcoming "
            "renewal reminders."
        ),
        who_affected=(
            "Anyone with multiple streaming, software, or membership "
            "subscriptions who wants visibility into recurring spending."
        ),
        why_matters=(
            "Subscriptions auto-renew and are easily forgotten, leading to "
            "unexpected charges. Central tracking with reminders helps users "
            "cancel unused services and budget accurately."
        ),
        domain="fintech",
        est_hours=55,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "cron",
            "analytics",
            "notifications",
        ],
        datasets=[{"name": "Sample subscriptions", "url": None}],
        approaches=[
            "Users add subscriptions with name, amount, currency, billing "
            "cycle, and next due date.",
            "A background job checks upcoming renewals daily and sends "
            "reminders before each charge date.",
            "Analytics aggregate spending by month, year, category, and "
            "service.",
            "Users can mark subscriptions as active, cancelled, or paused.",
            "Export spending reports as CSV.",
        ],
        original_text=(
            "# Subscription & Recurring Payment Tracker\n\n"
            "## Problem statement\n"
            "People accumulate streaming, software, gym, and membership "
            "subscriptions that renew automatically. It is easy to lose track "
            "of what is being charged and when, causing surprise expenses.\n\n"
            "## Proposed solution\n"
            "A personal dashboard where users log each subscription with amount, "
            "currency, billing cycle, and next due date. The app shows upcoming "
            "renewals, sends reminders before charges, and breaks down spending "
            "by month, year, and category.\n\n"
            "## Target audience\n"
            "Students, professionals, and households managing multiple "
            "subscriptions.\n\n"
            "## Real-world use case\n"
            "A user adds Netflix, Spotify, a gym membership, and cloud storage. "
            "The dashboard shows $45 due next week and $120/month total. A "
            "reminder two days before the gym charge lets them cancel an "
            "unused membership.\n\n"
            "## Core features (MVP)\n"
            "- Add subscriptions with amount, currency, cycle, and due date\n"
            "- Upcoming renewal list with reminders\n"
            "- Monthly and yearly spending analytics by category\n"
            "- Mark subscriptions active, cancelled, or paused\n"
            "- Export spending report to CSV\n\n"
            "## Optional features (post-MVP)\n"
            "- Bank or email import to detect subscriptions automatically\n"
            "- Multiple currency conversion\n"
            "- Shared household subscription view\n"
            "- Predicted annual spend\n\n"
            "## Stretch goals\n"
            "- Direct cancel-flow links to provider pages\n"
            "- Subscription price-change detection\n"
            "- Mobile app with push reminders\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, node-cron\n\n"
            "## Required skills\n"
            "Date-based background jobs, analytics, notification systems, data "
            "aggregation\n\n"
            "## Estimated development duration\n"
            "45–65 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Recurring date calculations, aggregation queries, reminders, "
            "CSV export, categorization\n\n"
            "## Technical challenges\n"
            "- Handling billing cycles that vary (monthly, yearly, custom days)\n"
            "- Accurately aggregating spend across partial months\n"
            "- Avoiding duplicate renewal reminders\n\n"
            "## Suggested implementation approach\n"
            "Create a subscriptions table with next_due_date. Run a daily cron "
            "job that finds dues within N days and creates reminders. Aggregate "
            "amounts grouped by month/category for charts.\n\n"
            "## Possible future improvements\n"
            "- Auto-detection, currency conversion, household view\n"
            "- Price-change detection, push notifications\n\n"
            "## Limitations\n"
            "MVP relies on manual entry; it does not connect to bank accounts "
            "or detect charges automatically."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-008",
        title="Open-Source Contribution Discovery Platform",
        summary=(
            "A platform that surfaces GitHub issues suitable for beginners, "
            "filterable by programming language, labels, and difficulty, with "
            "the ability to save issues and track contribution progress."
        ),
        who_affected=(
            "New and returning open-source contributors who struggle to find "
            "first issues matching their skills and preferred technologies."
        ),
        why_matters=(
            "Good first issues are scattered across thousands of repositories. "
            "A discovery tool lowers the barrier to contributing and helps "
            "contributors build a track record."
        ),
        domain="developer-tools",
        est_hours=70,
        tech_tags=[
            "react",
            "nodejs",
            "github-api",
            "pagination",
            "search",
            "authentication",
        ],
        datasets=[{"name": "Sample indexed issues", "url": None}],
        approaches=[
            "Fetch open issues from public repositories via the GitHub API with "
            "pagination.",
            "Index issues by repository, language, labels, and estimated "
            "difficulty.",
            "Let users filter and search issues by language, label, and "
            "difficulty.",
            "Users authenticate with GitHub and save issues they plan to work "
            "on.",
            "Track contribution progress (saved, in-progress, submitted, "
            "merged).",
        ],
        original_text=(
            "# Open-Source Contribution Discovery Platform\n\n"
            "## Problem statement\n"
            "People who want to contribute to open source often do not know "
            "which repositories or issues are beginner-friendly. Labels like "
            "\"good first issue\" are spread across tens of thousands of repos.\n\n"
            "## Proposed solution\n"
            "A discovery platform that indexes open GitHub issues tagged as "
            "beginner-friendly. Users filter by language, label, and "
            "difficulty, save interesting issues, and track whether they have "
            "submitted or had a pull request merged.\n\n"
            "## Target audience\n"
            "New contributors, students, and developers building open-source "
            "portfolios.\n\n"
            "## Real-world use case\n"
            "A JavaScript learner filters for \"good first issue\" + "
            "\"JavaScript\" + \"React\". They save three issues, start work on "
            "one, and mark it \"submitted\" after opening a pull request.\n\n"
            "## Core features (MVP)\n"
            "- Discover issues from GitHub public repositories\n"
            "- Filter by language, labels, and difficulty\n"
            "- Search issues by title and repository\n"
            "- Save issues to a personal list\n"
            "- Track contribution status (saved, in-progress, submitted, merged)\n"
            "- GitHub OAuth login\n\n"
            "## Optional features (post-MVP)\n"
            "- Repository recommendations based on saved issues\n"
            "- Contribution streak and stats\n"
            "- PR status tracking via GitHub API\n"
            "- Bookmark collections\n\n"
            "## Stretch goals\n"
            "- Mentor matching\n"
            "- Issue difficulty auto-tagging\n"
            "- Weekly digest of new beginner issues\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, GitHub REST API\n\n"
            "## Required skills\n"
            "GitHub API integration, pagination, search indexing, "
            "authentication, state tracking\n\n"
            "## Estimated development duration\n"
            "60–80 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Third-party API pagination, OAuth, filtering/search, contribution "
            "lifecycle tracking\n\n"
            "## Technical challenges\n"
            "- Respecting GitHub API rate limits while indexing many repos\n"
            "- Inferring difficulty from labels and repository context\n"
            "- Keeping saved issue status in sync with GitHub PR state\n\n"
            "## Suggested implementation approach\n"
            "Use GitHub OAuth for login. Search the GitHub API for issues with "
            "beginner labels, paginating results. Store user-saved issues and "
            "their local status in PostgreSQL; optionally refresh PR state via "
            "the API.\n\n"
            "## Possible future improvements\n"
            "- Repo recommendations, streaks, PR tracking\n"
            "- Mentor matching, weekly digest\n\n"
            "## Limitations\n"
            "MVP depends on public GitHub data and rate limits. Difficulty is "
            "label-based, not a guarantee of actual issue complexity."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-009",
        title="Digital Evidence & Document Verification Portal",
        summary=(
            "A portal where users upload documents, generate SHA-256 "
            "cryptographic hashes, and later verify whether a file has been "
            "modified by comparing hashes, with an audit history."
        ),
        who_affected=(
            "Organizations and individuals exchanging certificates, contracts, "
            "or other files who need proof that a document was not altered."
        ),
        why_matters=(
            "Documents can be tampered with between creation and receipt. "
            "Cryptographic hashing gives recipients a way to verify integrity "
            "and creates an auditable record."
        ),
        domain="cybersecurity",
        est_hours=60,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "sha-256",
            "file-processing",
            "audit-logging",
        ],
        datasets=[{"name": "Sample verification records", "url": None}],
        approaches=[
            "Users upload a document; the server computes its SHA-256 hash and "
            "stores the hash with metadata.",
            "The original file is stored securely and linked to its hash record.",
            "To verify, a user uploads a file; the server recomputes its hash "
            "and compares it to the stored hash.",
            "Each verification attempt is logged with timestamp, file name, "
            "and match result (audit trail).",
            "Users can download the original file and view its verification "
            "history.",
        ],
        original_text=(
            "# Digital Evidence & Document Verification Portal\n\n"
            "## Problem statement\n"
            "Certificates, contracts, and other files exchanged between parties "
            "can be altered without the recipient knowing. There is often no "
            "cryptographic proof of a file's original state.\n\n"
            "## Proposed solution\n"
            "A verification portal where an issuer uploads a document and the "
            "system computes and stores its SHA-256 hash. A recipient later "
            "uploads the same file; the system recomputes the hash and reports "
            "whether it matches the original. Every verification is logged.\n\n"
            "## Target audience\n"
            "Employers verifying certificates, legal teams handling contracts, "
            "and anyone exchanging sensitive documents.\n\n"
            "## Real-world use case\n"
            "A university uploads a graduate's certificate. The system stores "
            "its SHA-256 hash. An employer receives the file, uploads it to "
            "verify, and gets a match confirmation with a timestamped audit "
            "record.\n\n"
            "## Core features (MVP)\n"
            "- Upload documents and generate SHA-256 hashes\n"
            "- Secure file storage linked to hash records\n"
            "- Verify a file by recomputing and comparing its hash\n"
            "- Verification history and audit log per document\n"
            "- Download original files and view match results\n\n"
            "## Optional features (post-MVP)\n"
            "- Digital signatures with public/private keys\n"
            "- QR codes linking to verification records\n"
            "- Bulk upload and verification\n"
            "- Expiry dates for verification records\n\n"
            "## Stretch goals\n"
            "- Blockchain-backed timestamping\n"
            "- Integration with document-signing platforms\n"
            "- Role-based access for issuers and verifiers\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL, Node crypto module (SHA-256)\n\n"
            "## Required skills\n"
            "File processing, SHA-256 hashing, secure storage, audit logging\n\n"
            "## Estimated development duration\n"
            "50–70 hours (solo)\n\n"
            "## Suggested team size\n"
            "1\n\n"
            "## Concepts the developer will learn\n"
            "Cryptographic hashing, file integrity, audit trails, secure file "
            "handling, metadata modelling\n\n"
            "## Technical challenges\n"
            "- Hashing large files without blocking the server (streaming)\n"
            "- Storing files securely and serving them only to authorized users\n"
            "- Ensuring the audit log is append-only and tamper-evident\n\n"
            "## Suggested implementation approach\n"
            "On upload, stream the file through Node's crypto createHash to "
            "compute SHA-256 without loading it fully into memory. Store the "
            "hash, file path, and metadata. On verify, recompute and compare.\n\n"
            "## Possible future improvements\n"
            "- Digital signatures, QR codes, bulk upload\n"
            "- Blockchain timestamps, role-based access\n\n"
            "## Limitations\n"
            "SHA-256 proves integrity, not authenticity by itself. MVP does not "
            "include digital signatures or legal non-repudiation."
        ),
    ),
    _project(
        source_id="manabi-web-intermediate-010",
        title="Distributed Inventory & Stock Synchronization System",
        summary=(
            "A multi-location inventory system for small businesses that keeps "
            "stock counts consistent across outlets, tracks transfers and "
            "adjustments, and raises low-stock alerts."
        ),
        who_affected=(
            "Small businesses with multiple shops or warehouses that struggle "
            "with inconsistent stock records and overselling."
        ),
        why_matters=(
            "When outlets keep separate records, the same item can be sold "
            "twice or stock runs out unseen. Centralized synchronization "
            "prevents overselling and stockouts."
        ),
        domain="industry",
        est_hours=80,
        tech_tags=[
            "react",
            "nodejs",
            "postgresql",
            "transactions",
            "concurrency",
            "rest-api",
        ],
        datasets=[{"name": "Sample products and locations", "url": None}],
        approaches=[
            "Products and multiple locations (shops/warehouses) are registered "
            "in the system.",
            "Stock levels per product per location are tracked with "
            "transactions to avoid overselling.",
            "Stock transfers between locations are recorded with source and "
            "destination.",
            "Adjustments (damage, returns, stock-take corrections) are logged "
            "with reasons.",
            "Low-stock alerts fire when a product at a location falls below a "
            "threshold.",
        ],
        original_text=(
            "# Distributed Inventory & Stock Synchronization System\n\n"
            "## Problem statement\n"
            "Small businesses with several outlets often keep stock on paper or "
            "separate spreadsheets per shop. The same item can be oversold, and "
            "head office has no real-time view of total stock.\n\n"
            "## Proposed solution\n"
            "A central inventory system where each product has a stock level at "
            "every location. Sales and transfers use database transactions so "
            "stock never goes negative. Admins see consolidated stock and get "
            "low-stock alerts per location.\n\n"
            "## Target audience\n"
            "Retail chains, multi-shop traders, and small warehouses.\n\n"
            "## Real-world use case\n"
            "A customer buys the last headphones at the downtown shop. The sale "
            "decrements downtown stock to zero in a transaction, so the online "
            "store immediately shows the item as out of stock. Head office "
            "receives a low-stock alert and transfers units from the warehouse.\n\n"
            "## Core features (MVP)\n"
            "- Register products and multiple stock locations\n"
            "- Track stock quantity per product per location\n"
            "- Record stock transfers between locations\n"
            "- Log adjustments (damage, returns, stock-take) with reasons\n"
            "- Low-stock alerts per product per location\n"
            "- Database transactions to prevent overselling\n\n"
            "## Optional features (post-MVP)\n"
            "- Point-of-sale integration\n"
            "- Purchase orders to suppliers\n"
            "- Stock valuation reports\n"
            "- Barcode scanning for fast stock updates\n"
            "## Stretch goals\n"
            "- Multi-currency cost tracking\n"
            "- Demand forecasting for reordering\n"
            "- Mobile stock-take app\n\n"
            "## Suggested technology stack\n"
            "React, Node.js/Express, PostgreSQL\n\n"
            "## Required skills\n"
            "Database transactions, concurrency control, REST APIs, data "
            "consistency, reporting\n\n"
            "## Estimated development duration\n"
            "70–90 hours (solo)\n\n"
            "## Suggested team size\n"
            "1–2\n\n"
            "## Concepts the developer will learn\n"
            "Transactional stock updates, concurrency control, transfer ledgers, "
            "alerting, inventory reporting\n\n"
            "## Technical challenges\n"
            "- Preventing two concurrent sales from overselling the same item\n"
            "- Keeping transfer source and destination atomic\n"
            "- Reconciling physical stock counts with system records\n\n"
            "## Suggested implementation approach\n"
            "Model products, locations, and stock_levels. Use SELECT ... FOR "
            "UPDATE transactions when selling or transferring. Log every "
            "movement as a ledger row. Raise alerts when quantity < threshold.\n\n"
            "## Possible future improvements\n"
            "- POS integration, purchase orders, barcode scanning\n"
            "- Forecasting, multi-currency costs\n\n"
            "## Limitations\n"
            "MVP is web-based; physical stock-take still requires manual entry. "
            "No barcode hardware integration in the base version."
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
        f"Intermediate web projects — inserted: {inserted}, skipped: {skipped}, "
        f"total: {len(PROJECTS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
