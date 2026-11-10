"""Seed 1 learning-track project idea (test pack).

    python -m app.seed.seed_learning_projects
"""

from app.seed.runner import seed_problems


PROBLEMS = [
    dict(
        source_id="manabi-learning-001",
        title="Study Flashcards App with Spaced Repetition",
        summary=(
            "Build a personal study companion that keeps your flashcards, schedules them so "
            "you review the hardest cards more often, and shows you exactly how well a deck "
            "is sticking. In this brief you will go end to end: model the data (decks, cards, "
            "daily review logs), implement a simplified SM-2 spaced-repetition scheduler so "
            "cards return at the right intervals, and design the session flow of review -> "
            "grade (again / hard / good / easy) -> next card with instant feedback instead of "
            "a page reload. You will also add deck statistics - cards learned per day, "
            "retention rate per deck, upcoming review load - and an import/export feature so "
            "users can move their decks between devices. Finally, make it feel like a real "
            "product: keyboard-first review controls, a streak counter to keep momentum, and "
            "full persistence so no answer is ever lost when the app is closed."
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
    ),
]

if __name__ == "__main__":
    seed_problems(PROBLEMS, label="learning-track problems")
