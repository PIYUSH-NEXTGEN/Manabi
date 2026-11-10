"""Seed 1 learning-track project idea (test pack).

    python -m app.seed.seed_learning_projects
"""

from app.seed.runner import seed_problems


PROBLEMS = [
    dict(
        source_id="manabi-learning-001",
        title="Study Flashcards App with Spaced Repetition",
        summary=(
            "Build a study companion that keeps all your flashcards in one place and decides "
            "when each card comes back. Cards you keep forgetting return quickly; cards you "
            "know well drift out to weeks-long intervals. That scheduling is the whole product - "
            "everything else is plumbing.\n\n"
            "You will build it end to end. First the data: decks, cards, and an append-only "
            "review log. Then the scheduling logic: a simplified SM-2 algorithm that takes a "
            "card's current state plus your grade and computes the next interval. Then the "
            "review loop itself - question, reveal, grade, next card - without a full-page "
            "reload at any point in the cycle.\n\n"
            "Finish with the parts that make it usable daily: retention and streak stats read "
            "straight out of the review log, keyboard-only grading, and an import/export path "
            "so decks survive a device switch. The scheduling logic should be a pure function "
            "you trust through unit tests, not through clicking around."
        ),
        who_affected=(
            "Self-learners, students, and anyone from gym-note-takers to med-school crammers "
            "who wants to remember what they study without buying another subscription."
        ),
        why_matters=(
            "Cramming fades in days while spaced repetition is proven to beat it, yet most "
            "tools are clunky, bloated, or locked behind paywalls. Building your own teaches "
            "you scheduling algorithms and state management while producing something you "
            "genuinely use every day."
        ),
        field="web-dev",
        domain="education",
        difficulty="beginner",
        est_hours=30,
        tech_tags=["javascript", "typescript", "react", "state-management", "local-storage", "algorithms"],
        learning_concepts=[
            "Data modelling: designing decks, cards, and review logs as related entities",
            "The SM-2 spaced-repetition algorithm and how ease factor and intervals work",
            "Application state: managing card queues, grades, and session progress cleanly",
            "Persistence: saving and reloading data without losing a single review",
            "Derived data: computing retention rate, streaks, and upcoming review load from raw logs",
            "Keyboard-first UX and accessibility for a distraction-free study flow",
            "Import/export (JSON or CSV) and fault-tolerant parsing of user files",
            "Testing logic-heavy code: unit-testing the scheduler with fixed dates",
        ],
        datasets=[{"name": "No dataset needed - use your own notes as seed content", "url": None}],
        approaches=[
            "Model the core entities first: Deck, Card, and ReviewLog with their fields.",
            "Implement a simplified SM-2 scheduler as a pure function you can unit-test.",
            "Build the review session screen: show a card, reveal the answer, grade it.",
            "Wire up persistence so every grade survives a refresh or app restart.",
            "Add deck statistics (retention, streaks, upcoming load) from the review log.",
            "Finish with import/export of decks and keyboard shortcuts for grading.",
        ],
        source_name="MANABI Curated",
        source_note="Curated learning-track project idea.",
        original_text=(
            "Build a personal study companion that keeps your flashcards, schedules them so "
            "you review the hardest cards more often, and shows you exactly how well a deck "
            "is sticking."
        ),
        ai_fields=["field", "domain", "difficulty", "est_hours", "who_affected", "why_matters", "tech_tags"],
        goal="learning",
        build_guide=[
            dict(
                title="Model the data before any UI",
                summary=(
                    "Decide what a deck, a card, and a review actually are. Every later "
                    "phase depends on these three shapes being right, so no screens yet."
                ),
                steps=[
                    "List the fields a card needs: deck id, question, answer, and a review state (interval in days, ease factor, due date).",
                    "Keep decks separate from cards so a card can be moved or merged later without rewriting its answers.",
                    "Design the review log as append-only: card id, date, grade (again / hard / good / easy). Never edit past rows.",
                    "Sketch all of it in plain objects or a TODO list first; move to a real database only once the shapes survive a mock review session.",
                ],
            ),
            dict(
                title="Write the scheduler as a pure function",
                summary=(
                    "Spaced repetition is just arithmetic on one card. Keep it isolated "
                    "from storage and UI so you can test it without opening the app."
                ),
                steps=[
                    "Simplified SM-2: input (interval, ease, grade), output (new interval, new ease). Again resets to 0 days; good grows the interval; easy grows it faster.",
                    "Pass the current date in as an argument instead of reading the clock - tests then use fixed dates and never flake.",
                    "Unit-test the boundaries: a new card, the same card graded 'again' five times, a card at a 90-day interval.",
                    "No formula confidence yet? Interval = previous interval times ease, starting at 1 day and ease 2.0, is already good spaced repetition.",
                ],
            ),
            dict(
                title="Build the review screen",
                summary=(
                    "One screen, one job: show a card, take a grade, move on. This is "
                    "where the scheduler turns into something you can use."
                ),
                steps=[
                    "The flow: question visible, one action reveals the answer, then grading controls appear.",
                    "On grade, call the scheduler, persist the new card state, append the log row, and pull the next due card.",
                    "Cap new cards per day (start at 10) so the daily queue stays finishable.",
                    "Keyboard-first: space to reveal, 1-4 to grade. Buttons still exist, but the keys should be enough.",
                    "Show a small 'next review in X days' hint after grading so the schedule feels real.",
                ],
            ),
            dict(
                title="Make persistence boring",
                summary=(
                    "A refresh must never lose a grade. This phase is short but "
                    "non-negotiable, and it should come before any statistics."
                ),
                steps=[
                    "Save on every grade, not on app exit or a timer.",
                    "Write one roundtrip test: grade three cards, reload from storage, assert the same three cards come back due.",
                    "Version the saved format from day one ({\"v\": 1, decks: ...}) so later schema changes can migrate old data instead of corrupting it.",
                ],
            ),
            dict(
                title="Stats, then polish",
                summary=(
                    "Everything from here reads the review log you already have; no new "
                    "plumbing. Ship the reading features, then sweat the edges."
                ),
                steps=[
                    "Retention per deck: good + easy grades as a share of the last 30 days of reviews.",
                    "Upcoming load: count of cards due each day for the next 7 days, as a simple list or bar row.",
                    "Streak: consecutive calendar days with at least one review, computed from the log.",
                    "Import/export decks (with the version field) via copy-paste or file, and validate on the way in.",
                    "Final pass: empty states for a new deck, long questions or answers that overflow, and a deck you can rename or delete safely.",
                ],
            ),
        ],
    ),
]

if __name__ == "__main__":
    seed_problems(PROBLEMS, label="learning-track problems")
