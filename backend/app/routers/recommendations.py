from datetime import timedelta

from fastapi import APIRouter
from sqlalchemy import func, select

from app import schemas
from app.deps import DB, CurrentUser
from app.models import ProblemStar, User, as_utc, utcnow
from app.services import github
from app.services.presenters import problem_to_out
from app.services.recommender import recommendations_for_user

router = APIRouter(tags=["recommendations"])

SIGNALS_TTL = timedelta(minutes=10)


async def _refresh_signals(db: DB, user: User) -> None:
    fresh = user.signals_updated_at is not None and (utcnow() - as_utc(user.signals_updated_at)) < SIGNALS_TTL
    if user.signals_json is not None and fresh:
        return
    signals = await github.get_user_signals(user.github_token)
    if signals is not None:
        user.signals_json = signals
        user.signals_updated_at = utcnow()
        db.commit()


@router.get("/api/recommendations", response_model=schemas.RecommendationsOut)
async def recommendations(user: CurrentUser, db: DB):
    await _refresh_signals(db, user)
    recommended = recommendations_for_user(db, user)
    ids = [problem.id for problem, _, _ in recommended]
    # Batch the stars for the returned cards: presenting them one at a time
    # would add one query per recommendation.
    star_counts = (
        dict(
            db.execute(
                select(ProblemStar.problem_id, func.count(ProblemStar.id))
                .where(ProblemStar.problem_id.in_(ids))
                .group_by(ProblemStar.problem_id)
            ).all()
        )
        if ids
        else {}
    )
    starred = (
        set(
            db.scalars(
                select(ProblemStar.problem_id).where(
                    ProblemStar.user_id == user.id,
                    ProblemStar.problem_id.in_(ids),
                )
            ).all()
        )
        if ids
        else set()
    )
    items = [
        schemas.RecommendationItem(
            problem=problem_to_out(
                problem,
                0,
                star_count=int(star_counts.get(problem.id, 0)),
                starred_by_me=problem.id in starred,
            ),
            score=score,
            reasons=reasons,
        )
        for problem, score, reasons in recommended
    ]
    return schemas.RecommendationsOut(items=items)
